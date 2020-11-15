from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm
from django.contrib.auth.models import User
from django.core.files.images import get_image_dimensions

from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget


from account.models import Profile,FeedbackModel
from django.contrib.auth import get_user_model


User = get_user_model()

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email or Username')

class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length = 255, help_text = "Enter your valid email address")


    class Meta:
        model = get_user_model()
        fields = ('username', 'email' , 'password1' , 'password2','no_social',)


    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("This email already used")
        return data

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['password2'].help_text = ''
        self.fields['no_social'].widget = forms.HiddenInput()
        self.fields['no_social'].widget.attrs.update({
            'value':'true',
        })
        self.fields['username'] = forms.CharField(required = True, min_length = 5, max_length = 20)


class FeedbackForm(forms.Form):
    # class Meta:
    #     model = Feedback
    #     fields = ('mail_subject','mail_text',)

    mail_subject = forms.CharField(max_length = 255,label = "Mail subject")
    mail_text = forms.CharField(widget=forms.Textarea, label = "Describe your problem/offer")

    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.fields['mail_subject'].widget.attrs.update({ 'placeholder' :
        'Example: Problem - [Quiz name] or Great Idea - [Quiz name]'})
        self.fields['mail_text'].widget.attrs.update({ 'placeholder' :
        'Example: Question 3 is not сorrect or I would like to add this answer option'})

class ProfileImage(forms.Form):
    profile_photo = forms.ImageField(required = False,help_text = 'We have some defaults avatars')
    recaptcha = ReCaptchaField(widget = ReCaptchaWidget())

    def __init__(self, *args, **kwargs):
        super(ProfileImage, self).__init__(*args, **kwargs)
        self.fields['recaptcha'].label = ''

    def clean_captcha(self):
        recaptcha = ReCaptchaField(widget = ReCaptchaWidget())
        if  recaptcha is None:
            raise forms.ValidationError(u'Fill the cptcha')
        return recaptcha

    def clean_avatar(self):
        avatar = self.cleaned_data['profile_photo']
        if avatar is None:
            raise forms.ValidationError(u'Add an avatar')
        if 'image' not in avatar.content_type:
            raise forms.ValidationError(u'Invalid picture format')
        return avatar


class EmailChanged(forms.Form):
    new_email_1 = forms.EmailField(max_length = 255,label = "Enter a new email",)
    new_email_2 = forms.EmailField(max_length = 255,label = "Confirm new email",)
    password = forms.CharField(widget=forms.PasswordInput,label = "Enter your password",)

    # new_email_1.widget.attrs.update({'class': 'EmailChangeField'})
    # password.widget.attrs.update({'class': 'PasswordChangeField'})


    def clean(self):
        if self.cleaned_data.get('new_email_1', None) != self.cleaned_data.get('new_email_2', None):
            raise forms.ValidationError("The two email addresses fields didn't match")


class CustomChangePassword(PasswordChangeForm):
    pass


class AvatarUpdate(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar',)


    def __init__(self, *args, **kwargs):
        super(AvatarUpdate, self).__init__(*args, **kwargs)
        self.fields['avatar'].label = 'Update your avatar'

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']
        if avatar is None:
            raise forms.ValidationError('Add an avatar')
        if 'image' not in avatar.content_type:
            raise forms.ValidationError('Invalid picture format')
        return avatar

class ChangeName(forms.Form):
    name_field = forms.CharField(max_length = 30,label = "",required = False)

    def __init__(self, *args, **kwargs):
        super(ChangeName, self).__init__(*args, **kwargs)
        self.fields['name_field'].widget.attrs.update({
                'class':'add_placeholder mt-3'
            })
