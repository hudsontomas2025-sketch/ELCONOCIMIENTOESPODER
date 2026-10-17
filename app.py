import os
from flask import Flask, render_template_string, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuración de carpeta de descargas/archivos
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'pdf', 'xlsx', 'xls', 'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Datos iniciales en memoria
noticias_list = [
    {"id": 0, "titulo": "Alerta por El Niño en Concordia: Crecida del Río Uruguay", "pais": "Argentina 🇦🇷", "resumen": "El río Uruguay superó niveles críticos en la costa de Concordia.", "enlace": "https://www.fenix951.com.ar/noticia.php?id=356349", "imagen": "https://images.unsplash.com/photo-1547683905-f686c993aae5?auto=format&fit=crop&w=800&q=80"}
]

testimonios_list = [
    {"id": 0, "nombre": "Mariela Giménez (Vecina Barrio Puerto)", "ubicacion": "Concordia, Entre Ríos", "testimonio": "Cuando bajó el río, el lodo dentro de las piezas quedó como cemento fresco."}
]

soluciones_list = [
    {"id": 0, "titulo": "Rastrillo-Pala de Arrastre Ergonómico", "descripcion": "Diseñado para movilizar grandes volúmenes de lodo en espacios reducidos.", "costo": "$15 - $25 USD", "categoria": "Herramienta Manual", "imagen": "https://images.unsplash.com/photo-1584467735811-9985103cb136?auto=format&fit=crop&w=600&q=80"}
]

equipo_list = [
    {"nombre": "Tomás Hudson", "rol": "Integrantes del Equipo ELCONOCIMIENTOESPODER"},
    {"nombre": "Colaboradores UNER Concordia", "rol": "Sede Académica - Entre Ríos, Argentina"}
]

documentos_list = [
    {"id": 0, "nombre": "Informe_Tecnico_Desafio06.pdf", "tipo": "pdf", "fecha": "16 Oct 2026"},
    {"id": 1, "nombre": "Calculo_Costos_y_Materiales.xlsx", "tipo": "excel", "fecha": "16 Oct 2026"}
]

archivos_estado = {
    "youtube_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
    "tiktok_url": "https://www.tiktok.com/@giuli1160/video/7697398587696663828"
}

HTML_TEMPLATE = """<!DOCTYPE html>
