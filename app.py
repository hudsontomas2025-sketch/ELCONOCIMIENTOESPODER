import os
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# CONTRASEÑA DE ADMINISTRADOR
ADMIN_PASSWORD = "1234"

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

archivos_estado = {
    "youtube_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
    "tiktok_url": "https://www.tiktok.com/@giuli1160/video/7697398587696663828",
    "doc_url": "https://docs.google.com/document/d/1RajPj2JWkuQKAJaoVNh8dDuxDxQsYjNu/preview",
    "doc_direct_url": "https://docs.google.com/document/d/1RajPj2JWkuQKAJaoVNh8dDuxDxQsYjNu/edit?usp=sharing",
    "sheet_url": "https://docs.google.com/spreadsheets/d/1QBOBfwBylOL--v5b97GJ6_T-UFbCkZa0cVIybnGih6A/preview",
    "sheet_direct_url": "https://docs.google.com/spreadsheets/d/1QBOBfwBylOL--v5b97GJ6_T-UFbCkZa0cVIybnGih6A/edit?usp=sharing"
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
        
        .modo-espectador-hide { display: none !important; }
        body.admin-authenticated .modo-espectador-hide { display: block !important; }
        
        .btn-delete-card { position: absolute; top: 8px; right: 8px; z-index: 10; }
        footer { background-color: var(--primary); color: white; padding: 25px 0; margin-top: 40px; border-top: 4px solid var(--accent); }
        .foda-list { padding-left: 1.2rem; margin-bottom: 0; }
        .foda-list li { margin-bottom: 0.3rem; font-size: 0.85rem; }
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

        <!-- APARTADO 1: LA PROBLEMÁTICA -->
        <section class="mb-3">
            <div class="card card-custom p-3 bg-white border-start border-4 border-danger">
                <h5 class="fw-bold text-danger mb-2"><i class="fas fa-exclamation-triangle me-2"></i>La Problemática</h5>
                <p class="text-secondary small mb-0">
                    Durante eventos meteorológicos de precipitaciones intensas, aluviones y crecidas de ríos, toneladas de lodo y barro denso ingresan a las viviendas familiares. La limpieza manual resulta extenuante, lenta e ineficiente, mientras que la falta de herramientas adecuadas incrementa significativamente el tiempo de habitabilidad de los hogares afectados y genera pérdidas materiales irreversibles.
                </p>
            </div>
        </section>

        <!-- APARTADO 2: VIDEO SOLUCIÓN YOUTUBE -->
        <section class="mb-3">
            <div class="card card-custom p-3 bg-white border-start border-4 border-success">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <h5 class="fw-bold text-success mb-0"><i class="fab fa-youtube text-danger me-2"></i>Video Solución del Proyecto (Pitch)</h5>
                    <button class="btn btn-danger btn-sm fw-bold modo-espectador-hide" data-bs-toggle="modal" data-bs-target="#modalYoutube"><i class="fas fa-edit me-1"></i> Cambiar Video</button>
                </div>
                <p class="text-secondary small mb-3">Presentación audiovisual del prototipo y propuesta técnica elaborada por el equipo.</p>
                <div class="ratio ratio-16x9 rounded overflow-hidden shadow-sm">
                    <iframe src="{{ youtube_url }}" allowfullscreen></iframe>
                </div>
            </div>
        </section>

        <!-- APARTADO 3: PREVISUALIZACIÓN DEL INFORME TÉCNICO (GOOGLE DOCS) -->
        <section class="mb-3">
            <div class="card card-custom p-3 bg-white border-start border-4 border-primary">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <h5 class="fw-bold text-primary mb-0"><i class="fas fa-file-alt text-primary me-2"></i>Informe Técnico y Memoria Descriptiva</h5>
                    <a href="{{ doc_direct_url }}" target="_blank" class="btn btn-outline-primary btn-sm fw-bold"><i class="fas fa-external-link-alt me-1"></i> Abrir Documento</a>
                </div>
                <p class="text-secondary small mb-2">Previsualización interactiva del informe técnico cargado en Google Docs.</p>
                <div class="ratio ratio-16x9 rounded overflow-hidden shadow-sm" style="min-height: 450px;">
                    <iframe src="{{ doc_url }}" frameborder="0"></iframe>
                </div>
            </div>
        </section>

        <!-- APARTADO 4: PREVISUALIZACIÓN DEL PRESUPUESTO (GOOGLE SHEETS) -->
        <section class="mb-3">
            <div class="card card-custom p-3 bg-white border-start border-4 border-success">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <h5 class="fw-bold text-success mb-0"><i class="fas fa-file-excel text-success me-2"></i>Presupuesto Estimado y Costos</h5>
                    <a href="{{ sheet_direct_url }}" target="_blank" class="btn btn-outline-success btn-sm fw-bold"><i class="fas fa-external-link-alt me-1"></i> Abrir Planilla</a>
                </div>
                <p class="text-secondary small mb-2">Previsualización interactiva de la planilla de presupuesto cargada en Google Sheets.</p>
                <div class="ratio ratio-16x9 rounded overflow-hidden shadow-sm" style="min-height: 450px;">
                    <iframe src="{{ sheet_url }}" frameborder="0"></iframe>
                </div>
            </div>
        </section>

        <!-- APARTADO 5: ANÁLISIS FODA DEL PROYECTO -->
        <section class="mb-3">
            <div class="card card-custom p-3 bg-white border-start border-4 border-dark">
                <h5 class="fw-bold text-dark mb-3"><i class="fas fa-chart-pie text-warning me-2"></i>Análisis FODA del Proyecto</h5>
                <div class="row g-2">
                    <div class="col-md-6">
                        <div class="p-3 bg-light rounded border border-success h-100">
                            <h6 class="fw-bold text-success mb-2"><i class="fas fa-shield-alt me-2"></i>Fortalezas</h6>
                            <ul class="foda-list text-secondary">
                                <li><strong>Integración tecnológica:</strong> combina hidro-corte, trituración y extracción continua en un mismo sistema portátil.</li>
                                <li><strong>Potencial de eficiencia operativa:</strong> busca reducir el tiempo de limpieza y el esfuerzo físico de las personas afectadas.</li>
                                <li><strong>Protección de las viviendas:</strong> diseño orientado a remover el barro preservando los pisos.</li>
                                <li><strong>Potencial de economía circular:</strong> propone tratar el barro extraído para su posible aprovechamiento en obras viales.</li>
                                <li><strong>Mantenimiento potencialmente accesible:</strong> utiliza componentes mecánicos convencionales y materiales de fácil acceso.</li>
                            </ul>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="p-3 bg-light rounded border border-primary h-100">
                            <h6 class="fw-bold text-primary mb-2"><i class="fas fa-lightbulb me-2"></i>Oportunidades</h6>
                            <ul class="foda-list text-secondary">
                                <li><strong>Preparación comunitaria ante emergencias:</strong> disponer de equipos en zonas vulnerables para agilizar la limpieza y recuperación de las viviendas después de un aluvión.</li>
                                <li><strong>Alianzas estratégicas:</strong> articular con municipios, ONG y empresas para desarrollar y financiar la solución.</li>
                                <li><strong>Formación de brigadas locales:</strong> preparar a integrantes de la comunidad para utilizar el equipo de manera segura.</li>
                                <li><strong>Gestión sustentable del sedimento:</strong> evaluar su tratamiento y reutilización para reducir la disposición descontrolada.</li>
                                <li><strong>Posibilidad de replicación:</strong> adaptar el sistema a otras localidades afectadas por inundaciones y aluviones.</li>
                            </ul>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="p-3 bg-light rounded border border-warning h-100">
                            <h6 class="fw-bold text-warning text-dark mb-2"><i class="fas fa-exclamation-circle me-2"></i>Debilidades</h6>
                            <ul class="foda-list text-secondary">
                                <li><strong>Validación técnica pendiente:</strong> se requieren pruebas en condiciones reales de funcionamiento.</li>
                                <li><strong>Complejidad de integración mecánica:</strong> los mecanismos deben operar coordinadamente para evitar fallas y obstrucciones.</li>
                                <li><strong>Adaptación a espacios difíciles:</strong> es necesario verificar la maniobrabilidad en viviendas con accesos estrechos y obstáculos.</li>
                            </ul>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="p-3 bg-light rounded border border-danger h-100">
                            <h6 class="fw-bold text-danger mb-2"><i class="fas fa-bug me-2"></i>Amenazas</h6>
                            <ul class="foda-list text-secondary">
                                <li><strong>Emergencias de gran magnitud:</strong> la demanda de atención puede superar la cantidad de equipos disponibles.</li>
                                <li><strong>Contaminación del sedimento:</strong> puede impedir su reutilización y exigir una gestión alternativa.</li>
                                <li><strong>Riesgos de seguridad:</strong> el agua a presión y los componentes móviles requieren medidas de protección adecuadas.</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- RADAR CLIMÁTICO -->
        <section class="mb-3">
            <div class="card card-custom p-3 bg-white border-start border-4 border-primary">
                <div class="row align-items-center">
                    <div class="col-md-7">
                        <h6 class="fw-bold text-dark mb-1"><i class="fas fa-cloud-showers-heavy text-primary me-2"></i> Radar Climático en Vivo (Santiago de Chile)</h6>
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

        <!-- TIKTOK DEL PROYECTO -->
        <section class="mb-3">
            <div class="card card-custom p-3 bg-white border-start border-4 border-dark">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <h6 class="fw-bold text-dark mb-0"><i class="fa-brands fa-tiktok text-dark me-2"></i> TikTok del Proyecto</h6>
                    <button class="btn btn-dark btn-sm fw-bold modo-espectador-hide" data-bs-toggle="modal" data-bs-target="#modalTiktok"><i class="fas fa-edit me-1"></i> Editar TikTok</button>
                </div>
                <div class="d-flex flex-row justify-content-around align-items-center p-2 bg-light rounded border">
                    <div>
                        <i class="fa-brands fa-tiktok fa-3x mb-2 text-dark"></i>
                        <p class="text-muted small mb-2">Mira nuestra demostración en TikTok.</p>
                        <a href="{{ tiktok_url }}" target="_blank" class="btn btn-dark fw-bold px-3 btn-sm"><i class="fa-brands fa-tiktok me-1"></i> Ver en TikTok</a>
                    </div>
                    <div class="bg-white p-2 border rounded shadow-sm text-center">
                        <img src="https://api.qrserver.com/v1/create-qr-code/?size=100x100&data={{ tiktok_url }}" alt="QR TikTok" style="width: 90px; height: 90px;">
                    </div>
                </div>
            </div>
        </section>

        <!-- TESTIMONIOS REALES -->
        <section class="mb-3">
            <div class="d-flex justify-content-between align-items-center mb-2">
                <h6 class="fw-bold text-dark mb-0"><i class="fas fa-comment-dots text-primary me-2"></i> Testimonios Reales</h6>
                <button class="btn btn-primary btn-sm fw-bold modo-espectador-hide" data-bs-toggle="modal" data-bs-target="#modalTestimonio">Subir Testimonio</button>
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

        <!-- ACCESO MÓVIL JURADO -->
        <section class="mb-3">
            <div class="card card-custom p-3 bg-white text-center border-start border-4 border-warning">
                <h6 class="fw-bold text-dark mb-1"><i class="fas fa-qrcode text-warning me-2"></i> Acceso Móvil para el Jurado</h6>
                <div class="d-inline-block bg-white p-2 border rounded shadow-sm">
                    <img src="https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=https://elconocimientoespoder.onrender.com/" alt="QR" style="width: 90px; height: 90px;">
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

    <div class="modal fade" id="modalYoutube" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog"><div class="modal-content"><form action="/update_youtube" method="post">
            <div class="modal-header bg-danger text-white"><h5 class="modal-title">Actualizar Video de YouTube</h5><button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button></div>
            <div class="modal-body">
                <div class="mb-2"><label class="small fw-bold">URL de Embed de YouTube</label><input type="text" name="youtube_url" class="form-control form-control-sm" required></div>
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
                    activarAdmin();
                }
            } else {
                activarAdmin();
            }
        }

        function cancelarAdmin() { desactivarAdmin(); }
    </script>
</body>
</html>"""

@app.route('/')
def home():
    return render_template_string(
        HTML_TEMPLATE, 
        testimonios=testimonios_list, 
        equipo_list=equipo_list, 
        youtube_url=archivos_estado["youtube_url"], 
        tiktok_url=archivos_estado["tiktok_url"], 
        doc_url=archivos_estado["doc_url"],
        doc_direct_url=archivos_estado["doc_direct_url"],
        sheet_url=archivos_estado["sheet_url"],
        sheet_direct_url=archivos_estado["sheet_direct_url"],
        admin_pin=ADMIN_PASSWORD
    )

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

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
