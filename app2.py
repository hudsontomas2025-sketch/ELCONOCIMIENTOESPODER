import os
from flask import Flask, render_template_string, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Lista de Noticias con noticias reales de Octubre 2026
noticias_list = [
    {
        "titulo": "Alerta por El Niño en Concordia: Crecida del Río Uruguay obliga a evacuar familias en la costanera",
        "pais": "Argentina 🇦🇷",
        "fuente": "Diario El Heraldo / TN",
        "fecha": "11 Oct 2026",
        "resumen": "El río Uruguay superó los 11 metros en la costa de Concordia, desbordando áreas ribereñas e ingresando barro y agua a viviendas bajas.",
        "enlace": "https://www.fenix951.com.ar/noticia.php?id=356349",
        "imagen": "https://images.unsplash.com/photo-1547683905-f686c993aae5?auto=format&fit=crop&w=800&q=80"
    },
    {
        "titulo": "Aluvión en Santiago de Chile: Agua y lodo bajan de quebradas afectando viviendas y vehículos",
        "pais": "Chile 🇨🇱",
        "fuente": "Diario UNO / Senapred",
        "fecha": "10 Oct 2026",
        "resumen": "Más de 1.200 personas rescatadas y 56 casas destruidas tras el desprendimiento de barro y rocas precordilleranas.",
        "enlace": "https://www.diariouno.com.ar/sociedad/aluvion-chile-reportan-1200-rescatados-y-384-damnificados-y-sigue-el-debate-la-prevencion-n1605218",
        "imagen": "https://images.unsplash.com/photo-1584467735811-9985103cb136?auto=format&fit=crop&w=800&q=80"
    },
    {
        "titulo": "Emergencia Hídrica Provincial: Refuerzan barreras y tareas de desobstrucción de lodo",
        "pais": "Argentina 🇦🇷",
        "fuente": "Infobae",
        "fecha": "09 Oct 2026",
        "resumen": "Defensa Civil e instituciones locales coordinan brigadas comunitarias para asistir en la remoción rápida de sedimentos en zonas anegadas.",
        "enlace": "https://www.infobae.com/sociedad/2026/10/10/evacuaron-a-seis-familias-en-concordia-y-alertaron-por-una-nueva-crecida-critica-del-rio-uruguay/",
        "imagen": "https://images.unsplash.com/photo-1515694346937-94d85e41e6f0?auto=format&fit=crop&w=800&q=80"
    }
]

# Testimonios del Mundo
testimonios_list = [
    {
        "nombre": "Carlos M. González",
        "ubicacion": "Concordia, Entre Ríos (Argentina)",
        "testimonio": "El barro se secó como cemento en cuestión de horas dentro de mi casa. Sin luz no podíamos usar bombas convencionales. Dispositivos manuales de arrastre son vitales para estas emergencias.",
        "fecha": "12 Oct 2026",
        "foto": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=200&q=80"
    },
    {
        "nombre": "Francisca Silva",
        "ubicacion": "Las Condes, Santiago (Chile)",
        "testimonio": "Cuando bajó el aluvión de la quebrada, lo más duro fue retirar el lodo espeso de los pasillos estrechos. Las palas normales te rompen la espalda al levantar el peso muerto.",
        "fecha": "11 Oct 2026",
        "foto": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=200&q=80"
    }
]

soluciones_list = [
    {
        "titulo": "Rastrillo-Pala de Arrastre Ergonómico",
        "descripcion": "Diseñado para movilizar grandes volúmenes de lodo semi-húmedo en pasillos y habitaciones reducidas mediante arrastre horizontal.",
        "costo": "$15 - $25 USD",
        "categoria": "Herramienta Manual",
        "imagen": "https://images.unsplash.com/photo-1584467735811-9985103cb136?auto=format&fit=crop&w=600&q=80"
    },
    {
        "titulo": "Hidro-Extractor Venturi Comunitario",
        "descripcion": "Dispositivo hidráulico portátil que utiliza presión de agua externa para generar succión por vacío en rincones complejos.",
        "costo": "$40 - $70 USD",
        "categoria": "Succión / Hidráulico",
        "imagen": "https://images.unsplash.com/photo-1547683905-f686c993aae5?auto=format&fit=crop&w=600&q=80"
    }
]

archivos_estado = {
    "informe_pdf": None,
    "informe_financiero": None,
    "youtube_id": "dQw4w9WgXcQ"
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Remoción de Barro - ELCONOCIMIENTOESPODER</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --primary-color: #1b2a47;
            --accent-color: #d97706;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f8fafc;
            color: #334155;
        }
        header {
            background: linear-gradient(135deg, var(--primary-color), #0f172a);
            color: white;
            padding: 45px 0;
            border-bottom: 4px solid var(--accent-color);
        }
        .mode-bar {
            background-color: #0f172a;
            color: #cbd5e1;
            padding: 8px 0;
            font-size: 0.85rem;
        }
        .card-custom {
            border: none;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }
        .badge-team {
            background-color: var(--accent-color);
            color: white;
        }
        .video-container {
            position: relative;
            padding-bottom: 56.25%;
            height: 0;
            overflow: hidden;
            border-radius: 12px;
            background-color: #000;
        }
        .video-container iframe {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%; border: 0;
        }
        .pdf-preview {
            width: 100%; height: 380px; border: 1px solid #e2e8f0; border-radius: 8px;
        }
        .foda-card {
            border-radius: 10px; padding: 20px; color: #fff;
        }
        .foda-f { background-color: #15803d; }
        .foda-o { background-color: #0369a1; }
        .foda-d { background-color: #c2410c; }
        .foda-a { background-color: #b91c1c; }
        
        /* Estilos del Carrusel de Noticias */
        .carousel-item-news {
            height: 380px;
            background-size: cover;
            background-position: center;
            border-radius: 12px;
            position: relative;
        }
        .carousel-overlay {
            position: absolute;
            bottom: 0; top: 0; left: 0; right: 0;
            background: linear-gradient(to top, rgba(15,23,42,0.95) 15%, rgba(15,23,42,0.4) 60%, rgba(0,0,0,0.1));
            border-radius: 12px;
            padding: 30px;
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            color: white;
        }
        
        .modo-espectador-hide { display: block; }
        body.espectador-active .modo-espectador-hide { display: none !important; }
        
        footer {
            background-color: var(--primary-color); color: white; padding: 4
