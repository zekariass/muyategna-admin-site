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


@admin.register(JobRequest)
class JobRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "service", "customer", "description", "budget", "when_to_start_job", "status", "address", "created_at", "updated_at")


@admin.register(JobQuestionAnswers)
class JobQuestionAnswersAdmin(admin.ModelAdmin):
    list_display = ("id", "job_request", "flow_question", "answer_text", "answer_number", "answer_boolean", "answer_date", "answer_option_ids", "created_at", "updated_at")
