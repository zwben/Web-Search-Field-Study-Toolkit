# Generated by Django 3.2.7 on 2022-02-12 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_system', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resetpasswordrequest',
            name='expire',
            field=models.IntegerField(default=1644817086),
        ),
        migrations.AlterField(
            model_name='resetpasswordrequest',
            name='token',
            field=models.CharField(default='6e670984de7d', max_length=50),
        ),
    ]
