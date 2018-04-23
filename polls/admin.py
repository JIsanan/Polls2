from django.contrib import admin

from .models import Question, Choice, Comments
# Register your models here.


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3


class Comments(admin.StackedInline):
    model = Comments
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date Information', {'fields': ['pub_date']})
    ]
    inlines = [ChoiceInline, Comments]


admin.site.register(Question, QuestionAdmin)
