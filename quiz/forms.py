from django import forms
from quiz.models import Quizzes


class QuizCreationForm(forms.ModelForm):
    class Meta:
        model = Quizzes
        fields = ('quiz','questions_count','timer','image','preview_field',)

    def clean_avatar(self):
        quiz_image = self.cleaned_data['image']
        if quiz_image is None:
            raise forms.ValidationError(u'Add an image')
        if 'image' not in quiz_image.content_type:
            raise forms.ValidationError(u'Invalid picture format')
        return quiz_image

    def __init__(self, *args, **kwargs):
        super(QuizCreationForm, self).__init__(*args, **kwargs)
        self.fields['quiz'].widget.attrs.update({
                    'class':'quiz_form mr-3',
                    'placeholder':"Enter quiz name",
                    "required":"true",
                })
        self.fields['quiz'].label = "Qiuz Name"

        self.fields['questions_count'].widget.attrs.update({ 'placeholder': "Enter the number of questions",
        "required":"true"
        })

        self.fields['image'].label = "Image of the quiz"

        self.fields['preview_field'].label = "Description of the quiz"

        self.fields['preview_field'].widget.attrs.update({
        "required":"true"
        })

        self.fields['timer'].label = "Timer"
        self.fields['timer'].widget.attrs.update({
        "placeholder": "Enter the duration of the quiz (in seconds)",
        "required":"true"
        })
