from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
import requests
from django.db.models import F
from .models import YoutubeVideo
import json
from django.utils import timezone
from datetime import timedelta
from .models import Post, YoutubeVideo, Categories

from django.utils.translation import get_language

def main(request):
    categories = Categories.objects.all()
    language = get_language()  # Foydalanuvchi tanlagan tilni aniqlash

    # Tilga mos name maydonini tanlash
    name_field = f'name_{language}'

    # Postlar bilan ishlash
    all_posts = Post.objects.filter(image__isnull=False).order_by('-created_ad')[:30]
    latest_post_with_image = next((post for post in all_posts if post.image), None)

    latest_posts = {}
    for category in categories:
        category_name = getattr(category, name_field, None)
        if category_name:
            latest_post = Post.objects.filter(category__name_uz=category_name).order_by('-created_ad').first()
            if latest_post:
                latest_posts[category_name] = latest_post

    latest_sport_post_uz = Post.objects.filter(category__name_uz='Sport').order_by('-created_ad').first()
    latest_jamiyat_post_uz = Post.objects.filter(category__name_uz="Jamiyat").order_by('-created_ad').first()
    latest_jahon_post_uz = Post.objects.filter(category__name_uz="Jahon").order_by('-created_ad').first()
    latest_fantexnika_post_uz = Post.objects.filter(category__name_uz="Fan-texnika").order_by('-created_ad').first()
    latest_madaniyat_post_uz = Post.objects.filter(category__name_uz="Shou-biznes").order_by('-created_ad').first()

    latest_sport_post_en = Post.objects.filter(category__name_en='Sports').order_by('-created_ad').first()
    latest_jamiyat_post_en = Post.objects.filter(category__name_en="Society").order_by('-created_ad').first()
    latest_jahon_post_en = Post.objects.filter(category__name_en="the world").order_by('-created_ad').first()
    latest_fantexnika_post_en = Post.objects.filter(category__name_en="Science and technology").order_by('-created_ad').first()
    latest_madaniyat_post_en = Post.objects.filter(category__name_en="Show business").order_by('-created_ad').first()

    latest_sport_post_ru = Post.objects.filter(category__name_ru='Спорт').order_by('-created_ad').first()
    latest_jamiyat_post_ru = Post.objects.filter(category__name_ru="Общество").order_by('-created_ad').first()
    latest_jahon_post_ru = Post.objects.filter(category__name_ru="мир").order_by('-created_ad').first()
    latest_fantexnika_post_ru = Post.objects.filter(category__name_ru="Наука и технологии").order_by('-created_ad').first()
    latest_madaniyat_post_ru = Post.objects.filter(category__name_ru="Шоу-бизнес").order_by('-created_ad').first()

    post_jamiyat = Post.objects.filter(category__name_uz='Jamiyat').order_by('-created_ad')[1] if Post.objects.filter(category__name_uz='Jamiyat').count() > 1 else None
    post_sport = Post.objects.filter(category__name_uz='Sport').order_by('-created_ad')[1] if Post.objects.filter(category__name_uz='Sport').count() > 1 else None
    post_jahon = Post.objects.filter(category__name_uz='Jahon').order_by('-created_ad')[1] if Post.objects.filter(category__name_uz='Jahon').count() > 1 else None

    latest_post = Post.objects.latest('-created_ad')
    latest_posts_list = Post.objects.order_by('-created_ad')[:3]  # qaynoq yangiliklar uchun 3 ta Post

    jamiyat_posts_uz = Post.objects.filter(category__name_uz='Jamiyat').order_by('-created_ad')[:10]
    jamiyat_posts_en = Post.objects.filter(category__name_en='Society').order_by('-created_ad')[:10]
    jamiyat_posts_ru = Post.objects.filter(category__name_ru='Общество').order_by('-created_ad')[:10]

    sport_posts_uz = Post.objects.filter(category__name_uz='Sport').order_by('-created_ad')[:10]
    sport_posts_en = Post.objects.filter(category__name_en='Sports').order_by('-created_ad')[:10]
    sport_posts_ru = Post.objects.filter(category__name_ru='Спорт').order_by('-created_ad')[:10]

    now = timezone.now()
    last_week = now - timedelta(days=7)
    # Uzbek posts
    weekly_top_posts_uz = Post.objects.filter(created_ad__gte=last_week, category__name_uz='Jahon').order_by(
        '-created_ad')[:7]

    # English posts
    weekly_top_posts_en = Post.objects.filter(created_ad__gte=last_week, category__name_en='the world').order_by(
        '-created_ad')[:7]

    # Russian posts
    weekly_top_posts_ru = Post.objects.filter(created_ad__gte=last_week, category__name_ru='мир').order_by(
        '-created_ad')[:7]

    video_posts = YoutubeVideo.objects.filter(youtube_url__isnull=False).order_by('-created_ad')

    context = {
        'categories': categories,
        'latest_posts': latest_posts,
        'latest_post_with_image': latest_post_with_image,
        'latest_posts_list':latest_posts_list,

        'latest_sport_post_uz': latest_sport_post_uz,
        'latest_jamiyat_post_uz': latest_jamiyat_post_uz,
        'latest_jahon_post_uz': latest_jahon_post_uz,
        'latest_fantexnika_post_uz': latest_fantexnika_post_uz,
        'latest_madaniyat_post_uz': latest_madaniyat_post_uz,

        'latest_sport_post_en': latest_sport_post_en,
        'latest_jamiyat_post_en': latest_jamiyat_post_en,
        'latest_jahon_post_en': latest_jahon_post_en,
        'latest_fantexnika_post_en': latest_fantexnika_post_en,
        'latest_madaniyat_post_en': latest_madaniyat_post_en,

        'latest_sport_post_ru': latest_sport_post_ru,
        'latest_jamiyat_post_ru': latest_jamiyat_post_ru,
        'latest_jahon_post_ru': latest_jahon_post_ru,
        'latest_fantexnika_post_ru': latest_fantexnika_post_ru,
        'latest_madaniyat_post_ru': latest_madaniyat_post_ru,

        'post_jamiyat': post_jamiyat,
        'post_sport': post_sport,
        'post_jahon': post_jahon,

        'latest_post': latest_post,

        'jamiyat_posts_uz': jamiyat_posts_uz,
        'jamiyat_posts_en': jamiyat_posts_en,
        'jamiyat_posts_ru': jamiyat_posts_ru,
        'sport_posts_uz': sport_posts_uz,
        'sport_posts_en': sport_posts_en,
        'sport_posts_ru': sport_posts_ru,

        'all_posts': all_posts,

        'weekly_top_posts_uz': weekly_top_posts_uz,
        'weekly_top_posts_en': weekly_top_posts_en,
        'weekly_top_posts_ru': weekly_top_posts_ru,

        'language_code': request.LANGUAGE_CODE,
        'video_posts': video_posts,
    }

    return render(request, 'index.html', context)


def post_by_categories(request, category_name):
    categories = Categories.objects.all()
    category = get_object_or_404(Categories, name_uz=category_name)

    # Get the current language
    current_language = get_language()

    # Determine which fields to use based on the language
    if current_language == 'ru':
        title_field = 'title_ru'
        content_field = 'content_ru'
    elif current_language == 'en':
        title_field = 'title_en'
        content_field = 'content_en'
    else:  # default to Uzbek
        title_field = 'title_uz'
        content_field = 'content_uz'

    posts = Post.objects.filter(category=category).order_by('-created_ad').only(title_field, content_field, 'slug', 'image')

    # Prepare data for context
    posts_data = [
        {
            'title': getattr(post, title_field),
            'image': post.image.url if post.image else '',  # Check if image exists
            'slug': post.slug,
            'category_name': getattr(post.category, f'name_{current_language}')
        }
        for post in posts
    ]

    paginator = Paginator(posts_data, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'categories': categories,
        'category': category,
        'page_obj': page_obj,
    }

    return render(request, 'category.html', context=context)



def post_detail(request, slug):
    categories = Categories.objects.all()
    youtube_videos = YoutubeVideo.objects.all().order_by('-created_ad')[:5]
    post = get_object_or_404(Post, slug=slug)
    related_posts = Post.objects.filter(category=post.category).exclude(id=post.id)[:5]

    # Hozirgi tilni aniqlash
    current_language = get_language()

    # Tildan kelib chiqib tegishli maydonlarni aniqlash
    if current_language == 'ru':
        title = post.title_ru
        content = post.content_ru
        category_name = post.category.name_ru
    elif current_language == 'en':
        title = post.title_en
        content = post.content_en
        category_name = post.category.name_en
    else:
        title = post.title_uz
        content = post.content_uz
        category_name = post.category.name_uz

    context = {
        'post': post,
        'categories': categories,
        'related_posts': related_posts,
        'youtube_videos': youtube_videos,
        'title': title,
        'content': content,
        'category_name': category_name,
    }
    return render(request, 'details.html', context=context)


from django.db.models import Q

def search(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = Post.objects.filter(
            Q(title_uz__icontains=query) |
            Q(title_ru__icontains=query) |
            Q(title_en__icontains=query) |
            Q(content_uz__icontains=query) |
            Q(content_ru__icontains=query) |
            Q(content_en__icontains=query)
        )
    return render(request, 'search_results.html', {'results': results, 'query': query})



def get_currency_rates():
    # Fetching the latest exchange rates from a public API
    url = "https://v6.exchangerate-api.com/v6/922ab46cc16563b556e70cdb/latest/USD"
    response = requests.get(url)
    data = response.json()

    # Extracting relevant rates
    usd_to_uzs = data['conversion_rates']['UZS']
    rub_to_uzs = data['conversion_rates']['UZS'] / data['conversion_rates']['RUB']
    eur_to_uzs = data['conversion_rates']['UZS'] / data['conversion_rates']['EUR']

    usd_to_uzs_formatted = "{:,.2f}".format(usd_to_uzs)
    rub_to_uzs_formatted = "{:,.2f}".format(rub_to_uzs)
    eur_to_uzs_formatted = "{:,.2f}".format(eur_to_uzs)

    return {
        'usd_to_uzs': usd_to_uzs_formatted,
        'rub_to_uzs': rub_to_uzs_formatted,
        'eur_to_uzs':eur_to_uzs_formatted,
    }


def get_weather_data(city_name):
    api_key = "0e7cb669bdcd4d3c9e263346240608"  # WeatherAPI kalitini o'rniga qo'ying
    base_url = "https://api.weatherapi.com/v1/current.json?"
    complete_url = base_url + "key=" + api_key + "&q=" + city_name + "&aqi=no"

    try:
        response = requests.get(complete_url)
        response.raise_for_status()  # HTTP xatoliklarni tekshirish
        data = response.json()

        if "error" in data:
            return None

        city_weather = {
            "city": data["location"]["name"],
            "temperature": data["current"]["temp_c"],
            "condition": data["current"]["condition"]["text"],
        }

    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

    return city_weather


def base_view(request):
    cities = ['Tashkent', 'Samarkand', 'Bukhara', 'Fergana', 'Namangan', 'Andijan', 'Nukus', 'Karshi', 'Urgench']
    selected_city = request.GET.get('city', 'Tashkent')
    weather = get_weather_data(selected_city)

    return render(request, 'base.html', {'weather': weather, 'cities': cities, 'selected_city': selected_city})



def youtube_video_list(request):
    youtube_videos = YoutubeVideo.objects.all().values(
        'title_uz', 'content_uz', 'youtube_url', 'category__name_uz'
    )
    video_posts_json = json.dumps(list(youtube_videos))  # JSON formatiga o'tkazish
    return render(request, 'index.html', {'video_posts': video_posts_json})
