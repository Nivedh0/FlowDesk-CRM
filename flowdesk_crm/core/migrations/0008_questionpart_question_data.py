from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_questionpart_question_marks'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionpart',
            name='question_data',
            field=models.JSONField(blank=True, default=list),
        ),
    ]
