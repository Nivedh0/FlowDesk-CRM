from django.db import migrations, models
import django.db.models.deletion


DEFAULT_SOURCES = [
    "Walk-in",
    "Website",
    "Call",
    "Reference",
    "Facebook",
    "Instagram",
    "LinkedIn",
    "Other",
]


LEGACY_SOURCE_LABELS = {
    "walk-in": "Walk-in",
    "website": "Website",
    "call": "Call",
    "reference": "Reference",
    "facebook": "Facebook",
    "instagram": "Instagram",
    "linkedin": "LinkedIn",
    "other": "Other",
}


def forwards_copy_sources(apps, schema_editor):
    Source = apps.get_model("core", "Source")
    StudentEnquiry = apps.get_model("core", "StudentEnquiry")
    db_alias = schema_editor.connection.alias

    source_map = {}
    for source_name in DEFAULT_SOURCES:
        source_obj, _ = Source.objects.using(db_alias).get_or_create(source_name=source_name)
        source_map[source_name.lower()] = source_obj.id

    for lead in StudentEnquiry.objects.using(db_alias).all():
        raw_value = (lead.source or "").strip()
        if not raw_value:
            continue

        source_name = LEGACY_SOURCE_LABELS.get(raw_value.lower(), raw_value)
        source_obj, _ = Source.objects.using(db_alias).get_or_create(source_name=source_name)
        lead.source_ref_id = source_obj.id
        lead.save(update_fields=["source_ref"])


def backwards_copy_sources(apps, schema_editor):
    StudentEnquiry = apps.get_model("core", "StudentEnquiry")
    db_alias = schema_editor.connection.alias

    for lead in StudentEnquiry.objects.using(db_alias).select_related("source_ref"):
        lead.source = lead.source_ref.source_name if lead.source_ref else ""
        lead.save(update_fields=["source"])


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0013_pendingmail_maillog_overdue_fee"),
    ]

    operations = [
        migrations.CreateModel(
            name="Source",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("source_name", models.CharField(max_length=50, unique=True)),
            ],
            options={
                "ordering": ["source_name"],
            },
        ),
        migrations.AddField(
            model_name="studentenquiry",
            name="source_ref",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to="core.source"),
        ),
        migrations.RunPython(forwards_copy_sources, backwards_copy_sources),
        migrations.RemoveField(
            model_name="studentenquiry",
            name="source",
        ),
        migrations.RenameField(
            model_name="studentenquiry",
            old_name="source_ref",
            new_name="source",
        ),
    ]
