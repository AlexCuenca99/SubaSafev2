# Generated by Django 3.2.10 on 2022-01-21 17:55

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('start', models.DateTimeField()),
                ('current_time', models.DateTimeField()),
                ('article', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='articulo_subasta', to='article.article')),
            ],
            options={
                'verbose_name': 'Subasta',
                'verbose_name_plural': 'Subastas',
            },
        ),
    ]
