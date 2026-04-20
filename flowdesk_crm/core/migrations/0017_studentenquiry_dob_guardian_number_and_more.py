from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_fee_custom_installment_plan'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentenquiry',
            name='dob',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='studentenquiry',
            name='guardian_number',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='studentenquiry',
            name='year_of_passing',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
