from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,JsonResponse
from quiz.models import Quizzes,Questions,Answers,Comments,QuizzResult,GameQuestions,GameAnswers
from account.models import Profile
from quiz.forms import QuizCreationForm
from django.contrib.auth.models import User
from django.views.generic import ListView,DetailView,View
from django.contrib.auth.mixins import LoginRequiredMixin
import time
import datetime
import json
from random import randint
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.forms.models import model_to_dict
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import F,Q,Count


class HomePage(ListView):
    template_name = 'quiz/index.html'
    models = Quizzes
    context_object_name = 'quizzes'

    def get_queryset(self):
        return Quizzes.objects.annotate(p_passed=Count('people_passed')) \
                                 .order_by('-p_passed')[:3]

class QuizPage(ListView):
    template_name = 'quiz/quiz.html'
    models = Quizzes
    context_object_name = 'quizzes'

    def get_queryset(self):
        return Quizzes.objects.all().order_by('-publucation_time')


def preview(request,name):
    quiz = get_object_or_404(Quizzes,slug = name)
    comments = Comments.objects.filter(quizComment = quiz,reply = None).annotate(likes_count=Count('likes')) \
                                 .order_by('-likes_count','publicationDate')
    commentsLen = Comments.objects.filter(quizComment = quiz,reply = None).count()
    users_results = QuizzResult.objects.filter(quiz = quiz).order_by('-result_time')[:3]
    is_liked = False
    is_disliked = False
    is_comment_liked = False
    is_comment_disliked = False
    is_blocked = True

    result_unique_link = None
    first_question = None
    if request.user.is_authenticated:
        first_question = GameQuestions.objects.filter(Q(quiz = quiz) & Q(user = request.user)).last()
        if request.POST.get('start_quiz_btn_name'):
            result_unique_link = str(get_random_string(length = 8).lower())
            questions = Questions.objects.filter(quiz = quiz).order_by('?')
            total_answers = 0
            for question in questions:
                total_answers += question.answers_set.all().count()
                if question.image:
                    game_question = GameQuestions.objects.create(user = request.user, is_used = False, quiz = question.quiz, question = question.question, image = question.image.url, is_multiple_answers = question.is_multiple_answers).save()
                else:
                    game_question = GameQuestions.objects.create(user = request.user, is_used = False, quiz = question.quiz, question = question.question, image = None, is_multiple_answers = question.is_multiple_answers).save()

            answers = Answers.objects.filter(quiz_name = quiz).order_by('?')[:total_answers]
            for answer in answers:
                question = GameQuestions.objects.filter(Q(question = answer.question_name) & Q(user = request.user) & Q(is_used = False)).get()
                GameAnswers.objects.create(question_name = question, user = request.user, is_used = False, is_selected = False, quiz = answer.quiz_name , answer = answer.answer, complete = answer.complete).save()

            return redirect('game_view', quiz.slug, result_unique_link)

    if request.user.is_authenticated:
        user_comment = Comments.objects.filter(user = request.user)
        for comment in user_comment:
            if request.user.profile and request.user.profile.avatar.url != comment.user_img and request.user == comment.user:
                Comments.objects.filter(Q(quizComment = quiz) & Q(user = request.user)).update(user_img = request.user.profile.avatar.url)

    if quiz.likes.filter(id = request.user.id).exists():
        is_liked = True

    if quiz.dislikes.filter(id = request.user.id).exists():
        is_disliked = True

    time_to_wait_format = None
    if request.user.is_authenticated and QuizzResult.objects.filter(user = request.user).count() >= 1:
        quiz_result_time = QuizzResult.objects.filter(user = request.user).order_by('-id')[0]
        time_to_wait = quiz_result_time.result_time + timezone.timedelta(hours = quiz.attempt_time) - datetime.datetime.now()
        time_to_wait_format = str(time_to_wait).split(".")[0]

        if quiz_result_time.result_time + timezone.timedelta(hours = quiz.attempt_time) <= datetime.datetime.now():
            is_blocked = False
    else:
        is_blocked = False


    return render(request,'quiz/preview.html',{"comments":comments, "quizz":quiz,"comments_len":commentsLen,"is_liked":is_liked,"is_disliked":is_disliked,
        "is_comment_liked":is_comment_liked,"is_comment_disliked":is_comment_disliked,'total_likes':quiz.total_likes(),
        'total_dislikes':quiz.total_dislikes(),"total_passes":quiz.total_passes(),"is_blocked":is_blocked,
        "time_to_wait":time_to_wait_format,"users_results":users_results,"first_question":first_question,"unique_link":result_unique_link,})


def ajax_query(request,name):
    quiz = get_object_or_404(Quizzes,slug = name)
    comment = request.POST.get("text_data")
    reply_id = request.POST.get('comment_id')
    comment_query = None
    if request.method == "POST" and request.is_ajax():
        if reply_id:
            comment_query = Comments.objects.get(id = reply_id)
        commentLen = len(comment)
        if not comment.isspace() and comment:
            comment_result = quiz.comments_set.create(comment = comment, publicationDate = datetime.datetime.now(), user = request.user, reply = comment_query,user_img = request.user.profile.avatar.url)
            comment_result.save()
            data_user = request.user
            parent_comment = comment_query.user


    return JsonResponse({'result': model_to_dict(comment_result), "parent_comment":model_to_dict(parent_comment) ,"user" : model_to_dict(data_user)})

def ajax_query_edit(request,id,name):
    quiz = get_object_or_404(Quizzes,slug = name)
    comment_id = quiz.comments_set.get(id=id)
    # search_id = request.POST.get('id')
    comment_text = request.POST.get("text_data")
    result_data = None
    if request.method == "POST" and request.is_ajax():
        if request.POST.get("button"):
            commentLen = len(comment_text)
            if not comment_text.isspace():
                Comments.objects.filter(id = id).update(comment = comment_text,  user = request.user, reply = comment_id.reply, user_img = request.user.profile.avatar.url, is_edited = True)
                result_data = Comments.objects.filter(id = id).values().get()
                comment_likes_count = comment_id.likes.count()
                comment_dislikes_count = comment_id.dislikes.count()
    return JsonResponse({'result': result_data, "comment_likes_count":comment_likes_count, "comment_dislikes_count":comment_dislikes_count, "user":model_to_dict(request.user)} )

def ajax_query_delete(request,id,name):
    quiz = get_object_or_404(Quizzes,slug = name)
    comment = get_object_or_404(Comments,id=id)
    if request.method == "POST" and request.is_ajax():
        comment.delete()
    return JsonResponse({'result': 'ok'}, status = 200)

def like_comment(request,name):
    quiz = get_object_or_404(Quizzes, slug = name)
    comment = get_object_or_404(Comments,id = request.POST.get('comment_id'))
    is_comment_liked = False
    if comment.likes.filter(id = request.user.id).exists():
        comment.likes.remove(request.user)
        is_comment_liked = False
        is_comment_disliked = True
    else:
        comment.likes.add(request.user)
        comment.dislikes.remove(request.user)
        is_comment_liked = True
        is_comment_disliked = False
    context = {
        'comment':comment,
        "is_comment_liked": is_comment_liked,
        "is_comment_disliked": is_comment_disliked,
    }
    res = render_to_string('quiz/comment_like_section.html', context, request = request)
    return JsonResponse({"result" : res,"is_comment_liked": is_comment_liked,})

def dislike_comment(request,name):
    quiz = get_object_or_404(Quizzes, slug = name)
    comment = get_object_or_404(Comments,id = request.POST.get('comment_id'))
    is_comment_disliked = False
    if comment.dislikes.filter(id = request.user.id).exists():
        comment.dislikes.remove(request.user)
        is_comment_disliked = False
        is_comment_liked = True
    else:
        comment.dislikes.add(request.user)
        comment.likes.remove(request.user)
        is_comment_disliked = True
        is_comment_liked = False
    context = {
        'comment':comment,
        "is_comment_liked": is_comment_liked,
        "is_comment_disliked": is_comment_disliked,
    }
    res = render_to_string('quiz/comment_dislike_section.html', context, request = request)
    return JsonResponse({"result":res,"is_comment_liked": is_comment_liked,})


def like_quiz(request,name):
    quiz = get_object_or_404(Quizzes, slug = name)
    is_liked = False
    if quiz.likes.filter(id = request.user.id).exists():
        quiz.likes.remove(request.user)
        is_liked = False
        is_disliked = True
    else:
        quiz.likes.add(request.user)
        quiz.dislikes.remove(request.user)
        is_liked = True
        is_disliked = False
    context = {
        'quiz':quiz,
        'is_liked':is_liked,
        'is_disliked':is_disliked,
        'total_likes':quiz.total_likes(),
        'total_dislikes':quiz.total_dislikes(),
    }
    if request.is_ajax():
        res = render_to_string('quiz/like_section.html', context, request = request)
        return JsonResponse({"result" : res, "is_liked": is_liked, "is_disliked": is_disliked})

def dislike_quiz(request,name):
    quiz = get_object_or_404(Quizzes,slug = name)
    is_disliked = False
    if quiz.dislikes.filter(id = request.user.id).exists():
        quiz.dislikes.remove(request.user)
        is_disliked = False
        is_liked = True
    else:
        quiz.dislikes.add(request.user)
        quiz.likes.remove(request.user)
        is_disliked = True
        is_liked = False
    context = {
        'quiz':quiz,
        'is_disliked':is_disliked,
        'is_liked':is_liked,
        'total_dislikes':quiz.total_dislikes(),
        'total_likes':quiz.total_likes(),
    }
    if request.is_ajax():
        res = render_to_string('quiz/dislike_section.html', context, request = request)
        return JsonResponse({"result" : res, "is_liked": is_liked, "is_disliked":is_disliked,})



def game_view(request,name,unique):
    quiz = get_object_or_404(Quizzes,slug = name)
    questions = GameQuestions.objects.filter(quiz = quiz).order_by('-id')[:quiz.questions_count]
    total_answers = 0
    for question in questions:
        total_answers += question.gameanswers_set.all().count()
    answers = GameAnswers.objects.filter(quiz = quiz).order_by('-id')

    if QuizzResult.objects.filter(user = request.user).count() >= 1:
        quiz_result_time = QuizzResult.objects.filter(user = request.user).last()
        if quiz_result_time.result_time + timezone.timedelta(hours = quiz.attempt_time) >= datetime.datetime.now():
            return redirect('/')


    return render(request,'quiz/question.html',{"quizz":quiz,"answers":answers,"questions":questions,})

User = get_user_model()

def timer_ajax(request,name,unique):
    correct_answers = 0
    scores = 0
    result_unique_link = str(get_random_string(length = 8).lower())
    quiz = get_object_or_404(Quizzes,slug = name)
    questions = GameQuestions.objects.filter(quiz = quiz).order_by('-id')[:quiz.questions_count]
    total_answers = 0
    is_successfully_passed = True
    for question in questions:
        total_answers += question.gameanswers_set.all().count()
    answers = GameAnswers.objects.filter(quiz = quiz).order_by('-id')
    timer_data = request.POST.get("timer_data")
    timer_data_format = time.strftime("%M:%S", time.gmtime(int(timer_data)))
    if request.method == "POST" and request.is_ajax():
        for question in questions:
            if question.is_multiple_answers:
                all_corrected = None
                check_names = request.POST.getlist("n" + str(question.id), None)
                corrected_count = GameAnswers.objects.filter(Q(question_name = question) & Q(complete = True)).count()
                for answer in question.gameanswers_set.all():
                    if str(answer.id) in check_names:
                        GameAnswers.objects.filter(id = answer.id).update(is_selected = True)
                        selected = GameAnswers.objects.get(id = answer.id)
                        if answer.complete == True and corrected_count == len(check_names):
                            all_corrected = True
                        else:
                            all_corrected = False
                if all_corrected == True:
                    correct_answers += 1
                    scores += request.user.profile.scores_factor

            else:
                for answer in question.gameanswers_set.all():
                    if request.POST.get("n" + str(question.id)) == str(answer.id):
                        GameAnswers.objects.filter(id = answer.id).update(is_selected = True)
                        # selected = GameAnswers.objects.get(id = answer.id)
                        if answer.complete == True:
                            correct_answers += 1
                            scores += request.user.profile.scores_factor
        GameQuestions.objects.filter(Q(user = request.user) & Q(is_used = False)).update(is_used = True)
        GameAnswers.objects.filter(Q(user = request.user) & Q(is_used = False)).update(is_used = True)

        if int(timer_data) == quiz.timer or correct_answers < 1:
            scores = 0
            is_successfully_passed = False

        quiz_result = QuizzResult.objects.create(user = request.user, quiz = quiz, result_link = result_unique_link, correct_answers = correct_answers, duration = timer_data_format, scores = scores, is_successfully_passed = is_successfully_passed)
        User.objects.filter(username = request.user.username).update(total_scores = F('total_scores') + scores)
        quiz_result.save()
        quiz.people_passed.add(quiz_result)
        selected_result = QuizzResult.objects.get(result_link = result_unique_link)
        GameAnswers.objects.filter(Q(quiz_result = None) & Q(user = request.user)).update(quiz_result = selected_result)

        current_user = User.objects.get(username = request.user.username)


        if current_user.total_scores >= 25 and current_user.total_scores <= 75:
            User.objects.filter(username = request.user.username).update(rank = 'Genin')

        elif current_user.total_scores >= 75 and current_user.total_scores <= 150:
            User.objects.filter(username = request.user.username).update(rank = 'Chuunin')
            Profile.objects.filter(user = request.user).update(scores_factor = F('scores_factor') + 1)

        elif current_user.total_scores >= 150 and current_user.total_scores <= 250:
            User.objects.filter(username = request.user.username).update(rank = 'Jounin')

        elif current_user.total_scores >= 250 and current_user.total_scores <= 400:
            User.objects.filter(username = request.user.username).update(rank = 'ANBU')
            Profile.objects.filter(user = request.user).update(scores_factor = F('scores_factor') + 1)

        elif current_user.total_scores >= 400 and current_user.total_scores <= 600:
            User.objects.filter(username = request.user.username).update(rank = 'Sannin')
            Profile.objects.filter(user = request.user).update(scores_factor = F('scores_factor') + 1)

        elif current_user.total_scores >= 600 and current_user.total_scores <= 1000:
            User.objects.filter(username = request.user.username).update(rank = 'Kage')

        elif current_user.total_scores >= 1000:
            User.objects.filter(username = request.user.username).update(rank = 'NARUTO')

    return JsonResponse({'result':model_to_dict(quiz_result)})


class QuizResult(LoginRequiredMixin,View):

    login_url = '/login-warning'
    template_name = 'quiz/quiz_result.html'

    def get(self,request,name,result):
        quiz = get_object_or_404(Quizzes,slug = name)
        questions = GameQuestions.objects.filter(Q(quiz = quiz) & Q(user = request.user)).order_by('-id')[:quiz.questions_count]
        question_count = questions.count()
        quiz_result = get_object_or_404(QuizzResult,result_link = result)
        answers = GameAnswers.objects.filter(quiz = quiz).order_by('-id')

        return render(request, self.template_name, {"quiz":quiz,"questions":questions,"answers":answers,"question_count":question_count,"quiz_result":quiz_result})


class QuizCreation(LoginRequiredMixin,View):
    login_url = '/login-warning'
    model = Quizzes
    form_class = QuizCreationForm
    template_name = 'quiz/quiz_creation.html'

    def get(self,request,*args,**kwargs):
        if request.user.is_staff:
            form = self.form_class(request.FILES)

            return render(request, self.template_name, {'form':form,})
        else:
            return redirect('/')

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST,request.FILES)

        if form.is_valid():
            quiz_data = form.cleaned_data.get('quiz')
            questions_count_data = form.cleaned_data.get('questions_count')
            timer_data = form.cleaned_data.get('timer')
            image_data = form.cleaned_data['image']
            description_data = form.cleaned_data.get('preview_field')

            if not Quizzes.objects.filter(quiz = quiz_data):
                created_quiz = Quizzes.objects.create(quiz = quiz_data, questions_count = questions_count_data, timer = timer_data, image = image_data, preview_field = description_data,author = request.user)
                created_quiz.save()
                return redirect('questions_creation',created_quiz.slug)
            else:
                messages.warning(request,"This quiz name is already exists")
            return redirect(request.path)

        return render(request, self.template_name, {'form':form,})

class QuizQuestionsCreation(View):
    template_name = 'quiz/questions_creation.html'

    def get(self,request,name,*args,**kwargs):
        quiz = get_object_or_404(Quizzes,slug = name)
        if request.user != quiz.author:
            return redirect('/')

        return render(request,self.template_name,{'quiz':quiz})

class Rating(ListView):
    template_name = 'quiz/rating.html'
    model = User
    context_object_name = "users"
    paginate_by = 15

    def get_queryset(self,**kwargs):
        search_field = self.request.GET.get('search_user_field')
        if search_field:
            return User.objects.filter(username__icontains = search_field).order_by('-total_scores')
        else:
            return User.objects.order_by('-total_scores',)
