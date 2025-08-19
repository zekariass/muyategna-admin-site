from django.db import models
from service_app.models import Service
from user_app.models import UserProfile
from common_app.models import Language
from location_app.models import Address
from service_provider_app.models import ServiceProvider
from smart_selects.db_fields import ChainedForeignKey

# ===================== JOB REQUEST RELATED MODELS =====================


class DeliveryMode(models.TextChoices):
    ONSITE = 'ONSITE', 'Onsite'
    REMOTE = 'REMOTE', 'Remote'
    BOTH = 'BOTH', 'Both'


class JobStartTimeWindow(models.Model):
    id = models.BigAutoField(primary_key=True)
    code = models.CharField(unique=True, max_length=100)
    label = models.TextField()
    min_offset_days = models.IntegerField()
    max_offset_days = models.IntegerField()
    is_active = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'job_start_time_window'

    def __str__(self):
        return self.label


class JobRequestFlow(models.Model):
    id = models.BigAutoField(primary_key=True)
    service = models.ForeignKey(Service, models.DO_NOTHING)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        managed = False
        db_table = 'job_request_flow'

    def __str__(self):
        return self.name


class QuestionType(models.TextChoices):
    TEXT = 'TEXT', 'Text'
    NUMBER = 'NUMBER', 'Number'
    BOOLEAN = 'BOOLEAN', 'Boolean'
    DATE = 'DATE', 'Date'
    OPTION = 'SINGLE_SELECT', 'Single Select'
    MULTI_SELECT = 'MULTI_SELECT', 'Multi Select'

class JobQuestion(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.TextField(choices=QuestionType) 
    question = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        managed = False
        db_table = 'job_question'
    
    def __str__(self):
        return f"Question {self.id}: ({self.question})"


class JobRequestFlowQuestion(models.Model):
    id = models.BigAutoField(primary_key=True)
    flow = models.ForeignKey(JobRequestFlow, models.DO_NOTHING)
    question = models.ForeignKey(JobQuestion, models.DO_NOTHING)
    order_index = models.IntegerField(null=False, blank=False)
    is_start = models.BooleanField()
    is_terminal = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        managed = False
        db_table = 'job_request_flow_question'
        unique_together = (('flow', 'question'),)

    def __str__(self):
        return f"Flow: {self.flow.name}, Question: {self.question.question} (Order: {self.order_index})"


class JobQuestionTranslation(models.Model):
    id = models.BigAutoField(primary_key=True)
    question = models.ForeignKey(JobQuestion, models.DO_NOTHING)
    language = models.ForeignKey(Language, models.DO_NOTHING, related_name='job_question_translations')
    question_text = models.TextField(db_column='question')  # Field renamed because of name conflict.
    helptext = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        managed = False
        db_table = 'job_question_translation'
        unique_together = (('question_id', 'language_id'),)

    def __str__(self):
        return f"Translation for Question {self.question.id} in Language {self.language}: {self.question}"


class JobQuestionOption(models.Model):
    id = models.BigAutoField(primary_key=True)
    question = models.ForeignKey(JobQuestion, models.DO_NOTHING)
    value = models.TextField()
    order_index = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        managed = False
        db_table = 'job_question_option'
        

    def __str__(self):
        return f"Option for Question {self.question.id}: {self.value} (Order: {self.order_index})"


class JobQuestionOptionTranslation(models.Model):
    id = models.BigAutoField(primary_key=True)
    option = models.ForeignKey(JobQuestionOption, models.DO_NOTHING)
    language = models.ForeignKey(Language, models.DO_NOTHING, related_name='job_question_option_translations')
    label = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        managed = False
        db_table = 'job_question_option_translation'
        unique_together = (('option', 'language'),)

    def __str__(self):
        return f"Translation for Option {self.option.id} in Language {self.language}: {self.label}"



class JobQuestionTransition(models.Model):
    id = models.BigAutoField(primary_key=True)
    flow = models.ForeignKey(JobRequestFlow, models.DO_NOTHING)
    # from_flow_question = models.ForeignKey(JobRequestFlowQuestion, models.DO_NOTHING)
    # to_flow_question = models.ForeignKey(JobRequestFlowQuestion, models.DO_NOTHING, related_name='jobquestiontransition_next_flow_question_set')
    
    from_flow_question = ChainedForeignKey(
        JobRequestFlowQuestion,
        chained_field="flow",             # field on this model
        chained_model_field="flow",       # field on Service model
        related_name='jobquestiontransition_next_flow_question_set',
        show_all=False,
        auto_choose=True,
        sort=True,
        on_delete=models.CASCADE
    )


    to_flow_question = ChainedForeignKey(
        JobRequestFlowQuestion,
        chained_field="flow",             
        chained_model_field="flow",       
        show_all=False,
        auto_choose=True,
        sort=True,
        on_delete=models.CASCADE
    )
    
    # option = models.ForeignKey(JobQuestionOption, models.DO_NOTHING, blank=True, null=True)
    option = ChainedForeignKey(
        JobQuestionOption,
        chained_field="from_flow_question",             # field on this model
        chained_model_field="question",       
        show_all=False,
        auto_choose=True,
        sort=True,
        on_delete=models.CASCADE
    )

    condition_expression = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        managed = False
        db_table = 'job_question_transition'
        unique_together = (('flow', 'from_flow_question', 'option'),)

    def __str__(self):
        return f"Transition from {self.from_flow_question.question.id} to {self.to_flow_question.question.id} in Flow {self.flow.name} (Option: {self.option.value if self.option else 'None'})"


class JobStatusChoice(models.TextChoices):
    OPEN = 'OPEN', 'Open'
    REOPEN = 'REOPEN', 'Reopen'
    COMPLETED = 'COMPLETED', 'Completed'
    CANCELLED = 'CANCELLED', 'Cancelled'
    HIDDEN = 'HIDDEN', 'Hidden'
    PENDING_REVIEW = 'PENDING_REVIEW', 'Pending Review'
    EXPIRED = 'EXPIRED', 'Expired'
    PAUSED = 'PAUSED', 'Paused'


class JobRequest(models.Model):
    id = models.BigAutoField(primary_key=True)
    service = models.ForeignKey(Service, models.DO_NOTHING)
    customer = models.ForeignKey(UserProfile, models.DO_NOTHING)
    description = models.TextField(blank=True, null=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    start_window = models.ForeignKey(JobStartTimeWindow, models.DO_NOTHING)  # This field type is a guess.
    status = models.TextField(choices=JobStatusChoice)  # This field type is a guess.
    address = models.ForeignKey(Address, models.DO_NOTHING, blank=True, null=True)
    question_answers = models.JSONField(blank=True, null=True)
    extra_data = models.JSONField(blank=True, null=True)
    delivery_mode = models.CharField(choices=DeliveryMode, max_length=20, default=DeliveryMode.ONSITE)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        managed = False
        db_table = 'job_request'

    def __str__(self):
        return f"Job Request {self.id} for {self.service.name} by {self.customer.email if self.customer else 'Unknown'}"


class JobRequestMedia(models.Model):
    id = models.BigAutoField(primary_key=True)
    request = models.ForeignKey('JobRequest', models.DO_NOTHING)
    media_url = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'job_request_media'

    def __str__(self):
        return f"Media for Job Request {self.request.id}: {self.media_url}"
    

class JobLeadStatus(models.TextChoices):
    OPEN = 'OPEN', 'Open'
    CLAIMED_PARTIALLY = 'CLAIMED_PARTIALLY', 'Claimed Partially'
    CLAIMED_FULL = 'CLAIMED_FULL', 'Claimed Full'
    ASSIGNED = 'ASSIGNED', 'Assigned'
    EXPIRED = 'EXPIRED', 'Expired'
    CANCELLED = 'CANCELLED', 'Cancelled'
    ARCHIVED = 'ARCHIVED', 'Archived'


class ServiceProviderLeadStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    VIEWED = 'VIEWED', 'Viewed'
    QUOTED = 'QUOTED', 'Quoted'
    DECLINED = 'DECLINED', 'Declined'
    EXPIRED = 'EXPIRED', 'Expired'
    CUSTOMER_ACCEPTED = 'CUSTOMER_ACCEPTED', 'Customer Accepted'
    CUSTOMER_REJECTED = 'CUSTOMER_REJECTED', 'Customer Rejected'
    WITHDRAWN = 'WITHDRAWN', 'Withdrawn'
    REMINDER = 'REMINDER', 'Reminder'



class JobLead(models.Model):
    id = models.BigAutoField(primary_key=True)
    job_request = models.ForeignKey(JobRequest, models.DO_NOTHING, blank=True, null=True)
    status = models.TextField(choices=JobLeadStatus) 
    max_claims = models.IntegerField()  # Maximum number of claims allowed for this lead
    claimed_count = models.IntegerField(default=0)  # Current number of claims made on
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'job_lead'

    def __str__(self):
        return f"JobLead #{self.id} [{self.status}] (JobRequest ID: {self.job_request.id})"
    

class LeadClaimStatus(models.TextChoices):
        CLAIMED = 'CLAIMED', 'Claimed'
        QUOTED = 'QUOTED', 'Quoted'
        WITHDRAWN = 'WITHDRAWN', 'Withdrawn'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        REJECTED = 'REJECTED', 'Rejected'
        EXPIRED = 'EXPIRED', 'Expired'

class JobLeadClaim(models.Model):

    id = models.BigAutoField(primary_key=True)
    job_lead = models.ForeignKey(
        JobLead,
        on_delete=models.CASCADE,
        related_name='lead_claims'
    )
    provider = models.ForeignKey(
        ServiceProvider,
        on_delete=models.CASCADE,
        related_name='lead_claims'
    )
    status = models.CharField(
        max_length=20,
        choices=LeadClaimStatus.choices
    )

    requote_requested = models.BooleanField(default=False)  # Indicates if the customer has requested the provider to re-quote

    claimed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        db_table = 'job_lead_claim'
        unique_together = ('job_lead', 'provider')
        managed = False  
    
    def __str__(self):
        return f"Claim {self.id} for JobLead {self.job_lead.id} by Provider {self.provider.id} - Status: {self.status}"



class JobQuoteStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'       # auto
    ACCEPTED = 'ACCEPTED', 'Accepted'    # customer
    REJECTED = 'REJECTED', 'Rejected'    # customer
    WITHDRAWN = 'WITHDRAWN', 'Withdrawn' # provider



class JobQuote(models.Model):
    id = models.BigAutoField(primary_key=True)
    proposed_price = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    proposed_start_date = models.DateTimeField(blank=True, null=True)
    message = models.TextField()
    status = models.TextField(choices=JobQuoteStatus) 
    customer_feedback = models.TextField(blank=True, null=True)  # Customer's response to the quote
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    claim = models.ForeignKey(JobLeadClaim, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'job_quote'

    def __str__(self):
        return f"Quote {self.id} for Claim {self.claim.id} - Status: {self.status} (Proposed Price: {self.proposed_price})"
    


class InviteForQuote(models.Model):
    id = models.BigAutoField(primary_key=True)
    job_request = models.ForeignKey(JobRequest, models.DO_NOTHING)
    provider = models.ForeignKey(ServiceProvider, models.DO_NOTHING)
    viewed = models.BooleanField(blank=True, null=True)
    invited_at = models.DateTimeField(blank=True, null=True)
    viewed_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    accepted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'invite_for_quote'
        unique_together = (('job_request', 'provider'),)

    def __str__(self):
        return f"InviteForQuote {self.id} for JobRequest {self.job_request.id} to Provider {self.provider.id} - Viewed: {self.viewed}"