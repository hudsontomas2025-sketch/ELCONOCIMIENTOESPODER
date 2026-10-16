import os
from flask import Flask, render_template_string, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Noticias recientes para el carrusel
noticias_list = [
    {
        "titulo": "Alerta por El Niño en Concordia: Crecida del Río Uruguay obliga a evacuar familias en la costanera",
        "pais": "Argentina 🇦🇷",
        "fuente": "Diario El Heraldo / TN",
        "fecha": "11 Oct 2026",
        "resumen": "El río Uruguay superó niveles críticos en la costa de Concordia, desbordando áreas ribereñas e ingresando barro y agua a viviendas bajas.",
        "enlace": "https://www.fenix951.com.ar/noticia.php?id=356349",
        "imagen": "https://images.unsplash.com/photo-1547683905-f686c993aae5?auto=format&fit=crop&w=800&q=80"
    },
    {
        "titulo": "Aluvión en Santiago de Chile: Agua y lodo bajan de quebradas afectando viviendas y vehículos",
        "pais": "Chile 🇨🇱",
        "fuente": "Diario UNO / Senapred",
        "fecha": "10 Oct 2026",
        "resumen": "Más de 1.200 personas rescatadas y decenas de casas anegadas tras desprendimientos de barro y rocas precordilleranas.",
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

# Testimonios del mundo
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
        
        /* Carrusel de Noticias */
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
            background-color: var(--primary-color); color: white; padding: 40px 0; margin-top: 60px;
        }
    </style>
</head>
<body>

    <!-- MODO ESPECTADOR / ADMINISTRADOR SWITCH -->
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
            <div class="row align-items-center">
                <div class="col-lg-9 text-lg-start text-center">
                    <span class="badge badge-team px-3 py-2 rounded-pill mb-3 fw-bold">Rally Latinoamericano de Innovación 2026</span>
                    <h1 class="display-5 fw-bold">Sistema de Remoción y Extracción de Barro en Viviendas</h1>
                    <p class="lead mt-2 text-light opacity-90">Solución comunitaria de bajo costo, sustentable e independiente de la red eléctrica para emergencias post-aluvión.</p>
                </div>
                <div class="col-lg-3 text-center mt-4 mt-lg-0">
                    <div class="bg-white p-2 rounded shadow-lg d-inline-block">
                        <img src="{{ qr_url }}" alt="Código QR Interactivo" class="img-fluid" style="max-width: 130px;">
                        <p class="text-dark small fw-bold mb-0 mt-1" style="font-size: 0.75rem;"><i class="fas fa-qrcode me-1 text-warning"></i> Escanea para compartir</p>
                    </div>
                </div>
            </div>
        </div>
    </header>

    <main class="container my-5">

        <!-- EQUIPO -->
        <section class="mb-5">
            <div class="card card-custom p-4 bg-white border-start border-4 border-warning">
                <div class="row align-items-center">
                    <div class="col-md-8">
                        <h3 class="fw-bold text-dark mb-1"><i class="fas fa-users text-warning me-2"></i> Equipo: ELCONOCIMIENTOESPODER</h3>
                        <p class="text-muted mb-0"><strong>Sede:</strong> UNER CONCORDIA — Entre Ríos, Argentina 🇦🇷</p>
                        <p class="small text-secondary mt-1 mb-0">Desafío 06: Extracción y remoción de barro en viviendas anegadas.</p>
                    </div>
                    <div class="col-md-4 text-md-end mt-3 mt-md-0">
                        <span class="badge bg-primary p-2 fs-6"><i class="fas fa-user-check me-1"></i> 9 Integrantes Activos</span>
                    </div>
                </div>
                <hr class="my-3">
                <div class="table-responsive">
                    <table class="table table-sm table-hover align-middle mb-0">
                        <thead class="table-dark">
                            <tr>
                                <th>#</th>
                                <th>Participante</th>
                                <th>Estatus</th>
                                <th>Área de Estudio</th>
                                <th>Modalidad</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr><td>1</td><td>⭐ <strong>HILARIO MANUEL CARABALLO</strong></td><td><span class="badge bg-warning text-dark">Líder</span></td><td>Administración</td><td>Presencial</td></tr>
                            <tr><td>2</td><td>ENZO MACIEL</td><td>Integrante</td><td>Ingeniería</td><td>Presencial</td></tr>
                            <tr><td>3</td><td>VALENTINO GIOVENALE</td><td>Integrante</td><td>Ingeniería</td><td>Presencial</td></tr>
                            <tr><td>4</td><td>MARTINIANO GODOY</td><td>Integrante</td><td>Ingeniería</td><td>Presencial</td></tr>
                            <tr><td>5</td><td>GABRIEL MORENO</td><td>Integrante</td><td>Ingeniería</td><td>Presencial</td></tr>
                            <tr><td>6</td><td>TOMAS HUDSON</td><td>Integrante</td><td>Administración</td><td>Presencial</td></tr>
                            <tr><td>7</td><td>TOMÁS SILVETTI</td><td>Integrante</td><td>Administración</td><td>Presencial</td></tr>
                            <tr><td>8</td><td>LARA RODRÍGUEZ</td><td>Integrante</td><td>Economía - Contabilidad</td><td>Presencial</td></tr>
                            <tr><td>9</td><td>GUADALUPE RICHARD</td><td>Integrante</td><td>Economía - Contabilidad</td><td>Presencial</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </section>

        <!-- DIAGNÓSTICO -->
        <section class="mb-5">
            <div class="card card-custom p-4 bg-white border-start border-4 border-danger">
                <h2 class="fw-bold text-dark mb-3"><i class="fas fa-exclamation-triangle text-danger me-2"></i> Diagnóstico del Problema Principal</h2>
                <div class="row">
                    <div class="col-md-7">
                        <p class="text-secondary">Tras el retroceso de las aguas en anegamientos y aluviones, las viviendas quedan anegadas por capas gruesas de lodo y arcilla. El problema crítico es que <strong>este barro se fragua y compacta velozmente como cemento</strong> en cuestión de horas.</p>
                        <p class="text-secondary">Las familias se enfrentan a tres limitantes severas: <strong>1) Espacios estrechos e interiores</strong> donde la maquinaria pesada no puede ingresar, <strong>2) Corte total de energía eléctrica</strong> que inhabilita bombas convencionales, y <strong>3) Desgaste físico severo y riesgos lumbares</strong> al intentar palear peso muerto en vertical.</p>
                    </div>
                    <div class="col-md-5">
                        <div class="bg-light p-3 rounded border border-danger-subtle">
                            <h5 class="fw-bold text-dark mb-2"><i class="fas fa-bullseye text-danger me-2"></i> Objetivos del Proyecto:</h5>
                            <ul class="small text-muted mb-0 ps-3">
                                <li class="mb-1">Remover lodo denso sin consumo de energía eléctrica.</li>
                                <li class="mb-1">Reducir el esfuerzo físico mediante tracción horizontal ergonómica.</li>
                                <li class="mb-1">Mantener costos mínimos ($15 - $70 USD) de fabricación local.</li>
                                <li>Garantizar aplicabilidad comunitaria inmediata en Concordia y la región.</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- CARRUSEL DE NOTICIAS -->
        <section class="mb-5">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <div>
                    <h2 class="fw-bold text-dark mb-0"><i class="fas fa-newspaper text-danger me-2"></i> Monitoreo Climático & Noticias en Vivo</h2>
                    <p class="text-muted small mb-0">Crecidas, aluviones e impacto en tiempo real.</p>
                </div>
                <button class="btn btn-danger btn-sm fw-bold shadow-sm modo-espectador-hide" data-bs-toggle="modal" data-bs-target="#modalNoticia">
                    <i class="fas fa-plus-circle me-1"></i> Publicar Noticia
                </button>
            </div>

            <div id="carouselNoticias" class="carousel slide shadow-lg rounded-3 overflow-hidden" data-bs-ride="carousel">
                <div class="carousel-indicators">
                    {% for noti in noticias %}
                    <button type="button" data-bs-target="#carouselNoticias" data-bs-slide-to="{{ loop.index0 }}" class="{% if loop.first %}active{% endif %}"></button>
                    {% endfor %}
                </div>
                <div class="carousel-inner">
                    {% for noti in noticias %}
                    <div class="carousel-item {% if loop.first %}active{% endif %}">
                        <div class="carousel-item-news" style="background-image: url('{{ noti.imagen }}');">
                            <div class="carousel-overlay">
                                <div>
                                    <span class="badge bg-danger px-3 py-2 mb-2">{{ noti.pais }}</span>
                                    <span class="badge bg-dark px-3 py-2 mb-2 ms-1"><i class="fas fa-globe me-1"></i> {{ noti.fuente }}</span>
                                    <small class="text-light ms-2">{{ noti.fecha }}</small>
                                </div>
                                <h3 class="fw-bold text-white fs-4 mt-2 mb-2">{{ noti.titulo }}</h3>
                                <p class="text-light opacity-90 small col-lg-9 mb-3">{{ noti.resumen }}</p>
                                <div>
                                    <a href="{{ noti.enlace }}" target="_blank" class="btn btn-warning btn-sm fw-bold">Ver Noticia Completa <i class="fas fa-external-link-alt ms-1"></i></a>
                                </div>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
                <button class="carousel-control-prev" type="button" data-bs-target="#carouselNoticias" data-bs-slide="prev">
                    <span class="carousel-control-prev-icon"></span>
                </button>
                <button class="carousel-control-next" type="button" data-bs-target="#carouselNoticias" data-bs-slide="next">
                    <span class="carousel-control-next-icon"></span>
                </button>
            </div>
        </section>

        <!-- TESTIMONIOS GLOBALES -->
        <section class="mb-5">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <div>
                    <h2 class="fw-bold text-dark mb-0"><i class="fas fa-comment-dots text-primary me-2"></i> Testimonios Globales post-Desastre</h2>
                    <p class="text-muted small mb-0">Relatos y experiencias reales de vecinos y voluntarios afectados por lodo y anegamientos.</p>
                </div>
                <button class="btn btn-primary btn-sm fw-bold shadow-sm modo-espectador-hide" data-bs-toggle="modal" data-bs-target="#modalTestimonio">
                    <i class="fas fa-plus-circle me-1"></i> Sumar Testimonio
                </button>
            </div>

            <div class="row g-4">
                {% for test in testimonios %}
                <div class="col-md-6">
                    <div class="card card-custom h-100 p-4 bg-white border-start border-4 border-primary">
                        <div class="d-flex align-items-center mb-3">
                            <img src="{{ test.foto }}" class="rounded-circle me-3" style="width: 55px; height: 55px; object-fit: cover;" alt="Avatar">
                            <div>
                                <h5 class="fw-bold text-dark mb-0 fs-6">{{ test.nombre }}</h5>
                                <p class="text-primary small fw-bold mb-0"><i class="fas fa-map-marker-alt me-1"></i> {{ test.ubicacion }}</p>
                                <small class="text-muted" style="font-size: 0.75rem;">{{ test.fecha }}</small>
                            </div>
                        </div>
                        <p class="card-text text-secondary fst-italic small mb-0">"{{ test.testimonio }}"</p>
                    </div>
                </div>
                {% endfor %}
            </div>
        </section>

        <!-- IMPACTO Y EFICIENCIA -->
        <section class="mb-5">
            <h2 class="fw-bold text-dark mb-3"><i class="fas fa-chart-line text-primary me-2"></i> Impacto y Eficiencia Estimada</h2>
            <div class="card card-custom p-4 bg-white">
                <div class="table-responsive">
                    <table class="table table-bordered align-middle text-center mb-0">
                        <thead class="table-primary">
                            <tr>
                                <th>Criterio de Evaluación</th>
                                <th>Método Tradicional (Pala de mano)</th>
                                <th>Sistema ELCONOCIMIENTOESPODER</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td class="fw-bold text-start">Tiempo de Limpieza (por habitación)</td>
                                <td>~8 Horas / Habitación</td>
                                <td class="table-success fw-bold text-success">~2.5 Horas / Habitación</td>
                            </tr>
                            <tr>
                                <td class="fw-bold text-start">Riesgo Ergonómico / Lesiones</td>
                                <td class="text-danger fw-bold">Alto (Izamiento vertical repetitivo)</td>
                                <td class="table-success fw-bold text-success">Bajo (Arrastre mecánico asistido)</td>
                            </tr>
                            <tr>
                                <td class="fw-bold text-start">Dependencia Eléctrica</td>
                                <td>Requiere bombas eléctricas o generadores</td>
                                <td class="table-success fw-bold text-success">0% (100% Mecánico / Venturi)</td>
                            </tr>
                            <tr>
                                <td class="fw-bold text-start">Costo de Implementación</td>
                                <td>Maquinaria pesada ($1.500+ USD)</td>
                                <td class="table-success fw-bold text-success">$15 - $70 USD (Kits Barriales)</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </section>

        <!-- FINANCIAMIENTO Y SOCIOS -->
        <section class="row g-4 mb-5">
            <div class="col-lg-6">
                <div class="card card-custom h-100 p-4 bg-white border-top border-4 border-success">
                    <h3 class="fw-bold text-dark mb-3"><i class="fas fa-hand-holding-usd text-success me-2"></i> Estrategia de Financiamiento</h3>
                    <p class="text-muted small">Para escalar la producción de las herramientas y dotar a las brigadas de emergencia:</p>
                    <ul class="small text-secondary ps-3 mb-0">
                        <li class="mb-2"><strong>Fondos de Emergencia Climática:</strong> Asignación directa de Defensa Civil y municipios.</li>
                        <li class="mb-2"><strong>Proyectos de Vinculación Tecnológica:</strong> Subsidios universitarios de la UNER e instituciones de ciencia.</li>
                        <li class="mb-0"><strong>Donaciones y Crowdfunding:</strong> Campañas solidarias mediante Mercado Pago y PayPal.</li>
                    </ul>
                </div>
            </div>

            <div class="col-lg-6">
                <div class="card card-custom h-100 p-4 bg-white border-top border-4 border-primary">
                    <h3 class="fw-bold text-dark mb-3"><i class="fas fa-handshake text-primary me-2"></i> Socios Regionales Estratégicos</h3>
                    <p class="text-muted small">Alianzas clave en Concordia (Entre Ríos) y la región:</p>
                    <ul class="small text-secondary ps-3 mb-0">
                        <li class="mb-2"><strong>Defensa Civil Concordia:</strong> Articulación logística y distribución preventiva.</li>
                        <li class="mb-2"><strong>UNER Sede Concordia:</strong> Ensayos de laboratorio, ergonomía y validación.</li>
                        <li class="mb-0"><strong>Cooperativas Vecinales y Corralones:</strong> Provisión de insumos reciclados.</li>
                    </ul>
                </div>
            </div>
        </section>

        <!-- FODA -->
        <section class="mb-5">
            <h2 class="fw-bold text-dark mb-4"><i class="fas fa-chart-pie text-warning me-2"></i> Análisis FODA Estratégico</h2>
            <div class="row g-3">
                <div class="col-md-6">
                    <div class="foda-card foda-f shadow-sm">
                        <h5 class="fw-bold mb-2"><i class="fas fa-shield-alt me-2"></i> Fortalezas (F)</h5>
                        <ul class="mb-0 small ps-3">
                            <li>Bajo costo unitario ($15 - $70 USD).</li>
                            <li>Operatividad 100% independiente de electricidad.</li>
                            <li>Reducción significativa del esfuerzo lumbar.</li>
                        </ul>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="foda-card foda-o shadow-sm">
                        <h5 class="fw-bold mb-2"><i class="fas fa-globe-americas me-2"></i> Oportunidades (O)</h5>
                        <ul class="mb-0 small ps-3">
                            <li>Implementación en municipios vulnerables.</li>
                            <li>Fabricación comunitaria en talleres sociales.</li>
                            <li>Exportación del modelo a toda América Latina.</li>
                        </ul>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="foda-card foda-d shadow-sm">
                        <h5 class="fw-bold mb-2"><i class="fas fa-exclamation-triangle me-2"></i> Debilidades (D)</h5>
                        <ul class="mb-0 small ps-3">
                            <li>Barro hiper-seco requiere humectación hídrica previa.</li>
                            <li>Requiere capacitación básica a voluntarios.</li>
                        </ul>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="foda-card foda-a shadow-sm">
                        <h5 class="fw-bold mb-2"><i class="fas fa-skull-crossbones me-2"></i> Amenazas (A)</h5>
                        <ul class="mb-0 small ps-3">
                            <li>Falta de stock preventivo pre-catástrofe.</li>
                            <li>Cortes prolongados en la red de agua potable.</li>
                        </ul>
                    </div>
                </div>
            </div>
        </section>

        <!-- ENTREGABLES OFICIALES PDF -->
        <section class="mb-5">
            <h2 class="fw-bold mb-4 text-dark"><i class="fas fa-file-pdf text-danger me-2"></i> Entregables Oficiales (PDFs)</h2>
            <div class="row g-4">
                <div class="col-lg-6">
                    <div class="card card-custom h-100 p-4 bg-white border-top border-4 border-danger">
                        <h4 class="fw-bold text-dark mb-3"><i class="fas fa-file-alt text-danger me-2"></i> Informe Técnico Principal</h4>
                        <form action="/upload_pdf" method="post" enctype="multipart/form-data" class="mb-3 modo-espectador-hide">
                            <input type="hidden" name="tipo_doc" value="informe_pdf">
                            <div class="input-group input-group-sm">
                                <input type="file" name="archivo" class="form-control" accept=".pdf" required>
                                <button class="btn btn-danger" type="submit"><i class="fas fa-upload me-1"></i> Cargar</button>
                            </div>
                        </form>
                        {% if archivos.informe_pdf %}
                            <div class="alert alert-success py-2 px-3 small d-flex justify-content-between align-items-center mb-2">
                                <span><i class="fas fa-check-circle me-1"></i> {{ archivos.informe_pdf }}</span>
                                <a href="/uploads/{{ archivos.informe_pdf }}" target="_blank" class="btn btn-sm btn-outline-success">Ver Documento</a>
                            </div>
                            <iframe src="/uploads/{{ archivos.informe_pdf }}" class="pdf-preview"></iframe>
                        {% else %}
                            <div class="alert alert-secondary text-center py-4 text-muted small">Pendiente de carga de archivo PDF.</div>
                        {% endif %}
                    </div>
                </div>

                <div class="col-lg-6">
                    <div class="card card-custom h-100 p-4 bg-white border-top border-4 border-success">
                        <h4 class="fw-bold text-dark mb-3"><i class="fas fa-calculator text-success me-2"></i> Reporte Financiero & Costos</h4>
                        <form action="/upload_pdf" method="post" enctype="multipart/form-data" class="mb-3 modo-espectador-hide">
                            <input type="hidden" name="tipo_doc" value="informe_financiero">
                            <div class="input-group input-group-sm">
                                <input type="file" name="archivo" class="form-control" accept=".pdf" required>
                                <button class="btn btn-success" type="submit"><i class="fas fa-upload me-1"></i> Cargar</button>
                            </div>
                        </form>
                        {% if archivos.informe_financiero %}
                            <div class="alert alert-success py-2 px-3 small d-flex justify-content-between align-items-center mb-2">
                                <span><i class="fas fa-check-circle me-1"></i> {{ archivos.informe_financiero }}</span>
                                <a href="/uploads/{{ archivos.informe_financiero }}" target="_blank" class="btn btn-sm btn-outline-success">Ver Documento</a>
                            </div>
                            <iframe src="/uploads/{{ archivos.informe_financiero }}" class="pdf-preview"></iframe>
                        {% else %}
                            <div class="alert alert-secondary text-center py-4 text-muted small">Pendiente de carga de archivo PDF.</div>
                        {% endif %}
                    </div>
                </div>
            </div>
        </section>

        <!-- VIDEO PITCH -->
        <section class="mb-5">
            <div class="card card-custom p-4 bg-white border-top border-4 border-primary">
                <div class="row align-items-center mb-3">
                    <div class="col-md-7">
                        <h3 class="fw-bold text-dark mb-1"><i class="fab fa-youtube text-danger me-2"></i> Video Pitch Ejecutivo</h3>
                        <p class="text-muted small mb-0">Presentación de la solución para el jurado del Rally.</p>
                    </div>
                    <div class="col-md-5 mt-2 mt-md-0 modo-espectador-hide">
                        <form action="/update_youtube" method="post">
                            <div class="input-group input-group-sm">
                                <input type="text" name="youtube_url" class="form-control" placeholder="URL o ID de YouTube" required>
                                <button class="btn btn-primary" type="submit"><i class="fas fa-sync-alt me-1"></i> Enlazar</button>
                            </div>
                        </form>
                    </div>
                </div>
                <div class="video-container shadow-sm">
                    <iframe src="https://www.youtube.com/embed/{{ archivos.youtube_id }}" allowfullscreen></iframe>
                </div>
            </div>
        </section>

        <!-- SOLUCIONES Y DISPOSITIVOS DESARROLLADOS -->
        <section class="mb-5">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <div>
                    <h2 class="fw-bold text-dark mb-0"><i class="fas fa-tools text-warning me-2"></i> Soluciones & Dispositivos Desarrollados</h2>
                    <p class="text-muted small mb-0">Catálogo técnico de propuestas mecánicas e hidráulicas.</p>
                </div>
                <button class="btn btn-warning fw-bold text-dark btn-sm shadow-sm modo-espectador-hide" data-bs-toggle="modal" data-bs-target="#modalSolucion">
                    <i class="fas fa-plus-circle me-1"></i> Cargar Solución Manual
                </button>
            </div>
            
            <div class="row g-4">
                {% for sol in soluciones %}
                <div class="col-md-6 col-lg-4">
                    <div class="card card-custom h-100 bg-white position-relative shadow-sm">
                        <form action="/delete_solucion/{{ loop.index0 }}" method="post" class="position-absolute top-0 end-0 m-2 modo-espectador-hide" onsubmit="return confirm('¿Eliminar esta solución?');">
                            <button type="submit" class="btn btn-danger btn-sm rounded-circle p-1 px-2 shadow-sm" title="Eliminar">
                                <i class="fas fa-trash-alt"></i>
                            </button>
                        </form>

                        <img src="{{ sol.imagen }}" class="card-img-top" alt="Solución" style="height: 190px; object-fit: cover;">
                        <div class="card-body">
                            <span class="badge bg-secondary mb-2">{{ sol.categoria }}</span>
                            <h5 class="card-title fw-bold text-dark">{{ sol.titulo }}</h5>
                            <p class="card-text text-muted small">{{ sol.descripcion }}</p>
                        </div>
                        <div class="card-footer bg-light border-0 d-flex justify-content-between align-items-center">
                            <span class="small fw-bold text-success"><i class="fas fa-tag me-1"></i> {{ sol.costo }}</span>
                            <span class="badge bg-white text-dark border">Fabricación Local</span>
                        </div>
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
                <form action="/add_testimonio" method="post" enctype="multipart/form-data">
                    <div class="modal-header bg-primary text-white">
                        <h5 class="modal-title fw-bold"><i class="fas fa-comment-dots me-2"></i> Sumar Testimonio Global</h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="mb-3">
                            <label class="form-label fw-bold small">Nombre Completo</label>
                            <input type="text" name="nombre" class="form-control form-control-sm" required placeholder="Ej. Ana María Martínez">
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-bold small">Ubicación / Ciudad / País</label>
                            <input type="text" name="ubicacion" class="form-control form-control-sm" required placeholder="Ej. Concordia, Argentina">
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-bold small">Relato o Testimonio</label>
                            <textarea name="testimonio" class="form-control form-control-sm" rows="3" required placeholder="Cuéntanos tu experiencia tras el anegamiento o aluvión..."></textarea>
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-bold small">Foto de Perfil o Lugar (Opcional)</label>
                            <input type="file" name="foto_testimonio" class="form-control form-control-sm" accept="image/*">
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary btn-sm" data-bs-dismiss="modal">Cancelar</button>
                        <button type="submit" class="btn btn-primary btn-sm fw-bold">Guardar Testimonio</button>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <!-- MODAL NOTICIA -->
    <div class="modal fade" id="modalNoticia" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <form action="/add_noticia" method="post" enctype="multipart/form-data">
                    <div class="modal-header bg-danger text-white">
                        <h5 class="modal-title fw-bold"><i class="fas fa-newspaper me-2"></i> Publicar Noticia</h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="mb-3">
                            <label class="form-label fw-bold small">Titular</label>
                            <input type="text" name="titulo" class="form-control form-control-sm" required>
                        </div>
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label fw-bold small">País</label>
                                <input type="text" name="pais" class="form-control form-control-sm" required placeholder="Ej. Argentina">
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label fw-bold small">Fuente</label>
                                <input type="text" name="fuente" class="form-control form-control-sm" required placeholder="Ej. El Heraldo">
                            </div>
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-bold small">URL de la Nota Externa</label>
                            <input type="url" name="enlace" class="form-control form-control-sm" required placeholder="https://...">
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-bold small">Resumen</label>
                            <textarea name="resumen" class="form-control form-control-sm" rows="3" required></textarea>
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-bold small">Imagen de Portada</label>
                            <input type="file" name="foto_noticia" class="form-control form-control-sm" accept="image/*" required>
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

    <!-- MODAL SOLUCIÓN MANUAL -->
    <div class="modal fade" id="modalSolucion" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <form action="/add_solucion" method="post" enctype="multipart/form-data">
                    <div class="modal-header bg-warning">
                        <h5 class="modal-title fw-bold text-dark"><i class="fas fa-tools me-2"></i> Cargar Nueva Solución Manual</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="mb-3">
                            <label class="form-label fw-bold small">Nombre del Dispositivo / Herramienta</label>
                            <input type="text" name="titulo" class="form-control form-control-sm" required placeholder="Ej. Rastrillo de Arrastre...">
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-bold small">Categoría</label>
                            <select name="categoria" class="form-select form-select-sm">
                                <option value="Herramienta Manual">Herramienta Manual</option>
                                <option value="Succión / Hidráulico">Succión / Hidráulico</option>
                                <option value="Protección / Seguridad">Protección / Seguridad</option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-bold small">Descripción del Dispositivo</label>
                            <textarea name="descripcion" class="form-control form-control-sm" rows="3" required></textarea>
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-bold small">Costo Estimado</label>
                            <input type="text" name="costo" class="form-control form-control-sm" required placeholder="Ej. $20 - $35 USD">
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-bold small">Fotografía o Imagen del Dispositivo</label>
                            <input type="file" name="foto_solucion" class="form-control form-control-sm" accept="image/*" required>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary btn-sm" data-bs-dismiss="modal">Cancelar</button>
                        <button type="submit" class="btn btn-warning btn-sm fw-bold">Guardar y Publicar</button>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <footer class="text-center">
        <div class="container">
            <p class="mb-1 fw-bold">&copy; 2026 - Equipo ELCONOCIMIENTOESPODER | Sede UNER Concordia</p>
            <p class="small text-muted mb-0">Desafío 06 — Rally Latinoamericano de Innovación 2026</p>
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
    host_url = request.host_url.rstrip('/')
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=180x180&data={host_url}"
    return render_template_string(HTML_TEMPLATE, noticias=noticias_list, testimonios=testimonios_list, soluciones=soluciones_list, archivos=archivos_estado, qr_url=qr_url)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    tipo_doc = request.form.get('tipo_doc')
    if 'archivo' in request.files:
        file = request.files['archivo']
        if file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            archivos_estado[tipo_doc] = filename
    return redirect(url_for('home'))

@app.route('/update_youtube', methods=['POST'])
def update_youtube():
    url = request.form.get('youtube_url', '')
    if 'v=' in url:
        yt_id = url.split('v=')[1].split('&')[0]
    elif 'youtu.be/' in url:
        yt_id = url.split('youtu.be/')[1].split('?')[0]
    else:
        yt_id = url
    archivos_estado['youtube_id'] = yt_id
    return redirect(url_for('home'))

@app.route('/add_noticia', methods=['POST'])
def add_noticia():
    titulo = request.form.get('titulo')
    pais = request.form.get('pais')
    fuente = request.form.get('fuente')
    enlace = request.form.get('enlace')
    resumen = request.form.get('resumen')
    img_url = "https://images.unsplash.com/photo-1547683905-f686c993aae5?auto=format&fit=crop&w=600&q=80"
    if 'foto_noticia' in request.files:
        file = request.files['foto_noticia']
        if file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            img_url = f"/uploads/{filename}"

    noticias_list.insert(0, {
        "titulo": titulo, "pais": pais, "fuente": fuente, "enlace": enlace,
        "fecha": "Reciente", "resumen": resumen, "imagen": img_url
    })
    return redirect(url_for('home'))

@app.route('/add_testimonio', methods=['POST'])
def add_testimonio():
    nombre = request.form.get('nombre')
    ubicacion = request.form.get('ubicacion')
    testimonio = request.form.get('testimonio')
    foto_url = "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=200&q=80"
    if 'foto_testimonio' in request.files:
        file = request.files['foto_testimonio']
        if file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            foto_url = f"/uploads/{filename}"

    testimonios_list.insert(0, {
        "nombre": nombre, "ubicacion": ubicacion, "testimonio": testimonio,
        "fecha": "Reciente", "foto": foto_url
    })
    return redirect(url_for('home'))

@app.route('/add_solucion', methods=['POST'])
def add_solucion():
    titulo = request.form.get('titulo')
    categoria = request.form.get('categoria')
    descripcion = request.form.get('descripcion')
    costo = request.form.get('costo')
    img_url = "https://images.unsplash.com/photo-1584467735811-9985103cb136?auto=format&fit=crop&w=600&q=80"
    if 'foto_solucion' in request.files:
        file = request.files['foto_solucion']
        if file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            img_url = f"/uploads/{filename}"

    soluciones_list.append({
        "titulo": titulo, "categoria": categoria, "descripcion": descripcion, "costo": costo, "imagen": img_url
    })
    return redirect(url_for('home'))

@app.route('/delete_solucion/<int:index>', methods=['POST'])
def delete_solucion(index):
    if 0 <= index < len(soluciones_list):
        soluciones_list.pop(index)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)s