from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0015_course_advance_payment_amount"),
    ]

    operations = [
        migrations.AddField(
            model_name="fee",
            name="custom_installment_plan",
            field=models.BooleanField(default=False),
        ),
    ]
