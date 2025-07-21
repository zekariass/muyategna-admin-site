from django.contrib import admin
from .models import *

# ====================== JOB REQUEST FLOW RELATED MODELS ========================
@admin.register(JobRequestFlow)
class JobRequestFlowAdmin(admin.ModelAdmin):
    list_display = ("id", "service", "name", "description", "is_active", "created_at", "updated_at")
    search_fields = ("name",)
    ordering = ("name",)

@admin.register(JobRequestFlowQuestion)
class JobRequestFlowQuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "flow", "question", "order_index", "is_start", "is_terminal", "created_at", "updated_at")
    search_fields = ("question",)
    list_filter = ("flow", "is_start", "is_terminal")

@admin.register(JobQuestion)
class JobQuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "type", "question", "created_at", "updated_at")
    search_fields = ("type",)

@admin.register(JobQuestionTranslation)
class JobQuestionTranslationAdmin(admin.ModelAdmin):
    list_display = ("id", "question_id", "language_id", "question_text", "helptext", "created_at", "updated_at")
    search_fields = ("question__type", "language_id")
    list_filter = ("language_id",)

@admin.register(JobQuestionOption)
class JobQuestionOptionAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "value", "order_index", "created_at", "updated_at")
    search_fields = ("question__type", "order_index")
    list_filter = ("question",)


@admin.register(JobQuestionOptionTranslation)
class JobQuestionOptionTranslationAdmin(admin.ModelAdmin):
    list_display = ("id", "option", "language_id", "label", "created_at", "updated_at")
    search_fields = ("option__value", "language_id")
    list_filter = ("language_id",)


@admin.register(JobQuestionTransition)
class JobQuestionTransitionAdmin(admin.ModelAdmin):
    list_display = ("id", "flow", "from_flow_question", "to_flow_question", "option", "condition_expression", "created_at", "updated_at")
    search_fields = ("option",)
    # exclude = ("question",)


# @admin.register(JobRequest)
# class JobRequestAdmin(admin.ModelAdmin):
#     list_display = ("id", "service", "customer", "description", "budget", "start_window", "status", "address", "created_at", "updated_at")

@admin.register(JobRequest)
class JobRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'service', 
        'customer', 
        'status', 
        'budget', 
        'start_window',
        # 'question_answers', 
        # 'extra_data',
        'created_at', 
        'updated_at'
    )
    list_filter = ('status', 'created_at', 'service', 'start_window')
    search_fields = (
        'id', 
        'customer__email', 
        'customer__first_name', 
        'customer__last_name', 
        'service__name'
    )
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('customer', 'service', 'address', 'start_window')
    ordering = ('-created_at',)


# @admin.register(JobQuestionAnswers)
# class JobQuestionAnswersAdmin(admin.ModelAdmin):
#     list_display = ("id", "job_request", "flow_question", "answer_text", "answer_number", "answer_boolean", "answer_date", "answer_option_ids", "created_at", "updated_at")



@admin.register(JobRequestMedia)
class JobRequestMediaAdmin(admin.ModelAdmin):
    list_display = ("id", "request", "media_url", "created_at")
    list_filter = ("created_at",)
    search_fields = ("media_url", "request__id")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)

    def has_add_permission(self, request):
        return False  # Disable add since managed = False

    def has_change_permission(self, request, obj=None):
        return False  # Disable edit

    def has_delete_permission(self, request, obj=None):
        return False  # Disable delete


@admin.register(JobLead)
class JobLeadAdmin(admin.ModelAdmin):
    list_display = ('id', 'job_request_id', 'max_claims', 'claimed_count', 'status', 'job_request__address', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('id', 'job_request__id')
    ordering = ('-created_at',)


# @admin.register(ServiceProviderLead)
# class ServiceProviderLeadAdmin(admin.ModelAdmin):
#     list_display = ('id', 'job_lead_id', 'provider_id', 'status', 'viewed_at', 'responded_at', 'created_at')
#     list_filter = ('status', 'created_at', 'viewed_at')
#     search_fields = ('id', 'provider__id', 'job_lead__id')
#     ordering = ('-created_at',)


@admin.register(JobStartTimeWindow)
class JobStartTimeWindowAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'code', 
        'label', 
        'min_offset_days', 
        'max_offset_days', 
        'is_active', 
        'created_at', 
        'updated_at'
    )
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('code', 'label')
    ordering = ('code',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(JobLeadClaim)
class JobLeadClaimAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'job_lead',
        'provider',
        'status',
        'claimed_at',
        'created_at',
        'updated_at',
    )
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('job_lead__id', 'provider__id')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(JobQuote)
class JobQuoteAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'claim',
        'status',
        'customer_feedback',
        'proposed_price',
        'proposed_start_date',
        'created_at',
        'updated_at',
    )
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('message', 'claim__id', 'id')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': (
                'claim',
                'status',
                'proposed_price',
                'proposed_start_date',
                'message',
                'created_at',
                'updated_at',
            )
        }),
    )