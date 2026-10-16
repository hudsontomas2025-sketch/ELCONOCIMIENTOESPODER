import os
from flask import Flask, render_template_string, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

noticias_list = [
    {
        "titulo": "Alerta por El Niño en Concordia: Crecida del Río Uruguay obliga a evacuar familias en la costanera",
        "pais": "Argentina 🇦🇷",
        "fuente": "Diario El Heraldo / TN",
        "fecha": "11 Oct 2026",
        "resumen": "El río Uruguay superó niveles críticos en la costa de Concordia, desbordando áreas ribereñas e ingresando barro y agua a viviendas bajas.",
        "enlace": "https://www.fenix951.com.ar/noticia.php?id=356349",
        "imagen": "https://images.unsplash.com/photo-1547683905-f686c993aae5?auto=format&fit=crop&w=800&q=80"
    }
]

testimonios_list = [
    {
        "nombre": "Carlos M. González",
        "ubicacion": "Concordia, Entre Ríos (Argentina)",
        "testimonio": "El barro se secó como cemento en cuestión de horas dentro de mi casa. Sin luz no podíamos usar bombas convencionales.",
        "fecha": "12 Oct 2026",
        "foto": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=200&q=80"
    }
]

soluciones_list = [
    {
        "titulo": "Rastrillo-Pala de Arrastre Ergonómico",
        "descripcion": "Diseñado para movilizar grandes volúmenes de lodo semi-húmedo en pasillos y habitaciones reducidas.",
        "costo": "$15 - $25 USD",
        "categoria": "Herramienta Manual",
        "imagen": "https://images.unsplash.com/photo-1584467735811-9985103cb136?auto=format&fit=crop&w=600&q=80"
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
        :root { --primary: #1b2a47; --accent: #d97706; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f8fafc; color: #334155; }
        header { background: linear-gradient(135deg, var(--primary), #0f172a); color: white; padding: 40px 0; border-bottom: 4px solid var(--accent); }
        .mode-bar { background-color: #0f172a; color: #cbd5e1; padding: 6px 0; font-size: 0.85rem; }
        .card-custom { border: none; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
        .carousel-item-news { height: 350px; background-size: cover; background-position: center; border-radius: 12px; position: relative; }
        .carousel-overlay { position: absolute; bottom: 0; top: 0; left: 0; right: 0; background: linear-gradient(to top, rgba(15,23,42,0.95), rgba(15,23,42,0.3)); border-radius: 12px; padding: 30px; display: flex; flex-direction: column; justify-content: flex-end; color: white; }
        .modo-espectador-hide { display: block; }
        body.espectador-active .modo-espectador-hide { display: none !important; }
        footer { background-color: var(--primary); color: white; padding: 30px 0; margin-top: 50px; }
    </style>
</head>
<body>

    <div class="mode-bar">
        <div class="container d-flex justify-content-between align-items-center">
            <span><i class="fas fa-eye me-1 text-warning"></i> <strong>Visualización:</strong></span>
            <div class="form-check form-switch m-0">
                <input class="form-check-input" type="checkbox" id="switchModoEspectador" onchange="toggleEspectador(this)">
                <label class="form-check-label text-white fw-bold small" for="switchModoEspectador" id="labelModo">Modo Administrador (Edición)</label>
            </div>
        </div>
    </div>

    <header class="text-center">
        <div class="container">
            <h1 class="display-6 fw-bold">Sistema de Remoción y Extracción de Barro</h1>
            <p class="lead mb-0 text-light opacity-90">Equipo ELCONOCIMIENTOESPODER — Sede UNER Concordia</p>
        </div>
    </header>

    <main class="container my-5">

        <!-- CARRUSEL DE NOTICIAS -->
        <section class="mb-5">
            <h3 class="fw-bold text-dark mb-3"><i class="fas fa-newspaper text-danger me-2"></i> Noticias & Alertas de Aluviones</h3>
            <div id="carouselNoticias" class="carousel slide shadow-lg rounded-3 overflow-hidden" data-bs-ride="carousel">
                <div class="carousel-inner">
                    {% for noti in noticias %}
                    <div class="carousel-item {% if loop.first %}active{% endif %}">
                        <div class="carousel-item-news" style="background-image: url('{{ noti.imagen }}');">
                            <div class="carousel-overlay">
                                <span class="badge bg-danger mb-2 align-self-start">{{ noti.pais }}</span>
                                <h4 class="fw-bold text-white">{{ noti.titulo }}</h4>
                                <p class="small text-light">{{ noti.resumen }}</p>
                                <a href="{{ noti.enlace }}" target="_blank" class="btn btn-warning btn-sm fw-bold align-self-start">Leer Nota Completa</a>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
                <button class="carousel-control-prev" type="button" data-bs-target="#carouselNoticias" data-bs-slide="prev"><span class="carousel-control-prev-icon"></span></button>
                <button class="carousel-control-next" type="button" data-bs-target="#carouselNoticias" data-bs-slide="next"><span class="carousel-control-next-icon"></span></button>
            </div>
        </section>

        <!-- TESTIMONIOS -->
        <section class="mb-5">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h3 class="fw-bold text-dark mb-0"><i class="fas fa-comment-dots text-primary me-2"></i> Testimonios Globales</h3>
                <button class="btn btn-primary btn-sm fw-bold modo-espectador-hide" data-bs-toggle="modal" data-bs-target="#modalTestimonio">Subir Testimonio</button>
            </div>
            <div class="row g-4">
                {% for test in testimonios %}
                <div class="col-md-6">
                    <div class="card card-custom p-4 bg-white border-start border-4 border-primary h-100">
                        <h5 class="fw-bold text-dark mb-1">{{ test.nombre }}</h5>
                        <p class="text-primary small fw-bold mb-2">{{ test.ubicacion }}</p>
                        <p class="text-secondary fst-italic small mb-0">"{{ test.testimonio }}"</p>
                    </div>
                </div>
                {% endfor %}
            </div>
        </section>

    </main>

    <!-- MODAL TESTIMONIO -->
    <div class="modal fade" id="modalTestimonio" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <form action="/add_testimonio" method="post">
                    <div class="modal-header bg-primary text-white">
                        <h5 class="modal-title fw-bold">Agregar Testimonio</h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="mb-3">
                            <label class="form-label small fw-bold">Nombre</label>
                            <input type="text" name="nombre" class="form-control form-control-sm" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label small fw-bold">Ubicación</label>
                            <input type="text" name="ubicacion" class="form-control form-control-sm" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label small fw-bold">Testimonio</label>
                            <textarea name="testimonio" class="form-control form-control-sm" rows="3" required></textarea>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary btn-sm" data-bs-dismiss="modal">Cancelar</button>
                        <button type="submit" class="btn btn-primary btn-sm fw-bold">Guardar</button>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <footer class="text-center">
        <div class="container">
            <p class="mb-0 small fw-bold">&copy; 2026 - Equipo ELCONOCIMIENTOESPODER | Sede UNER Concordia</p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        function toggleEspectador(checkbox) {
            const label = document.getElementById('labelModo');
            if (checkbox.checked) {
                document.body.classList.add('espectador-active');
                label.innerText = 'Modo Espectador / Jurado (Limpio)';
            } else {
                document.body.classList.remove('espectador-active');
                label.innerText = 'Modo Administrador (Edición)';
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, noticias=noticias_list, testimonios=testimonios_list)

@app.route('/add_testimonio', methods=['POST'])
def add_testimonio():
    nombre = request.form.get('nombre')
    ubicacion = request.form.get('ubicacion')
    testimonio = request.form.get('testimonio')
    testimonios_list.insert(0, {"nombre": nombre, "ubicacion": ubicacion, "testimonio": testimonio, "fecha": "Reciente", "foto": "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=200&q=80"})
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)
