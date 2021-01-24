# Generated by Django 3.0.5 on 2020-08-05 16:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_tags'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tags',
            old_name='tags',
            new_name='tag',
        ),
        migrations.RemoveField(
            model_name='tags',
            name='auction',
        ),
        migrations.AddField(
            model_name='listings',
            name='tag',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auctions.Tags'),
        ),
    ]