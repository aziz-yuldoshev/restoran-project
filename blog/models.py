from django.db import models


# =========================
# CATEGORY
# =========================

class Category(models.Model):

    title = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Category Title"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


# =========================
# ARTICLE
# =========================

class Article(models.Model):

    title = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Article Title"
    )

    content = models.TextField(
        verbose_name="Article Content"
    )

    photo = models.ImageField(
        upload_to="photos/",
        verbose_name="Article Photo",
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Article Created"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Article Updated"
    )

    publish = models.BooleanField(
        default=True,
        verbose_name="Article Published"
    )

    views = models.IntegerField(
        default=0,
        verbose_name="Article Views"
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Article Price"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Article Category"
    )


    # =========================
    # PHOTO
    # =========================

    def get_photo(self):

        if self.photo:
            return self.photo.url

        return (
            'https://tse1.mm.bing.net/th/id/'
            'OIP.dyo8eAySdb2afZg3eszPQAHaFj'
            '?r=0&rs=1&pid=ImgDetMain&o=7&rm=3'
        )


    # =========================
    # STRING
    # =========================

    def __str__(self):
        return self.title


    # =========================
    # META
    # =========================

    class Meta:

        verbose_name = "Article"
        verbose_name_plural = "Articles"


# =========================
# FAVORITE
# =========================

class Favorite(models.Model):

    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='favorites'
    )

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='favorited_by'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    # =========================
    # STRING
    # =========================

    def __str__(self):
        return f"{self.user.username} - {self.article.title}"


    # =========================
    # META
    # =========================

    class Meta:

        verbose_name = "Favorite"
        verbose_name_plural = "Favorites"

        unique_together = (
            'user',
            'article'
        )