# Generated by Django 2.2.5 on 2020-03-04 11:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('products', '0004_auto_20190917_0012'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('items', models.ManyToManyField(to='products.Article')),
                ('ownwer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Profile')),
            ],
        ),
    ]