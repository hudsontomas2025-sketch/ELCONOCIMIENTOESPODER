import os
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

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

archivos_estado = {
    "youtube_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
    "tiktok_url": "https://www.tiktok.com/@giuli1160/video/7697398587696663828"
}

HTML_TEMPLATE = """<!DOCTYPE html>
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
        header { background: linear-gradient(135deg, var(--primary), #0f172a); color: white; padding: 30px 0; border-bottom: 4px solid var(--accent); }
        .mode-bar { background-color: #0f172a; color: #cbd5e1; padding: 6px 0; font-size: 0.85rem; }
        .card-custom { border: none; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); position: relative; }
        .carousel-item-news { height: 320px; background-size: cover; background-position: center; border-radius: 12px; position: relative; }
        .carousel-overlay { position: absolute; bottom: 0; top: 0; left: 0; right: 0; background: linear-gradient(to top, rgba(15,23,42,0.95) 15%, rgba(15,23,42,0.4) 60%); border-radius: 12px; padding: 20px; display: flex; flex-direction: column; justify-content: flex-end; color: white; }
        .modo-espectador-hide { display: block; }
        body.espectador-active .modo-espectador-hide { display: none !important; }
        .btn-delete-card { position: absolute; top: 10px; right: 10px; z-index: 10; }
        .metric-card { background: white; border-radius: 12px; padding: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); text-align: center; border-top: 4px solid var(--accent); }
        footer { background-color: var(--primary); color: white; padding: 25px 0; margin-top: 40px; }
    </style>
</head>
<body>
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
            <h1 class="h3 fw-bold">Sistema de Remoción y Extracción de Barro en Viviendas</h1>
            <p class="small text-light opacity-90 mb-1">Equipo ELCONOCIMIENTOESPODER — Sede UNER Concordia (Entre Ríos, Argentina)</p>
            <span class="badge bg-warning text-dark">Desafío 06 — Rally Latinoamericano de Innovación 2026</span>
        </div>
    </header>
    <main class="container my-4">
        <section class="mb-4">
            <div class="card card-custom p-3 bg-white border-start border-4 border-danger">
                <div class="row align-items-center">
                    <div class="col-md-7">
                        <h5 class="fw-bold text-dark mb-1"><i class="fas fa-cloud-showers-heavy text-danger me-2"></i> Radar y Monitoreo Climático</h5>
                        <p class="text-secondary small mb-0">Seguimiento en tiempo real de precipitaciones y crecida del Río Uruguay en Concordia.</p>
                    </div>
                    <div class="col-md-5 mt-2 mt-md-0">
                        <div class="ratio ratio-16x9 rounded overflow-hidden shadow-sm">
                            <iframe src="https://embed.windy.com/embed2.html?lat=-31.393&lon=-58.021&zoom=10&level=surface&overlay=rain&product=ecmwf&menu=&message=&marker=&calendar=now&pressure=&type=map&location=coordinates&detail=&metricWind=km%2Fh&metricTemp=%C2%B0C&radarRange=-1" frameborder="0"></iframe>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        <section class="mb-4">
            <div class="card card-custom p-3 bg-white border-start border-4 border-warning">
                <h5 class="fw-bold text-dark mb-2"><i class="fas fa-calculator text-warning me-2"></i> Simulador y Calculadora Comparativa</h5>
                <div class="row g-2 align-items-end">
                    <div class="col-md-4">
                        <label class="form-label small fw-bold">Superficie afectada (m²):</label>
                        <input type="number" id="inputMetros" class="form-control form-control-sm" value="50" min="10" max="500" oninput="calcularComparacion()">
                    </div>
                    <div class="col-md-4">
                        <div class="p-2 bg-light rounded border">
                            <span class="d-block small text-muted">A mano:</span> <strong id="resManualTiempo" class="text-danger">--</strong> | <strong id="resManualCosto" class="text-danger">--</strong>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="p-2 bg-light rounded border border-success">
                            <span class="d-block small text-success">Con ELCONOCIMIENTOESPODER:</span> <strong id="resMaquinaTiempo" class="text-success">--</strong> | <strong id="resMaquinaCosto" class="text-success">--</strong>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        <section class="mb-4">
            <div class="row g-2">
                <div class="col-md-4"><div class="metric-card"><h4 class="fw-bold text-primary mb-1">-65%</h4><p class="text-secondary small mb-0 fw-bold">Tiempo de limpieza</p></div></div>
                <div class="col-md-4"><div class="metric-card"><h4 class="fw-bold text-warning mb-1">$20 USD</h4><p class="text-secondary small mb-0 fw-bold">Costo de herramientas</p></div></div>
                <div class="col-md-4"><div class="metric-card"><h4 class="fw-bold text-success mb-1">100%</h4><p class="text-secondary small mb-0 fw-bold">Independencia eléctrica</p></div></div>
            </div>
        </section>
        <section class="mb-4">
            <div class="card card-custom p-3 bg-white text-center border-start border-4 border-primary">
                <h5 class="fw-bold text-dark mb-1"><i class="fas fa-qrcode text-primary me-2"></i> Acceso Móvil para el Jurado</h5>
                <div class="d-inline-block bg-white p-2 border rounded shadow-sm mt-1">
                    <img src="https://api.qrserver.com/v1/create-qr-code/?size=110x110&data=https://rally-extraccion-barro.onrender.com/" alt="QR" style="width: 100px; height: 100px;">
                </div>
            </div>
        </section>
        <section class="mb-4">
            <div class="d-flex justify-content-between align-items-center mb-2">
                <h5 class="fw-bold text-dark mb-0"><i class="fas fa-newspaper text-danger me-2"></i> Noticias & Alertas</h5>
                <button class="btn btn-danger btn-sm fw-bold modo-espectador-hide" data-bs-toggle="modal" data-bs-target="#modalNoticia">Publicar</button>
            </div>
            <div id="carouselNoticias" class="carousel slide shadow-sm rounded overflow-hidden" data-bs-ride="carousel">
                <div class="carousel-inner">
                    {% for noti in noticias %}
                    <div class="carousel-item {% if loop.first %}active{% endif %}">
                        <div class="carousel-item-news" style="background-image: url('{{ noti.imagen }}');">
                            <form action="/delete_noticia/{{ noti.id }}" method="post" class="modo-espectador-hide btn-delete-card">
                                <button type="submit" class="btn btn-danger btn-sm"><i class="fas fa-trash"></i></button>
                            </form>
                            <div class="carousel-overlay">
                                <span class="badge bg-danger mb-1 align-self-start">{{ noti.pais }}</span>
                                <h6 class="fw-bold text-white mb-1">{{ noti.titulo }}</h6>
                                <p class="small text-light mb-1">{{ noti.resumen }}</p>
                                <a href="{{ noti.enlace }}" target="_blank" class="btn btn-warning btn-sm fw-bold align-self-start">Leer Nota</a>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </section>
        <section class="mb-4">
            <div class="d-flex justify-content-between align-items-center mb-2">
                <h5 class="fw-bold text-dark mb-0"><i class="fas fa-tools text-warning me-2"></i> Soluciones Propuestas</h5>
                <button class="btn btn-warning btn-sm fw-bold text-dark modo-espectador-hide" data-bs-toggle="modal" data-bs-target="#modalSolucion">Agregar</button>
            </div>
            <div class="row g-2">
                {% for sol in soluciones %}
                <div class="col-md-6">
                    <div class="card card-custom h-100 bg-white d-flex flex-row overflow-hidden">
                        <form action="/delete_solucion/{{ sol.id }}" method="post" class="modo-espectador-hide btn-delete-card">
                            <button type="submit" class="btn btn-danger btn-sm"><i class="fas fa-trash"></i></button>
                        </form>
                        <img src="{{ sol.imagen }}" style="width: 110px; object-fit: cover;" alt="Tool">
                        <div class="p-2 d-flex flex-column justify-content-between">
                            <div>
                                <span class="badge bg-secondary mb-1">{{ sol.categoria }}</span>
                                <h6 class="fw-bold text-dark mb-1">{{ sol.titulo }}</h6>
                                <p class="text-secondary small mb-1">{{ sol.descripcion }}</p>
                            </div>
                            <span class="fw-bold text-success small">{{ sol.costo }}</span>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
        </section>
        <section class="mb-4">
            <div class="d-flex justify-content-between align-items-center mb-2">
                <h5 class="fw-bold text-dark mb-0"><i class="fas fa-comment-dots text-primary me-2"></i> Testimonios Reales</h5>
                <button class="btn btn-primary btn-sm fw-bold modo-espectador-hide" data-bs-toggle="modal" data-bs-target="#modalTestimonio">Subir</button>
            </div>
            <div class="row g-2">
                {% for test in testimonios %}
                <div class="col-md-6">
                    <div class="card card-custom p-3 bg-white border-start border-4 border-primary h-100">
                        <form action="/delete_testimonio/{{ test.id }}" method="post" class="modo-espectador-hide btn-delete-card">
                            <button type="submit" class="btn btn-danger btn-sm"><i class="fas fa-trash"></i></button>
                        </form>
                        <h6 class="fw-bold text-dark mb-1">{{ test.nombre }}</h6>
                        <p class="text-primary small fw-bold mb-1">{{ test.ubicacion }}</p>
                        <p class="text-secondary fst-italic small mb-0">"{{ test.testimonio }}"</p>
                    </div>
                </div>
                {% endfor %}
            </div>
        </section>
        <section class="mb-4">
            <div class="row g-2">
                <div class="col-md-6">
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <h5 class="fw-bold text-dark mb-0"><i class="fas fa-video text-danger me-2"></i> Pitch (YouTube)</h5>
                        <button class="btn btn-danger btn-sm fw-bold modo-espectador-hide" data-bs-toggle="modal" data-bs-target="#modalYoutube">Editar</button>
                    </div>
                    <div class="card card-custom p-2 bg-white">
                        <div class="ratio ratio-16x9 rounded overflow-hidden">
                            <iframe src="{{ youtube_url }}" allowfullscreen></iframe>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <h5 class="fw-bold text-dark mb-0"><i class="fa-brands fa-tiktok text-dark me-2"></i> TikTok del Proyecto</h5>
                        <button class="btn btn-dark btn-sm fw-bold modo-espectador-hide" data-bs-toggle="modal" data-bs-target="#modalTiktok">Editar</button>
                    </div>
                    <div class="card card-custom p-3 bg-white text-center d-flex flex-row justify-content-around align-items-center h-100" style="min-height: 200px;">
                        <div>
                            <i class="fa-brands fa-tiktok fa-3x mb-2 text-dark"></i>
                            <p class="text-muted small mb-2">Mira nuestra demostración.</p>
                            <a href="{{ tiktok_url }}" target="_blank" class="btn btn-dark fw-bold px-3 btn-sm"><i class="fa-brands fa-tiktok me-1"></i> Ver en TikTok</a>
                        </div>
                        <div class="bg-light p-2 border rounded shadow-sm text-center">
                            <img src="https://api.qrserver.com/v1/create-qr-code/?size=110x110&data={{ tiktok_url }}" alt="QR TikTok" style="width: 100px; height: 100px;">
                            <span class="d-block small text-muted mt-1" style="font-size: 11px;">Escanea el QR</span>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        <section class="mb-4">
            <h5 class="fw-bold text-dark mb-2"><i class="fas fa-users text-primary me-2"></i> Equipo ELCONOCIMIENTOESPODER</h5>
            <div class="card card-custom p-3 bg-white">
                <div class="row g-2">
                    {% for miem in equipo_list %}
                    <div class="col-md-6">
                        <div class="p-2 bg-light rounded border-start border-3 border-primary">
                            <h6 class="fw-bold text-dark mb-0">{{ miem.nombre }}</h6>
                            <small class="text-muted">{{ miem.rol }}</small>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </section>
    </main>
    <div class="modal fade" id="modalTestimonio" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog"><div class="modal-content"><form action="/add_testimonio" method="post">
            <div class="modal-header bg-primary text-white"><h5 class="modal-title">Agregar Testimonio</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div>
            <div class="modal-body">
                <div class="mb-2"><label class="small fw-bold">Nombre / Rol</label><input type="text" name="nombre" class="form-control form-control-sm" required></div>
                <div class="mb-2"><label class="small fw-bold">Ubicación</label><input type="text" name="ubicacion" class="form-control form-control-sm" required></div>
                <div class="mb-2"><label class="small fw-bold">Testimonio</label><textarea name="testimonio" class="form-control form-control-sm" rows="2" required></textarea></div>
            </div>
            <div class="modal-footer"><button type="submit" class="btn btn-primary btn-sm">Guardar</button></div>
        </form></div></div>
    </div>
    <div class="modal fade" id="modalNoticia" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog"><div class="modal-content"><form action="/add_noticia" method="post">
            <div class="modal-header bg-danger text-white"><h5 class="modal-title">Publicar Noticia</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div>
            <div class="modal-body">
                <div class="mb-2"><label class="small fw-bold">Titular</label><input type="text" name="titulo" class="form-control form-control-sm" required></div>
                <div class="mb-2"><label class="small fw-bold">País</label><input type="text" name="pais" class="form-control form-control-sm" required></div>
                <div class="mb-2"><label class="small fw-bold">Enlace</label><input type="url" name="enlace" class="form-control form-control-sm" required></div>
                <div class="mb-2"><label class="small fw-bold">Resumen</label><textarea name="resumen" class="form-control form-control-sm" rows="2" required></textarea></div>
            </div>
            <div class="modal-footer"><button type="submit" class="btn btn-danger btn-sm">Publicar</button></div>
        </form></div></div>
    </div>
    <div class="modal fade" id="modalSolucion" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog"><div class="modal-content"><form action="/add_solucion" method="post">
            <div class="modal-header bg-warning text-dark"><h5 class="modal-title">Agregar Solución</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div>
            <div class="modal-body">
                <div class="mb-2"><label class="small fw-bold">Título</label><input type="text" name="titulo" class="form-control form-control-sm" required></div>
                <div class="mb-2"><label class="small fw-bold">Categoría</label><input type="text" name="categoria" class="form-control form-control-sm" required></div>
                <div class="mb-2"><label class="small fw-bold">Costo</label><input type="text" name="costo" class="form-control form-control-sm" required></div>
                <div class="mb-2"><label class="small fw-bold">Descripción</label><textarea name="descripcion" class="form-control form-control-sm" rows="2" required></textarea></div>
            </div>
            <div class="modal-footer"><button type="submit" class="btn btn-warning btn-sm text-dark">Guardar</button></div>
        </form></div></div>
    </div>
    <div class="modal fade" id="modalYoutube" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog"><div class="modal-content"><form action="/update_youtube" method="post">
            <div class="modal-header bg-danger text-white"><h5 class="modal-title">Actualizar Video de YouTube</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div>
            <div class="modal-body">
                <div class="mb-2"><label class="small fw-bold">URL de Embed de YouTube</label><input type="text" name="youtube_url" class="form-control form-control-sm" placeholder="Ej: https://www.youtube.com/embed/TU_ID" required></div>
            </div>
            <div class="modal-footer"><button type="submit" class="btn btn-danger btn-sm">Actualizar</button></div>
        </form></div></div>
    </div>
    <div class="modal fade" id="modalTiktok" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog"><div class="modal-content"><form action="/update_tiktok" method="post">
            <div class="modal-header bg-dark text-white"><h5 class="modal-title">Actualizar Enlace de TikTok</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div>
            <div class="modal-body">
                <div class="mb-2"><label class="small fw-bold">URL del video de TikTok</label><input type="url" name="tiktok_url" class="form-control form-control-sm" required></div>
            </div>
            <div class="modal-footer"><button type="submit" class="btn btn-dark btn-sm">Actualizar</button></div>
        </form></div></div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        function toggleEspectador(cb) {
            document.body.classList.toggle('espectador-active', cb.checked);
            document.getElementById('labelModo').innerText = cb.checked ? 'Modo Espectador / Jurado (Limpio)' : 'Modo Administrador (Edición)';
        }
        function calcularComparacion() {
            const m2 = parseFloat(document.getElementById('inputMetros').value) || 0;
            document.getElementById('resManualTiempo').innerText = (m2 * 0.8).toFixed(1) + ' hs';
            document.getElementById('resManualCosto').innerText = '$' + (m2 * 12).toFixed(0) + ' USD';
            document.getElementById('resMaquinaTiempo').innerText = (m2 * 0.25).toFixed(1) + ' hs';
            document.getElementById('resMaquinaCosto').innerText = '$' + (m2 * 4).toFixed(0) + ' USD';
        }
        window.onload = calcularComparacion;
    </script>
</body>
</html>"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, noticias=noticias_list, testimonios=testimonios_list, soluciones=soluciones_list, equipo_list=equipo_list, youtube_url=archivos_estado["youtube_url"], tiktok_url=archivos_estado["tiktok_url"])

@app.route('/update_youtube', methods=['POST'])
def update_youtube():
    if u := request.form.get('youtube_url'): archivos_estado["youtube_url"] = u
    return redirect(url_for('home'))

@app.route('/update_tiktok', methods=['POST'])
def update_tiktok():
    if u := request.form.get('tiktok_url'): archivos_estado["tiktok_url"] = u
    return redirect(url_for('home'))

@app.route('/add_testimonio', methods=['POST'])
def add_testimonio():
    testimonios_list.insert(0, {"id": max([t["id"] for t in testimonios_list], default=-1) + 1, "nombre": request.form.get('nombre'), "ubicacion": request.form.get('ubicacion'), "testimonio": request.form.get('testimonio')})
    return redirect(url_for('home'))

@app.route('/delete_testimonio/<int:item_id>', methods=['POST'])
def delete_testimonio(item_id):
    global testimonios_list
    testimonios_list = [t for t in testimonios_list if t["id"] != item_id]
    return redirect(url_for('home'))

@app.route('/add_noticia', methods=['POST'])
def add_noticia():
    noticias_list.insert(0, {"id": max([n["id"] for n in noticias_list], default=-1) + 1, "titulo": request.form.get('titulo'), "pais": request.form.get('pais'), "resumen": request.form.get('resumen'), "enlace": request.form.get('enlace'), "imagen": "https://images.unsplash.com/photo-1547683905-f686c993aae5?auto=format&fit=crop&w=800&q=80"})
    return redirect(url_for('home'))

@app.route('/delete_noticia/<int:item_id>', methods=['POST'])
def delete_noticia(item_id):
    global noticias_list
    noticias_list = [n for n in noticias_list if n["id"] != item_id]
    return redirect(url_for('home'))

@app.route('/add_solucion', methods=['POST'])
def add_solucion():
    soluciones_list.insert(0, {"id": max([s["id"] for s in soluciones_list], default=-1) + 1, "titulo": request.form.get('titulo'), "descripcion": request.form.get('descripcion'), "costo": request.form.get('costo'), "categoria": request.form.get('categoria'), "imagen": "https://images.unsplash.com/photo-1584467735811-9985103cb136?auto=format&fit=crop&w=600&q=80"})
    return redirect(url_for('home'))

@app.route('/delete_solucion/<int:item_id>', methods=['POST'])
def delete_solucion(item_id):
    global soluciones_list
    soluciones_list = [s for s in soluciones_list if s["id"] != item_id]
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)
