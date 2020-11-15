from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Questions,Answers,Quizzes,Comments,QuizzResult,GameQuestions,GameAnswers


@admin.register(GameQuestions)
class GameQuestionsAdmin(admin.ModelAdmin):
    list_display = ("question","quiz","is_multiple_answers",)
    search_fields = ['question',]
    list_filter = ['quiz',]

@admin.register(GameAnswers)
class GameAnswersAdmin(admin.ModelAdmin):
    list_display = ("answer","question_name","complete","is_selected")

@admin.register(Quizzes)
class QuizzesAdmin(admin.ModelAdmin):
    list_display = ("quiz","get_image","quiz_duration","questions_count","passed_count")
    readonly_fields = ("likes","dislikes","people_passed")

    def passed_count(self,obj):
        return obj.people_passed.all().count()

    def quiz_duration(self,obj):
        return str(obj.timer) + " secondes"

    def get_image(self,obj):
        if obj.image:
            return mark_safe(f'<img src = {obj.image.url} width = "80px" height = "80px">')

    get_image.short_description = "Profile image"

@admin.register(QuizzResult)
class QuizzesResultAdmin(admin.ModelAdmin):
    list_display = ("user","quiz","scores","correct_answers","duration")
    list_filter = ("user","quiz",)


@admin.register(Answers)
class AnswersAdmin(admin.ModelAdmin):
    list_display = ("answer","question_name","complete",)
    list_editable = ("complete",)


@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ("question","quiz","is_multiple_answers","get_image")
    search_fields = ['question',]
    list_filter = ['quiz',]

    def get_image(self,obj):
        if obj.image:
            return mark_safe(f'<img src = {obj.image.url} width = "80px" height = "80px">')


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ("comment","user","quizComment","get_image",)
    readonly_fields = ('likes','dislikes','get_image',)

    def get_image(self,obj):
        return mark_safe(f'<img src = {obj.user_img} width = "80px" height = "80px">')

    get_image.short_description = "Commentator image"

admin.site.site_title = "Naruto Quizz Admin"
admin.site.site_header = "Naruto Quizz Admin"
