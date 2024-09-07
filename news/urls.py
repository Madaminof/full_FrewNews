from django.http import HttpResponseRedirect
from django.urls import path

from .views import main, post_detail, post_by_categories, search, youtube_video_list
from django.utils.translation import activate

def set_language(request, lang_code):
    activate(lang_code)
    request.session[translation.LANGUAGE_SESSION_KEY] = lang_code
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
urlpatterns = [

    path('', main, name="main"),
    path('post/<slug:slug>/', post_detail, name='post_detail'),
    path('category/<str:category_name>/', post_by_categories, name='post_by_categories'),
    path('youtube-videos/', youtube_video_list, name='youtube_video_list'),

    path('search/', search, name='search'),
]