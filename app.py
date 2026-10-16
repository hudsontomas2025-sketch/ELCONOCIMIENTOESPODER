import os
from flask import Flask, render_template_string, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Base de datos en memoria dinámica
noticias_list = [
    {
        "id": 0,
        "titulo": "Alerta por El Niño en Concordia: Crecida del Río Uruguay obliga a evacuar familias en la costanera",
        "pais": "Argentina 🇦🇷",
        "fuente": "Diario El Heraldo / TN",
        "fecha": "11 Oct 2026",
        "resumen": "El río Uruguay superó niveles críticos en la costa de Concordia, desbordando áreas ribereñas e ingresando barro y agua a viviendas bajas.",
        "enlace": "https://www.fenix951.com.ar/noticia.php?id=356349",
        "imagen": "https://images.unsplash.com/photo-1547683905-f686c993aae5?auto=format&fit=crop&w=800&q=80"
    },
    {
        "id": 1,
        "titulo": "Aluvión en Santiago de Chile: Agua y lodo bajan de quebradas afectando viviendas y vehículos",
        "pais": "Chile 🇨🇱",
        "fuente": "Diario UNO / Senapred",
        "fecha": "10 Oct 2026",
        "resumen": "Más de 1.200 personas rescatadas y decenas de casas anegadas tras desprendimientos de barro y rocas precordilleranas.",
        "enlace": "https://www.diariouno.com.ar/sociedad/aluvion-chile-reportan-1200-rescatados-y-384-damnificados-y-sigue-el-debate-la-prevencion-n1605218",
        "imagen": "https://images.unsplash.com/photo-1584467735811-9985103cb136?auto=format&fit=crop&w=800&q=80"
    }
]

testimonios_list = [
    {
        "id": 0,
        "nombre": "Mariela Giménez (Vecina Barrio Puerto)",
        "ubicacion": "Concordia, Entre Ríos (Argentina)",
        "testimonio": "Cuando bajó el río, el lodo dentro de las piezas quedó como cemento fresco. Sacarlo a pala nos llevó días enteros y destrozó nuestras espaldas.",
        "fecha": "12 Oct 2026",
        "foto": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=200&q=80"
    },
    {
        "id": 1,
        "nombre": "Esteban Ruarte (Damnificado por crecida)",
        "ubicacion": "Salto / Concordia (Ribera del Río Uruguay)",
        "testimonio": "El mayor problema no es sacar el agua, sino el barro pesado que entra por las aberturas y se mete en cada rincón sin que las bombas comunes sirvan.",
        "fecha": "11 Oct 2026",
        "foto": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=200&q=80"
    }
]

soluciones_list = [
    {
        "id": 0,
        "titulo": "Rastrillo-Pala de Arrastre Ergonómico",
        "descripcion": "Diseñado para movilizar grandes volúmenes de lodo semi-húmedo en pasillos y habitaciones reducidas mediante arrastre horizontal.",
        "costo": "$15 - $25 USD",
        "categoria": "Herramienta Manual",
        "imagen": "https://images.unsplash.com/photo-1584467735811-9985103cb136?auto=format&fit=crop&w=600&q=80"
    },
    {
        "id": 1,
        "titulo": "Kit de Neutralización Enzimática de Lodo",
        "descripcion": "Solución de bajo costo basada en biopolímeros para romper la cohesión del barro arcilloso, facilitando su succión y lavado.",
        "costo": "$10 USD por kit",
        "categoria": "Insumo Químico / Biológico",
        "imagen": "https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?auto=format&fit=crop&w=600&q=80"
    }
]

equipo_list = [
    {"nombre": "Tomás Hudson", "rol": "Integrantes del Equipo ELCONOCIMIENTOESPODER"},
    {"nombre": "Colaboradores UNER Concordia", "rol": "Sede Académica - Entre Ríos, Argentina"}
]

archivos_estado = {
    "youtube_id": "dQw4w9WgXcQ",
    "tiktok_url": "https://www.tiktok.com/embed/7234567890123456789" # Puedes cambiarlo o actualizarlo
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
        :root { --primary: #1b2a47; --accent: #d97706; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f8fafc; color: #334155; }
        header { background: linear-gradient(135deg, var(--primary), #0f172a); color: white; padding: 45px 0; border-bottom: 4px solid var(--accent); }
        .mode-bar { background-color: #0f172a; color: #cbd5e1; padding: 8px 0; font-size: 0.85rem; }
        .card-custom { border: none; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); position: relative; }
        .carousel-item-news { height: 380px; background-size: cover; background-position: center; border-radius: 12px; position: relative; }
        .carousel-overlay { position: absolute; bottom: 0; top: 0; left: 0; right: 0; background: linear-gradient(to top, rgba(15,23,42,0.95) 15%, rgba(15,23,42,0.4) 60%); border-radius: 12px; padding: 30px; display: flex; flex-direction: column; justify-content: flex-end; color: white; }
        .modo-espectador-hide { display: block; }
        body.espectador-active .modo-espectador-hide { display: none !important; }
        .btn-delete-card { position: absolute; top: 10px; right: 10px; z-index: 10; }
        .metric-card { background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4
