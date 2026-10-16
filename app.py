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
    "youtube_id": "dQw4w9WgXcQ",
    "tiktok_url": "https://www.tiktok.com/embed/7234567890123456789"
}

HTML_TEMPLATE = '''<!DOCTYPE html>
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
        .mode-bar { background-color: #0f172a; color: #cbd5e1; padding: 8px 0; font-size: 0.85rem; }
        .card-custom { border: none; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); position: relative; }
        .carousel-item-news { height: 350px; background-size: cover; background-position: center; border-radius: 12px; position: relative; }
        .carousel-overlay { position: absolute; bottom: 0; top: 0; left: 0; right: 0; background: linear-gradient(to top, rgba(15,23,42,0.95) 15%, rgba(15,23,42,0.4) 60%); border-radius: 12px; padding: 25px; display: flex; flex-direction: column; justify-content: flex-end; color: white; }
        .modo-espectador-hide { display: block; }
        body.espectador-active .modo-espectador-hide { display: none !important; }
        .btn-delete-card { position: absolute; top: 10px; right: 10px; z-index: 10; }
        .metric-card { background: white; border-radius: 12px; padding: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); text-align: center; border-top: 4px solid var(--accent); }
        footer { background-color: var(--primary); color: white; padding: 30px 0; margin-top: 50px; }
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
            <h1 class="display-5 fw-bold">Sistema de Remoción y Extracción de Barro en Viviendas</h1>
            <p class="lead mt-2 text-light opacity-90">Equipo ELCONOCIMIENTOESPODER — Sede UNER Concordia (Entre Ríos, Argentina)</p>
            <p class="badge bg-warning text-dark fs-6 mt-2">Desafío 06 — Rally Latinoamericano de Innovación 2026</p>
        </div>
    </header>
    <main class="container my-4">
        <section class="mb-4">
            <div class="card card-custom p-3 bg-white border-start border-4 border-danger">
                <div class="row align-items-center">
                    <div class="col-md-7">
                        <h4 class="fw-bold text-dark mb-2"><i class="fas fa-cloud-showers-heavy text-danger me-2"></i> Radar y Monitoreo Climático Regional</h4>
                        <p class="text-secondary small mb-2">Seguimiento en tiempo real de precipitaciones y crecida del Río Uruguay en Concordia.</p>
                    </div>
                    <div class="col-md-5">
                        <div class="ratio ratio-16x9 rounded overflow-hidden shadow-sm">
                            <iframe src="https://embed.windy.com/embed2.html?lat=-31.393&lon=-58.021&zoom=10&level=surface&overlay=rain&product=ecmwf&menu=&message=&marker=&calendar=now&pressure=&type=map&location=coordinates&detail=&metricWind=km%2Fh&metricTemp=%C2%B0C&radarRange=-1" frameborder="0"></iframe>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        <section class="mb-4">
            <div class="card card-custom p-3 bg-white border-start border-4 border-warning">
                <h4 class="fw-bold text-dark mb-2"><i class="fas fa-calculator text-warning me-2"></i> Simulador y Calculadora Comparativa</h4>
                <div class="row g-3 align-items-end">
                    <div class="col-md-4">
                        <label class="form-label small fw-bold text-dark">Superficie afectada (m²):</label>
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
            <div class="row g-3">
                <div class="col-md-4"><div class="metric-card"><h3 class="fw-bold text-primary">-65%</h3><p class="text-secondary small mb-0 fw-bold">Tiempo de limpieza</p></div></div>
                <div class="col-md-4"><div class="metric-card"><h3 class="fw-bold text-warning">$20 USD</h3><p class="text-secondary small mb-0 fw-bold">Costo de herramientas</p></div></div>
                <div class="col-md-4"><div class="metric-card"><h3 class="fw-bold text-success">100%</h3><p class="text-secondary small mb-0 fw-bold">Independencia eléctrica</p></div></div>
            </div>
        </section>
        <section class="mb-4">
            <div class="card card-custom p-3 bg-white text-center border-start border-4 border-primary">
                <h4 class="fw-bold text-dark mb-1"><i class="fas fa-qrcode text-primary me-2"></i> Acceso Móvil para el Jurado</h4>
                <div class="d-inline-block bg-white p-2 border rounded shadow-sm mt-2">
                    <img src="https://api.qrserver.com/v1/create-qr-code/?size=120x120&data=https://rally-extraccion-barro.onrender.com/" alt="QR" style="width: 100px; height: 100px;">
                </div>
            </div>
        </section>
        <section class="mb-4">
            <div class="d-flex justify-content-between align-items-center mb-2">
                <h4 class="fw-bold text-dark mb-0"><i class="fas fa-newspaper text-danger me-2"></i> Noticias & Alertas</h4>
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
                                <span class="badge bg-danger mb-2 align-self-start">{{ noti.pais }}</span>
                                <h5 class="fw-bold text-white">{{ noti.titulo }}</h5>
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
                <h4 class="fw-bold text-dark mb-0"><i class="fas fa-tools text-warning me-2"></i> Soluciones Propuestas</h4>
                <button class="btn btn-warning btn-sm fw-bold text-dark modo-espectador-hide" data-bs-toggle="modal" data-bs-target="#modalSolucion">Agregar</button>
            </div>
            <div class="row g-3">
                {% for sol in soluciones %}
                <div class="col-md-6">
                    <div class="card card-custom h-100 bg-white d-flex flex
