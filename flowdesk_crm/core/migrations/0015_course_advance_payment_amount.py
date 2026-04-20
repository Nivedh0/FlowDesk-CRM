from decimal import Decimal

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0014_source_model_and_studentenquiry_source_fk"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="advance_payment_amount",
            field=models.DecimalField(decimal_places=2, default=Decimal("1000.00"), max_digits=10),
        ),
    ]
