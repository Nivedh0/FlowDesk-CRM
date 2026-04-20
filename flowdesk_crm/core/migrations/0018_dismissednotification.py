from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0017_studentenquiry_dob_guardian_number_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DismissedNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_key', models.CharField(max_length=120)),
                ('dismissed_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dismissed_notifications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-dismissed_at'],
            },
        ),
        migrations.AddConstraint(
            model_name='dismissednotification',
            constraint=models.UniqueConstraint(fields=('user', 'notification_key'), name='unique_dismissed_notification'),
        ),
    ]
