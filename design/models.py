from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True,
                                       verbose_name='Прошел активацию?')
    send_messages = models.BooleanField(default=True,
                                        verbose_name='Слать оповещения о новых комментариях?')

    patronymic = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Отчество'
    )

    class Meta(AbstractUser.Meta):
        pass

class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название категории')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

def validate_image_size(image):
    limit = 2 * 1024 * 1024
    if image.size > limit:
        raise ValidationError('Размер файла не должен превышать 2 Мб.')

class Application(models.Model):
    STATUS_CHOICES = (
        ('new', 'Новая'),
        ('in_progress', 'Принято в работу'),
        ('done', 'Выполнено'),
    )

    user = models.ForeignKey(AdvUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='Категория')

    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    image = models.ImageField(
        upload_to='applications/',
        verbose_name='Фото помещения',
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'bmp']),
            validate_image_size
        ]
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')

    admin_comment = models.TextField(blank=True, null=True, verbose_name='Комментарий администратора')
    design_image = models.ImageField(
        upload_to='designs/',
        blank=True,
        null=True,
        verbose_name='Готовый дизайн',
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'bmp']),
            validate_image_size
        ]
    )

    def __str__(self):
        return f"{self.title} ({self.user.username})"

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']