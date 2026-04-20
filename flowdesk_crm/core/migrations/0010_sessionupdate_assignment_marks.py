from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_questionpart_part_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='sessionupdate',
            name='assignment_marks',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
