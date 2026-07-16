#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate NextThink's static interior pages with shared SEO structure."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://nextthink.es"
OG_IMAGE = f"{SITE}/assets/social/og-nextthink.jpg"


def head(title: str, description: str, path: str, schema: dict, robots: str = "index,follow,max-image-preview:large") -> str:
    url = f"{SITE}{path}"
    return f'''<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="robots" content="{robots}">
  <link rel="canonical" href="{url}">
  <meta name="theme-color" content="#faf8f4">
  <link rel="icon" href="/assets/icons/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/assets/icons/favicon-32.png" sizes="32x32" type="image/png">
  <link rel="apple-touch-icon" href="/assets/icons/apple-touch-icon.png">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="es_ES">
  <meta property="og:site_name" content="NextThink">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{OG_IMAGE}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="NextThink: software e IA a medida para operaciones B2B">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{description}">
  <meta name="twitter:image" content="{OG_IMAGE}">
  <meta name="twitter:image:alt" content="NextThink: software e IA a medida para operaciones B2B">
  <link rel="stylesheet" href="/assets/css/site.css">
  <script defer src="/assets/js/site.js"></script>
  <script type="application/ld+json">
{json.dumps(schema, ensure_ascii=False, indent=2)}
  </script>
</head>'''


def header(active: str) -> str:
    links = [
        ("servicios", "/servicios/", "Servicios"),
        ("casos", "/casos-de-exito/", "Casos"),
        ("nosotros", "/nosotros/", "Nosotros"),
        ("contacto", "/contacto/", "Contacto"),
    ]
    def nav_link(key: str, url: str, label: str, *, mobile: bool = False) -> str:
        current = ' aria-current="page"' if key == active else ''
        text = "Casos de éxito" if mobile and key == "casos" else label
        return f'<a href="{url}"{current}>{text}</a>'

    desktop = "\n        ".join(nav_link(key, url, label) for key, url, label in links)
    mobile = "\n      ".join(nav_link(key, url, label, mobile=True) for key, url, label in links)
    return f'''<a class="skip-link" href="#contenido">Saltar al contenido</a>
  <header class="site-header">
    <div class="wrap nav-shell">
      <a class="brand-link" href="/" aria-label="NextThink, inicio">
        <img src="/brand/wordmark-only.png" alt="NextThink" width="300" height="69">
      </a>
      <nav class="desktop-nav" aria-label="Navegación principal">
        {desktop}
      </nav>
      <a class="nav-cta" href="/contacto/">Cuéntanos tu problema <span aria-hidden="true">→</span></a>
      <button class="mobile-toggle" type="button" aria-expanded="false" aria-controls="mobile-menu" aria-label="Abrir menú">
        <span class="mobile-toggle-lines" aria-hidden="true"><span></span><span></span><span></span></span>
      </button>
    </div>
    <nav class="mobile-panel" id="mobile-menu" aria-label="Navegación móvil">
      {mobile}
      <a class="button" href="/contacto/">Cuéntanos tu problema</a>
    </nav>
  </header>'''


def footer() -> str:
    return '''<footer class="site-footer">
    <div class="wrap">
      <div class="footer-grid">
        <div class="footer-brand">
          <img src="/brand/wordmark-only.png" alt="NextThink" width="300" height="69" loading="lazy" decoding="async">
          <p>Software e inteligencia artificial a medida para convertir problemas operativos B2B en sistemas que funcionan.</p>
        </div>
        <nav class="footer-col" aria-label="Servicios del pie">
          <h2>Servicios</h2>
          <ul><li><a href="/servicios/software-a-medida/">Software a medida</a></li><li><a href="/servicios/inteligencia-artificial/">IA aplicada</a></li><li><a href="/servicios/auditoria-tecnica/">Auditoría técnica</a></li></ul>
        </nav>
        <nav class="footer-col" aria-label="Empresa del pie">
          <h2>Empresa</h2>
          <ul><li><a href="/nosotros/">Nosotros</a></li><li><a href="/casos-de-exito/">Casos de éxito</a></li><li><a href="/contacto/">Contacto</a></li></ul>
        </nav>
        <nav class="footer-col" aria-label="Contacto del pie">
          <h2>Contacto</h2>
          <ul><li><a href="mailto:info@nextthink.es">info@nextthink.es</a></li><li><a href="https://wa.me/34684011183" rel="noopener">WhatsApp</a></li><li><a href="https://www.linkedin.com/company/nextthink-sl/" rel="noopener">LinkedIn</a></li></ul>
        </nav>
      </div>
      <div class="footer-bottom">
        <span>© <span data-current-year>2026</span> NEXTTHINK GLOBAL SL</span>
        <nav class="footer-legal" aria-label="Información legal"><a href="/aviso-legal/">Aviso legal</a><a href="/privacidad/">Privacidad</a><a href="/politica-de-cookies/">Cookies</a></nav>
      </div>
    </div>
  </footer>'''


def breadcrumbs(items: list[tuple[str, str | None]]) -> str:
    def crumb(label: str, url: str | None) -> str:
        value = f'<a href="{url}">{label}</a>' if url else label
        return f'<li>{value}</li>'

    lis = "".join(crumb(label, url) for label, url in items)
    return f'<nav class="breadcrumbs" aria-label="Migas de pan"><ol>{lis}</ol></nav>'


def cta() -> str:
    return '''<section class="cta-section" aria-labelledby="cta-title">
      <div class="wrap">
        <h2 id="cta-title"><span class="display-serif">Cuéntanos</span> el cuello de botella.</h2>
        <p>En una primera conversación de 30 minutos entendemos el problema y te decimos con claridad si podemos ayudar.</p>
        <div class="cta-actions">
          <a class="button" href="/contacto/">Preparar la conversación <span aria-hidden="true">→</span></a>
          <a class="button button-secondary" href="mailto:info@nextthink.es">info@nextthink.es</a>
        </div>
      </div>
    </section>'''


def faq(items: list[tuple[str, str]], title: str = "Preguntas frecuentes") -> str:
    rows = "\n".join(
        f'''<details class="faq-item"><summary>{question}</summary><div class="faq-answer"><p>{answer}</p></div></details>'''
        for question, answer in items
    )
    return f'''<section class="section" aria-labelledby="faq-title">
      <div class="wrap split">
        <div class="split-aside"><p class="eyebrow">Decisiones</p><h2 id="faq-title">{title}</h2></div>
        <div class="faq-list">{rows}</div>
      </div>
    </section>'''


def schema_graph(path: str, title: str, description: str, page_type: str, crumbs: list[tuple[str, str]], extras: list[dict] | None = None) -> dict:
    url = f"{SITE}{path}"
    nodes: list[dict] = [
        {
            "@type": "Organization",
            "@id": f"{SITE}/#organization",
            "name": "NextThink",
            "legalName": "NEXTTHINK GLOBAL SL",
            "taxID": "B24782468",
            "url": f"{SITE}/",
            "email": "info@nextthink.es",
            "telephone": "+34684011183",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "C/ Centuria Romana, 8",
                "postalCode": "30600",
                "addressLocality": "Archena",
                "addressRegion": "Murcia",
                "addressCountry": "ES",
            },
            "sameAs": ["https://www.linkedin.com/company/nextthink-sl/"],
            "areaServed": {"@type": "Country", "name": "España"},
        },
        {
            "@type": page_type,
            "@id": f"{url}#webpage",
            "url": url,
            "name": title,
            "description": description,
            "inLanguage": "es",
            "about": {"@id": f"{SITE}/#organization"},
        },
        {
            "@type": "BreadcrumbList",
            "@id": f"{url}#breadcrumb",
            "itemListElement": [
                {"@type": "ListItem", "position": i, "name": label, "item": f"{SITE}{item_path}"}
                for i, (label, item_path) in enumerate(crumbs, 1)
            ],
        },
    ]
    if extras:
        nodes.extend(extras)
    return {"@context": "https://schema.org", "@graph": nodes}


def faq_schema(path: str, items: list[tuple[str, str]]) -> dict:
    return {
        "@type": "FAQPage",
        "@id": f"{SITE}{path}#faq",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in items
        ],
    }


def render(path: str, title: str, description: str, active: str, body: str, schema: dict, robots: str = "index,follow,max-image-preview:large") -> None:
    target = ROOT / path.strip("/") / "index.html" if path != "/" else ROOT / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    document = f'''<!doctype html>
<html lang="es">
{head(title, description, path, schema, robots)}
<body>
  {header(active)}
  <main id="contenido">
{body}
  </main>
  {footer()}
</body>
</html>
'''
    target.write_text(document, encoding="utf-8")
    print(target.relative_to(ROOT))


# Services hub
path = "/servicios/"
title = "Servicios de software e IA a medida | NextThink"
description = "Software a medida, inteligencia artificial aplicada y auditoría técnica para automatizar operaciones B2B en empresas de toda España."
crumb_data = [("Inicio", "/"), ("Servicios", path)]
body = f'''    <section class="page-hero">
      <div class="wrap">
        {breadcrumbs([("Inicio", "/"), ("Servicios", None)])}
        <p class="eyebrow">Servicios para operaciones B2B</p>
        <h1>La solución empieza por <span class="display-serif">el problema correcto.</span></h1>
        <p class="page-hero-lead">Combinamos diagnóstico, desarrollo de software e inteligencia artificial para transformar procesos manuales o frágiles en sistemas operables.</p>
      </div>
    </section>
    <section class="section" aria-labelledby="servicios-lista">
      <div class="wrap">
        <div class="section-head"><div><p class="eyebrow">Capacidades</p><h2 class="section-title" id="servicios-lista">Tres puntos de entrada, <span class="display-serif">un mismo criterio.</span></h2></div><p class="section-intro">Construir solo lo necesario, medir lo importante y dejar la solución preparada para operar.</p></div>
        <div class="card-grid">
          <article class="card"><span class="card-index">01 / CONSTRUIR</span><h3>Desarrollo de software a medida</h3><p>Aplicaciones internas, backend, APIs e integraciones que encajan con la operación existente.</p><a class="text-link" href="/servicios/software-a-medida/">Explorar el servicio <span aria-hidden="true">→</span></a></article>
          <article class="card"><span class="card-index">02 / AUTOMATIZAR</span><h3>Inteligencia artificial aplicada</h3><p>IA integrada en procesos concretos, con evaluación, control humano y seguimiento desde producción.</p><a class="text-link" href="/servicios/inteligencia-artificial/">Explorar el servicio <span aria-hidden="true">→</span></a></article>
          <article class="card"><span class="card-index">03 / DECIDIR</span><h3>Diagnóstico y auditoría técnica</h3><p>Una revisión independiente para comprender riesgos, prioridades y opciones antes de invertir en construcción.</p><a class="text-link" href="/servicios/auditoria-tecnica/">Explorar el servicio <span aria-hidden="true">→</span></a></article>
        </div>
      </div>
    </section>
    <section class="section section-dark" aria-labelledby="criterios-title"><div class="wrap"><div class="section-head"><div><p class="eyebrow eyebrow-light">Cómo elegimos</p><h2 class="section-title" id="criterios-title">Tecnología subordinada a <span class="display-serif">la operación.</span></h2></div><p class="section-intro">No empezamos por una herramienta. Empezamos por el flujo, las personas, los datos disponibles y la decisión que debe mejorar.</p></div><div class="feature-grid"><article class="feature"><h3>Valor observable</h3><p>Definimos qué debe cambiar y cómo se comprobará antes de ampliar el alcance.</p></article><article class="feature"><h3>Riesgo explícito</h3><p>Priorizamos integraciones, datos y dependencias que pueden alterar coste o viabilidad.</p></article><article class="feature"><h3>Producción desde el diseño</h3><p>Despliegue, observabilidad y operación forman parte de la solución, no de una fase posterior.</p></article><article class="feature"><h3>Autonomía del equipo</h3><p>Documentación, traspaso y decisiones comprensibles para evitar dependencias ocultas.</p></article></div></div></section>
    {cta()}'''
schema = schema_graph(path, title, description, "CollectionPage", crumb_data)
render(path, title, description, "servicios", body, schema)

# Software service
path = "/servicios/software-a-medida/"
title = "Desarrollo de software a medida para empresas | NextThink"
description = "Diseñamos backend, plataformas internas, APIs e integraciones a medida para automatizar operaciones B2B y llevarlas a producción."
faqs = [
    ("¿Qué tipo de software desarrolla NextThink?", "Construimos principalmente sistemas internos, backend, APIs, integraciones y aplicaciones que soportan procesos operativos concretos. El alcance se define después de entender el flujo y los sistemas existentes."),
    ("¿Podéis integrar la solución con nuestro software actual?", "Sí, cuando las herramientas existentes ofrecen mecanismos de integración adecuados. La auditoría inicial identifica APIs, datos, permisos y dependencias antes de comprometer el diseño."),
    ("¿Quién es propietario del código y la documentación?", "La propiedad y las condiciones de entrega se acuerdan expresamente en cada propuesta. Nuestro objetivo operativo es que el cliente pueda entender, mantener y evolucionar el sistema sin dependencias ocultas."),
    ("¿Qué ocurre después del despliegue?", "El cierre incluye documentación, traspaso y criterios de operación. El acompañamiento posterior depende de las necesidades y se define antes de comenzar."),
]
crumb_data = [("Inicio", "/"), ("Servicios", "/servicios/"), ("Software a medida", path)]
service = {"@type": "Service", "@id": f"{SITE}{path}#service", "name": "Desarrollo de software a medida", "serviceType": "Desarrollo de software a medida", "provider": {"@id": f"{SITE}/#organization"}, "areaServed": {"@type": "Country", "name": "España"}}
body = f'''    <section class="page-hero"><div class="wrap">{breadcrumbs([("Inicio", "/"), ("Servicios", "/servicios/"), ("Software a medida", None)])}<p class="eyebrow">Desarrollo de software a medida</p><h1>Sistemas construidos alrededor de <span class="display-serif">tu operación real.</span></h1><p class="page-hero-lead">Creamos software para procesos que ya no caben en hojas de cálculo, tareas manuales o herramientas desconectadas.</p><div class="page-hero-actions"><a class="button" href="/contacto/">Evaluar un proyecto <span aria-hidden="true">→</span></a><a class="button button-secondary" href="/casos-de-exito/">Ver casos</a></div></div></section>
    <section class="section"><div class="wrap split"><div class="split-aside"><p class="eyebrow">Cuándo encaja</p><h2>Cuando adaptar la operación cuesta más que construir bien.</h2></div><div class="prose"><p>El software a medida tiene sentido cuando un proceso crítico depende de tareas repetitivas, transferencias manuales o sistemas que no comparten información.</p><h3>Situaciones habituales</h3><ul><li>Plataformas internas para centralizar decisiones y trabajo operativo.</li><li>APIs e integraciones entre ERP, CRM, proveedores o herramientas propias.</li><li>Backend para procesos con reglas de negocio específicas.</li><li>Sustitución gradual de hojas de cálculo o aplicaciones frágiles.</li><li>Automatización de documentos, presupuestos y flujos de aprobación.</li></ul><blockquote>No añadimos software a un proceso sin entender primero qué decisión debe mejorar.</blockquote></div></div></section>
    <section class="section section-dark" aria-labelledby="entregables-title"><div class="wrap"><div class="section-head"><div><p class="eyebrow eyebrow-light">Alcance</p><h2 class="section-title" id="entregables-title">De la arquitectura al <span class="display-serif">traspaso.</span></h2></div><p class="section-intro">Cada proyecto define sus entregables, pero estos elementos forman parte del criterio de construcción.</p></div><div class="feature-grid"><article class="feature"><h3>Diseño técnico defendible</h3><p>Arquitectura, integraciones y decisiones registradas para comprender por qué el sistema funciona así.</p></article><article class="feature"><h3>Implementación operable</h3><p>Aplicación, backend o integración preparada para su entorno real de producción.</p></article><article class="feature"><h3>Observabilidad</h3><p>Señales suficientes para detectar fallos y comprender el comportamiento del sistema.</p></article><article class="feature"><h3>Documentación y autonomía</h3><p>Traspaso técnico y operativo para que el equipo no dependa de conocimiento implícito.</p></article></div></div></section>
    {faq(faqs)}
    {cta()}'''
schema = schema_graph(path, title, description, "WebPage", crumb_data, [service, faq_schema(path, faqs)])
render(path, title, description, "servicios", body, schema)

# AI service
path = "/servicios/inteligencia-artificial/"
title = "Inteligencia artificial aplicada a empresas | NextThink"
description = "Integramos IA en procesos B2B con evaluación, control humano y métricas de negocio: automatización, clasificación, agentes y búsqueda."
faqs = [
    ("¿Cómo sabéis si un proceso necesita inteligencia artificial?", "Comparamos la IA con alternativas deterministas y manuales. Solo la proponemos cuando los datos, la variabilidad del problema y el impacto esperado justifican su coste y riesgo."),
    ("¿Cómo se evalúa un sistema de IA?", "Definimos ejemplos representativos, criterios de calidad y umbrales antes de producción. Después monitorizamos errores, coste y comportamiento sobre casos reales."),
    ("¿Puede existir revisión humana?", "Sí. Cuando el impacto de un error lo requiere, diseñamos aprobación, escalado o muestreo humano dentro del flujo, no como una corrección improvisada."),
    ("¿Qué ocurre con los datos de la empresa?", "El tratamiento depende de la arquitectura y proveedores elegidos. Antes de construir se revisan sensibilidad, permisos, retención y opciones de aislamiento para tomar una decisión explícita."),
]
crumb_data = [("Inicio", "/"), ("Servicios", "/servicios/"), ("Inteligencia artificial", path)]
service = {"@type": "Service", "@id": f"{SITE}{path}#service", "name": "Inteligencia artificial aplicada a empresas", "serviceType": "Consultoría e implementación de inteligencia artificial", "provider": {"@id": f"{SITE}/#organization"}, "areaServed": {"@type": "Country", "name": "España"}}
body = f'''    <section class="page-hero"><div class="wrap">{breadcrumbs([("Inicio", "/"), ("Servicios", "/servicios/"), ("Inteligencia artificial", None)])}<p class="eyebrow">Inteligencia artificial aplicada</p><h1>IA integrada en un proceso, no <span class="display-serif">una demo aislada.</span></h1><p class="page-hero-lead">Identificamos dónde la IA aporta valor, diseñamos cómo medirla y la conectamos con el trabajo diario hasta dejarla operando.</p><div class="page-hero-actions"><a class="button" href="/contacto/">Evaluar un caso de uso <span aria-hidden="true">→</span></a><a class="button button-secondary" href="/servicios/auditoria-tecnica/">Empezar por un diagnóstico</a></div></div></section>
    <section class="section"><div class="wrap split"><div class="split-aside"><p class="eyebrow">Aplicaciones</p><h2>Automatizar donde existe una decisión repetible.</h2></div><div class="prose"><p>La IA puede reducir trabajo manual o hacer accesible información dispersa, pero también introduce incertidumbre. Por eso el caso de uso, la evaluación y el control importan tanto como el modelo.</p><h3>Problemas que solemos explorar</h3><ul><li>Clasificación y extracción de información en documentos.</li><li>Búsqueda y respuestas sobre conocimiento interno con fuentes.</li><li>Asistentes para preparar trabajo, no para ocultar decisiones.</li><li>Automatización de tareas con herramientas y reglas de aprobación.</li><li>Priorización de casos para revisión por parte del equipo.</li></ul><h3>Cuándo no utilizar IA</h3><p>Si una regla clara, una integración o un cambio de proceso resuelve mejor el problema, esa alternativa debe prevalecer. La complejidad solo se justifica cuando mejora el resultado.</p></div></div></section>
    <section class="section section-dark" aria-labelledby="ia-control-title"><div class="wrap"><div class="section-head"><div><p class="eyebrow eyebrow-light">Producción responsable</p><h2 class="section-title" id="ia-control-title">Evaluar antes de <span class="display-serif">confiar.</span></h2></div><p class="section-intro">Una solución útil necesita límites, trazabilidad y un comportamiento observable.</p></div><div class="feature-grid"><article class="feature"><h3>Conjunto de evaluación</h3><p>Ejemplos reales y criterios claros para comparar cambios y detectar regresiones.</p></article><article class="feature"><h3>Guardarraíles</h3><p>Validaciones, permisos y límites adaptados al impacto de una respuesta incorrecta.</p></article><article class="feature"><h3>Control humano</h3><p>Aprobación o escalado cuando una decisión requiere contexto o responsabilidad.</p></article><article class="feature"><h3>Coste y observabilidad</h3><p>Seguimiento del uso, errores y coste para decidir con datos una vez desplegado.</p></article></div></div></section>
    {faq(faqs)}
    {cta()}'''
schema = schema_graph(path, title, description, "WebPage", crumb_data, [service, faq_schema(path, faqs)])
render(path, title, description, "servicios", body, schema)

# Audit service
path = "/servicios/auditoria-tecnica/"
title = "Auditoría técnica y diagnóstico de software | NextThink"
description = "Auditamos procesos, datos y arquitectura para priorizar riesgos y definir un roadmap técnico antes de invertir en software o inteligencia artificial."
faqs = [
    ("¿Cuánto dura el diagnóstico?", "El formato inicial planteado por NextThink dura dos semanas y tiene precio fijo. El alcance concreto se confirma antes de comenzar según los procesos, sistemas y personas implicadas."),
    ("¿Qué recibe el equipo al terminar?", "Un mapa del problema, riesgos priorizados, opciones de solución y un roadmap defendible. Los entregables exactos se acuerdan al cerrar el alcance."),
    ("¿Es obligatorio construir después con NextThink?", "No. El diagnóstico debe permitir tomar una decisión informada incluso si la implementación la realiza el equipo interno u otro proveedor."),
    ("¿Se puede auditar un sistema ya existente?", "Sí. La revisión puede centrarse en arquitectura, integraciones, operación, deuda técnica o la viabilidad de incorporar automatización e IA."),
]
crumb_data = [("Inicio", "/"), ("Servicios", "/servicios/"), ("Auditoría técnica", path)]
service = {"@type": "Service", "@id": f"{SITE}{path}#service", "name": "Auditoría técnica y diagnóstico de software", "serviceType": "Auditoría técnica de software y procesos", "provider": {"@id": f"{SITE}/#organization"}, "areaServed": {"@type": "Country", "name": "España"}}
body = f'''    <section class="page-hero"><div class="wrap">{breadcrumbs([("Inicio", "/"), ("Servicios", "/servicios/"), ("Auditoría técnica", None)])}<p class="eyebrow">Diagnóstico y auditoría técnica</p><h1>Entender el riesgo antes de <span class="display-serif">escribir código.</span></h1><p class="page-hero-lead">Dos semanas para comprender el proceso, revisar datos y tecnología y salir con un plan priorizado. Precio fijo y sin obligación de continuar.</p><div class="page-hero-actions"><a class="button" href="/contacto/">Plantear un diagnóstico <span aria-hidden="true">→</span></a></div></div></section>
    <section class="section"><div class="wrap split"><div class="split-aside"><p class="eyebrow">Objetivo</p><h2>Reducir incertidumbre antes de comprometer inversión.</h2></div><div class="prose"><p>Un proyecto puede fallar por una integración inexistente, datos insuficientes o una comprensión incompleta del trabajo real. El diagnóstico busca esas restricciones antes de que sean costosas.</p><h3>Qué revisamos</h3><ul><li>Flujo operativo, participantes y decisiones críticas.</li><li>Sistemas, integraciones y fuentes de datos disponibles.</li><li>Riesgos técnicos, organizativos y de adopción.</li><li>Alternativas de solución, incluida la opción de no construir.</li><li>Secuencia recomendada y dependencias del roadmap.</li></ul><blockquote>El resultado no es un informe que pide otro informe, sino una base para decidir y ejecutar.</blockquote></div></div></section>
    <section class="section section-dark" aria-labelledby="salida-title"><div class="wrap"><div class="section-head"><div><p class="eyebrow eyebrow-light">Salida</p><h2 class="section-title" id="salida-title">Una decisión <span class="display-serif">defendible.</span></h2></div><p class="section-intro">El equipo debe poder explicar qué problema aborda, qué riesgos acepta y cuál es el siguiente paso.</p></div><div class="feature-grid"><article class="feature"><h3>Mapa del problema</h3><p>Proceso, actores, datos y restricciones expresados de forma compartida.</p></article><article class="feature"><h3>Riesgos priorizados</h3><p>Bloqueos y dudas ordenados por impacto sobre viabilidad y coste.</p></article><article class="feature"><h3>Opciones de solución</h3><p>Alternativas comparables sin asumir que una tecnología es obligatoria.</p></article><article class="feature"><h3>Roadmap</h3><p>Secuencia de trabajo con dependencias y criterios para validar cada etapa.</p></article></div></div></section>
    {faq(faqs)}
    {cta()}'''
schema = schema_graph(path, title, description, "WebPage", crumb_data, [service, faq_schema(path, faqs)])
render(path, title, description, "servicios", body, schema)

# Cases hub
path = "/casos-de-exito/"
title = "Casos de éxito de software e IA a medida | NextThink"
description = "Proyectos de software e inteligencia artificial aplicados a problemas operativos reales, desde el diagnóstico hasta un sistema en producción."
crumb_data = [("Inicio", "/"), ("Casos de éxito", path)]
body = f'''    <section class="page-hero"><div class="wrap">{breadcrumbs([("Inicio", "/"), ("Casos de éxito", None)])}<p class="eyebrow">Trabajo en producción</p><h1>Problemas concretos. <span class="display-serif">Sistemas verificables.</span></h1><p class="page-hero-lead">Documentamos el contexto, las decisiones y el resultado sin convertir métricas agregadas en promesas universales.</p></div></section>
    <section class="section" aria-labelledby="casos-title"><div class="wrap"><div class="section-head"><div><p class="eyebrow">Caso publicado</p><h2 class="section-title" id="casos-title">Automatizar sin obligar a la operación a <span class="display-serif">empezar de cero.</span></h2></div><p class="section-intro">Tamevi necesitaba convertir un presupuesto de carpintería de aluminio en una hoja de corte utilizando su propia plantilla de trabajo.</p></div><article class="card" style="max-width:760px"><span class="card-index">TAMEVI SL · SOFTWARE A MEDIDA</span><h3>Automatización de presupuestos y hojas de corte</h3><p>Un sistema construido alrededor de un flujo concreto y de la plantilla que el equipo ya utilizaba.</p><a class="text-link" href="/casos-de-exito/tamevi-automatizacion-presupuestos/">Leer el caso completo <span aria-hidden="true">→</span></a></article></div></section>
    <section class="section section-dark"><div class="wrap case-feature"><div><p class="case-label" style="color:rgba(255,255,255,.6)">Criterio de publicación</p></div><blockquote>Publicamos resultados cuando podemos explicar <span class="display-serif">qué se resolvió</span> sin inventar cifras, plazos o tecnologías que el caso no acredita.</blockquote></div></section>
    {cta()}'''
schema = schema_graph(path, title, description, "CollectionPage", crumb_data)
render(path, title, description, "casos", body, schema)

# Tamevi case
path = "/casos-de-exito/tamevi-automatizacion-presupuestos/"
title = "Automatización de presupuestos para Tamevi | NextThink"
description = "Caso de software a medida: un sistema para presupuestar carpintería de aluminio y generar hojas de corte desde la plantilla de Tamevi."
crumb_data = [("Inicio", "/"), ("Casos de éxito", "/casos-de-exito/"), ("Tamevi", path)]
article = {"@type": "Article", "@id": f"{SITE}{path}#article", "headline": "Automatización de presupuestos y hojas de corte para Tamevi", "description": description, "inLanguage": "es", "author": {"@id": f"{SITE}/#organization"}, "publisher": {"@id": f"{SITE}/#organization"}, "mainEntityOfPage": {"@id": f"{SITE}{path}#webpage"}}
body = f'''    <article>
      <header class="page-hero"><div class="wrap">{breadcrumbs([("Inicio", "/"), ("Casos de éxito", "/casos-de-exito/"), ("Tamevi", None)])}<p class="eyebrow">Caso de éxito · Tamevi SL</p><h1>Del presupuesto de aluminio a <span class="display-serif">la hoja de corte.</span></h1><p class="page-hero-lead">Un sistema de software a medida para resolver un flujo concreto desde la plantilla que Tamevi ya utilizaba.</p></div></header>
      <section class="section"><div class="wrap split"><div class="split-aside"><p class="eyebrow">El reto</p><h2>Presupuestar y preparar el trabajo sin separar ambos procesos.</h2></div><div class="prose"><p>Tamevi SL planteó un problema preciso: presupuestar trabajos de carpintería de aluminio y obtener su correspondiente hoja de corte.</p><p>La solución debía encajar con una forma de trabajo existente y partir de la propia plantilla del cliente, en lugar de obligar al equipo a adoptar un flujo genérico.</p><h3>El enfoque</h3><p>NextThink tradujo ese proceso en un sistema que utiliza la plantilla de Tamevi como punto de partida y conecta el presupuesto con la información necesaria para la hoja de corte.</p><p>El caso demuestra el criterio central del software a medida: adaptar la tecnología al problema operativo real cuando las herramientas genéricas no representan el flujo.</p></div></div></section>
      <section class="section section-dark"><div class="wrap case-feature"><div><p class="case-label" style="color:rgba(255,255,255,.6)">Testimonio</p></div><div><blockquote>“Les llevamos un problema muy concreto —presupuestar carpintería de aluminio con su hoja de corte— y NextThink no nos vendió una promesa: montaron un <span class="display-serif">sistema</span> que lo resuelve desde nuestra propia plantilla.”</blockquote><p class="case-attribution" style="color:rgba(255,255,255,.6)">José María Rodríguez · CEO de Tamevi SL</p></div></div></section>
      <section class="section"><div class="wrap split"><div class="split-aside"><p class="eyebrow">Resultado</p><h2>Un flujo resuelto dentro del contexto del cliente.</h2></div><div class="prose"><p>El resultado publicado es cualitativo: Tamevi dispone de un sistema que resuelve el problema desde su propia plantilla.</p><p>No atribuimos a este caso las métricas agregadas de otros proyectos ni publicamos cifras, plazos o tecnologías que no estén acreditados por la información autorizada.</p><p><a class="text-link" href="/servicios/software-a-medida/">Cómo abordamos el software a medida <span aria-hidden="true">→</span></a></p></div></div></section>
    </article>
    {cta()}'''
schema = schema_graph(path, title, description, "WebPage", crumb_data, [article])
render(path, title, description, "casos", body, schema)

# About
path = "/nosotros/"
title = "NextThink: software e IA para operaciones B2B"
description = "Conoce el método y los principios de NextThink para diseñar, construir y transferir sistemas de software e IA a empresas de toda España."
crumb_data = [("Inicio", "/"), ("Nosotros", path)]
body = f'''    <section class="page-hero"><div class="wrap">{breadcrumbs([("Inicio", "/"), ("Nosotros", None)])}<p class="eyebrow">Sobre NextThink</p><h1>La tecnología es útil cuando el equipo puede <span class="display-serif">operarla y defenderla.</span></h1><p class="page-hero-lead">Ayudamos a empresas de toda España a convertir problemas operativos en software e inteligencia artificial que funcionan en producción.</p></div></section>
    <section class="section"><div class="wrap split"><div class="split-aside"><p class="eyebrow">Nuestra forma de trabajar</p><h2>Comprender, construir y transferir.</h2></div><div class="prose"><p>NextThink trabaja con equipos B2B que necesitan automatizar un proceso, conectar sistemas o decidir si la inteligencia artificial puede aportar valor real.</p><p>El proyecto no termina al entregar código. Incluye las decisiones, controles y conocimiento necesarios para que la solución pueda operar fuera del contexto de quien la construyó.</p><h3>El problema antes que la herramienta</h3><p>No partimos de una tecnología predeterminada. Revisamos el flujo, los datos, las restricciones y el impacto de un error antes de elegir cómo resolverlo.</p><h3>Producción como requisito</h3><p>Despliegue, observabilidad, documentación y traspaso se consideran durante el diseño, no cuando el prototipo ya está terminado.</p></div></div></section>
    <section class="section section-dark" aria-labelledby="principios-title"><div class="wrap"><div class="section-head"><div><p class="eyebrow eyebrow-light">Principios</p><h2 class="section-title" id="principios-title">Menos promesas. <span class="display-serif">Más decisiones explícitas.</span></h2></div></div><div class="feature-grid"><article class="feature"><h3>Claridad</h3><p>Explicar riesgos, alternativas y límites de forma comprensible antes de comprometer el alcance.</p></article><article class="feature"><h3>Medición</h3><p>Definir qué cambio indicará que la solución está resolviendo el problema.</p></article><article class="feature"><h3>Responsabilidad</h3><p>No ocultar incertidumbre detrás de una interfaz o de una afirmación sobre IA.</p></article><article class="feature"><h3>Autonomía</h3><p>Dejar documentación y contexto suficientes para que el cliente pueda tomar el control.</p></article></div></div></section>
    {cta()}'''
schema = schema_graph(path, title, description, "AboutPage", crumb_data)
render(path, title, description, "nosotros", body, schema)

# Contact
path = "/contacto/"
title = "Contacto para proyectos de software e IA | NextThink"
description = "Cuéntanos el problema operativo que quieres resolver. Primera conversación de 30 minutos por email o WhatsApp, sin compromiso."
crumb_data = [("Inicio", "/"), ("Contacto", path)]
body = f'''    <section class="page-hero"><div class="wrap">{breadcrumbs([("Inicio", "/"), ("Contacto", None)])}<p class="eyebrow">Primera conversación</p><h1>Cuéntanos el problema, no <span class="display-serif">la solución prefabricada.</span></h1><p class="page-hero-lead">En 30 minutos revisamos el contexto, el impacto y las restricciones principales. Si no somos el equipo adecuado, también te lo diremos.</p></div></section>
    <section class="section" aria-labelledby="canales-title"><div class="wrap"><div class="section-head"><div><p class="eyebrow">Contacto directo</p><h2 class="section-title" id="canales-title">Elige el canal <span class="display-serif">más cómodo.</span></h2></div><p class="section-intro">Trabajamos con empresas de toda España. No necesitas preparar un documento formal para la primera conversación.</p></div><div class="contact-grid"><article class="contact-card"><span class="contact-card-label">Email</span><h3>info@nextthink.es</h3><p>Útil si quieres compartir contexto, sistemas implicados o documentación inicial.</p><a class="text-link" href="mailto:info@nextthink.es?subject=Proyecto%20de%20software%20o%20IA">Escribir un email <span aria-hidden="true">→</span></a></article><article class="contact-card"><span class="contact-card-label">WhatsApp</span><h3>684 011 183</h3><p>Para abrir la conversación y acordar cuándo revisar el problema con calma.</p><a class="text-link" href="https://wa.me/34684011183" rel="noopener">Abrir WhatsApp <span aria-hidden="true">→</span></a></article></div></div></section>
    <section class="section section-dark" aria-labelledby="preparar-title"><div class="wrap split"><div class="split-aside"><p class="eyebrow eyebrow-light">Para aprovechar la llamada</p><h2 id="preparar-title">Cuatro datos son suficientes para empezar.</h2></div><div class="prose"><ol><li>Qué proceso o decisión genera el problema.</li><li>Quién participa actualmente y qué herramientas utiliza.</li><li>Qué ocurre cuando el proceso falla o se retrasa.</li><li>Qué tendría que cambiar para considerar útil una solución.</li></ol><p>No hace falta definir tecnología, arquitectura ni modelo de IA antes de hablar.</p></div></div></section>'''
schema = schema_graph(path, title, description, "ContactPage", crumb_data)
render(path, title, description, "contacto", body, schema)

# Legal notice
path = "/aviso-legal/"
title = "Aviso legal corporativo | NextThink"
description = "Información identificativa y condiciones generales de uso del sitio web de NEXTTHINK GLOBAL SL, titular de nextthink.es."
crumb_data = [("Inicio", "/"), ("Aviso legal", path)]
body = f'''    <section class="page-hero"><div class="wrap">{breadcrumbs([("Inicio", "/"), ("Aviso legal", None)])}<p class="eyebrow">Información legal</p><h1>Aviso legal</h1><p class="page-hero-lead">Datos del titular y condiciones generales de uso de nextthink.es.</p></div></section>
    <section class="section"><div class="wrap split"><div class="split-aside"><p class="eyebrow">Titular</p><h2>NEXTTHINK GLOBAL SL</h2></div><div class="prose"><h2>Datos identificativos</h2><ul><li><strong>Titular:</strong> NEXTTHINK GLOBAL SL</li><li><strong>NIF:</strong> B24782468</li><li><strong>Domicilio:</strong> C/ Centuria Romana, 8, 30600 Archena, Murcia, España</li><li><strong>Correo electrónico:</strong> <a href="mailto:info@nextthink.es">info@nextthink.es</a></li><li><strong>Sitio web:</strong> https://nextthink.es</li></ul><h2>Objeto del sitio</h2><p>Este sitio presenta los servicios de consultoría, desarrollo de software e inteligencia artificial de NEXTTHINK GLOBAL SL y facilita canales de contacto para solicitar información o plantear un proyecto.</p><h2>Condiciones de uso</h2><p>El acceso al sitio implica utilizarlo de forma lícita y respetuosa. La información publicada tiene carácter general y no constituye por sí sola una oferta contractual. El alcance, condiciones y responsabilidades de cada proyecto se establecerán en su propuesta o contrato correspondiente.</p><h2>Propiedad intelectual</h2><p>Los textos, diseño, identidad visual, código y demás contenidos propios del sitio pertenecen a NEXTTHINK GLOBAL SL o se utilizan con autorización. No pueden reproducirse, distribuirse o transformarse fuera de los límites permitidos por la ley sin autorización previa.</p><h2>Enlaces externos</h2><p>El sitio puede enlazar a servicios de terceros, como LinkedIn o WhatsApp. NEXTTHINK GLOBAL SL no controla sus contenidos, disponibilidad ni políticas. El acceso a esos servicios queda sujeto a las condiciones del proveedor correspondiente.</p><h2>Responsabilidad</h2><p>Se trabaja para mantener la información y disponibilidad del sitio, pero no se garantiza la ausencia absoluta de errores o interrupciones. Si detectas información incorrecta, puedes comunicarlo a <a href="mailto:info@nextthink.es">info@nextthink.es</a>.</p><h2>Legislación aplicable</h2><p>Estas condiciones se rigen por la legislación española. Cualquier controversia se resolverá conforme a las normas sobre jurisdicción y competencia que resulten aplicables.</p></div></div></section>'''
schema = schema_graph(path, title, description, "WebPage", crumb_data)
render(path, title, description, "", body, schema, "noindex,follow")

# Privacy policy
path = "/privacidad/"
title = "Política de privacidad | NextThink"
description = "Información sobre cómo NEXTTHINK GLOBAL SL trata los datos recibidos por email, WhatsApp y durante las relaciones comerciales."
crumb_data = [("Inicio", "/"), ("Privacidad", path)]
body = f'''    <section class="page-hero"><div class="wrap">{breadcrumbs([("Inicio", "/"), ("Privacidad", None)])}<p class="eyebrow">Protección de datos</p><h1>Política de privacidad</h1><p class="page-hero-lead">Cómo tratamos los datos cuando contactas con NextThink o mantienes una relación profesional con nosotros.</p></div></section>
    <section class="section"><div class="wrap split"><div class="split-aside"><p class="eyebrow">Responsable</p><h2>Información clara sobre tus datos.</h2></div><div class="prose"><h2>Responsable del tratamiento</h2><ul><li><strong>Responsable:</strong> NEXTTHINK GLOBAL SL</li><li><strong>NIF:</strong> B24782468</li><li><strong>Domicilio:</strong> C/ Centuria Romana, 8, 30600 Archena, Murcia, España</li><li><strong>Contacto:</strong> <a href="mailto:info@nextthink.es">info@nextthink.es</a></li></ul><p>NEXTTHINK GLOBAL SL no dispone actualmente de Delegado de Protección de Datos.</p><h2>Qué datos tratamos</h2><p>Podemos tratar datos identificativos y de contacto, el contenido de tus mensajes y la información profesional o técnica que decidas compartir al solicitar información, plantear un proyecto o mantener una relación comercial.</p><h2>Finalidades y bases jurídicas</h2><ul><li><strong>Atender consultas y solicitudes:</strong> sobre la base de tu consentimiento al contactar y, cuando corresponda, de medidas precontractuales solicitadas por ti.</li><li><strong>Preparar y gestionar una relación profesional:</strong> para ejecutar medidas precontractuales, un contrato y las obligaciones legales asociadas.</li><li><strong>Proteger el sitio y sus servicios:</strong> sobre la base del interés legítimo en mantener la seguridad y prevenir usos abusivos.</li></ul><p>No utilizamos los datos recibidos a través de estos canales para enviar publicidad no solicitada.</p><h2>Conservación</h2><p>Los datos se conservarán durante el tiempo necesario para atender la consulta o gestionar la relación y, posteriormente, durante los plazos exigidos para cumplir obligaciones legales o atender posibles responsabilidades.</p><h2>Destinatarios y proveedores</h2><p>No vendemos datos personales. Pueden acceder a ellos proveedores técnicos necesarios para prestar el servicio, como alojamiento, correo electrónico, seguridad o comunicaciones, sujetos a sus obligaciones contractuales y legales.</p><p>Si eliges contactar mediante WhatsApp o visitar LinkedIn, esos proveedores tratarán información conforme a sus propias políticas. Algunos proveedores pueden realizar transferencias internacionales amparadas en los mecanismos previstos por la normativa aplicable.</p><h2>Derechos</h2><p>Puedes solicitar acceso, rectificación, supresión, oposición, limitación o portabilidad cuando corresponda escribiendo a <a href="mailto:info@nextthink.es">info@nextthink.es</a>. Para evitar accesos indebidos podremos pedir información razonable para verificar tu identidad.</p><p>También puedes presentar una reclamación ante la Agencia Española de Protección de Datos en <a href="https://www.aepd.es/" rel="noopener">www.aepd.es</a>.</p><h2>Actualizaciones</h2><p>Esta política se actualizará si cambian los canales, finalidades o proveedores utilizados. La versión publicada en esta página será la vigente.</p></div></div></section>'''
schema = schema_graph(path, title, description, "WebPage", crumb_data)
render(path, title, description, "", body, schema, "noindex,follow")

# Cookies policy
path = "/politica-de-cookies/"
title = "Política de cookies | NextThink"
description = "Información sobre el uso actual de cookies técnicas y la ausencia de cookies analíticas o publicitarias en el sitio web de NextThink."
crumb_data = [("Inicio", "/"), ("Política de cookies", path)]
body = f'''    <section class="page-hero"><div class="wrap">{breadcrumbs([("Inicio", "/"), ("Política de cookies", None)])}<p class="eyebrow">Privacidad</p><h1>Política de cookies</h1><p class="page-hero-lead">Qué tecnologías utiliza actualmente nextthink.es y cuándo sería necesario solicitar consentimiento.</p></div></section>
    <section class="section"><div class="wrap split"><div class="split-aside"><p class="eyebrow">Configuración actual</p><h2>Sin analítica ni publicidad.</h2></div><div class="prose"><h2>Uso actual de cookies</h2><p>El sitio nextthink.es no instala actualmente cookies analíticas, publicitarias ni de personalización y no incorpora herramientas de seguimiento comercial.</p><p>La infraestructura de alojamiento y protección puede utilizar cookies o identificadores estrictamente necesarios para seguridad, prevención de abuso, equilibrio de carga o entrega técnica del sitio. Estas tecnologías no se utilizan por NextThink para crear perfiles publicitarios.</p><h2>Servicios externos</h2><p>Los enlaces a WhatsApp y LinkedIn no cargan contenido de esas plataformas dentro de la web. Sus políticas se aplicarán cuando decidas abrir el enlace y visitar el servicio externo.</p><h2>Cambios futuros</h2><p>Si en el futuro se incorporan analítica, publicidad u otras tecnologías que requieran consentimiento, se actualizará esta política y se mostrará un mecanismo para aceptar o rechazar esas finalidades antes de activarlas.</p><h2>Contacto</h2><p>Puedes enviar cualquier consulta sobre privacidad o cookies a <a href="mailto:info@nextthink.es">info@nextthink.es</a>.</p></div></div></section>'''
schema = schema_graph(path, title, description, "WebPage", crumb_data)
render(path, title, description, "", body, schema, "noindex,follow")
