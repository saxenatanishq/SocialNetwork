# Generated by Django 5.1.4 on 2025-03-03 15:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_remove_thread_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thread',
            name='comments',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
