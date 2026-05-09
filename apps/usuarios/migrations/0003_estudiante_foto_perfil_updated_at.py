from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("usuarios", "0002_alter_usuario_rol_docente_estudiante"),
    ]

    operations = [
        migrations.AddField(
            model_name="estudiante",
            name="foto_perfil_updated_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
