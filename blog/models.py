from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name="Назва")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"


class Post(models.Model):
    title = models.CharField(max_length=30, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Опис")
    published_date = models.DateTimeField(auto_created=True, verbose_name="Дата публікації")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категорія")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор", default='1')
    image = models.URLField(default="http://placehold.it/900x300")
    slug = models.SlugField(max_length=200, db_index=True, default='1')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock = models.PositiveIntegerField(default='1')
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Пости"

    def get_absolute_url(self):
        return reverse('blog:post',
                       args=[self.id, self.slug])


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='user_avatar')
    # avatar = models.URLField(default="https://cdn-icons-png.freepik.com/512/3135/3135715.png")
    telephone = models.CharField(max_length=10, default="+380-00-000-00-00", unique=True)

    def __str__(self):
        return self.user.username


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.text}"


class PostPhoto(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')
    image = models.ImageField(verbose_name="Фото", upload_to="Post_photos")

    class Meta:
        verbose_name = "Фото"
        verbose_name_plural = "Фотографії"
