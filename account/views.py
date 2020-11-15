import random
import os
import datetime

from django.views.generic import TemplateView,View,DetailView,CreateView
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth import login,authenticate,get_user_model,views,update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.db.models import Sum,Min,Avg,Max
from django.db.models import Q,Count


from account.forms import RegisterForm,ProfileImage,LoginForm,EmailChanged,CustomChangePassword,AvatarUpdate,ChangeName,FeedbackForm
from account.models import Profile,CustomUser,FeedbackModel
from quiz.models import QuizzResult

from django.core.mail import send_mail
from django.contrib import messages


User = get_user_model()


class RegisterView(CreateView):
    form_class = RegisterForm
    second_form_class = ProfileImage

    template_name = 'registration/register.html'

    def get(self,request,*args,**kwargs):
        form = self.form_class
        image_form = self.second_form_class
        return render(request, self.template_name, {'form':form,'image':image_form})

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        image_form = self.second_form_class(request.POST,request.FILES)


        if form.is_valid() and image_form.is_valid():
            form.save()

            register_link = str(get_random_string(length = 16).lower())
            user_data = form.cleaned_data.get("username")
            user_prof_data = User.objects.get(username = user_data)
            avatar_data = image_form.cleaned_data.get("profile_photo")
            if avatar_data is None:
                avatars = ['naruto_fvjqws','sauske_azye10','sakura_bgqvwo']
                avatar_data = os.path.join('defaults_profile_img/', random.choice(avatars))
            user_profile = Profile.objects.create(user = user_prof_data,avatar = avatar_data)
            user_profile.save()

            return redirect('successfully_registered', register_link)

        elif not image_form.is_valid():
            messages.warning(request,'Fill the captcha')



        return render(request, self.template_name, {'form':form,'image':image_form })



class LoginView(views.LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'


class LoginWarning(TemplateView):
    template_name = 'account/login_warning.html'

    def get(self,request):
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, self.template_name, {})


class SuccessfullyRegistered(TemplateView):
    template_name = 'account/sign_up_successfully.html'

class ProfileStats(DetailView):
    template_name = 'account/profile_stats.html'
    models = QuizzResult

    def get_object(self,*args,**kwargs):
        slug = self.kwargs.get('name')
        instance = get_object_or_404(User, slug = slug)
        return instance

    def get_context_data(self, **kwargs):
        slug = self.kwargs.get('name')
        instance = get_object_or_404(User, slug = slug)
        user_quiz_result = QuizzResult.objects.filter(user = instance).order_by('-result_time')
        if user_quiz_result.count() != 0:
            successfully_passes = int(user_quiz_result.filter(is_successfully_passed = True).count() / user_quiz_result.count() * 100)
            unsuccessfully_passes = int(user_quiz_result.filter(is_successfully_passed = False).count() / user_quiz_result.count() * 100)
            best_time = QuizzResult.objects.filter(Q(user = instance) & Q(is_successfully_passed = True)).annotate(Min('duration')).order_by('duration')[0]
        else:
            successfully_passes = 0
            unsuccessfully_passes = 0
            best_time = None
        context = super().get_context_data(**kwargs)
        context['user_quiz_results'] = user_quiz_result
        context['successfully_passes'] = successfully_passes
        context['unsuccessfully_passes'] = unsuccessfully_passes
        context['best_time'] = best_time
        context['user_instance'] = instance
        return context



class PublicProfile(DetailView):
    template_name = 'account/public_profile.html'
    models = QuizzResult
    context_object_name = 'user_instance'

    def get_object(self,*args,**kwargs):
        slug = self.kwargs.get('name')
        instance = get_object_or_404(User, slug = slug)
        return instance

    def get_context_data(self, **kwargs):
        slug = self.kwargs.get('name')
        instance = get_object_or_404(User, slug = slug)
        user_quiz_result = QuizzResult.objects.filter(user = instance).all().order_by('-result_time')
        academy_limit_scores = 25
        genin_limit_scores = 75
        chunin_limit_scores = 150
        jounin_limit_scores = 250
        anbu_limit_scores = 400
        sanin_limit_scores = 600
        kage_limit_scores = 1000
        context = super().get_context_data(**kwargs)
        context['user_quiz_results'] = user_quiz_result
        context['user_instance'] = instance
        context['academy_limit_scores'] = academy_limit_scores
        context['genin_limit_scores'] = genin_limit_scores
        context['chunin_limit_scores'] = chunin_limit_scores
        context['jounin_limit_scores'] = jounin_limit_scores
        context['anbu_limit_scores'] = anbu_limit_scores
        context['sanin_limit_scores'] = sanin_limit_scores
        context['kage_limit_scores'] = kage_limit_scores
        return context


class Feedback(LoginRequiredMixin,View):
    login_url = '/login-warning'
    template_name = 'account/feedback.html'
    form_class = FeedbackForm

    def get(self,request,*args,**kwargs):
        mail_form = self.form_class
        can_send_email = False

        feedback_filter = None
        if FeedbackModel.objects.filter(user = request.user).count() > 0:
            feedback_filter = FeedbackModel.objects.filter(user = request.user).order_by('-id')[0]
            time_to_wait = feedback_filter.send_time + timezone.timedelta(hours = 6) - timezone.now()
            time_to_wait_format = str(time_to_wait).split(".")[0]
            if feedback_filter.send_time + timezone.timedelta(hours = 6) <= timezone.now():
                can_send_email = True
        else:
            can_send_email = True
            time_to_wait_format = None


        return render(request, self.template_name, {'mail_form':mail_form,'time_to_wait_format':time_to_wait_format,'can_send_email':can_send_email})

    def post(self,request,*args,**kwargs):
        mail_form = self.form_class(request.POST)
        can_send_email = False

        feedback_filter = None
        if FeedbackModel.objects.filter(user = request.user).count() > 0:
            feedback_filter = FeedbackModel.objects.filter(user = request.user).order_by('-id')[0]
            time_to_wait = feedback_filter.send_time + timezone.timedelta(minutes = 2) - timezone.now()
            time_to_wait_format = str(time_to_wait).split(".")[0]
            if feedback_filter.send_time + timezone.timedelta(minutes = 2) <= timezone.now():
                can_send_email = True
        else:
            can_send_email = True
            time_to_wait_format = None

        if mail_form.is_valid():
            mail_subject = mail_form.cleaned_data['mail_subject']
            mail_text = mail_form.cleaned_data.get('mail_text')


            if FeedbackModel.objects.filter(user = request.user).count() == 0:
                send_mail(mail_subject,mail_text,request.user.email,['artem.logachov773@gmail.com'],fail_silently = False)
                feedback = FeedbackModel.objects.create(mail_subject = mail_subject, mail_text = mail_text, user = request.user)
                feedback.save()
                messages.success(request,'Email sent successfully')
                return HttpResponseRedirect(request.path)

            elif FeedbackModel.objects.filter(user = request.user).exists() and feedback_filter.send_time + timezone.timedelta(minutes = 2) <= timezone.now():
                send_mail(mail_subject,mail_text,request.user.email,['artem.logachov773@gmail.com'],fail_silently = False)
                feedback = FeedbackModel.objects.create(mail_subject = mail_subject, mail_text = mail_text,user = request.user)
                feedback.save()
                messages.success(request,'Email sent successfully')
                return HttpResponseRedirect(request.path)

            else:
                return HttpResponseRedirect(request.path)


        return render(request, self.template_name, {'mail_form':mail_form,'can_send_email':can_send_email,'time_to_wait_format':time_to_wait_format})
class AccountData(LoginRequiredMixin,View):
    login_url = '/login-warning/'

    form_class = EmailChanged
    second_form_class = CustomChangePassword
    third_form_class = AvatarUpdate
    fourth_form_class = ChangeName

    template_name = 'account/account_data.html'

    def get(self,request,*args,**kwargs):
        form = self.form_class
        password_form = self.second_form_class(request.user)
        avatar_form = self.third_form_class
        name_form = self.fourth_form_class
        return render(request, self.template_name, {'form':form,'pass_form':password_form,'avatar_form':avatar_form,'name_form':name_form})

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        password_form = self.second_form_class(request.user,request.POST)
        avatar_form = self.third_form_class(request.POST,request.FILES)
        name_form = self.fourth_form_class(request.POST)

        if name_form.is_valid():
            user = request.user
            user.first_name = name_form.cleaned_data.get('name_field')
            user.save()


        if form.is_valid():
            user = request.user
            password = form.cleaned_data['password']
            if user.check_password(password):
                if form.cleaned_data['new_email_1'] != user.email:
                    user.email = form.cleaned_data['new_email_1']
                    user.save()
                    messages.success(request,'Email successfully updated')
                else:
                    messages.warning(request,'The email address is the same as the one already defined')
            else:
                messages.warning(request,'Uncorrect password')

        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password successfully updated")


        if avatar_form.is_valid():
            try:
                profile = Profile.objects.get(user = request.user)
                profile.delete()
            except:
                pass

            new_avatar = request.FILES['avatar']
            user_profile = Profile.objects.create(user = request.user,avatar = new_avatar)
            user_profile.save()
            messages.success(request,'Avatar successfully updated')


        return render(request, self.template_name, {'form':form,'pass_form':password_form,'avatar_form':avatar_form,'name_form':name_form})
