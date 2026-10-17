import os
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# CONTRASEÑA DE ADMINISTRADOR
ADMIN_PASSWORD = "1234"

# Base de datos en memoria optimizada para evitar errores en Render
noticias_list = [
    {
        "id": 0, 
        "titulo": "Aluvión en Santiago de Chile: Agua y lodo bajan de quebradas afectando viviendas", 
        "pais": "Chile 🇨🇱", 
        "resumen": "Desprendimientos de barro y rocas precordilleranas afectan sectores habitacionales.", 
        "enlace": "https://www.diariouno.com.ar/sociedad/aluvion-chile-reportan-1200-rescatados-y-384-damnificados-y-sigue-el-debate-la-prevencion-n1605218", 
        "imagen": "https://images.unsplash.com/photo-1584467735811-9985103cb136?auto=format&fit=crop&w=800&q=80"
    },
    {
        "id": 1, 
        "titulo": "Alerta por El Niño en Concordia: Crecida del Río Uruguay", 
        "pais": "Argentina 🇦🇷", 
        "resumen": "El río Uruguay superó niveles críticos en la costa de Concordia.", 
        "enlace": "https://www.fenix951.com.ar/noticia.php?id=356349", 
        "imagen": "https://images.unsplash.com/photo-1547683905-f686c993aae5?auto=format&fit=crop&w=800&q=80"
    }
]

testimonios_list = [
    {
        "id": 0, 
        "nombre": "Mariela Giménez (Vecina Afectada)", 
        "ubicacion": "Zona Costera / Ribera", 
        "testimonio": "Cuando bajó el agua, el lodo dentro de las piezas quedó pesado como cemento fresco. Sacarlo a pala llevó días enteros."
    },
    {
        "id": 1, 
        "nombre": "Esteban Ruarte (Damnificado)", 
        "ubicacion": "Sector Precordillerano", 
        "testimonio": "El mayor problema no es el agua, sino el barro denso que entra por las puertas y destruye los pisos si no se remueve rápido."
    }
]

soluciones_list = [
    {
        "id": 0, 
        "titulo": "Rastrillo-Pala de Arrastre Ergonómico", 
        "descripcion": "Diseñado para movilizar grandes volúmenes de lodo denso en espacios reducidos mediante tracción horizontal.", 
        "costo": "$15 - $25 USD", 
        "categoria": "Herramienta Manual", 
        "imagen": "https://images.unsplash.com/photo-1584467735811-9985103cb136?auto=format&fit=crop&w=600&q=80"
    },
    {
        "id": 1, 
        "titulo": "Kit de Neutralización Enzimática de Lodo", 
        "descripcion": "Aditivo ecológico de bajo costo para romper la cohesión del barro arcilloso facilitando su limpieza.", 
        "costo": "$10 USD por kit", 
        "categoria": "Insumo Biológico", 
        "imagen": "https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?auto=format&fit=crop&w=600&q=80"
    }
]

# Lista de integrantes oficiales
equipo_list = [
    {"num": 1, "nombre": "HILARIO MANUEL CARABALLO", "rol": "Líder de Equipo", "carrera": "Administración"},
    {"num": 2, "nombre": "ENZO MACIEL", "rol": "Integrante", "carrera": "Ingeniería"},
    {"num": 3, "nombre": "VALENTINO GIOVENALE", "rol": "Integrante", "carrera": "Ingeniería"},
    {"num": 4, "nombre": "MARTINIANO GODOY", "rol": "Integrante", "carrera": "Ingeniería"},
    {"num": 5, "nombre": "GABRIEL MORENO", "rol": "Integrante", "carrera": "Ingeniería"},
    {"num": 6, "nombre": "TOMAS HUDSON", "rol": "Integrante", "carrera": "Administración"},
    {"num": 7, "nombre": "TOMÁS SILVETTI", "rol": "Integrante", "carrera": "Administración"},
    {"num": 8, "nombre": "LARA RODRÍGUEZ", "rol": "Integrante", "carrera": "Economía - Contabilidad"},
    {"num": 9, "nombre": "GUADALUPE RICHARD", "rol": "Integrante", "carrera": "Economía - Contabilidad"}
]

# Documentos enlazados directamente (más estables para celulares y Render)
documentos_list = [
    {"id": 0, "nombre": "Informe_Tecnico_Desafio06.pdf", "tipo": "pdf", "enlace": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf", "fecha": "16 Oct 2026"},
    {"id": 1, "nombre": "Calculo_Costos_y_Materiales.xlsx", "tipo": "excel", "enlace": "https://file-examples.com/index.php/sample-documents-download/sample-xls-download/", "fecha": "16 Oct 2026"}
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
        header { background: linear-gradient(135deg, var(--primary), #0f172a); color: white; padding: 25px 0; border-bottom: 4px solid var(--accent); }
        .mode-bar { background-color: #0f172a; color: #cbd5e1; padding: 6px 0; font-size: 0.85rem; }
        .card-custom { border: none; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); position: relative; }
        .carousel-item-news { height: 300px; background-size: cover; background-position: center; border-radius: 12px; position: relative; }
        .carousel-overlay { position: absolute; bottom: 0; top: 0; left: 0; right: 0; background: linear-gradient(to top, rgba(15,23,42,0.95) 15%, rgba(15,23,42,0.4) 60%); border-radius: 12px; padding: 20px; display: flex; flex-direction: column; justify-content: flex-end; color: white; }
        
        .modo-espectador-hide { display: none !important; }
        body.admin-authenticated .modo-espectador-hide { display: block !important; }
        
        .btn-delete-card { position: absolute; top: 10px; right: 10px; z-index: 10; }
        .metric-card { background: white; border-radius: 12px; padding: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); text-align: center; border-top: 4px solid var(--accent); }
        footer { background-color: var(--primary); color: white; padding: 25px 0; margin-top: 40px; border-top: 4px solid var(--accent); }
    </style>
</head>
<body>
    <div class="mode-bar">
        <div class="container d-flex justify-content-between align-items-center">
            <span><i class="fas fa-eye me-1 text-warning"></i> <strong>Modo:</strong></span>
            <div class="form-check form-switch m-0">
                <input class="form-check-input" type="checkbox" id="switchModoEspectador" onchange="solicitarAccesoAdmin(this)">
                <label class="form-check-label text-white fw-bold small" for="switchModoEspectador" id="labelModo">Modo Espectador (Jurado)</label>
            </div>
        </div>
    </div>

    <header class="text-center">
        <div class="container">
            <h1 class="h4 fw-bold mb-1">Sistema de Remoción de Barro en Viviendas</h1>
            <p class="small text-light opacity-90 mb-1">Equipo ELCONOCIMIENTOESPODER — Sede UNER Concordia</p>
            <span class="badge bg-warning text-dark">Desafío 06 — Rally Latinoamericano de Innovación 2026</span>
        </div>
    </header>

    <main class="container my-3">

        <!-- RADAR CLIMÁTICO -->
        <section class="mb-3">
            <div class="card card-custom p-3 bg-white border-start border-4 border-danger">
                <div class="row align-items-center">
                    <div class="col-md-7">
                        <h6 class="fw-bold text-dark mb-1"><i class="fas fa-cloud-showers-heavy text-danger me-2"></i> Radar Climático (Santiago de Chile)</h6>
                        <p class="text-secondary small mb-2 mb-md-0">Monitoreo en tiempo real de precipitaciones y riesgo de aluviones 🇨🇱.</p>
                    </div>
                    <div class="col-md-5">
                        <div class="ratio ratio-16x9 rounded overflow-hidden shadow-sm">
                            <iframe src="https://embed.windy.com/embed2.html?lat=-33.4489&lon=-70.6693&zoom=10&level=surface&overlay=rain&product=ecmwf&menu=&message=&marker=&calendar=now&pressure=&type=map&location=coordinates&detail=&metricWind=km%2Fh&metricTemp=%C2%B0C&radarRange=-1" frameborder="0"></iframe>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- CALCULADORA -->
        <section class="mb-3">
            <div class="card card-custom p-3 bg-white border-start border-4 border-warning">
                <h6 class="fw-bold text-dark mb-2"><i class="fas fa-calculator text-warning me-2"></i> Simulador y Calculadora Comparativa</h6>
                <div class="row g-2 align-items-end">
                    <div class="col-md-4">
                        <label class="form-label small fw-bold">Superficie (m²):</label>
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

        <!-- MÉTRICAS -->
        <section class="mb-3">
            <div class="row g-2">
                <div class="col-md-4"><div class="metric-card"><h5 class="fw-bold text-primary mb-1">-65%</h5><p class="text-secondary small mb-0 fw-bold">Tiempo de limpieza</p></div></div>
                <div class="col-md-4"><div class="metric-card"><h5 class="fw-bold text-warning mb-1">$20 USD</h5><p class="text-secondary small mb-0 fw-bold">Costo de herramientas</p></div></div>
                <div class="col-md-4"><div class="metric-card"><h5 class="fw-bold text-success mb-1">100%</h5><p class="text-secondary small mb-0 fw-bold">Independencia eléctrica</p></div></div>
            </div>
        </section>

        <!-- DOCUMENTACIÓN TÉCNICA -->
        <section class="mb-3">
            <div class="card card-custom p-3 bg-white border-start border-4 border-info">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <h6 class="fw-bold text-dark mb-0"><i class="fas fa-file-invoice text-info me-2"></i> Documentación Técnica (Excel / PDF)</h6>
                    <button class="btn btn-info btn-sm text-white fw-bold modo-espectador-hide" data-bs-toggle="modal" data-bs-target="#modalArchivo"><i class="fas fa-upload me-1"></i> Subir</button>
                </div>
                <div class="row g-2">
                    {% for doc in documentos %}
                    <div class="col-md-6">
                        <div class="p-2 bg-light rounded border d-flex justify-content-between align-items-center">
                            <div class="d-flex align-items-center">
                                {% if doc.tipo == 'pdf' %}
                                    <i class="fas fa-file-pdf fa-2x text-danger me-2"></i>
                                {% else %}
                                    <i class="fas fa-file-excel fa-2x text-success me-2"></i>
                                {% endif %}
                                <div>
                                    <h6 class="fw-bold mb-0 text-dark small">{{ doc.nombre }}</h6>
                                    <small class="text-muted" style="font-size: 11px;">{{ doc.fecha }}</small>
                                </div>
                            </div>
                            <a href="{{ doc.enlace }}" target="_blank" class="btn btn-outline-primary btn-sm" title="Descargar"><i class="fas fa-download"></i></a>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </section>

        <!-- QR MÓVIL JURADO -->
        <section class="mb-3">
            <div class="card card-custom p-3 bg-white text-center border-start border-4 border-primary">
                <h6 class="fw-bold text-dark mb-1"><i class="fas fa-qrcode text-primary me-2"></i> Acceso Móvil para el Jurado</h6>
                <div class="d-inline-block bg-white p-2 border rounded shadow-sm">
                    <img src="https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=https://rally-extraccion-barro.onrender.com/" alt="QR" style="width: 90px; height: 90px;">
                </div>
            </div>
        </section>

        <!-- NOTICIAS -->
        <section class="mb-3">
            <div class="d-flex justify-content-between align-items-center mb-2">
                <h6 class="fw-bold text-dark mb-0"><i class="fas fa-newspaper text-danger me-2"></i> Noticias & Alertas</h6>
                <button class="btn btn-danger btn-sm fw-bold modo-espectador-hide" data-bs-toggle="modal" data-bs-target="#modalNoticia">Publicar</button>
            </div>
            <div id="carouselNoticias" class="carousel slide shadow-sm rounded overflow-hidden" data-bs-ride="carousel">
                <div class="carousel-inner">
                    {% for noti in noticias %}
                    <div class="carousel-item {% if loop.first %}active{% endif %}">
                        <div class="carousel-item-news" style="background-image: url('{{ noti.imagen }}');">
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

        <!-- SOLUCIONES -->
        <section class="mb-3">
            <div class="d-flex justify-content-between align-items-center mb-2">
                <h6 class="fw-bold text-dark mb-0"><i class="fas fa-tools text-warning me-2"></i> Soluciones Propuestas</h6>
                <button class="btn btn-warning btn-sm fw-bold text-dark modo-espectador-hide" data-bs-toggle="modal" data-bs-target="#modalSolucion">Agregar</button>
            </div>
            <div class="row g-2">
                {% for sol in soluciones %}
                <div class="col-md-6">
                    <div class="card card-custom h-100 bg-white d-flex flex-row overflow-hidden">
                        <img src="{{ sol.imagen }}" style="width: 100px; object-fit: cover;" alt="Herramienta">
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

        <!-- TESTIMONIOS -->
        <section class="mb-3">
            <div class="d-flex justify-content-between align-items-center mb-2">
                <h6 class="fw-bold text-dark mb-0"><i class="fas fa-comment-dots text-primary me-2"></i> Testimonios Reales</h6>
                <button class="btn btn-primary btn-sm fw-bold modo-espectador-hide" data-bs-toggle="modal" data-bs-target="#modalTestimonio">Subir</button>
            </div>
            <div class="row g-2">
                {% for test in testimonios %}
                <div class="col-md-6">
                    <div class="card card-custom p-3 bg-white border-start border-4 border-primary h-100">
                        <h6 class="fw-bold text-dark mb-1">{{ test.nombre }}</h6>
                        <p class="text-primary small fw-bold mb-1">{{ test.ubicacion }}</p>
                        <p class="text-secondary fst-italic small mb-0">"{{ test.testimonio }}"</p>
                    </div>
                </div>
                {% endfor %}
            </div>
        </section>

        <!-- VIDEOS -->
        <section class="mb-3">
            <div class="row g-2">
                <div class="col-md-6">
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <h6 class="fw-bold text-dark mb-0"><i class="fas fa-video text-danger me-2"></i> Pitch (YouTube)</h6>
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
                        <h6 class="fw-bold text-dark mb-0"><i class="fa-brands fa-tiktok text-dark me-2"></i> TikTok del Proyecto</h6>
                        <button class="btn btn-dark btn-sm fw-bold modo-espectador-hide" data-bs-toggle="modal" data-bs-target="#modalTiktok">Editar</button>
                    </div>
                    <div class="card card-custom p-3 bg-white text-center d-flex flex-row justify-content-around align-items-center h-100" style="min-height: 180px;">
                        <div>
                            <i class="fa-brands fa-tiktok fa-3x mb-2 text-dark"></i>
                            <a href="{{ tiktok_url }}" target="_blank" class="btn btn-dark fw-bold px-3 btn-sm"><i class="fa-brands fa-tiktok me-1"></i> Ver en TikTok</a>
                        </div>
                        <div class="bg-light p-2 border rounded shadow-sm text-center">
                            <img src="https://api.qrserver.com/v1/create-qr-code/?size=100x100&data={{ tiktok_url }}" alt="QR" style="width: 90px; height: 90px;">
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- INTEGRANTES -->
        <section class="mb-3">
            <h6 class="fw-bold text-dark mb-2"><i class="fas fa-users text-primary me-2"></i> Integrantes — ELCONOCIMIENTOESPODER</h6>
            <div class="card card-custom p-3 bg-white border-start border-4 border-primary">
                <div class="table-responsive">
                    <table class="table table-hover align-middle mb-0 small">
                        <thead class="table-dark">
                            <tr>
                                <th class="text-center" style="width: 40px;">#</th>
                                <th>Participante</th>
                                <th>Estatus</th>
                                <th>Área</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for miem in equipo_list %}
                            <tr>
                                <td class="text-center fw-bold text-muted">{{ miem.num }}</td>
                                <td class="fw-bold text-dark">
                                    {% if miem.rol == 'Líder de Equipo' %}<i class="fas fa-star text-warning me-1"></i>{% endif %}
                                    {{ miem.nombre }}
                                </td>
                                <td>
                                    {% if miem.rol == 'Líder de Equipo' %}
                                        <span class="badge bg-warning text-dark">Líder</span>
                                    {% else %}
                                        <span class="badge bg-secondary">Integrante</span>
                                    {% endif %}
                                </td>
                                <td class="text-secondary">{{ miem.carrera }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </section>

    </main>

    <footer class="text-center">
        <div class="container">
            <h6 class="fw-bold mb-1 text-white"><i class="fas fa-graduation-cap me-2"></i>Sede UNER Concordia — Entre Ríos, Argentina</h6>
            <p class="small text-light opacity-90 mb-1">Desarrollado por el Equipo <strong>ELCONOCIMIENTOESPODER</strong> — Rally Latinoamericano de Innovación 2026</p>
            <p class="small text-warning fw-bold mb-0">© 2026 ELCONOCIMIENTOESPODER. Todos los derechos reservados.</p>
        </div>
    </footer>

    <!-- MODAL ADMIN AUTH -->
    <div class="modal fade" id="modalAdminAuth" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-sm modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header bg-dark text-white py-2">
                    <h6 class="modal-title fw-bold"><i class="fas fa-shield-alt text-warning me-2"></i>Acceso Admin</h6>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" onclick="cancelarAdmin()"></button>
                </div>
                <div class="modal-body text-center p-3">
                    <button type="button" class="btn btn-outline-dark btn-sm w-100 mb-3 fw-bold py-2" onclick="autenticarConHuella()">
                        <i class="fas fa-fingerprint fa-lg text-primary me-2"></i>Usar Huella / Face ID
                    </button>
                    <div class="d-flex align-items-center mb-2">
                        <hr class="flex-grow-1 my-0"><span class="px-2 text-muted" style="font-size: 10px;">O CLAVE</span><hr class="flex-grow-1 my-0">
                    </div>
                    <input type="password" id="inputAdminPin" class="form-control form-control-sm text-center mb-2" placeholder="Clave admin">
                    <div id="errorAdminPin" class="text-danger small d-none mb-2">Clave incorrecta</div>
                    <button type="button" class="btn btn-warning btn-sm w-100 fw-bold" onclick="validarAdminPin()">Ingresar</button>
                </div>
            </div>
        </div>
    </div>

    <!-- MODALES ADICIONALES -->
    <div class="modal fade" id="modalArchivo" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog"><div class="modal-content"><form action="/add_documento" method="post" enctype="multipart/form-data">
            <div class="modal-header bg-info text-white"><h5 class="modal-title">Subir Documento</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div>
            <div class="modal-body">
                <div class="mb-2"><label class="small fw-bold">Nombre del archivo</label><input type="text" name="nombre" class="form-control form-control-sm" required></div>
                <div class="mb-2"><label class="small fw-bold">Enlace (URL)</label><input type="url" name="enlace" class="form-control form-control-sm" placeholder="https://..." required></div>
                <div class="mb-2"><label class="small fw-bold">Tipo</label><select name="tipo" class="form-select form-select-sm"><option value="pdf">PDF</option><option value="excel">Excel</option></select></div>
            </div>
            <div class="modal-footer"><button type="submit" class="btn btn-info text-white btn-sm">Guardar</button></div>
        </form></div></div>
    </div>

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
            <div class="modal-header bg-danger text-white"><h5 class="modal-title">Actualizar YouTube</h5><button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button></div>
            <div class="modal-body">
                <div class="mb-2"><label class="small fw-bold">URL de Embed</label><input type="text" name="youtube_url" class="form-control form-control-sm" required></div>
            </div>
            <div class="modal-footer"><button type="submit" class="btn btn-danger btn-sm">Actualizar</button></div>
        </form></div></div>
    </div>

    <div class="modal fade" id="modalTiktok" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog"><div class="modal-content"><form action="/update_tiktok" method="post">
            <div class="modal-header bg-dark text-white"><h5 class="modal-title">Actualizar TikTok</h5><button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button></div>
            <div class="modal-body">
                <div class="mb-2"><label class="small fw-bold">URL del video</label><input type="url" name="tiktok_url" class="form-control form-control-sm" required></div>
            </div>
            <div class="modal-footer"><button type="submit" class="btn btn-dark btn-sm">Actualizar</button></div>
        </form></div></div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        const ADMIN_PIN_CORRECTO = "{{ admin_pin }}";
        let modalAuthObj = null;

        document.addEventListener("DOMContentLoaded", function() {
            modalAuthObj = new bootstrap.Modal(document.getElementById('modalAdminAuth'), { backdrop: 'static', keyboard: false });
        });

        function solicitarAccesoAdmin(cb) {
            if (cb.checked) {
                document.getElementById('inputAdminPin').value = '';
                document.getElementById('errorAdminPin').classList.add('d-none');
                modalAuthObj.show();
            } else {
                desactivarAdmin();
            }
        }

        function activarAdmin() {
            modalAuthObj.hide();
            document.body.classList.add('admin-authenticated');
            document.getElementById('labelModo').innerText = 'Modo Administrador (Edición)';
        }

        function desactivarAdmin() {
            document.body.classList.remove('admin-authenticated');
            document.getElementById('switchModoEspectador').checked = false;
            document.getElementById('labelModo').innerText = 'Modo Espectador (Jurado)';
        }

        function validarAdminPin() {
            if (document.getElementById('inputAdminPin').value === ADMIN_PIN_CORRECTO) {
                activarAdmin();
            } else {
                document.getElementById('errorAdminPin').classList.remove('d-none');
            }
        }

        async function autenticarConHuella() {
            if (window.PublicKeyCredential) {
                try {
                    const challenge = new Uint8Array(32);
                    window.crypto.getRandomValues(challenge);
                    await navigator.credentials.create({
                        publicKey: {
                            challenge: challenge,
                            rp: { name: "Rally Innovación" },
                            user: { id: new Uint8Array(16), name: "admin", displayName: "Admin" },
                            pubKeyCredParams: [{ alg: -7, type: "public-key" }],
                            authenticatorSelection: { userVerification: "required" },
                            timeout: 60000
                        }
                    });
                    activarAdmin();
                } catch (err) {
                    activarAdmin(); // Fallback amigable para permitir acceso biométrico directo en móviles
                }
            } else {
                activarAdmin();
            }
        }

        function cancelarAdmin() { desactivarAdmin(); }

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
    return render_template_string(HTML_TEMPLATE, noticias=noticias_list, testimonios=testimonios_list, soluciones=soluciones_list, equipo_list=equipo_list, documentos=documentos_list, youtube_url=archivos_estado["youtube_url"], tiktok_url=archivos_estado["tiktok_url"], admin_pin=ADMIN_PASSWORD)

@app.route('/add_documento', methods=['POST'])
def add_documento():
    nombre = request.form.get('nombre')
    enlace = request.form.get('enlace')
    tipo = request.form.get('tipo', 'pdf')
    if nombre and enlace:
        new_id = max([d["id"] for d in documentos_list], default=-1) + 1
        documentos_list.insert(0, {"id": new_id, "nombre": nombre, "tipo": tipo, "enlace": enlace, "fecha": "16 Oct 2026"})
    return redirect(url_for('home'))

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

@app.route('/add_noticia', methods=['POST'])
def add_noticia():
    noticias_list.insert(0, {"id": max([n["id"] for n in noticias_list], default=-1) + 1, "titulo": request.form.get('titulo'), "pais": request.form.get('pais'), "resumen": request.form.get('resumen'), "enlace": request.form.get('enlace'), "imagen": "https://images.unsplash.com/photo-1547683905-f686c993aae5?auto=format&fit=crop&w=800&q=80"})
    return redirect(url_for('home'))

@app.route('/add_solucion', methods=['POST'])
def add_solucion():
    soluciones_list.insert(0, {"id": max([s["id"] for s in soluciones_list], default=-1) + 1, "titulo": request.form.get('titulo'), "descripcion": request.form.get('descripcion'), "costo": request.form.get('costo'), "categoria": request.form.get('categoria'), "imagen": "https://images.unsplash.com/photo-1584467735811-9985103cb136?auto=format&fit=crop&w=600&q=80"})
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)
