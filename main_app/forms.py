from django import forms
from .models import Profile, Post, City, Comment
from django.contrib import admin

class ProfileCreationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [ 'email', 'slug', 'firstname', 'lastname', 'currentcity', 'picture' ]
        widgets = {'slug' : forms.HiddenInput()}

class PostCreationForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'picture']

class CityCreationForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['name', 'slug', 'picture', 'country']
        widgets = { 'slug' : forms.HiddenInput()}

class CommentCreationForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']