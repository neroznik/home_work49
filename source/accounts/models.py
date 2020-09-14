from django.db import models
from django.contrib.auth import get_user_model

class Profile(models.Model):
    avatar = models.ImageField(null=True, blank=True, upload_to='user_pics', verbose_name='Аватар')
    user = models.OneToOneField(get_user_model(), related_name='profile', on_delete=models.CASCADE, verbose_name='Пользователь')
    about = models.TextField(max_length=4000, null=True,blank=True, verbose_name='О себе')
    git_url = models.URLField(max_length=200, null=True,blank=True, verbose_name= 'GitHub link')


    def __str__(self):
        return self.user.get_full_name() + "'s Profile"

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        permissions = [('can_see_list','Может видеть пользователей')]