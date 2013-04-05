from django.contrib import admin

from quiz.models import Quiz, Question, Choice

# Question is ForeignKey of Choice
# Quiz is ForeignKey of Question
#

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
               (None, { 'fields': ['quiz', 'question'] }),
               ]
    inlines = [ChoiceInline]

class QuizAdmin(admin.ModelAdmin):
    fieldsets = [
                 (None, {'fields': ['subject','title']}),
                ]
    inlines = [QuestionInline]


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
