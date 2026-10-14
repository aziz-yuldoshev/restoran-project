from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, F

from .forms import *
from .models import *


# =========================
# HOME
# =========================

def index(request):

    categories = Category.objects.all()
    articles = Article.objects.all()

    favorite_ids = set()

    if request.user.is_authenticated:
        favorite_ids = set(
            Favorite.objects.filter(
                user=request.user
            ).values_list(
                'article_id',
                flat=True
            )
        )

    context = {
        'title': 'Main Page',
        'categories': categories,
        'articles': articles,
        'favorite_ids': favorite_ids,
    }

    return render(
        request,
        'blog/index.html',
        context
    )


# =========================
# LOGIN
# =========================

def user_login(request):

    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":

        form = LoginForm(data=request.POST)

        if form.is_valid():

            user = form.get_user()

            auth_login(request, user)

            messages.success(
                request,
                f"Welcome {user.username}!"
            )

            return redirect('index')

    else:

        form = LoginForm()

    return render(
        request,
        'blog/user_login.html',
        {
            'form': form,
            'title': 'Login'
        }
    )


# =========================
# REGISTER
# =========================

def register(request):

    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            auth_login(
                request,
                user
            )

            messages.success(
                request,
                "Account created successfully!"
            )

            return redirect('index')

    else:

        form = RegisterForm()

    return render(
        request,
        'blog/register.html',
        {
            'form': form,
            'title': 'Register'
        }
    )


# =========================
# LOGOUT
# =========================

def user_logout(request):

    auth_logout(request)

    return redirect('index')


# =========================
# ABOUT
# =========================

def about(request):

    return render(
        request,
        'blog/about.html',
        {
            'title': 'About Us'
        }
    )


# =========================
# RESERVATION
# =========================

def reservation(request):

    if request.method == "POST":

        messages.success(
            request,
            "Reservation successfully sent 🍽️"
        )

        return redirect('reservation')

    return render(
        request,
        'blog/reservation.html',
        {
            'title': 'Reservation'
        }
    )


# =========================
# SEARCH
# =========================

def search(request):

    word = request.GET.get('q')

    articles = Article.objects.all()

    if word:

        articles = articles.filter(
            Q(title__icontains=word) |
            Q(content__icontains=word)
        )

    favorite_ids = set()

    if request.user.is_authenticated:
        favorite_ids = set(
            Favorite.objects.filter(
                user=request.user
            ).values_list(
                'article_id',
                flat=True
            )
        )

    return render(
        request,
        'blog/index.html',
        {
            'title': 'Search',
            'articles': articles,
            'favorite_ids': favorite_ids,
        }
    )


# =========================
# CATEGORY
# =========================

def category_page(request, category_id):

    categories = Category.objects.all()

    category = get_object_or_404(
        Category,
        id=category_id
    )

    articles = Article.objects.filter(
        category=category
    )

    favorite_ids = set()

    if request.user.is_authenticated:
        favorite_ids = set(
            Favorite.objects.filter(
                user=request.user
            ).values_list(
                'article_id',
                flat=True
            )
        )

    return render(
        request,
        'blog/index.html',
        {
            'title': category.title,
            'categories': categories,
            'articles': articles,
            'favorite_ids': favorite_ids,
        }
    )


# =========================
# ARTICLE DETAIL
# =========================

def article_detail(request, article_id):

    article = get_object_or_404(
        Article,
        id=article_id
    )

    Article.objects.filter(
        id=article_id
    ).update(
        views=F('views') + 1
    )

    article.refresh_from_db()

    is_favorite = False

    if request.user.is_authenticated:

        is_favorite = Favorite.objects.filter(
            user=request.user,
            article=article
        ).exists()

    # Similar articles

    articles = Article.objects.filter(
        category=article.category
    ).exclude(
        id=article.id
    )

    return render(
        request,
        'blog/article_detail.html',
        {
            'title': article.title,
            'article': article,
            'articles': articles,
            'is_favorite': is_favorite,
        }
    )


# =========================
# ADD ARTICLE
# =========================

@login_required
def add_article(request):

    if request.method == "POST":

        form = ArticleForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            article = form.save()

            return redirect(
                'article',
                article.id
            )

    else:

        form = ArticleForm()

    return render(
        request,
        'blog/add_article.html',
        {
            'form': form,
            'title': 'Add Article'
        }
    )


# =========================
# UPDATE ARTICLE
# =========================

@login_required
def update_article(request, article_id):

    article = get_object_or_404(
        Article,
        id=article_id
    )

    if request.method == "POST":

        form = ArticleForm(
            request.POST,
            request.FILES,
            instance=article
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Article updated successfully!"
            )

            return redirect(
                'article',
                article.id
            )

    else:

        form = ArticleForm(
            instance=article
        )

    return render(
        request,
        'blog/update_article.html',
        {
            'form': form,
            'article': article,
            'title': 'Update Article'
        }
    )


# =========================
# DELETE ARTICLE
# =========================

@login_required
def delete_article(request, article_id):

    article = get_object_or_404(
        Article,
        id=article_id
    )

    if request.method == "POST":

        article.delete()

        messages.success(
            request,
            "Article deleted successfully!"
        )

        return redirect('index')

    return render(
        request,
        'blog/delete_article.html',
        {
            'article': article,
            'title': 'Delete Article'
        }
    )


# =========================
# TOGGLE FAVORITE
# =========================

@login_required
def toggle_favorite(request, article_id):

    article = get_object_or_404(
        Article,
        id=article_id
    )

    favorite = Favorite.objects.filter(
        user=request.user,
        article=article
    ).first()

    if favorite:

        favorite.delete()

        messages.success(
            request,
            f"💔 {article.title} removed from favorites!"
        )

    else:

        Favorite.objects.create(
            user=request.user,
            article=article
        )

        messages.success(
            request,
            f"❤️ {article.title} added to favorites!"
        )

    return redirect(
        request.META.get(
            'HTTP_REFERER',
            'index'
        )
    )


# =========================
# FAVORITES PAGE
# =========================

@login_required
def favorites(request):

    favorite_articles = Article.objects.filter(
        favorited_by__user=request.user
    )

    return render(
        request,
        'blog/favorites.html',
        {
            'title': 'My Favorites',
            'articles': favorite_articles
        }
    )