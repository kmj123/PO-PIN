

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0011_companionpost_report_count_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companionpost',
            name='report_count',
        ),
        migrations.RemoveField(
            model_name='exchangereview',
            name='report_count',
        ),
        migrations.RemoveField(
            model_name='proxypost',
            name='report_count',
        ),
        migrations.RemoveField(
            model_name='sharingpost',
            name='report_count',
        ),
        migrations.RemoveField(
            model_name='statuspost',
            name='report_count',
        ),
    ]
