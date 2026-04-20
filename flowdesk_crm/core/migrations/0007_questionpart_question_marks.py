from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_maillog_pendingmail'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionpart',
            name='question_marks',
            field=models.TextField(blank=True, default=''),
        ),
    ]
