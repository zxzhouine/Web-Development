from django import forms
from django.forms import ModelForm
from grumblr.models import *
from django.contrib.auth.forms import *
class RegistrationForm(forms.Form):
    username  = forms.CharField(max_length = 20)
    first_name= forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    email     = forms.EmailField(help_text='A valid email address, please.')
    password1 = forms.CharField(max_length = 200,
                                label='Password',
                                widget = forms.PasswordInput())
    password2 = forms.CharField(max_length = 200,
                                label='Confirm password',
                                widget = forms.PasswordInput())

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("Passwords did not match.")
        return cleaned_data

    def clean_username(self):
        username=self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")
        return username 
    def clean_email(self):
        email=self.cleaned_data.get('email')
        if User.objects.filter(email__exact=email):
            raise forms.ValidationError("This email is already taken.")
        return email

class ProfileForm(ModelForm):
    class Meta:
        model=UserProfile
        exclude=('user','username','follow')
        widget={'picture':forms.FileInput()}
    def clean(self):
        cleaned_data = super(ProfileForm, self).clean()
        return cleaned_data

class UserPostsForm(ModelForm):
    class Meta:
        model = UserPost
        exclude=('user','username','time','profile','last_modified')
        widgets = {'text': forms.Textarea(attrs={'class':"form-control", "rows":"3", "maxlength":"42",
                                           'placeholder': "What's happening"})}

    def clean(self):
        cleaned_data = super(UserPostsForm, self).clean()
        return cleaned_data

class UserCommentForm(ModelForm):
    class Meta:
        model   = PostComment
        fields = ('comment',)
        widgets = {'comment': forms.Textarea(attrs={'class':"form-control", "rows":"3", "maxlength":"42",
                                           'placeholder': "Write your comment"})}
    def clean(self):
        cleaned_data = super(UserCommentForm, self).clean()
        return cleaned_data