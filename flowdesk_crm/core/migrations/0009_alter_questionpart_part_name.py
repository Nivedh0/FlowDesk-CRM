from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_questionpart_question_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionpart',
            name='part_name',
            field=models.CharField(max_length=50),
        ),
    ]
