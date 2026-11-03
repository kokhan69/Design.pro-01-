from django.db import models
from django.contrib.auth.models import AbstractUser

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