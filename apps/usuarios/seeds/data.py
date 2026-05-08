from datetime import timedelta
from uuid import UUID

from django.utils import timezone

NOW = timezone.now()

ADMIN_USERS = [
    {
        "username": "admin",
        "email": "admin@unisca.edu.pe",
        "first_name": "Valeria",
        "last_name": "Quispe Ramos",
    }
]

DOCENTES = [
    {
        "username": "docente.ana",
        "email": "ana.torres@unisca.edu.pe",
        "first_name": "Ana",
        "last_name": "Torres Salazar",
        "codigo_docente": "DOC-001",
        "departamento": "Ingenieria de Software",
    },
    {
        "username": "docente.carlos",
        "email": "carlos.mendoza@unisca.edu.pe",
        "first_name": "Carlos",
        "last_name": "Mendoza Paredes",
        "codigo_docente": "DOC-002",
        "departamento": "Ciencias de la Computacion",
    },
    {
        "username": "docente.maria",
        "email": "maria.fernandez@unisca.edu.pe",
        "first_name": "Maria",
        "last_name": "Fernandez Rojas",
        "codigo_docente": "DOC-003",
        "departamento": "Matematica Aplicada",
    },
]

ESTUDIANTES = [
    {
        "username": "estudiante.lucia",
        "email": "lucia.vargas@alumnos.unisca.edu.pe",
        "first_name": "Lucia",
        "last_name": "Vargas Huaman",
        "codigo_estudiante": "EST-2026-001",
        "carrera": "Ingenieria de Software",
        "ciclo": 5,
    },
    {
        "username": "estudiante.diego",
        "email": "diego.ramirez@alumnos.unisca.edu.pe",
        "first_name": "Diego",
        "last_name": "Ramirez Soto",
        "codigo_estudiante": "EST-2026-002",
        "carrera": "Ingenieria de Software",
        "ciclo": 5,
    },
    {
        "username": "estudiante.camila",
        "email": "camila.rojas@alumnos.unisca.edu.pe",
        "first_name": "Camila",
        "last_name": "Rojas Medina",
        "codigo_estudiante": "EST-2026-003",
        "carrera": "Ciencia de Datos",
        "ciclo": 4,
    },
    {
        "username": "estudiante.mateo",
        "email": "mateo.castro@alumnos.unisca.edu.pe",
        "first_name": "Mateo",
        "last_name": "Castro Leon",
        "codigo_estudiante": "EST-2026-004",
        "carrera": "Ciencia de Datos",
        "ciclo": 4,
    },
    {
        "username": "estudiante.sofia",
        "email": "sofia.navarro@alumnos.unisca.edu.pe",
        "first_name": "Sofia",
        "last_name": "Navarro Flores",
        "codigo_estudiante": "EST-2026-005",
        "carrera": "Ingenieria de Sistemas",
        "ciclo": 6,
    },
    {
        "username": "estudiante.joaquin",
        "email": "joaquin.arias@alumnos.unisca.edu.pe",
        "first_name": "Joaquin",
        "last_name": "Arias Cardenas",
        "codigo_estudiante": "EST-2026-006",
        "carrera": "Ingenieria de Sistemas",
        "ciclo": 6,
    },
    {
        "username": "estudiante.valentina",
        "email": "valentina.perez@alumnos.unisca.edu.pe",
        "first_name": "Valentina",
        "last_name": "Perez Luna",
        "codigo_estudiante": "EST-2026-007",
        "carrera": "Ingenieria Industrial",
        "ciclo": 3,
    },
    {
        "username": "estudiante.sebastian",
        "email": "sebastian.gomez@alumnos.unisca.edu.pe",
        "first_name": "Sebastian",
        "last_name": "Gomez Marin",
        "codigo_estudiante": "EST-2026-008",
        "carrera": "Ingenieria Industrial",
        "ciclo": 3,
    },
    {
        "username": "estudiante.renata",
        "email": "renata.salas@alumnos.unisca.edu.pe",
        "first_name": "Renata",
        "last_name": "Salas Vega",
        "codigo_estudiante": "EST-2026-009",
        "carrera": "Administracion",
        "ciclo": 2,
    },
    {
        "username": "estudiante.andres",
        "email": "andres.molina@alumnos.unisca.edu.pe",
        "first_name": "Andres",
        "last_name": "Molina Campos",
        "codigo_estudiante": "EST-2026-010",
        "carrera": "Administracion",
        "ciclo": 2,
    },
    {
        "username": "estudiante.paula",
        "email": "paula.silva@alumnos.unisca.edu.pe",
        "first_name": "Paula",
        "last_name": "Silva Herrera",
        "codigo_estudiante": "EST-2026-011",
        "carrera": "Contabilidad",
        "ciclo": 1,
    },
    {
        "username": "estudiante.nicolas",
        "email": "nicolas.cruz@alumnos.unisca.edu.pe",
        "first_name": "Nicolas",
        "last_name": "Cruz Tapia",
        "codigo_estudiante": "EST-2026-012",
        "carrera": "Contabilidad",
        "ciclo": 1,
    },
]

CURSOS = [
    {
        "codigo": "ISW-501",
        "nombre": "Arquitectura de Software",
        "ciclo_academico": 202601,
        "codigo_docente": "DOC-001",
    },
    {
        "codigo": "ISW-502",
        "nombre": "Gestion de Proyectos Agiles",
        "ciclo_academico": 202601,
        "codigo_docente": "DOC-001",
    },
    {
        "codigo": "CCD-401",
        "nombre": "Aprendizaje Automatico",
        "ciclo_academico": 202601,
        "codigo_docente": "DOC-002",
    },
    {
        "codigo": "SIS-601",
        "nombre": "Seguridad Informatica",
        "ciclo_academico": 202601,
        "codigo_docente": "DOC-002",
    },
    {
        "codigo": "MAT-301",
        "nombre": "Estadistica Aplicada",
        "ciclo_academico": 202601,
        "codigo_docente": "DOC-003",
    },
    {
        "codigo": "ADM-201",
        "nombre": "Analisis de Procesos",
        "ciclo_academico": 202601,
        "codigo_docente": "DOC-003",
    },
]

SESIONES = [
    {
        "codigo": "ISW-501-ACTIVA",
        "curso_codigo": "ISW-501",
        "qr_token": UUID("11111111-1111-4111-8111-111111111111"),
        "fecha_inicio": NOW - timedelta(hours=1),
        "fecha_fin": None,
        "activa": True,
    },
    {
        "codigo": "ISW-501-CERRADA",
        "curso_codigo": "ISW-501",
        "qr_token": UUID("11111111-1111-4111-8111-111111111112"),
        "fecha_inicio": NOW - timedelta(days=2, hours=2),
        "fecha_fin": NOW - timedelta(days=2, hours=1),
        "activa": False,
    },
    {
        "codigo": "ISW-502-ACTIVA",
        "curso_codigo": "ISW-502",
        "qr_token": UUID("22222222-2222-4222-8222-222222222221"),
        "fecha_inicio": NOW - timedelta(minutes=45),
        "fecha_fin": None,
        "activa": True,
    },
    {
        "codigo": "CCD-401-ACTIVA",
        "curso_codigo": "CCD-401",
        "qr_token": UUID("33333333-3333-4333-8333-333333333331"),
        "fecha_inicio": NOW - timedelta(minutes=30),
        "fecha_fin": None,
        "activa": True,
    },
    {
        "codigo": "SIS-601-ACTIVA",
        "curso_codigo": "SIS-601",
        "qr_token": UUID("44444444-4444-4444-8444-444444444441"),
        "fecha_inicio": NOW - timedelta(minutes=20),
        "fecha_fin": None,
        "activa": True,
    },
    {
        "codigo": "MAT-301-CERRADA",
        "curso_codigo": "MAT-301",
        "qr_token": UUID("55555555-5555-4555-8555-555555555551"),
        "fecha_inicio": NOW - timedelta(days=1, hours=3),
        "fecha_fin": NOW - timedelta(days=1, hours=2),
        "activa": False,
    },
]

ASISTENCIAS = [
    {
        "sesion_codigo": "ISW-501-ACTIVA",
        "codigo_estudiante": "EST-2026-001",
        "metodo": "qr+facial",
        "face_verified": True,
        "timestamp_registro": NOW - timedelta(minutes=50),
    },
    {
        "sesion_codigo": "ISW-501-ACTIVA",
        "codigo_estudiante": "EST-2026-002",
        "metodo": "qr",
        "face_verified": False,
        "timestamp_registro": NOW - timedelta(minutes=45),
    },
    {
        "sesion_codigo": "ISW-501-CERRADA",
        "codigo_estudiante": "EST-2026-001",
        "metodo": "qr+facial",
        "face_verified": True,
        "timestamp_registro": NOW - timedelta(days=2, minutes=40),
    },
    {
        "sesion_codigo": "ISW-501-CERRADA",
        "codigo_estudiante": "EST-2026-003",
        "metodo": "qr+facial",
        "face_verified": True,
        "timestamp_registro": NOW - timedelta(days=2, minutes=35),
    },
    {
        "sesion_codigo": "ISW-502-ACTIVA",
        "codigo_estudiante": "EST-2026-005",
        "metodo": "qr",
        "face_verified": False,
        "timestamp_registro": NOW - timedelta(minutes=25),
    },
    {
        "sesion_codigo": "CCD-401-ACTIVA",
        "codigo_estudiante": "EST-2026-003",
        "metodo": "qr+facial",
        "face_verified": True,
        "timestamp_registro": NOW - timedelta(minutes=20),
    },
    {
        "sesion_codigo": "SIS-601-ACTIVA",
        "codigo_estudiante": "EST-2026-006",
        "metodo": "qr+facial",
        "face_verified": True,
        "timestamp_registro": NOW - timedelta(minutes=15),
    },
    {
        "sesion_codigo": "MAT-301-CERRADA",
        "codigo_estudiante": "EST-2026-009",
        "metodo": "qr",
        "face_verified": False,
        "timestamp_registro": NOW - timedelta(days=1, hours=2, minutes=30),
    },
]
