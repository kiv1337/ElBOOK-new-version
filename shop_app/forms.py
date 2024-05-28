from django import forms
from .models import UserProfile, ForumTopic, ForumPost, Review

class AvatarForm(forms.ModelForm):
    avatar = forms.ImageField(label='', widget=forms.FileInput(attrs={'class': 'custom-file-input', 'onchange': 'form.submit();'}))
    
    class Meta:
        model = UserProfile
        fields = ['avatar']



class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    rating = forms.ChoiceField(choices=RATING_CHOICES, label='Rating', widget=forms.RadioSelect)

    class Meta:
        model = Review
        fields = ['rating', 'text']


class ForumTopicForm(forms.ModelForm):
    class Meta:
        model = ForumTopic
        fields = ['название', 'тег']

class ForumPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ['сообщение']
        

class ChangeUsernameForm(forms.Form):
    new_username = forms.CharField(label='Новое имя пользователя', min_length=3, max_length=20)

class ChangeEmailForm(forms.Form):
    new_email = forms.EmailField(label='Новая почта')
