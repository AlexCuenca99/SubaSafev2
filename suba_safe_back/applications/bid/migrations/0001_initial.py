# Generated by Django 3.2.10 on 2022-01-06 18:33

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
            name='Bid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('offer', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Oferta')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articulo_ofertas', to='article.article')),
            ],
            options={
                'verbose_name': 'Oferta',
                'verbose_name_plural': 'Ofertas',
            },
        ),
    ]
