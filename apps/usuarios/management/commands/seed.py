from django.core.management.base import BaseCommand

from apps.usuarios.seeds.runner import run_seed


class Command(BaseCommand):
    help = "Carga datos iniciales de demostracion en espanol."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Elimina primero los datos de demostracion administrados por el seed.",
        )

    def handle(self, *args, **options):
        summary = run_seed(reset=options["reset"])

        self.stdout.write(self.style.SUCCESS("Seed completado correctamente."))
        self.stdout.write("")
        self.stdout.write("Resumen:")
        for label, count in summary.items():
            self.stdout.write(f"- {label}: {count}")

        self.stdout.write("")
        self.stdout.write("Credenciales de prueba:")
        self.stdout.write("- admin / Demo12345!")
        self.stdout.write("- docente.ana / Demo12345!")
        self.stdout.write("- estudiante.lucia / Demo12345!")
