from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_payment_legacy_component_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='maillog',
            name='fee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mail_logs', to='core.fee'),
        ),
        migrations.AddField(
            model_name='pendingmail',
            name='fee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pending_mails', to='core.fee'),
        ),
        migrations.AlterField(
            model_name='maillog',
            name='mail_type',
            field=models.CharField(choices=[('batch', 'Batch Assignment'), ('payment', 'Payment Success'), ('overdue', 'Overdue Mail')], max_length=20),
        ),
        migrations.AlterField(
            model_name='pendingmail',
            name='mail_type',
            field=models.CharField(choices=[('batch', 'Batch Assignment'), ('payment', 'Payment Success'), ('overdue', 'Overdue Mail')], max_length=20),
        ),
    ]
