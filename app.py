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
        "nombre": "Carlos M. González",
        "ubicacion": "Concordia, Entre Ríos (Argentina)",
        "testimonio": "El barro se secó como cemento en cuestión de horas dentro de mi casa. Sin luz no podíamos usar bombas convencionales.",
        "fecha": "12 Oct 2026",
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
    {"nombre": "Tomás Hudson", "rol": "Liderazgo Técnico & Software", "avatar": "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=200&q=80"},
    {"nombre": "Equipo UNER", "rol": "Ingeniería y Diseño de Procesos", "avatar": "https://images.unsplash.com/photo-1570295999919-56ceb5ecca61?auto=format&fit=crop&w=200&q=80"}
]

archivos_estado = {
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
        header { background: linear-gradient(135deg, var(--primary), #0f172a); color: white; padding: 45px 0; border-bottom: 4px solid var(--accent); }
        .mode-bar { background-color: #0f172a; color: #cbd5e1; padding: 8px 0; font-size: 0.85rem; }
        .card-custom { border: none; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); position: relative; }
        .carousel-item-news { height: 380px; background-size: cover; background-position: center; border-radius: 12px; position: relative; }
        .carousel-overlay { position: absolute; bottom: 0; top: 0; left: 0; right: 0; background: linear-gradient(to top, rgba(15,23,42,0.95) 15%, rgba(15,23,42,0.4) 60%); border-radius: 12px; padding: 30px; display: flex; flex-direction: column; justify-content: flex-end; color: white; }
        .modo-espectador-hide { display: block; }
        body.espectador-active .modo-espectador-hide { display: none !important; }
        .btn-delete-card { position: absolute; top: 10px; right: 10px; z-index: 10; }
        .metric-card { background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); text-align: center; border-top: 4px solid var(--accent); }
        footer { background-color: var(--primary); color: white; padding: 40px 0; margin-top: 60px; }
    </style>
</head>
<body>

    <!-- MODO ESPECTADOR / JURADO SWITCH -->
    <div class="mode-bar">
        <div class="container d-flex justify-content-between align-items-center">
            <span><i class="fas fa-eye me-1 text-warning"></i> <strong>Modo de Visualización:</strong></span>
            <div class="form-check form-switch m-0">
                <input class="form-check-input" type="checkbox" id="switchModoEspectador" onchange="toggleEspectador(this)">
                <label class="form-check-label text-white fw-bold small" for="switchModoEspectador" id="labelModo">Modo Administrador (Edición)</label>
            </div>
        </div>
    </div>

    <header class="text-center">
        <div class="container">
            <h1 class="display-5 fw-bold">Sistema de Remoción y Extracción de Barro en Viviendas</h1>
            <p class="lead mt-2 text-light opacity-90">Equipo ELCONOCIMIENTOESPODER — Sede UNER Concordia (Entre Ríos, Argentina)</p>
            <p class="badge bg-warning text-dark fs-6 mt-2">Desafío 06 — Rally Latinoamericano de Innovación 2026</p>
        </div>
    </header>

    <main class="container my-5">

        <!-- MAPA Y ESTADO CLIMÁTICO EN VIVO -->
        <section class="mb-5">
            <div class="card card-custom p-4 bg-white border-start border-4 border-danger">
                <div class="row align-items-center">
                    <div class="col-md-7">
                        <h3 class="fw-bold text-dark mb-2"><i class="fas fa-cloud-showers-heavy text-danger me-2"></i> Radar y Monitoreo Climático Regional</h3>
                        <p class="text-secondary small mb-3">Seguimiento en tiempo real de precipitaciones, crecida del Río Uruguay y zonas de riesgo en Concordia y la hidrovía.</p>
                        <ul class="list-unstyled small text-secondary mb-0">
                            <li><i class="fas fa-check text-success me-2"></i><strong>Estado del Río:</strong> Nivel de alerta / evacuación preventiva.</li>
                            <li><i class="fas fa-check text-success me-2"></i><strong>Zona de Impacto:</strong> Costanera y asentamientos bajos.</li>
                        </ul>
                    </div>
                    <div class="col-md-5 mt-3 mt-md-0">
                        <div class="ratio ratio-16x9 rounded overflow-hidden shadow-sm">
                            <iframe src="https://embed.windy.com/embed2.html?lat=-31.393&lon=-58.021&zoom=10&level=surface&overlay=rain&product=ecmwf&menu=&message=&marker=&calendar=now&pressure=&type=map&location=coordinates&detail=&metricWind=km%2Fh&metricTemp=%C2%B0C&radarRange=-1" frameborder="0"></iframe>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- CALCULADORA COMPARATIVA (MANO VS MÁQUINA) -->
        <section class="mb-5">
            <div class="card card-custom p-4 bg-white border-start border-4 border-warning">
                <h3 class="fw-bold text-dark mb-3"><i class="fas fa-calculator text-warning me-2"></i> Simulador y Calculadora Comparativa (Manual vs. Nuestra Solución)</h3>
                <p class="text-secondary small mb-4">Calcula el tiempo estimado y el costo operativo para despejar una vivienda afectada según los metros cuadrados de lodo acumulado.</p>
                <div class="row g-3 align-items-end">
                    <div class="col-md-4">
                        <label class="form-label small fw-bold text-dark">Superficie afectada (m²):</label>
                        <input type="number" id="inputMetros" class="form-control" value="50" min="10" max="500" oninput="calcularComparacion()">
                    </div>
                    <div class="col-md-4">
                        <div class="p-3 bg-light rounded border">
                            <span class="d-block small text-muted fw-bold">Limpieza Tradicional (A mano):</span>
                            <strong id="resManualTiempo" class="text-danger">-- hs</strong> | <strong id="resManualCosto" class="text-danger">--</strong>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="p-3 bg-light rounded border border-success">
                            <span class="d-block small text-success fw-bold">Con Equipo ELCONOCIMIENTOESPODER:</span>
                            <strong id="resMaquinaTiempo" class="text-success">-- hs</strong> | <strong id="resMaquinaCosto" class="text-success">--</strong>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- MÉTRICAS DE IMPACTO -->
        <section class="mb-5">
            <h3 class="fw-bold text-dark mb-3"><i class="fas fa-chart-line text-success me-2"></i> Impacto Esperado del Proyecto</h3>
            <div class="row g-4">
                <div class="col-md-4">
                    <div class="metric-card">
                        <h2 class="fw-bold text-primary display-6">-65%</h2>
                        <p class="text-secondary mb-0 fw-bold">Tiempo de limpieza post-inundación en hogares</p>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="metric-card">
                        <h2 class="fw-bold text-warning display-6">$20 USD</h2>
                        <p class="text-secondary mb-0 fw-bold">Costo promedio de fabricación de herramientas</p>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="metric-card">
                        <h2 class="fw-bold text-success display-6">100%</h2>
                        <p class="text-secondary mb-0 fw-bold">Independencia de red eléctrica inicial</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- CARRUSEL DE NOTICIAS -->
        <section class="mb-5">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h3 class="fw-bold text-dark mb-0"><i class="fas fa-newspaper text-danger me-2"></i> Noticias & Alertas de Aluviones</h3>
                <button class="btn btn-danger btn-sm fw-bold modo-espectador-hide" data-bs-toggle="modal" data-bs-target="#modalNoticia"><i class="fas fa-plus me-1"></i> Publicar Noticia</button>
            </div>
            <div id="carouselNoticias" class="carousel slide shadow-lg rounded-3 overflow-hidden" data-bs-ride="carousel">
                <div class="carousel-inner">
                    {% for noti in noticias %}
                    <div class="carousel-item {% if loop.first %}active{% endif %}">
                        <div class="carousel-item-news" style="background-image: url('{{ noti.imagen }}');">
                            <form action="/delete_noticia/{{ noti.id }}" method="post" class="modo-espectador-hide btn-delete-card">
                                <button type="submit" class="btn btn-danger btn-sm shadow" title="Eliminar noticia"><i class="fas fa-trash"></i></button>
                            </form>
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

        <!-- SECCIÓN SOLUCIONES / HERRAMIENTAS -->
        <section class="mb-5">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h3 class="fw-bold text-dark mb-0"><i class="fas fa-tools text-warning me-2"></i> Soluciones Tecnológicas Propuestas</h3>
                <button class="btn btn-warning btn-sm fw-bold text-dark modo-espectador-hide" data-bs-toggle="modal" data-bs-target="#modalSolucion"><i class="fas fa-plus me-1"></i> Agregar Solución</button>
            </div>
            <div class="row g-4">
                {% for sol in soluciones %}
                <div class="col-md-6">
                    <div class="card card-custom h-100 bg-white d-flex flex-row overflow-hidden">
                        <form action="/delete_solucion/{{ sol.id }}" method="post" class="modo-espectador-hide btn-delete-card">
                            <button type="submit" class="btn btn-danger btn-sm shadow" title="Eliminar solución"><i class="fas fa-trash"></i></button>
                        </form>
                        <img src="{{ sol.imagen }}" style="width: 140px; object-fit: cover;" alt="Herramienta">
                        <div class="p-3 d-flex flex-column justify-content-between">
                            <div>
                                <span class="badge bg-secondary mb-1">{{ sol.categoria }}</span>
                                <h5 class="fw-bold text-dark mb-1">{{ sol.titulo }}</h5>
                                <p class="text-secondary small mb-2">{{ sol.descripcion }}</p>
                            </div>
                            <span class="fw-bold text-success small">{{ sol.costo }}</span>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
        </section>

        <!-- TESTIMONIOS -->
        <section class="mb-5">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h3 class="fw-bold text-dark mb-0"><i class="fas fa-comment-dots text-primary me-2"></i> Testimonios Globales</h3>
                <button class="btn btn-primary btn-sm fw-bold modo-espectador-hide" data-bs-toggle="modal" data-bs-target="#modalTestimonio"><i class="fas fa-plus me-1"></i> Subir Testimonio</button>
            </div>
            <div class="row g-4">
                {% for test in testimonios %}
                <div class="col-md-6">
                    <div class="card card-custom p-4 bg-white border-start border-4 border-primary h-100">
                        <form action="/delete_testimonio/{{ test.id }}" method="post" class="modo-espectador-hide btn-delete-card">
                            <button type="submit" class="btn btn-danger btn-sm shadow" title="Eliminar testimonio"><i class="fas fa-trash"></i></button>
                        </form>
                        <h5 class="fw-bold text-dark mb-1">{{ test.nombre }}</h5>
                        <p class="text-primary small fw-bold mb-2">{{ test.ubicacion }}</p>
                        <p class="text-secondary fst-italic small mb-0">"{{ test.testimonio }}"</p>
                    </div>
                </div>
                {% endfor %}
            </div>
        </section>

        <!-- EQUIPO DE TRABAJO -->
        <section class="mb-5">
            <h3 class="fw-bold text-dark mb-3"><i class="fas fa-users text-primary me-2"></i> Equipo de Trabajo</h3>
            <div class="row g-4">
                {% for miem in equipo_list %}
                <div class="col-md-6">
                    <div class="card card-custom p-3 bg-white d-flex flex-row align-items-center">
                        <img src="{{ miem.avatar }}" class="rounded-circle me-3" style="width: 60px; height: 60px; object-fit: cover;" alt="Avatar">
                        <div>
                            <h5 class="fw-bold text-dark mb-0">{{ miem.nombre }}</h5>
                            <p class="text-muted small mb-0">{{ miem.rol }}</p>
                            <span class="badge bg-light text-dark border mt-1">Sede UNER Concordia</span>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
        </section>

        <!-- PITCH Y VIDEO -->
        <section class="mb-5">
            <h3 class="fw-bold text-dark mb-3"><i class="fas fa-video text-danger me-2"></i> Pitch del Proyecto</h3>
            <div class="card card-custom p-3 bg-white">
                <div class="ratio ratio-16x9 rounded overflow-hidden">
                    <iframe src="https://www.youtube.com/embed/{{ youtube_id }}" title="Pitch" allowfullscreen></iframe>
                </div>
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

    <!-- MODAL NOTICIA -->
    <div class="modal fade" id="modalNoticia" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <form action="/add_noticia" method="post">
                    <div class="modal-header bg-danger text-white">
                        <h5 class="modal-title fw-bold">Publicar Noticia</h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="mb-3">
                            <label class="form-label small fw-bold">Titular</label>
                            <input type="text" name="titulo" class="form-control form-control-sm" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label small fw-bold">País</label>
                            <input type="text" name="pais" class="form-control form-control-sm" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label small fw-bold">Enlace Externo</label>
                            <input type="url" name="enlace" class="form-control form-control-sm" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label small fw-bold">Resumen</label>
                            <textarea name="resumen" class="form-control form-control-sm" rows="3" required></textarea>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary btn-sm" data-bs-dismiss="modal">Cancelar</button>
                        <button type="submit" class="btn btn-danger btn-sm fw-bold">Publicar</button>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <!-- MODAL SOLUCIÓN -->
    <div class="modal fade" id="modalSolucion" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <form action="/add_solucion" method="post">
                    <div class="modal-header bg-warning text-dark">
                        <h5 class="modal-title fw-bold">Agregar Solución Tecnológica</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="mb-3">
                            <label class="form-label small fw-bold">Título de la Solución</label>
                            <input type="text" name="titulo" class="form-control form-control-sm" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label small fw-bold">Categoría</label>
                            <input type="text" name="categoria" class="form-control form-control-sm" placeholder="Ej: Herramienta Manual" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label small fw-bold">Costo Estimado</label>
                            <input type="text" name="costo" class="form-control form-control-sm" placeholder="Ej: $15 - $25 USD" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label small fw-bold">Descripción</label>
                            <textarea name="descripcion" class="form-control form-control-sm" rows="3" required></textarea>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary btn-sm" data-bs-dismiss="modal">Cancelar</button>
                        <button type="submit" class="btn btn-warning btn-sm fw-bold text-dark">Guardar Solución</button>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <footer class="text-center">
        <div class="container">
            <p class="mb-1 fw-bold">&copy; 2026 - Equipo ELCONOCIMIENTOESPODER</p>
            <p class="mb-0 small text-light opacity-75">Sede UNER Concordia (Entre Ríos, Argentina) — Rally Latinoamericano de Innovación</p>
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

        function calcularComparacion() {
            const m2 = parseFloat(document.getElementById('inputMetros').value) || 0;
            // Supuestos: A mano requiere ~0.8 horas por m2 y costo humano/esfuerzo de $10/m2. Con máquina reduce a 0.25 horas y $3/m2.
            const horasManual = (m2 * 0.8).toFixed(1);
            const costoManual = (m2 * 12).toFixed(0);

            const horasMaquina = (m2 * 0.25).toFixed(1);
            const costoMaquina = (m2 * 4).toFixed(0);

            document.getElementById('resManualTiempo').innerText = horasManual + ' horas';
            document.getElementById('resManualCosto').innerText = '$' + costoManual + ' USD';

            document.getElementById('resMaquinaTiempo').innerText = horasMaquina + ' horas';
            document.getElementById('resMaquinaCosto').innerText = '$' + costoMaquina + ' USD';
        }

        // Ejecutar al cargar
        window.onload = calcularComparacion;
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, noticias=noticias_list, testimonios=testimonios_list, soluciones=soluciones_list, equipo_list=equipo_list, youtube_id=archivos_estado["youtube_id"])

@app.route('/add_testimonio', methods=['POST'])
def add_testimonio():
    new_id = max([t["id"] for t in testimonios_list], default=-1) + 1
    testimonios_list.insert(0, {
        "id": new_id,
        "nombre": request.form.get('nombre'),
        "ubicacion": request.form.get('ubicacion'),
        "testimonio": request.form.get('testimonio'),
        "fecha": "Reciente",
        "foto": "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=200&q=80"
    })
    return redirect(url_for('home'))

@app.route('/delete_testimonio/<int:item_id>', methods=['POST'])
def delete_testimonio(item_id):
    global testimonios_list
    testimonios_list = [t for t in testimonios_list if t["id"] != item_id]
    return redirect(url_for('home'))

@app.route('/add_noticia', methods=['POST'])
def add_noticia():
    new_id = max([n["id"] for n in noticias_list], default=-1) + 1
    noticias_list.insert(0, {
        "id": new_id,
        "titulo": request.form.get('titulo'),
        "pais": request.form.get('pais'),
        "fuente": "Comunidad",
        "fecha": "Reciente",
        "resumen": request.form.get('resumen'),
        "enlace": request.form.get('enlace'),
        "imagen": "https://images.unsplash.com/photo-1547683905-f686c993aae5?auto=format&fit=crop&w=800&q=80"
    })
    return redirect(url_for('home'))

@app.route('/delete_noticia/<int:item_id>', methods=['POST'])
def delete_noticia(item_id):
    global noticias_list
    noticias_list = [n for n in noticias_list if n["id"] != item_id]
    return redirect(url_for('home'))

@app.route('/add_solucion', methods=['POST'])
def add_solucion():
    new_id = max([s["id"] for s in soluciones_list], default=-1) + 1
    soluciones_list.insert(0, {
        "id": new_id,
        "titulo": request.form.get('titulo'),
        "descripcion": request.form.get('descripcion'),
        "costo": request.form.get('costo'),
        "categoria": request.form.get('categoria'),
        "imagen": "https://images.unsplash.com/photo-1584467735811-9985103cb136?auto=format&fit=crop&w=600&q=80"
    })
    return redirect(url_for('home'))

@app.route('/delete_solucion/<int:item_id>', methods=['POST'])
def delete_solucion(item_id):
    global soluciones_list
    soluciones_list = [s for s in soluciones_list if s["id"] != item_id]
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)
