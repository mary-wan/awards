from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post,Rating,Profile
from django.forms.widgets import Textarea

class UserRegisterForm(UserCreationForm):
    email= forms.EmailField()
    
    # specify model it will interact with
    class Meta:
        model = User  
        fields= ['username','email','password1','password2']
        
        help_texts = { 'username': None, 'password2': None, }


User._meta.get_field('email')._unique = True 

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('photo', 'title', 'url', 'description', 'technologies_used',)
        
   

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['design', 'usability', 'content']
        
class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email')


class UpdateUserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'profile_pic', 'bio', 'phone_number']
        
        widgets = {
            'bio': Textarea(attrs={'cols': 20, 'rows': 5}),
        }
        