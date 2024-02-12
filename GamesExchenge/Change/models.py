from django.db import models
from django.contrib.auth.models import User


# Платформа на которой выпущена как игра (их может быть несколько), и предлагаемый товар (там платформа одна)
class Platform(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    pic = models.ImageField(upload_to='platform/pics/%Y/%m/%d', blank=True)
    game = models.ManyToManyField('Game', through='GamePlatform', blank=True, related_name='platform')

    def __str__(self):
        return self.title


# Тэги жанры игры
class Tags(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    game = models.ManyToManyField('Game', through='GameTags', blank=True, related_name='tag')

    def __str__(self):
        return self.title


# Комментарии к товару
class Comments(models.Model):
    user = models.ForeignKey(User,
                             verbose_name='Автор коментария',
                             on_delete=models.SET_DEFAULT,
                             blank=True,
                             default='Пользователь не найден',
                             related_name='comment_user')
    good = models.ForeignKey('Goods',
                             verbose_name='Товар',
                             on_delete=models.CASCADE,
                             related_name='good')
    text = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


# Ответ на комментарий
class Answer(models.Model):
    comment = models.ForeignKey(Comments,
                                verbose_name='Комент',
                                on_delete=models.CASCADE,
                                related_name='comment')
    user = models.ForeignKey(User,
                             verbose_name='Автор ответа',
                             on_delete=models.SET_DEFAULT,
                             default='Пользователь не найден',
                             related_name='answer_user')
    text = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


# Отзыв на пользователя
class Review(models.Model):
    author = models.ForeignKey(User,
                               verbose_name='Автор отзыва',
                               on_delete=models.SET_DEFAULT,
                               default='Пользователь не найден',
                               related_name='author')
    rewuser = models.ForeignKey(User,
                                verbose_name='Пользователь, которому оставили отзыв',
                                on_delete=models.CASCADE,
                                related_name='rewuser')
    text = models.TextField()
    rating = models.IntegerField(default=0)
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

# Модель чата
class Chat(models.Model):
    sender = models.ForeignKey(User,
                               verbose_name='Отправитель',
                               on_delete=models.CASCADE,
                               related_name='sender')
    recipient = models.ForeignKey(User,
                                  verbose_name='Получатель',
                                  on_delete=models.CASCADE,
                                  related_name='recipient')


# Модель сообщения
class Message(models.Model):
    chat = models.ForeignKey(Chat, verbose_name='Чат', on_delete=models.CASCADE, related_name='chat')
    text = models.TextField('Сообщение')
    time_create = models.DateTimeField(auto_now_add=True)
    isRead = models.BooleanField(default=False)

    def __str__(self):
        return self.text


# Игра, отображает платформы, жанры, гот выпуска
class Game(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    photo = models.ImageField(upload_to='photos/%Y/%m/%d')
    year = models.IntegerField()
    rating = models.IntegerField()
    game_platform = models.ManyToManyField('Game',
                                      through='GamePlatform',
                                      blank=True)
    tags = models.ManyToManyField(Tags, through='GameTags', blank=True, related_name='tag')
    desired_games = models.ManyToManyField('Goods', through='GameGoods', blank=True)


    def __str__(self):
        return self.title


# Товар указывается конкретная игра, которую предлагает пользователь, так же содержит желаемые для обмена игры
class Goods(models.Model):
    goods_game = models.ForeignKey(Game, verbose_name='Игра', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='Опубликовал', on_delete=models.CASCADE)
    title = models.CharField('Текст объявления', max_length=100)
    goods_platform = models.ForeignKey(Platform, verbose_name='Платформа', on_delete=models.CASCADE)
    price = models.IntegerField('Цена')
    goods_desired_games = models.ManyToManyField(Game, through='GameGoods', blank=True, related_name='desired')
    text = models.TextField()
    isPublished = models.BooleanField(default=False)
    just_sell = models.BooleanField(default=False)
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Технические таблицы для реализации связей многие со многими
class GamePlatform(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)


class GameTags(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    tags = models.ForeignKey(Tags, on_delete=models.CASCADE)

class GameGoods(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    good = models.ForeignKey(Goods, on_delete=models.CASCADE)
