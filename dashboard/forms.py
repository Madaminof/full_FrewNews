from news.models import Post, Advertisement, YoutubeVideo
from django import forms
from .models import Profile


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title_uz','title_en', 'title_ru', 'content_uz', 'content_en', 'content_ru', 'slug', 'category', 'image', 'video']


class YoutubeVideoForm(forms.ModelForm):
    class Meta:
        model = YoutubeVideo
        fields = ['title_uz','title_en', 'title_ru', 'content_uz', 'content_en', 'content_ru', 'youtube_url', 'slug']


class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ['title_uz','title_en', 'title_ru', 'image', 'url', 'is_active']


# profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'birth_date']
