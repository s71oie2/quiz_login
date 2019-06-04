# Generated by Django 2.1.5 on 2019-06-04 03:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('staff', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='qna',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='질문자'),
        ),
        migrations.AddField(
            model_name='hitcount',
            name='post',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='staff.Board'),
        ),
        migrations.AddField(
            model_name='board',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staff.Category', verbose_name='분류'),
        ),
        migrations.AddField(
            model_name='board',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='boards', to=settings.AUTH_USER_MODEL, verbose_name='게시자'),
        ),
    ]