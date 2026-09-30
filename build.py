#!/usr/bin/env python3
"""Boston Pain Center static site generator. Run: python3 build.py"""
import html, os

ROOT = os.path.dirname(os.path.abspath(__file__))
PAGE_LANG = 'es'

def esc(s): return html.escape(str(s), quote=True)

def t(en, es, tag='p', cls='', extra=''):
    """Bilingual leaf element. Default text follows the page's default language."""
    default = es if PAGE_LANG == 'es' else en
    c = f' class="{cls}"' if cls else ''
    x = f' {extra}' if extra else ''
    return f'<{tag}{c} data-en="{esc(en)}" data-es="{esc(es)}"{x}>{esc(default)}</{tag}>'

def tph(en, es):
    return f'data-en-ph="{esc(en)}" data-es-ph="{esc(es)}" placeholder="{esc(es if PAGE_LANG=="es" else en)}"'

PHONE_DISPLAY = "(617) 555-0100"  # fictional 555 range — MUST be replaced before launch

NAV = [
    ('home', 'index.html', 'Home', 'Inicio', None),
    ('about', 'about.html', 'About', 'Nosotros', None),
    ('physicians', None, 'Physicians', 'Médicos', [
        ('roberto', 'dr-roberto-feliz.html', 'Dr. Roberto Feliz', 'Dr. Roberto Feliz'),
        ('eddie', 'dr-eddie-feliz.html', 'Dr. Eddie Feliz', 'Dr. Eddie Feliz'),
    ]),
    ('pain', 'pain-management.html', 'Pain Management', 'Manejo del dolor', None),
    ('regen', None, 'Regenerative', 'Regenerativa', [
        ('regen-overview', 'regenerative-medicine.html', 'Overview', 'Resumen'),
        ('prp', 'prp-therapy.html', 'PRP Therapy', 'Terapia PRP'),
        ('stem', 'stem-cell-therapy.html', 'Stem Cell Therapy', 'Terapia con células madre'),
        ('exosome', 'exosome-therapy.html', 'Exosome Therapy', 'Terapia con exosomas'),
        ('peptide', 'peptide-therapy.html', 'Terapia con péptidos', 'Terapia con péptidos'),
    ]),
    ('crps', 'crps-center.html', 'CRPS Center', 'Centro de CRPS', None),
    ('ketamine', 'ketamine-infusion.html', 'Ketamine', 'Ketamina', None),
    ('telehealth', 'telehealth.html', 'Telehealth', 'Telesalud', None),
    ('second', 'second-opinions.html', 'Second Opinions', 'Segundas opiniones', None),
    ('media', None, 'Media', 'Medios', [
        ('podcast', 'podcast.html', 'Podcast', 'Podcast'),
        ('tips', 'video-tips.html', 'Daily Video Tips', 'Consejos diarios en video'),
    ]),
    ('resources', 'patient-resources.html', 'Resources', 'Recursos', None),
    ('pro', 'professional-portal.html', 'Professionals', 'Profesionales', None),
    ('contact', 'contact.html', 'Contact', 'Contacto', None),
]

def nav_html(active):
    out = []
    for key, href, en, es, drop in NAV:
        label = es if PAGE_LANG == 'es' else en
        if drop:
            kids = ''.join(
                f'<a href="{h}" class="{"active" if k == active else ""}" data-en="{esc(ke)}" data-es="{esc(ks)}">{esc(ks if PAGE_LANG=="es" else ke)}</a>'
                for k, h, ke, ks in drop)
            is_active = ' active' if any(k == active for k, _, _, _ in drop) else ''
            out.append(
                f'<li class="has-drop"><button class="nav-parent{is_active}" data-en="{esc(en)}" data-es="{esc(es)}" aria-haspopup="true">{esc(label)}</button>'
                f'<div class="drop">{kids}</div></li>')
        else:
            cls = 'active' if key == active else ''
            out.append(f'<li><a href="{href}" class="{cls}" data-en="{esc(en)}" data-es="{esc(es)}">{esc(label)}</a></li>')
    return '\n'.join(out)

def header_html(active):
    sched_en, sched_es = 'Schedule', 'Agendar'
    sched = sched_es if PAGE_LANG == 'es' else sched_en
    portal_en, portal_es = 'Patient Portal', 'Portal del paciente'
    portal = portal_es if PAGE_LANG == 'es' else portal_en
    return f'''<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="header-top"><div class="wrap">
    <span><span data-en="Questions? Call " data-es="¿Preguntas? Llame al ">¿Preguntas? Llame al </span><a href="tel:+16175550100">{PHONE_DISPLAY}</a> <span class="verify-note" data-en="Number to be verified" data-es="Número por verificar">Número por verificar</span></span>
    <span><a href="patient-portal.html" data-en="Patient Portal (Demo)" data-es="Portal del paciente (Demostración)">Portal del paciente (Demostración)</a> &nbsp;·&nbsp; <span data-en="Se habla español" data-es="Se habla español">Se habla español</span></span>
  </div></div>
  <div class="header-main"><div class="wrap">
    <a class="wordmark" href="index.html" aria-label="Boston Pain Center — Home"><span class="wm-mark">B</span><span>Boston Pain Center<small data-en="Pain &amp; Regenerative Medicine" data-es="Dolor y medicina regenerativa">Dolor y medicina regenerativa</small></span></a>
    <nav class="main-nav" id="mainNav" aria-label="Main"><ul>{nav_html(active)}</ul></nav>
    <div class="header-actions">
      <div class="lang-toggle" role="group" aria-label="Language / Idioma">
        <button data-lang="en" aria-label="English">EN</button><button data-lang="es" aria-label="Español">ES</button>
      </div>
      <a class="btn btn-gold btn-sm" href="booking.html" data-en="{sched_en}" data-es="{sched_es}">{sched}</a>
      <button class="menu-btn" aria-label="Menu" data-en-aria="Open menu" data-es-aria="Abrir menú">☰</button>
    </div>
  </div></div>
</header>'''

def footer_html():
    return f'''<div class="emergency-strip" role="alert"><span data-en="Medical emergency? Call " data-es="¿Emergencia médica? Llame al ">¿Emergencia médica? Llame al </span><a href="tel:911">911</a><span data-en=" or go to your nearest emergency department." data-es=" o acuda al departamento de emergencias más cercano."> o acuda al departamento de emergencias más cercano.</span></div>
<footer class="site-footer"><div class="wrap">
  <div class="footer-grid">
    <div>
      <h4 data-en="Boston Pain Center" data-es="Boston Pain Center">Boston Pain Center</h4>
      <p style="font-size:.92rem" data-en="Comprehensive pain management and regenerative medicine in Boston, Massachusetts." data-es="Manejo integral del dolor y medicina regenerativa en Boston, Massachusetts.">Manejo integral del dolor y medicina regenerativa en Boston, Massachusetts.</p>
      <p style="font-size:.92rem"><a href="tel:+16175550100">{PHONE_DISPLAY}</a><br>
      <span data-en="Boston, MA — street address to be verified" data-es="Boston, MA — dirección por verificar">Boston, MA — dirección por verificar</span><br>
      <span class="verify-note" data-en="Contact details to be verified before launch" data-es="Datos de contacto por verificar antes del lanzamiento">Datos de contacto por verificar antes del lanzamiento</span></p>
    </div>
    <div><h4 data-en="Centers" data-es="Centros">Centros</h4><ul>
      <li><a href="pain-management.html" data-en="Pain Management" data-es="Manejo del dolor">Manejo del dolor</a></li>
      <li><a href="regenerative-medicine.html" data-en="Regenerative Medicine" data-es="Medicina regenerativa">Medicina regenerativa</a></li>
      <li><a href="crps-center.html" data-en="CRPS Center" data-es="Centro de CRPS">Centro de CRPS</a></li>
      <li><a href="ketamine-infusion.html" data-en="Ketamine Infusion Center" data-es="Centro de infusión de ketamina">Centro de infusión de ketamina</a></li>
    </ul></div>
    <div><h4 data-en="Patients" data-es="Pacientes">Pacientes</h4><ul>
      <li><a href="booking.html" data-en="Schedule &amp; Pay" data-es="Agendar y pagar">Agendar y pagar</a></li>
      <li><a href="telehealth.html" data-en="Telehealth" data-es="Telesalud">Telesalud</a></li>
      <li><a href="second-opinions.html" data-en="Second Opinions" data-es="Segundas opiniones">Segundas opiniones</a></li>
      <li><a href="patient-resources.html" data-en="Patient Resources" data-es="Recursos para pacientes">Recursos para pacientes</a></li>
      <li><a href="podcast.html" data-en="Podcast" data-es="Podcast">Podcast</a></li>
      <li><a href="video-tips.html" data-en="Daily Video Tips" data-es="Consejos diarios en video">Consejos diarios en video</a></li>
    </ul></div>
    <div><h4 data-en="Practice" data-es="Práctica">Práctica</h4><ul>
      <li><a href="about.html" data-en="About" data-es="Nosotros">Nosotros</a></li>
      <li><a href="dr-roberto-feliz.html" data-en="Dr. Roberto Feliz" data-es="Dr. Roberto Feliz">Dr. Roberto Feliz</a></li>
      <li><a href="dr-eddie-feliz.html" data-en="Dr. Eddie Feliz" data-es="Dr. Eddie Feliz">Dr. Eddie Feliz</a></li>
      <li><a href="professional-portal.html" data-en="Professional Portal" data-es="Portal profesional">Portal profesional</a></li>
      <li><a href="contact.html" data-en="Contact" data-es="Contacto">Contacto</a></li>
      <li><a href="privacy-disclaimer.html" data-en="Privacy &amp; Medical Disclaimer" data-es="Privacidad y descargo médico">Privacidad y descargo médico</a></li>
    </ul></div>
  </div>
  <div class="footer-bottom">
    <span>© <span data-year></span> <span data-en="Boston Pain Center. All rights reserved." data-es="Boston Pain Center. Todos los derechos reservados.">Boston Pain Center. Todos los derechos reservados.</span></span>
    <span><a href="privacy-disclaimer.html" data-en="Privacy &amp; Disclaimer" data-es="Privacidad y descargo">Privacidad y descargo</a> · <span data-en="Educational content only — not medical advice." data-es="Contenido educativo únicamente — no es consejo médico.">Contenido educativo únicamente — no es consejo médico.</span></span>
  </div>
</div></footer>'''

def page(title_en, title_es, active, body, default_lang='es', desc_en='', desc_es=''):
    global PAGE_LANG
    PAGE_LANG = default_lang
    title = title_es if default_lang == 'es' else title_en
    desc = desc_es if default_lang == 'es' else desc_en
    return f'''<!DOCTYPE html>
<html lang="{default_lang}" data-default-lang="{default_lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title data-en="{esc(title_en)}" data-es="{esc(title_es)}">{esc(title)}</title>
<meta name="description" data-en="{esc(desc_en)}" data-es="{esc(desc_es)}" content="{esc(desc)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
<link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
</head>
<body>
{header_html(active)}
<main id="main">{body}</main>
{footer_html()}
<script src="assets/js/payment-config.js"></script>
<script src="assets/js/main.js"></script>
</body>
</html>'''

def page_hero(eyebrow_en, eyebrow_es, h1_en, h1_es, lead_en, lead_es, crumb_en='Home', crumb_es='Inicio'):
    return f'''<div class="page-hero"><div class="wrap">
  <div class="breadcrumb"><a href="index.html" data-en="Home" data-es="Inicio">{crumb_es if PAGE_LANG=='es' else crumb_en}</a> / {esc(h1_es if PAGE_LANG=='es' else h1_en)}</div>
  {t(eyebrow_en, eyebrow_es, 'span', 'eyebrow')}
  {t(h1_en, h1_es, 'h1')}
  {t(lead_en, lead_es, 'p', 'lead')}
</div></div>'''

def cta_band(h_en, h_es, p_en, p_es):
    return f'''<section><div class="wrap"><div class="cta-band">
  {t(h_en, h_es, 'h2')}
  {t(p_en, p_es, 'p')}
  <div class="hero-ctas">
    <a class="btn btn-gold" href="booking.html" data-en="Schedule &amp; Pay" data-es="Agendar y pagar">{'Agendar y pagar' if PAGE_LANG=='es' else 'Schedule &amp; Pay'}</a>
    <a class="btn btn-outline" style="border-color:#fff;color:#fff" href="contact.html" data-en="Contact Us" data-es="Contáctenos">{'Contáctenos' if PAGE_LANG=='es' else 'Contact Us'}</a>
  </div>
</div></div></section>'''

def reg_notice(kind):
    texts = {
      'stem': ('Many stem cell applications remain investigational and are subject to FDA regulation. Boston Pain Center offers stem cell–related evaluation and care only where appropriate under applicable law, and only after individualized physician assessment. This page is educational and does not promise any outcome.',
               'Muchas aplicaciones de células madre siguen siendo de investigación y están sujetas a la regulación de la FDA. Boston Pain Center ofrece evaluación y cuidado relacionados con células madre solo cuando es apropiado según la ley aplicable, y solo después de una evaluación médica individualizada. Esta página es educativa y no promete ningún resultado.'),
      'exosome': ('Exosome-based interventions are an emerging, investigational area. Evidence is evolving and regulatory frameworks continue to develop. Any exosome-related care at Boston Pain Center follows careful physician evaluation and applicable regulations. This page is educational and does not promise any outcome.',
               'Las intervenciones basadas en exosomas son un área emergente y de investigación. La evidencia está en evolución y los marcos regulatorios continúan desarrollándose. Cualquier cuidado relacionado con exosomas en Boston Pain Center sigue una cuidadosa evaluación médica y las regulaciones aplicables. Esta página es educativa y no promete ningún resultado.'),
      'peptide': ('Peptide therapies are individualized, and some uses are considered off-label. A Boston Pain Center physician will review whether a peptide-related plan is appropriate for you, including risks, alternatives, and applicable regulations. This page is educational and does not promise any outcome.',
               'Las terapias con péptidos son individualizadas y algunos usos se consideran fuera de indicación (off-label). Un médico de Boston Pain Center revisará si un plan relacionado con péptidos es apropiado para usted, incluyendo riesgos, alternativas y regulaciones aplicables. Esta página es educativa y no promete ningún resultado.'),
      'ketamine': ('Ketamine infusion for pain and mood conditions is an off-label use administered in a monitored clinical setting. Candidacy requires medical screening, and treatment follows established safety protocols under physician supervision. This page is educational and does not promise any outcome.',
               'La infusión de ketamina para condiciones de dolor y del estado de ánimo es un uso fuera de indicación (off-label) administrado en un entorno clínico monitoreado. La candidatura requiere evaluación médica y el tratamiento sigue protocolos de seguridad establecidos bajo supervisión médica. Esta página es educativa y no promete ningún resultado.'),
    }
    en, es = texts[kind]
    return f'''<div class="notice notice-regulatory"><h4 data-en="Regulatory notice" data-es="Aviso regulatorio">Aviso regulatorio</h4>
    <p data-en="{esc(en)}" data-es="{esc(es)}">{esc(es if PAGE_LANG=='es' else en)}</p></div>'''

def faq(items):
    out = []
    for q_en, q_es, a_en, a_es in items:
        out.append(f'''<div class="faq"><button class="faq-q" data-en="{esc(q_en)}" data-es="{esc(q_es)}">{esc(q_es if PAGE_LANG=='es' else q_en)}</button>
        <div class="faq-a" data-en="{esc(a_en)}" data-es="{esc(a_es)}">{esc(a_es if PAGE_LANG=='es' else a_en)}</div></div>''')
    return '\n'.join(out)

def verify_badge():
    return t('Physician details pending verification — published only after review.',
             'Datos del médico pendientes de verificación — se publican solo después de la revisión.',
             'span', 'verify-note')

def write(name, content):
    path = os.path.join(ROOT, name)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('wrote', name, len(content), 'bytes')

# ============================ HOME ============================
def build_index():
    centers = [
        ('pain-management.html', '🎯', 'Pain Management', 'Manejo del dolor',
         'Comprehensive evaluation, image-guided interventional care, and coordinated treatment plans.',
         'Evaluación integral, cuidado intervencionista guiado por imagen y planes de tratamiento coordinados.'),
        ('regenerative-medicine.html', '🌱', 'Regenerative Medicine', 'Medicina regenerativa',
         'PRP, stem cell, exosome, and peptide education — with clear, honest regulatory guidance.',
         'Educación sobre PRP, células madre, exosomas y péptidos — con orientación regulatoria clara y honesta.'),
        ('crps-center.html', '🧠', 'CRPS Center', 'Centro de CRPS',
         'Specialized evaluation and management for complex regional pain syndrome.',
         'Evaluación y manejo especializados para el síndrome de dolor regional complejo.'),
        ('ketamine-infusion.html', '💧', 'Ketamine Infusion Center', 'Centro de infusión de ketamina',
         'Screened, monitored infusion care for selected pain and mood conditions.',
         'Cuidado de infusión evaluado y monitoreado para condiciones seleccionadas de dolor y del estado de ánimo.'),
    ]
    center_cards = '\n'.join(
        f'''<div class="card"><div class="icon-badge">{icon}</div><h3 data-en="{esc(en)}" data-es="{esc(es)}">{esc(es if PAGE_LANG=='es' else en)}</h3>
        <p data-en="{esc(den)}" data-es="{esc(des)}">{esc(des if PAGE_LANG=='es' else den)}</p>
        <a class="card-link" href="{href}" data-en="Learn more →" data-es="Más información →">{'Más información →' if PAGE_LANG=='es' else 'Learn more →'}</a></div>'''
        for href, icon, en, es, den, des in centers)
    conditions = ['CRPS', 'Neuropathic pain', 'Spine disorders', 'Joint pain', 'Fibromyalgia', 'Migraine', 'Tendon injuries', 'Peripheral nerve pain']
    conditions_es = ['CRPS', 'Dolor neuropático', 'Trastornos de la columna', 'Dolor articular', 'Fibromialgia', 'Migraña', 'Lesiones de tendones', 'Dolor de nervios periféricos']
    cond_chips = '\n'.join(
        f'<span data-en="{esc(en)}" data-es="{esc(es)}">{esc(es if PAGE_LANG=="es" else en)}</span>' for en, es in zip(conditions, conditions_es))
    why = [
        ('Evidence-based care', 'Atención basada en evidencia', 'Evaluation and treatment grounded in current clinical evidence.', 'Evaluación y tratamiento basados en la evidencia clínica actual.'),
        ('Image-guided procedures', 'Procedimientos guiados por imagen', 'Precision techniques supported by imaging where appropriate.', 'Técnicas de precisión apoyadas por imagen cuando es apropiado.'),
        ('Individualized plans', 'Planes individualizados', 'Care plans shaped around your history, goals, and response.', 'Planes de cuidado adaptados a su historial, objetivos y respuesta.'),
        ('Infusion capability', 'Capacidad de infusión', 'A monitored infusion setting for selected therapies.', 'Un entorno de infusión monitoreado para terapias seleccionadas.'),
        ('Coordinated care', 'Cuidado coordinado', 'Communication with your existing physicians and care team.', 'Comunicación con sus médicos actuales y su equipo de cuidado.'),
        ('Patient-centered experience', 'Experiencia centrada en el paciente', 'Clear explanations, unhurried visits, and bilingual care.', 'Explicaciones claras, visitas sin prisa y atención bilingüe.'),
    ]
    why_cards = '\n'.join(
        f'''<div class="card"><h3 data-en="{esc(en)}" data-es="{esc(es)}">{esc(es if PAGE_LANG=='es' else en)}</h3>
        <p data-en="{esc(den)}" data-es="{esc(des)}">{esc(des if PAGE_LANG=='es' else den)}</p></div>'''
        for en, es, den, des in why)
    body = f'''
<section class="hero"><div class="wrap">
  {t('Boston Pain Center — Boston, Massachusetts', 'Boston Pain Center — Boston, Massachusetts', 'span', 'eyebrow')}
  {t('Regenerate. Restore. Relieve.', 'Regenerar. Restaurar. Aliviar.', 'h1')}
  <div class="gold-rule"></div>
  {t('Comprehensive pain management, regenerative medicine, and interventional care — built around you and your goals.',
     'Manejo integral del dolor, medicina regenerativa y cuidado intervencionista — centrados en usted y sus objetivos.', 'p', 'lead')}
  <div class="hero-ctas">
    <a class="btn btn-gold" href="booking.html" data-en="Schedule &amp; Pay" data-es="Agendar y pagar">{'Agendar y pagar' if PAGE_LANG=='es' else 'Schedule &amp; Pay'}</a>
    <a class="btn btn-outline" style="border-color:#fff;color:#fff" href="telehealth.html" data-en="Telehealth Visit" data-es="Visita por telesalud">{'Visita por telesalud' if PAGE_LANG=='es' else 'Telehealth Visit'}</a>
    <a class="btn btn-outline" style="border-color:#fff;color:#fff" href="second-opinions.html" data-en="Second Opinion" data-es="Segunda opinión">{'Segunda opinión' if PAGE_LANG=='es' else 'Second Opinion'}</a>
  </div>
  <div class="hero-badges">
    <span data-en="Se habla español" data-es="Se habla español">Se habla español</span>
    <span data-en="Physician-led care" data-es="Atención dirigida por médicos">Atención dirigida por médicos</span>
    <span data-en="In-person &amp; telehealth" data-es="Presencial y telesalud">Presencial y telesalud</span>
  </div>
</div></section>

<section><div class="wrap">
  {t('Centers of Excellence', 'Centros de excelencia', 'span', 'eyebrow')}
  {t('Specialized care, one roof', 'Cuidado especializado, un solo techo', 'h2')}
  <div class="gold-rule"></div>
  <div class="grid grid-4">{center_cards}</div>
</div></section>

<section class="section-alt"><div class="wrap">
  {t('Meet our physicians', 'Conozca a nuestros médicos', 'span', 'eyebrow')}
  {t('Physician-led, patient-first', 'Dirigido por médicos, centrado en el paciente', 'h2')}
  <div class="gold-rule"></div>
  <div class="grid grid-2">
    <div class="card doc-card"><div class="monogram">RF</div>
      {t('Dr. Roberto Feliz', 'Dr. Roberto Feliz', 'h3')}
      {t('Physician — Boston Pain Center', 'Médico — Boston Pain Center', 'p', 'doc-role')}
      {verify_badge()}
      <div><a class="btn btn-teal btn-sm" style="margin-top:1rem" href="dr-roberto-feliz.html" data-en="View Profile" data-es="Ver perfil">{'Ver perfil' if PAGE_LANG=='es' else 'View Profile'}</a></div>
    </div>
    <div class="card doc-card"><div class="monogram">EF</div>
      {t('Dr. Eddie Feliz', 'Dr. Eddie Feliz', 'h3')}
      {t('Physician — Boston Pain Center', 'Médico — Boston Pain Center', 'p', 'doc-role')}
      {verify_badge()}
      <div><a class="btn btn-teal btn-sm" style="margin-top:1rem" href="dr-eddie-feliz.html" data-en="View Profile" data-es="Ver perfil">{'Ver perfil' if PAGE_LANG=='es' else 'View Profile'}</a></div>
    </div>
  </div>
</div></section>

<section><div class="wrap">
  {t('Conditions we evaluate', 'Condiciones que evaluamos', 'span', 'eyebrow')}
  {t('Where we may be able to help', 'Donde podemos ayudarle', 'h2')}
  <div class="gold-rule"></div>
  <div class="hero-badges" style="margin-top:0">{cond_chips}</div>
  {t('Not sure if your condition fits? A consultation is the right first step.',
     '¿No está seguro si su condición aplica? Una consulta es el primer paso correcto.', 'p', 'kbd-hint')}
</div></section>

<section class="section-alt"><div class="wrap">
  {t('Why Boston Pain Center', 'Por qué Boston Pain Center', 'span', 'eyebrow')}
  {t('A careful, coordinated approach', 'Un enfoque cuidadoso y coordinado', 'h2')}
  <div class="gold-rule"></div>
  <div class="grid grid-3">{why_cards}</div>
</div></section>

<section><div class="wrap"><div class="two-col">
  <div class="card">
    {t('Care from anywhere', 'Cuidado desde cualquier lugar', 'span', 'eyebrow')}
    {t('Telehealth & second opinions', 'Telesalud y segundas opiniones', 'h2')}
    {t('Meet your physician by secure video, or get an independent review of your diagnosis and options — wherever you are, subject to licensure and applicable law.',
       'Reúnase con su médico por video seguro u obtenga una revisión independiente de su diagnóstico y opciones — dondequiera que esté, sujeto a licencia y ley aplicable.', 'p')}
    <div class="hero-ctas">
      <a class="btn btn-teal" href="telehealth.html" data-en="How Telehealth Works" data-es="Cómo funciona la telesalud">{'Cómo funciona la telesalud' if PAGE_LANG=='es' else 'How Telehealth Works'}</a>
      <a class="btn btn-outline" href="second-opinions.html" data-en="Request a Second Opinion" data-es="Solicitar una segunda opinión">{'Solicitar una segunda opinión' if PAGE_LANG=='es' else 'Request a Second Opinion'}</a>
    </div>
  </div>
  <div class="card">
    {t('Learn every week', 'Aprenda cada semana', 'span', 'eyebrow')}
    {t('Dr. Feliz Podcast & daily tips', 'Podcast del Dr. Feliz y consejos diarios', 'h2')}
    {t('A weekly podcast and short daily video tips with Dr. Roberto Feliz — plain-language education on pain, recovery, and regenerative medicine.',
       'Un podcast semanal y consejos breves diarios en video con el Dr. Roberto Feliz — educación en lenguaje claro sobre dolor, recuperación y medicina regenerativa.', 'p')}
    <div class="hero-ctas">
      <a class="btn btn-teal btn-sm" href="podcast.html" data-en="Listen" data-es="Escuchar">{'Escuchar' if PAGE_LANG=='es' else 'Listen'}</a>
      <a class="btn btn-outline btn-sm" href="video-tips.html" data-en="Daily Tips" data-es="Consejos diarios">{'Consejos diarios' if PAGE_LANG=='es' else 'Daily Tips'}</a>
    </div>
  </div>
</div></div></section>
{cta_band('Ready to take the first step?', '¿Listo para dar el primer paso?',
          'Choose your service, pick a time, and pay securely at booking through Stripe.',
          'Elija su servicio, seleccione un horario y pague de forma segura al reservar a través de Stripe.')}
'''
    return page('Boston Pain Center | Regenerate. Restore. Relieve.',
                'Boston Pain Center | Regenerar. Restaurar. Aliviar.', 'home', body,
                desc_en='Comprehensive pain management and regenerative medicine in Boston, MA. Schedule and pay online.',
                desc_es='Manejo integral del dolor y medicina regenerativa en Boston, MA. Agende y pague en línea.')

# ============================ ABOUT ============================
def build_about():
    body = page_hero('About Boston Pain Center', 'Sobre Boston Pain Center',
        'Care built around the person, not just the pain', 'Cuidado centrado en la persona, no solo en el dolor',
        'Our mission is straightforward: careful evaluation, honest guidance, and coordinated care for people living with pain.',
        'Nuestra misión es clara: evaluación cuidadosa, orientación honesta y cuidado coordinado para personas que viven con dolor.')
    body += f'''
<section><div class="wrap"><div class="two-col"><div>
  {t('Our philosophy', 'Nuestra filosofía', 'span', 'eyebrow')}
  {t('Listen first. Then plan.', 'Escuchar primero. Luego planificar.', 'h2')}
  <div class="gold-rule"></div>
  {t('Pain is personal. Two people with the same diagnosis can have very different experiences — so we start by listening. Your history, your goals, and your response to prior treatments shape everything that follows.',
     'El dolor es personal. Dos personas con el mismo diagnóstico pueden tener experiencias muy diferentes — por eso comenzamos escuchando. Su historial, sus objetivos y su respuesta a tratamientos previos dan forma a todo lo que sigue.', 'p')}
  {t('From there, your physician builds a plan that may combine interventional procedures, regenerative options, infusion therapy, rehabilitation coordination, and medication stewardship — always explained in plain language, in English or Spanish.',
     'A partir de ahí, su médico elabora un plan que puede combinar procedimientos intervencionistas, opciones regenerativas, terapia de infusión, coordinación de rehabilitación y manejo de medicamentos — siempre explicado en lenguaje claro, en inglés o español.', 'p')}
</div><div>
  <div class="card">{t('Our care model', 'Nuestro modelo de cuidado', 'h3')}
  {t('1. Comprehensive evaluation — history, examination, and review of prior imaging and records.', '1. Evaluación integral — historial, examen y revisión de imágenes y registros previos.', 'p')}
  {t('2. Plain-language diagnosis — what we found and what it means for you.', '2. Diagnóstico en lenguaje claro — lo que encontramos y lo que significa para usted.', 'p')}
  {t('3. Individualized plan — options, benefits, risks, and alternatives discussed openly.', '3. Plan individualizado — opciones, beneficios, riesgos y alternativas discutidos abiertamente.', 'p')}
  {t('4. Coordinated follow-through — we stay in communication with your care team.', '4. Seguimiento coordinado — nos mantenemos en comunicación con su equipo de cuidado.', 'p')}
  </div>
</div></div></div></section>
<section class="section-alt"><div class="wrap">
  {t('What guides us', 'Lo que nos guía', 'span', 'eyebrow')}
  {t('Our commitments', 'Nuestros compromisos', 'h2')}<div class="gold-rule"></div>
  <div class="grid grid-3">
    <div class="card">{t('Honest guidance', 'Orientación honesta', 'h3')}{t('If a treatment is unlikely to help you, we will tell you — and explain what might.', 'Si es poco probable que un tratamiento le ayude, se lo diremos — y le explicaremos qué podría ayudar.', 'p')}</div>
    <div class="card">{t('No outcome promises', 'Sin promesas de resultados', 'h3')}{t('Medicine has uncertainties. We discuss realistic expectations, never guarantees.', 'La medicina tiene incertidumbres. Discutimos expectativas realistas, nunca garantías.', 'p')}</div>
    <div class="card">{t('Bilingual care', 'Atención bilingüe', 'h3')}{t('Full care in English and Spanish — because understanding your plan matters.', 'Atención completa en inglés y español — porque entender su plan es importante.', 'p')}</div>
  </div>
</div></section>
{cta_band('Meet the physicians behind the mission', 'Conozca a los médicos detrás de la misión',
          'Physician-led care, with profiles published after verification.',
          'Atención dirigida por médicos, con perfiles publicados después de la verificación.')}
'''
    return page('About | Boston Pain Center', 'Nosotros | Boston Pain Center', 'about', body,
                desc_en='Mission, philosophy, and care model of Boston Pain Center.',
                desc_es='Misión, filosofía y modelo de cuidado de Boston Pain Center.')

# ============================ PHYSICIANS ============================
def physician_page(slug, name, initials, extra_sections_en_es):
    secs = ''
    for h_en, h_es, b_en, b_es in extra_sections_en_es:
        secs += f'''<div class="card">{t(h_en, h_es, 'h3')}{t(b_en, b_es, 'p')}{verify_badge()}</div>'''
    body = page_hero('Our Physicians', 'Nuestros médicos', name, name,
        'Physician — Boston Pain Center. Full biography and credentials are published after verification.',
        'Médico — Boston Pain Center. La biografía completa y las credenciales se publican después de la verificación.')
    body += f'''
<section><div class="wrap"><div class="two-col"><div>
  <div class="card doc-card" style="text-align:left;display:flex;gap:24px;align-items:center;flex-wrap:wrap">
    <div class="monogram lg">{initials}</div>
    <div>{t(name, name, 'h2')}
    {t('Physician — Boston Pain Center', 'Médico — Boston Pain Center', 'p', 'doc-role')}
    {verify_badge()}
    <div class="notice notice-demo" style="margin-top:1rem"><p style="margin:0" data-en="Portrait placeholder. A verified professional portrait will appear here." data-es="Imagen provisional. Aquí aparecerá un retrato profesional verificado.">{'Imagen provisional. Aquí aparecerá un retrato profesional verificado.' if PAGE_LANG=='es' else 'Portrait placeholder. A verified professional portrait will appear here.'}</p></div>
    </div>
  </div>
  <div class="grid grid-2" style="margin-top:22px">{secs}</div>
</div>
<div>
  <div class="card">{t('Schedule with '+name, 'Agendar con '+name, 'h3')}
  {t('Consultations are available in person and by telehealth, where appropriate.',
     'Consultas disponibles en persona y por telesalud, cuando sea apropiado.', 'p')}
  <a class="btn btn-gold" href="booking.html" data-en="Schedule &amp; Pay" data-es="Agendar y pagar">{'Agendar y pagar' if PAGE_LANG=='es' else 'Schedule &amp; Pay'}</a></div>
  <div class="card" style="margin-top:18px">{t('A note on credentials', 'Una nota sobre las credenciales', 'h3')}
  {t('Titles, training, certifications, affiliations, and licensing are published only after verification. Nothing on this page should be read as a credential claim until verified information appears here.',
     'Títulos, formación, certificaciones, afiliaciones y licencias se publican solo después de la verificación. Nada en esta página debe interpretarse como una credencial hasta que aparezca aquí la información verificada.', 'p')}</div>
</div></div></div></section>
'''
    return page(name + ' | Boston Pain Center', name + ' | Boston Pain Center', slug, body,
                desc_en=name + ' — physician profile at Boston Pain Center (verified biography pending).',
                desc_es=name + ' — perfil médico en Boston Pain Center (biografía verificada pendiente).')

def build_roberto():
    return physician_page('roberto', 'Dr. Roberto Feliz', 'RF', [
        ('Biography', 'Biografía',
         'Verified biography pending — this section will describe Dr. Roberto Feliz’s background, training, and clinical focus after review.',
         'Biografía verificada pendiente — esta sección describirá los antecedentes, la formación y el enfoque clínico del Dr. Roberto Feliz después de la revisión.'),
        ('Clinical interests', 'Intereses clínicos',
         'Published after verification. Dr. Feliz hosts the weekly Dr. Feliz Podcast and the daily video tips series.',
         'Se publican después de la verificación. El Dr. Feliz presenta el podcast semanal Dr. Feliz y la serie diaria de consejos en video.'),
        ('Procedures & services', 'Procedimientos y servicios',
         'A verified list of procedures and services will appear here.',
         'Aquí aparecerá una lista verificada de procedimientos y servicios.'),
        ('Media & education', 'Medios y educación',
         'Weekly podcast host and daily video tips educator — new content every week.',
         'Presentador del podcast semanal y educador de los consejos diarios en video — contenido nuevo cada semana.'),
    ])

def build_eddie():
    return physician_page('eddie', 'Dr. Eddie Feliz', 'EF', [
        ('Biography', 'Biografía',
         'Verified biography pending — this section will describe Dr. Eddie Feliz’s background, training, and clinical focus after review.',
         'Biografía verificada pendiente — esta sección describirá los antecedentes, la formación y el enfoque clínico del Dr. Eddie Feliz después de la revisión.'),
        ('Clinical interests', 'Intereses clínicos',
         'Published after verification.',
         'Se publican después de la verificación.'),
        ('Telehealth & second opinions', 'Telesalud y segundas opiniones',
         'Availability for telehealth visits and second-opinion reviews will be listed here after verification.',
         'La disponibilidad para visitas por telesalud y revisiones de segunda opinión se indicará aquí después de la verificación.'),
        ('Procedures & services', 'Procedimientos y servicios',
         'A verified list of procedures and services will appear here.',
         'Aquí aparecerá una lista verificada de procedimientos y servicios.'),
    ])

# ============================ SERVICE PAGES ============================
def service_page(active, eyebrow_en, eyebrow_es, h1_en, h1_es, lead_en, lead_es,
                 sections, faqs, notice_kind=None, guides=None, cta_service='consult_new'):
    body = page_hero(eyebrow_en, eyebrow_es, h1_en, h1_es, lead_en, lead_es)
    secs = ''
    for h_en, h_es, b_en, b_es in sections:
        secs += f'''<div class="card">{t(h_en, h_es, 'h3')}{t(b_en, b_es, 'p')}</div>'''
    if guides:
        glinks = ''.join(f'<li><a href="{h}">{esc(l_es if PAGE_LANG=="es" else l_en)}</a></li>' for h, l_en, l_es in guides)
        secs += f'''<div class="card">{t('Preparation guides', 'Guías de preparación', 'h3')}<ul>{glinks}</ul></div>'''
    notice = reg_notice(notice_kind) if notice_kind else ''
    body += f'''
<section><div class="wrap"><div class="two-col"><div>
  {notice}
  <div class="grid grid-2">{secs}</div>
  <div style="margin-top:28px">{t('Frequently asked questions', 'Preguntas frecuentes', 'h2')}{faq(faqs)}</div>
</div><div>
  <div class="card">{t('Take the next step', 'Dé el siguiente paso', 'h3')}
  {t('Book a consultation and pay securely at booking through Stripe.',
     'Reserve una consulta y pague de forma segura al reservar a través de Stripe.', 'p')}
  <a class="btn btn-gold" href="booking.html" data-en="Schedule &amp; Pay" data-es="Agendar y pagar">{'Agendar y pagar' if PAGE_LANG=='es' else 'Schedule &amp; Pay'}</a>
  <div style="margin-top:.8rem"><a href="second-opinions.html" data-en="Or request a second opinion →" data-es="O solicite una segunda opinión →">{'O solicite una segunda opinión →' if PAGE_LANG=='es' else 'Or request a second opinion →'}</a></div></div>
  <div class="card" style="margin-top:18px">{t('Good to know', 'Conviene saber', 'h3')}
  {t('Every plan starts with an individualized physician evaluation. Educational content on this site is not medical advice for your specific situation.',
     'Todo plan comienza con una evaluación médica individualizada. El contenido educativo de este sitio no es consejo médico para su situación específica.', 'p')}</div>
</div></div></div></section>
'''
    return page(h1_en + ' | Boston Pain Center', h1_es + ' | Boston Pain Center', active, body,
                desc_en=lead_en, desc_es=lead_es)

def build_pain():
    return service_page('pain', 'Pain Management', 'Manejo del dolor',
        'Comprehensive pain management', 'Manejo integral del dolor',
        'Careful evaluation first — then a coordinated plan that may include interventional procedures, rehabilitation, and medication stewardship.',
        'Primero una evaluación cuidadosa — luego un plan coordinado que puede incluir procedimientos intervencionistas, rehabilitación y manejo de medicamentos.',
        [
            ('Evaluation', 'Evaluación',
             'Your visit starts with a thorough history and examination, plus review of prior imaging, procedures, and treatments — so the plan builds on what is already known.',
             'Su visita comienza con un historial y examen exhaustivos, además de la revisión de imágenes, procedimientos y tratamientos previos — para que el plan se base en lo que ya se conoce.'),
            ('Interventional care', 'Cuidado intervencionista',
             'Where appropriate, image-guided procedures can target the source of pain as part of a broader plan — always discussed with benefits, risks, and alternatives.',
             'Cuando es apropiado, los procedimientos guiados por imagen pueden tratar la fuente del dolor como parte de un plan más amplio — siempre discutiendo beneficios, riesgos y alternativas.'),
            ('Coordinated follow-through', 'Seguimiento coordinado',
             'We coordinate with your primary care physician, specialists, and therapists, and adjust the plan based on your response over time.',
             'Coordinamos con su médico primario, especialistas y terapeutas, y ajustamos el plan según su respuesta en el tiempo.'),
            ('Medication stewardship', 'Manejo responsable de medicamentos',
             'Thoughtful, monitored use of medications as one part of the plan — with attention to safety, interactions, and your goals.',
             'Uso cuidadoso y monitoreado de medicamentos como una parte del plan — con atención a la seguridad, las interacciones y sus objetivos.'),
        ],
        [
            ('What should I bring to my first visit?', '¿Qué debo llevar a mi primera visita?',
             'Prior imaging (MRI, X-ray, CT), procedure reports, a medication list, and any records from previous pain treatments help us evaluate you efficiently.',
             'Imágenes previas (resonancia, rayos X, tomografía), informes de procedimientos, una lista de medicamentos y registros de tratamientos previos nos ayudan a evaluarle eficientemente.'),
            ('Will I need a procedure?', '¿Necesitaré un procedimiento?',
             'Not necessarily. Procedures are one tool among several; your physician will recommend only what fits your evaluation, and explain alternatives.',
             'No necesariamente. Los procedimientos son una herramienta entre varias; su médico recomendará solo lo que corresponda a su evaluación y le explicará las alternativas.'),
            ('Do you treat my condition?', '¿Tratan mi condición?',
             'We evaluate a wide range of painful conditions. A consultation is the right way to determine whether our care fits your situation.',
             'Evaluamos una amplia gama de condiciones dolorosas. Una consulta es la forma correcta de determinar si nuestro cuidado se adapta a su situación.'),
        ])

def build_regen_hub():
    cards = [
        ('prp-therapy.html', 'PRP Therapy', 'Terapia PRP', 'Platelet-rich plasma — candidacy, uses, and FAQs.', 'Plasma rico en plaquetas — candidatura, usos y preguntas frecuentes.'),
        ('stem-cell-therapy.html', 'Stem Cell Therapy', 'Terapia con células madre', 'Educational overview with regulatory guidance.', 'Resumen educativo con orientación regulatoria.'),
        ('exosome-therapy.html', 'Exosome Therapy', 'Terapia con exosomas', 'An emerging, investigational area — explained carefully.', 'Un área emergente y de investigación — explicada con cuidado.'),
        ('peptide-therapy.html', 'Peptide Therapy', 'Terapia con péptidos', 'Individualized consultation with compliance clarity.', 'Consulta individualizada con claridad regulatoria.'),
    ]
    ch = '\n'.join(f'''<div class="card"><h3 data-en="{esc(en)}" data-es="{esc(es)}">{esc(es if PAGE_LANG=='es' else en)}</h3>
      <p data-en="{esc(den)}" data-es="{esc(des)}">{esc(des if PAGE_LANG=='es' else den)}</p>
      <a class="card-link" href="{h}" data-en="Learn more →" data-es="Más información →">{'Más información →' if PAGE_LANG=='es' else 'Learn more →'}</a></div>'''
      for h, en, es, den, des in cards)
    body = page_hero('Regenerative Medicine', 'Medicina regenerativa',
        'Regenerative medicine, explained honestly', 'Medicina regenerativa, explicada con honestidad',
        'Education on PRP, stem cell, exosome, and peptide therapies — what they are, who they may suit, and the regulations that govern them.',
        'Educación sobre terapias de PRP, células madre, exosomas y péptidos — qué son, para quién pueden ser adecuadas y las regulaciones que las rigen.')
    body += f'''
<section><div class="wrap">
  <div class="notice notice-regulatory"><h4 data-en="Our approach to regenerative care" data-es="Nuestro enfoque del cuidado regenerativo">Nuestro enfoque del cuidado regenerativo</h4>
  <p data-en="Regenerative medicine holds promise — and it also carries real uncertainties and regulations. We explain candidacy, evidence, and limits plainly before any decision, and we never promise outcomes." data-es="La medicina regenerativa es prometedora — y también conlleva incertidumbres y regulaciones reales. Explicamos claramente la candidatura, la evidencia y los límites antes de cualquier decisión, y nunca prometemos resultados.">{'La medicina regenerativa es prometedora — y también conlleva incertidumbres y regulaciones reales. Explicamos claramente la candidatura, la evidencia y los límites antes de cualquier decisión, y nunca prometemos resultados.' if PAGE_LANG=='es' else 'Regenerative medicine holds promise — and it also carries real uncertainties and regulations. We explain candidacy, evidence, and limits plainly before any decision, and we never promise outcomes.'}</p></div>
  <div class="grid grid-2" style="margin-top:8px">{ch}</div>
</div></section>
{cta_band('Wondering if regenerative care fits you?', '¿Se pregunta si el cuidado regenerativo es para usted?',
          'Start with a physician evaluation — candidacy, evidence, and alternatives discussed openly.',
          'Comience con una evaluación médica — candidatura, evidencia y alternativas discutidas abiertamente.')}
'''
    return page('Regenerative Medicine | Boston Pain Center', 'Medicina regenerativa | Boston Pain Center', 'regen-overview', body,
                desc_en='PRP, stem cell, exosome, and peptide therapy education at Boston Pain Center.',
                desc_es='Educación sobre PRP, células madre, exosomas y péptidos en Boston Pain Center.')

def build_prp():
    return service_page('prp', 'Regenerative Medicine', 'Medicina regenerativa',
        'PRP therapy', 'Terapia PRP',
        'Platelet-rich plasma uses a concentrated portion of your own blood to support the body’s natural repair processes in selected musculoskeletal conditions.',
        'El plasma rico en plaquetas utiliza una porción concentrada de su propia sangre para apoyar los procesos naturales de reparación del cuerpo en condiciones musculoesqueléticas seleccionadas.',
        [
            ('How it works', 'Cómo funciona',
             'A small blood sample is processed to concentrate platelets, which are then precisely placed at the target area — often with image guidance.',
             'Se procesa una pequeña muestra de sangre para concentrar las plaquetas, que luego se colocan con precisión en el área objetivo — a menudo con guía de imagen.'),
            ('Common musculoskeletal uses', 'Usos musculoesqueléticos comunes',
             'PRP is most often discussed for tendon, ligament, and joint conditions. Your physician will review whether your specific case fits the current evidence.',
             'El PRP se discute con mayor frecuencia para condiciones de tendones, ligamentos y articulaciones. Su médico revisará si su caso específico se ajusta a la evidencia actual.'),
            ('Candidacy assessment', 'Evaluación de candidatura',
             'Not everyone is a candidate. History, examination, imaging, and prior treatments all factor into the decision — discussed openly with alternatives.',
             'No todos son candidatos. El historial, el examen, las imágenes y los tratamientos previos influyen en la decisión — discutida abiertamente con alternativas.'),
            ('What to expect', 'Qué esperar',
             'The visit is typically brief and office-based. Your physician will explain preparation, aftercare, and realistic timelines at your consultation.',
             'La visita suele ser breve y en el consultorio. Su médico le explicará la preparación, los cuidados posteriores y los plazos realistas en su consulta.'),
        ],
        [
            ('Is PRP painful?', '¿Es doloroso el PRP?',
             'Most patients report brief, manageable discomfort. Your physician will discuss comfort measures for the procedure.',
             'La mayoría de los pacientes reportan una molestia breve y manejable. Su médico discutirá las medidas de confort para el procedimiento.'),
            ('How many sessions are typical?', '¿Cuántas sesiones son típicas?',
             'Plans vary by condition and response. Your physician will outline a proposed course — and adjust based on how you respond.',
             'Los planes varían según la condición y la respuesta. Su médico le presentará un curso propuesto — y lo ajustará según su respuesta.'),
            ('Are results guaranteed?', '¿Los resultados están garantizados?',
             'No. Responses vary between individuals, and we discuss realistic expectations rather than promises.',
             'No. Las respuestas varían entre personas, y discutimos expectativas realistas en lugar de promesas.'),
        ],
        guides=[('guides/prp-preparation-guide.html', 'PRP preparation guide (printable)', 'Guía de preparación para PRP (imprimible)')])

def build_stem():
    return service_page('stem', 'Regenerative Medicine', 'Medicina regenerativa',
        'Stem cell therapy', 'Terapia con células madre',
        'An educational overview of stem cell–based approaches: the science, the current evidence, and the regulations that govern their use.',
        'Un resumen educativo de los enfoques basados en células madre: la ciencia, la evidencia actual y las regulaciones que rigen su uso.',
        [
            ('The science in plain language', 'La ciencia en lenguaje claro',
             'Stem cells are the body’s raw-material cells with the ability to develop into more specialized cell types. Research is exploring how they may support tissue repair.',
             'Las células madre son las células primarias del cuerpo con la capacidad de convertirse en tipos de células más especializadas. La investigación explora cómo pueden apoyar la reparación de tejidos.'),
            ('Evidence and investigational status', 'Evidencia y estado de investigación',
             'Many applications remain investigational: studied, but not yet established as standard care. We explain where the evidence stands for your specific question.',
             'Muchas aplicaciones siguen siendo de investigación: estudiadas, pero aún no establecidas como cuidado estándar. Explicamos el estado de la evidencia para su pregunta específica.'),
            ('Candidate evaluation', 'Evaluación de candidatura',
             'A physician evaluation comes first — diagnosis, prior treatments, goals, and whether a stem cell–related approach is appropriate and lawful in your case.',
             'Primero una evaluación médica — diagnóstico, tratamientos previos, objetivos y si un enfoque relacionado con células madre es apropiado y legal en su caso.'),
        ],
        [
            ('Is stem cell therapy FDA approved?', '¿La terapia con células madre está aprobada por la FDA?',
             'A small number of cell-based products are FDA-approved for specific uses; many other applications are investigational. Your physician will explain what applies to your situation.',
             'Un pequeño número de productos basados en células están aprobados por la FDA para usos específicos; muchas otras aplicaciones son de investigación. Su médico le explicará qué aplica a su situación.'),
            ('Why do regulations matter here?', '¿Por qué importan las regulaciones aquí?',
             'Because they protect patients. We offer stem cell–related evaluation and care only where appropriate under applicable law.',
             'Porque protegen a los pacientes. Ofrecemos evaluación y cuidado relacionados con células madre solo cuando es apropiado según la ley aplicable.'),
        ],
        notice_kind='stem')

def build_exosome():
    return service_page('exosome', 'Regenerative Medicine', 'Medicina regenerativa',
        'Exosome therapy', 'Terapia con exosomas',
        'Exosomes are tiny messengers between cells — an emerging, investigational area of regenerative science we explain with care.',
        'Los exosomas son pequeños mensajeros entre células — un área emergente y de investigación de la ciencia regenerativa que explicamos con cuidado.',
        [
            ('What exosomes are', 'Qué son los exosomas',
             'Exosomes are nano-sized vesicles released by cells that carry signals involved in communication and repair processes. Research interest is growing rapidly.',
             'Los exosomas son vesículas de tamaño nanométrico liberadas por las células que transportan señales involucradas en procesos de comunicación y reparación. El interés de la investigación crece rápidamente.'),
            ('An investigational landscape', 'Un panorama de investigación',
             'Evidence is early and evolving, and regulatory frameworks are still developing. We give you a candid picture of what is known — and what is not.',
             'La evidencia es temprana y está en evolución, y los marcos regulatorios aún se están desarrollando. Le ofrecemos una imagen sincera de lo que se sabe — y lo que no.'),
            ('Physician evaluation first', 'Primero la evaluación médica',
             'Any exosome-related discussion at Boston Pain Center begins with careful physician evaluation and follows applicable regulations.',
             'Cualquier discusión relacionada con exosomas en Boston Pain Center comienza con una cuidadosa evaluación médica y sigue las regulaciones aplicables.'),
        ],
        [
            ('Are exosome treatments proven?', '¿Los tratamientos con exosomas están probados?',
             'No — this remains an investigational area. We discuss the current state of evidence openly so you can make an informed decision.',
             'No — sigue siendo un área de investigación. Discutimos abiertamente el estado actual de la evidencia para que pueda tomar una decisión informada.'),
            ('Is it legal?', '¿Es legal?',
             'Regulations are evolving. We proceed only within applicable law and after individualized physician assessment.',
             'Las regulaciones están en evolución. Procedemos solo dentro de la ley aplicable y después de una evaluación médica individualizada.'),
        ],
        notice_kind='exosome')

def build_peptide():
    return service_page('peptide', 'Regenerative Medicine', 'Medicina regenerativa',
        'Peptide therapy', 'Terapia con péptidos',
        'Peptides are short chains of amino acids being studied for roles in recovery and function — approached here with individualized, compliant care.',
        'Los péptidos son cadenas cortas de aminoácidos que se estudian por sus roles en la recuperación y la función — abordados aquí con cuidado individualizado y conforme a la normativa.',
        [
            ('What peptides are', 'Qué son los péptidos',
             'Peptides occur naturally in the body and act as signaling molecules. Research is exploring several peptides in musculoskeletal and recovery contexts.',
             'Los péptidos se encuentran naturalmente en el cuerpo y actúan como moléculas de señalización. La investigación explora varios péptidos en contextos musculoesqueléticos y de recuperación.'),
            ('An individualized approach', 'Un enfoque individualizado',
             'There is no one-size-fits-all peptide plan. Your physician reviews your history, goals, risks, and alternatives before discussing any option.',
             'No existe un plan de péptidos único para todos. Su médico revisa su historial, objetivos, riesgos y alternativas antes de discutir cualquier opción.'),
            ('Compliance and candor', 'Cumplimiento y franqueza',
             'Some peptide uses are considered off-label. We explain the regulatory picture, the evidence, and the uncertainties plainly.',
             'Algunos usos de péptidos se consideran fuera de indicación. Explicamos claramente el panorama regulatorio, la evidencia y las incertidumbres.'),
        ],
        [
            ('Do I need labs first?', '¿Necesito análisis primero?',
             'Often, yes. Your physician will determine what evaluation is needed before any discussion of a peptide-related plan.',
             'A menudo, sí. Su médico determinará qué evaluación se necesita antes de cualquier discusión sobre un plan relacionado con péptidos.'),
            ('Are peptides safe?', '¿Son seguros los péptidos?',
             'Safety depends on the specific peptide, dose, source, and your health. That is exactly what the physician consultation is for.',
             'La seguridad depende del péptido específico, la dosis, la fuente y su salud. Para eso es precisamente la consulta médica.'),
        ],
        notice_kind='peptide')

def build_ketamine():
    return service_page('ketamine', 'Ketamine Infusion Center', 'Centro de infusión de ketamina',
        'Ketamine infusion center', 'Centro de infusión de ketamina',
        'Screened, monitored ketamine infusion care for selected pain and mood conditions — with safety protocols at every step.',
        'Cuidado de infusión de ketamina evaluado y monitoreado para condiciones seleccionadas de dolor y del estado de ánimo — con protocolos de seguridad en cada paso.',
        [
            ('Screening first', 'Primero la evaluación',
             'Candidacy begins with a thorough medical and psychiatric screening to determine whether infusion therapy is appropriate and safe for you.',
             'La candidatura comienza con una evaluación médica y psiquiátrica exhaustiva para determinar si la terapia de infusión es apropiada y segura para usted.'),
            ('A monitored setting', 'Un entorno monitoreado',
             'Infusions take place in a clinical setting with vital-sign monitoring and physician oversight throughout the session.',
             'Las infusiones se realizan en un entorno clínico con monitoreo de signos vitales y supervisión médica durante toda la sesión.'),
            ('Selected indications', 'Indicaciones seleccionadas',
             'Ketamine infusion is discussed for certain chronic pain and mood conditions, as an off-label use, when prior approaches have been inadequate — a decision made carefully with your physician.',
             'La infusión de ketamina se discute para ciertas condiciones crónicas de dolor y del estado de ánimo, como uso fuera de indicación, cuando los enfoques previos han sido inadecuados — una decisión tomada con cuidado junto a su médico.'),
            ('Ongoing assessment', 'Evaluación continua',
             'Response is reassessed over time, and the plan is adjusted — or stopped — based on benefit, side effects, and your goals.',
             'La respuesta se reevalúa en el tiempo, y el plan se ajusta — o se detiene — según el beneficio, los efectos secundarios y sus objetivos.'),
        ],
        [
            ('Is ketamine treatment safe?', '¿Es seguro el tratamiento con ketamina?',
             'When screened and monitored appropriately, ketamine infusion has an established safety record in clinical settings — but it is not without risks, which your physician will review with you.',
             'Cuando se evalúa y monitorea adecuadamente, la infusión de ketamina tiene un historial de seguridad establecido en entornos clínicos — pero no está exenta de riesgos, que su médico revisará con usted.'),
            ('Will I need multiple sessions?', '¿Necesitaré múltiples sesiones?',
             'Treatment courses vary. Your physician will propose a plan and reassess based on your response.',
             'Los cursos de tratamiento varían. Su médico le propondrá un plan y lo reevaluará según su respuesta.'),
            ('Can I drive after?', '¿Puedo conducir después?',
             'No — you will need a responsible adult to take you home after each session.',
             'No — necesitará que un adulto responsable le lleve a casa después de cada sesión.'),
        ],
        notice_kind='ketamine',
        guides=[('guides/ketamine-preparation-guide.html', 'Ketamine visit preparation guide (printable)', 'Guía de preparación para la visita de ketamina (imprimible)')])

def build_crps():
    return service_page('crps', 'CRPS Center', 'Centro de CRPS',
        'CRPS Center', 'Centro de CRPS',
        'Specialized evaluation and coordinated management for complex regional pain syndrome — a condition that deserves focused expertise.',
        'Evaluación especializada y manejo coordinado para el síndrome de dolor regional complejo — una condición que merece experiencia enfocada.',
        [
            ('Recognizing CRPS', 'Reconociendo el CRPS',
             'CRPS often follows an injury or surgery, with pain disproportionate to the event — plus changes in skin color or temperature, swelling, sweating, or movement difficulty in the affected limb.',
             'El CRPS a menudo sigue a una lesión o cirugía, con un dolor desproporcionado al evento — además de cambios en el color o la temperatura de la piel, hinchazón, sudoración o dificultad de movimiento en la extremidad afectada.'),
            ('How we evaluate', 'Cómo evaluamos',
             'Diagnosis is clinical, supported by careful history, examination, and exclusion of other causes. We review prior records and imaging to build the full picture.',
             'El diagnóstico es clínico, apoyado por un historial cuidadoso, examen y exclusión de otras causas. Revisamos registros e imágenes previas para construir el panorama completo.'),
            ('Coordinated management', 'Manejo coordinado',
             'Care may combine interventional options, rehabilitation coordination, medication stewardship, and — where fitting — infusion or regenerative evaluation. Plans are individualized and reassessed over time.',
             'El cuidado puede combinar opciones intervencionistas, coordinación de rehabilitación, manejo de medicamentos y — cuando corresponda — evaluación de infusión o regenerativa. Los planes son individualizados y se reevalúan en el tiempo.'),
            ('Second opinions welcome', 'Segundas opiniones bienvenidas',
             'CRPS is complex, and a fresh review can help. We offer structured second-opinion reviews for patients, physicians, and international cases.',
             'El CRPS es complejo y una revisión nueva puede ayudar. Ofrecemos revisiones estructuradas de segunda opinión para pacientes, médicos y casos internacionales.'),
        ],
        [
            ('Is CRPS curable?', '¿El CRPS tiene cura?',
             'There is no single cure, but early, coordinated care can improve function and reduce pain for many patients. We focus on realistic, measurable goals.',
             'No existe una cura única, pero el cuidado temprano y coordinado puede mejorar la función y reducir el dolor en muchos pacientes. Nos enfocamos en objetivos realistas y medibles.'),
            ('What should I bring?', '¿Qué debo llevar?',
             'Our preparation checklist below covers records, imaging, medication lists, and symptom notes that make your evaluation more productive.',
             'Nuestra lista de verificación a continuación cubre registros, imágenes, listas de medicamentos y notas de síntomas que hacen su evaluación más productiva.'),
        ],
        guides=[('guides/crps-preparation-checklist.html', 'CRPS preparation checklist (printable)', 'Lista de verificación de preparación para CRPS (imprimible)')])

# ============================ TELEHEALTH / SECOND OPINIONS ============================
def build_telehealth():
    body = page_hero('Telehealth', 'Telesalud',
        'Care from where you are', 'Cuidado desde donde esté',
        'Secure video visits for consultations, follow-ups, and second opinions — where clinically appropriate.',
        'Visitas por video seguro para consultas, seguimientos y segundas opiniones — cuando sea clínicamente apropiado.')
    body += f'''
<section><div class="wrap"><div class="two-col"><div>
  <div class="notice notice-info"><h4 data-en="Licensure &amp; location" data-es="Licencia y ubicación">{'Licencia y ubicación' if PAGE_LANG=='es' else 'Licensure &amp; location'}</h4>
  {t('Telehealth availability depends on where you are located, physician licensure, and applicable law. We confirm eligibility before scheduling your video visit.',
     'La disponibilidad de telesalud depende de dónde se encuentre usted, la licencia del médico y la ley aplicable. Confirmamos la elegibilidad antes de agendar su visita por video.', 'p')}</div>
  <div class="grid grid-2">
    <div class="card">{t('How it works', 'Cómo funciona', 'h3')}
    {t('1. Book a telehealth consultation below. 2. We confirm eligibility and send your secure video link. 3. Meet your physician from home.', '1. Reserve una consulta por telesalud abajo. 2. Confirmamos la elegibilidad y le enviamos su enlace de video seguro. 3. Reúnase con su médico desde su hogar.', 'p')}</div>
    <div class="card">{t('Good fit for', 'Adecuado para', 'h3')}
    {t('New consultations, follow-up visits, medication reviews, and second opinions — whenever a physical examination is not required.', 'Nuevas consultas, visitas de seguimiento, revisiones de medicamentos y segundas opiniones — cuando no se requiera un examen físico.', 'p')}</div>
    <div class="card">{t('What you need', 'Lo que necesita', 'h3')}
    {t('A smartphone, tablet, or computer with a camera, plus a quiet, private space. We will guide you through the connection.', 'Un teléfono inteligente, tableta o computadora con cámara, además de un espacio tranquilo y privado. Le guiaremos en la conexión.', 'p')}</div>
    <div class="card">{t('In-person when it matters', 'En persona cuando importa', 'h3')}
    {t('Some evaluations and all procedures require an in-person visit. Your physician will advise the right setting for your case.', 'Algunas evaluaciones y todos los procedimientos requieren una visita en persona. Su médico le indicará el entorno adecuado para su caso.', 'p')}</div>
  </div>
</div><div>
  <div class="card">{t('Book a telehealth visit', 'Reserve una visita por telesalud', 'h3')}
  {t('Choose the telehealth consultation at booking and pay securely through Stripe.',
     'Elija la consulta por telesalud al reservar y pague de forma segura a través de Stripe.', 'p')}
  <a class="btn btn-gold" href="booking.html" data-en="Schedule &amp; Pay" data-es="Agendar y pagar">{'Agendar y pagar' if PAGE_LANG=='es' else 'Schedule &amp; Pay'}</a></div>
</div></div></div></section>
'''
    return page('Telehealth | Boston Pain Center', 'Telesalud | Boston Pain Center', 'telehealth', body,
                desc_en='Secure video visits — eligibility, workflow, and booking.',
                desc_es='Visitas por video seguro — elegibilidad, proceso y reserva.')

def build_second():
    body = page_hero('Second Opinions', 'Segundas opiniones',
        'An independent review you can trust', 'Una revisión independiente en la que puede confiar',
        'For patients, physicians, and international cases — a structured, documented review of your diagnosis and options.',
        'Para pacientes, médicos y casos internacionales — una revisión estructurada y documentada de su diagnóstico y opciones.')
    body += f'''
<section><div class="wrap"><div class="grid grid-3">
  <div class="card">{t('For patients', 'Para pacientes', 'h3')}
  {t('Unclear diagnosis? Conflicting recommendations? We review your records and imaging and give you a clear, written assessment with options.',
     '¿Diagnóstico poco claro? ¿Recomendaciones contradictorias? Revisamos sus registros e imágenes y le damos una evaluación clara y escrita con opciones.', 'p')}</div>
  <div class="card">{t('For physicians', 'Para médicos', 'h3')}
  {t('Refer complex or refractory cases for an independent interventional or regenerative perspective — with timely, collegial communication back to you.',
     'Refiera casos complejos o refractarios para una perspectiva intervencionista o regenerativa independiente — con comunicación oportuna y colegiada de vuelta a usted.', 'p')}</div>
  <div class="card">{t('International', 'Internacional', 'h3')}
  {t('Remote record review and video consultation for patients abroad, with guidance on whether travel for care is warranted.',
     'Revisión remota de registros y consulta por video para pacientes en el extranjero, con orientación sobre si viajar para recibir cuidado está justificado.', 'p')}</div>
</div>
<div class="card" style="margin-top:26px"><div class="two-col"><div>
  {t('How a second opinion works', 'Cómo funciona una segunda opinión', 'h3')}
  {t('1. Book a second-opinion review. 2. Share your records and imaging through our secure process. 3. Receive a documented assessment with recommendations — by video or in person.',
     '1. Reserve una revisión de segunda opinión. 2. Comparta sus registros e imágenes a través de nuestro proceso seguro. 3. Reciba una evaluación documentada con recomendaciones — por video o en persona.', 'p')}
</div><div style="align-self:center">
  <a class="btn btn-gold" href="booking.html" data-en="Schedule &amp; Pay" data-es="Agendar y pagar">{'Agendar y pagar' if PAGE_LANG=='es' else 'Schedule &amp; Pay'}</a>
  <div style="margin-top:.8rem"><a href="professional-portal.html" data-en="Physicians: use the Professional Portal →" data-es="Médicos: use el Portal profesional →">{'Médicos: use el Portal profesional →' if PAGE_LANG=='es' else 'Physicians: use the Professional Portal →'}</a></div>
</div></div></div>
</div></section>
'''
    return page('Second Opinions | Boston Pain Center', 'Segundas opiniones | Boston Pain Center', 'second', body,
                desc_en='Independent second-opinion reviews for patients, physicians, and international cases.',
                desc_es='Revisiones independientes de segunda opinión para pacientes, médicos y casos internacionales.')

# ============================ PORTALS ============================
def build_professional():
    global PAGE_LANG
    body = page_hero('Professional Portal', 'Portal profesional',
        'A direct line for professionals', 'Una línea directa para profesionales',
        'For physicians, attorneys, employers, insurers, case managers, facilities, and international partners.',
        'Para médicos, abogados, empleadores, aseguradoras, gestores de casos, instituciones y socios internacionales.')
    body += f'''
<section><div class="wrap"><div class="two-col"><div>
  <div class="notice notice-demo"><h4>Demonstration intake</h4>
  <p style="margin:.3rem 0 0">This is a front-end demonstration. Submissions are not transmitted to a secure system yet. Do not include patient-identifiable information.</p></div>
  <div class="form-card"><form class="bpc-form" data-ref-prefix="BPC-PRO" novalidate>
    <div class="field"><label for="pf-org">Organization type *</label>
      <select id="pf-org" data-required><option value="">Select…</option>
      <option>Physician / Practice</option><option>Attorney / Law Firm</option><option>Employer</option>
      <option>Insurer / Payer</option><option>Case Manager</option><option>Hospital / Rehab Facility</option>
      <option>International Healthcare Partner</option><option>Media / Sponsorship</option><option>Other</option></select>
      <span class="err">Please choose an organization type.</span></div>
    <div class="grid grid-2">
      <div class="field"><label for="pf-name">Full name *</label><input id="pf-name" data-required autocomplete="name"><span class="err">Required.</span></div>
      <div class="field"><label for="pf-title">Title / Role</label><input id="pf-title" autocomplete="organization-title"></div>
    </div>
    <div class="grid grid-2">
      <div class="field"><label for="pf-email">Work email *</label><input id="pf-email" type="email" data-required autocomplete="email"><span class="err">Enter a valid email.</span></div>
      <div class="field"><label for="pf-phone">Phone *</label><input id="pf-phone" data-required data-validate="phone" autocomplete="tel"><span class="err">Enter a valid phone.</span></div>
    </div>
    <div class="field"><label for="pf-orgname">Organization name *</label><input id="pf-orgname" data-required autocomplete="organization"><span class="err">Required.</span></div>
    <div class="field"><label for="pf-req">Describe your request *</label><textarea id="pf-req" rows="5" data-required></textarea><span class="err">Required — do not include patient names or identifiers.</span></div>
    <div class="field"><label class="checkrow"><input type="checkbox" data-required><span>I understand this demonstration form is not a secure medical-record system, and I will not submit patient-identifiable information here.</span></label><span class="err">Please acknowledge to continue.</span></div>
    <button class="btn btn-navy" type="submit">Submit Request</button>
  </form>
  <div class="form-confirm"><h3>Request received</h3>
    <p>Thank you — a member of our team will follow up. Your reference number:</p>
    <div class="ref-number">BPC-PRO-…</div>
    <p class="kbd-hint">Save this number for your records.</p></div></div>
</div><div>
  <div class="card"><h3>Who uses this portal</h3>
  <p>Referring physicians · Attorneys &amp; law firms · Employers · Insurers · Case managers · Hospitals &amp; rehab facilities · International partners · Media &amp; sponsors</p></div>
  <div class="card" style="margin-top:18px"><h3>Prefer to talk?</h3>
  <p>Call <a href="tel:+16175550100">{PHONE_DISPLAY}</a> <span class="verify-note">Number to be verified</span></p></div>
</div></div></div></section>
'''
    return page('Professional Portal | Boston Pain Center', 'Portal profesional | Boston Pain Center', 'pro', body,
                default_lang='en',
                desc_en='Professional intake for physicians, attorneys, employers, insurers, and partners.')

def build_patient_portal():
    body = page_hero('Patient Portal', 'Portal del paciente',
        'Patient portal — demonstration', 'Portal del paciente — demostración',
        'Explore a preview of the future patient portal. Nothing here is connected to real records.',
        'Explore una vista previa del futuro portal del paciente. Nada aquí está conectado a registros reales.')
    body += f'''
<section><div class="wrap" style="max-width:760px">
  <div class="notice notice-demo"><h4 data-en="Demonstration only" data-es="Solo demostración">{'Solo demostración' if PAGE_LANG=='es' else 'Demonstration only'}</h4>
  {t('This is a non-production preview. Do not enter real personal or medical information.',
     'Esta es una vista previa no productiva. No ingrese información personal o médica real.', 'p')}</div>
  <div id="demoLoginWrap" class="form-card">
    <form id="demoLoginForm" novalidate>
      {t('Demo sign-in', 'Inicio de sesión de demostración', 'h3')}
      <div class="field"><label data-en="Email" data-es="Correo electrónico">{'Correo electrónico' if PAGE_LANG=='es' else 'Email'}</label><input type="email" {tph('you@example.com', 'usted@ejemplo.com')}></div>
      <div class="field"><label data-en="Password" data-es="Contraseña">{'Contraseña' if PAGE_LANG=='es' else 'Password'}</label><input type="password" {tph('Demo password', 'Contraseña de demostración')}></div>
      <button class="btn btn-teal" type="submit" data-en="Enter Demo" data-es="Entrar a la demostración">{'Entrar a la demostración' if PAGE_LANG=='es' else 'Enter Demo'}</button>
      <p class="kbd-hint" style="margin-top:.8rem" data-en="Any email and password will enter the demo." data-es="Cualquier correo y contraseña entrará a la demostración.">{'Cualquier correo y contraseña entrará a la demostración.' if PAGE_LANG=='es' else 'Any email and password will enter the demo.'}</p>
    </form>
  </div>
  <div id="demoDash" style="display:none">
    <div class="card">
      {t('Welcome to your portal preview', 'Bienvenido a la vista previa de su portal', 'h3')}
      <p><span class="verify-note" data-en="Sample data — demonstration only" data-es="Datos de muestra — solo demostración">{'Datos de muestra — solo demostración' if PAGE_LANG=='es' else 'Sample data — demonstration only'}</span></p>
      <div class="grid grid-2" style="margin-top:1rem">
        <div><strong data-en="Next visit (sample)" data-es="Próxima visita (muestra)">{'Próxima visita (muestra)' if PAGE_LANG=='es' else 'Next visit (sample)'}</strong><p data-en="Tue, Oct 6 · 10:30 AM — Follow-up" data-es="Mar, 6 oct · 10:30 AM — Seguimiento">{'Mar, 6 oct · 10:30 AM — Seguimiento' if PAGE_LANG=='es' else 'Tue, Oct 6 · 10:30 AM — Follow-up'}</p></div>
        <div><strong data-en="Messages (sample)" data-es="Mensajes (muestra)">{'Mensajes (muestra)' if PAGE_LANG=='es' else 'Messages (sample)'}</strong><p data-en="1 unread from your care team" data-es="1 sin leer de su equipo de cuidado">{'1 sin leer de su equipo de cuidado' if PAGE_LANG=='es' else '1 unread from your care team'}</p></div>
        <div><strong data-en="Prescriptions (sample)" data-es="Recetas (muestra)">{'Recetas (muestra)' if PAGE_LANG=='es' else 'Prescriptions (sample)'}</strong><p data-en="2 active" data-es="2 activas">{'2 activas' if PAGE_LANG=='es' else '2 active'}</p></div>
        <div><strong data-en="Documents (sample)" data-es="Documentos (muestra)">{'Documentos (muestra)' if PAGE_LANG=='es' else 'Documents (sample)'}</strong><p data-en="After-visit summary available" data-es="Resumen de visita disponible">{'Resumen de visita disponible' if PAGE_LANG=='es' else 'After-visit summary available'}</p></div>
      </div>
    </div>
  </div>
</div></section>
'''
    return page('Patient Portal Demo | Boston Pain Center', 'Demostración del portal | Boston Pain Center', 'patient-portal', body,
                desc_en='Demonstration preview of the future Boston Pain Center patient portal.',
                desc_es='Vista previa de demostración del futuro portal del paciente de Boston Pain Center.')

# ============================ PODCAST / VIDEO TIPS ============================
def build_podcast():
    body = page_hero('Dr. Feliz Podcast', 'Podcast del Dr. Feliz',
        'A weekly conversation on pain & recovery', 'Una conversación semanal sobre dolor y recuperación',
        'Dr. Roberto Feliz breaks down pain, regenerative medicine, and recovery in plain language — new episode every week.',
        'El Dr. Roberto Feliz explica el dolor, la medicina regenerativa y la recuperación en lenguaje claro — nuevo episodio cada semana.')
    body += f'''
<section><div class="wrap">
  <div id="podcastFeatured" style="margin-bottom:26px"></div>
  <div class="two-col"><div>
    {t('Episode archive', 'Archivo de episodios', 'h2')}
    <input id="podcastSearch" {tph('Search episodes…', 'Buscar episodios…')} style="width:100%;padding:12px 14px;border:1.5px solid var(--line);border-radius:10px;margin:.6rem 0" aria-label="Search">
    <div id="podcastFilters" class="filter-bar"></div>
    <div id="podcastList" class="grid" style="grid-template-columns:1fr"></div>
    <div id="podcastEmpty" class="empty-state" style="display:none"><div class="big">🎙️</div>
      {t('New episodes weekly — check back soon.', 'Nuevos episodios cada semana — vuelva pronto.', 'h3')}
      {t('Subscribe below and we will let you know when the next episode drops.', 'Suscríbase abajo y le avisaremos cuando salga el próximo episodio.', 'p')}</div>
  </div><div>
    <div class="card">{t('Never miss an episode', 'No se pierda ningún episodio', 'h3')}
    {t('Get a short email when a new weekly episode is published.', 'Reciba un correo breve cuando se publique un nuevo episodio semanal.', 'p')}
    <form class="bpc-form" data-ref-prefix="BPC-NEWS" novalidate>
      <div class="field"><label data-en="Email *" data-es="Correo electrónico *">{'Correo electrónico *' if PAGE_LANG=='es' else 'Email *'}</label>
      <input type="email" data-required {tph('you@example.com', 'usted@ejemplo.com')}><span class="err" data-en="Enter a valid email." data-es="Ingrese un correo válido.">{'Ingrese un correo válido.' if PAGE_LANG=='es' else 'Enter a valid email.'}</span></div>
      <button class="btn btn-teal btn-sm" type="submit" data-en="Subscribe" data-es="Suscribirse">{'Suscribirse' if PAGE_LANG=='es' else 'Subscribe'}</button>
    </form>
    <div class="form-confirm">{t('Subscribed!', '¡Suscripción lista!', 'h3')}
      {t('Your reference:', 'Su referencia:', 'p')}<div class="ref-number">BPC-NEWS-…</div></div></div>
    <div class="card" style="margin-top:18px">{t('Coming soon', 'Próximamente', 'h3')}
    {t('Spotify, Apple Podcasts, and YouTube integrations are on the roadmap.',
       'Las integraciones con Spotify, Apple Podcasts y YouTube están en camino.', 'p')}</div>
  </div></div>
</div></section>
'''
    return page('Dr. Feliz Podcast | Boston Pain Center', 'Podcast del Dr. Feliz | Boston Pain Center', 'podcast', body,
                desc_en='Weekly podcast with Dr. Roberto Feliz on pain, recovery, and regenerative medicine.',
                desc_es='Podcast semanal con el Dr. Roberto Feliz sobre dolor, recuperación y medicina regenerativa.')

def build_tips():
    body = page_hero('Daily Video Tips', 'Consejos diarios en video',
        'One short tip, every day', 'Un consejo breve, cada día',
        'Dr. Roberto Feliz shares a quick, practical video tip daily — movement, recovery, and living better with pain.',
        'El Dr. Roberto Feliz comparte un consejo breve y práctico en video cada día — movimiento, recuperación y vivir mejor con dolor.')
    body += f'''
<section><div class="wrap">
  <div id="tipsFeatured" style="margin-bottom:26px"></div>
  {t('Tip archive', 'Archivo de consejos', 'h2')}
  <input id="tipsSearch" {tph('Search tips…', 'Buscar consejos…')} style="width:100%;max-width:480px;padding:12px 14px;border:1.5px solid var(--line);border-radius:10px;margin:.6rem 0" aria-label="Search">
  <div id="tipsFilters" class="filter-bar"></div>
  <div id="tipsList" class="grid grid-2"></div>
  <div id="tipsEmpty" class="empty-state" style="display:none"><div class="big">▶</div>
    {t('New tips daily — check back soon.', 'Nuevos consejos cada día — vuelva pronto.', 'h3')}
    {t('Dr. Roberto Feliz posts a short video tip every day.', 'El Dr. Roberto Feliz publica un consejo breve en video cada día.', 'p')}</div>
  <div class="notice notice-info" style="margin-top:26px"><h4 data-en="Educational only" data-es="Solo educativo">{'Solo educativo' if PAGE_LANG=='es' else 'Educational only'}</h4>
  {t('Video tips are general education, not medical advice for your situation. Always consult your physician about your own care.',
     'Los consejos en video son educación general, no consejo médico para su situación. Siempre consulte a su médico sobre su propio cuidado.', 'p')}</div>
</div></section>
'''
    return page('Daily Video Tips | Boston Pain Center', 'Consejos diarios | Boston Pain Center', 'tips', body,
                desc_en='Daily short video tips with Dr. Roberto Feliz.',
                desc_es='Consejos breves diarios en video con el Dr. Roberto Feliz.')

# ============================ RESOURCES / BOOKING / CONTACT / PRIVACY ============================
def build_resources():
    guides = [
        ('guides/crps-preparation-checklist.html', '📋', 'CRPS preparation checklist', 'Lista de verificación de preparación para CRPS',
         'Records, imaging, medications, and symptom notes to bring.', 'Registros, imágenes, medicamentos y notas de síntomas para llevar.'),
        ('guides/prp-preparation-guide.html', '💉', 'PRP preparation guide', 'Guía de preparación para PRP',
         'Before and after your PRP visit.', 'Antes y después de su visita de PRP.'),
        ('guides/ketamine-preparation-guide.html', '💧', 'Ketamine visit preparation guide', 'Guía de preparación para la visita de ketamina',
         'Screening, what to expect, and aftercare.', 'Evaluación, qué esperar y cuidados posteriores.'),
    ]
    gc = '\n'.join(f'''<div class="card"><div class="icon-badge">{icon}</div>
      <h3 data-en="{esc(en)}" data-es="{esc(es)}">{esc(es if PAGE_LANG=='es' else en)}</h3>
      <p data-en="{esc(den)}" data-es="{esc(des)}">{esc(des if PAGE_LANG=='es' else den)}</p>
      <a class="btn btn-outline btn-sm" href="{h}" data-en="View &amp; Print" data-es="Ver e imprimir">{'Ver e imprimir' if PAGE_LANG=='es' else 'View &amp; Print'}</a></div>'''
      for h, icon, en, es, den, des in guides)
    body = page_hero('Patient Resources', 'Recursos para pacientes',
        'Prepare with confidence', 'Prepárese con confianza',
        'Checklists, preparation guides, and education to make every visit count.',
        'Listas de verificación, guías de preparación y educación para aprovechar cada visita.')
    body += f'''
<section><div class="wrap">
  {t('Downloadable guides', 'Guías descargables', 'h2')}<div class="gold-rule"></div>
  <div class="grid grid-3">{gc}</div>
  <div class="grid grid-2" style="margin-top:26px">
    <div class="card">{t('Your first visit', 'Su primera visita', 'h3')}
    {t('Bring prior imaging, procedure reports, a full medication list, and notes on what has — and has not — helped your pain.',
       'Traiga imágenes previas, informes de procedimientos, una lista completa de medicamentos y notas sobre lo que ha ayudado — y lo que no — a su dolor.', 'p')}</div>
    <div class="card">{t('Questions to ask', 'Preguntas para hacer', 'h3')}
    {t('What is the diagnosis? What are my options with benefits and risks? What happens if I do nothing? What is the realistic timeline?',
       '¿Cuál es el diagnóstico? ¿Cuáles son mis opciones con beneficios y riesgos? ¿Qué pasa si no hago nada? ¿Cuál es el plazo realista?', 'p')}</div>
  </div>
</div></section>
'''
    return page('Patient Resources | Boston Pain Center', 'Recursos para pacientes | Boston Pain Center', 'resources', body,
                desc_en='Preparation checklists and downloadable guides.',
                desc_es='Listas de verificación y guías descargables.')

def build_booking():
    body = page_hero('Schedule & Pay', 'Agendar y pagar',
        'Book your visit in minutes', 'Reserve su visita en minutos',
        'Choose your service, pick your details, and pay securely at booking through Stripe.',
        'Elija su servicio, complete sus datos y pague de forma segura al reservar a través de Stripe.')
    body += f'''
<section><div class="wrap" id="bookingApp">
  <div class="steps" id="bookSteps">
    <div class="step" data-en="1. Choose service" data-es="1. Elija el servicio">{'1. Elija el servicio' if PAGE_LANG=='es' else '1. Choose service'}</div>
    <div class="step" data-en="2. Your details" data-es="2. Sus datos">{'2. Sus datos' if PAGE_LANG=='es' else '2. Your details'}</div>
    <div class="step" data-en="3. Pay &amp; confirm" data-es="3. Pagar y confirmar">{'3. Pagar y confirmar' if PAGE_LANG=='es' else '3. Pay &amp; confirm'}</div>
  </div>
  <div class="notice notice-demo"><h4 data-en="Demonstration booking" data-es="Reserva de demostración">{'Reserva de demostración' if PAGE_LANG=='es' else 'Demonstration booking'}</h4>
  {t('This booking flow is a demonstration until a HIPAA-compliant backend is connected. Please do not enter sensitive medical details.',
     'Este flujo de reserva es una demostración hasta que se conecte un sistema compatible con HIPAA. Por favor no ingrese detalles médicos sensibles.', 'p')}</div>
  <div id="svcGrid" class="service-pick"></div>
  <div id="bookStep2" style="display:none"><div class="form-card">
    <h3><span data-en="Booking:" data-es="Reserva:">{'Reserva:' if PAGE_LANG=='es' else 'Booking:'}</span> <span id="chosenSvcName"></span></h3>
    <p><strong id="chosenSvcPrice"></strong></p>
    <form id="bookingForm" novalidate>
      <div class="grid grid-2">
        <div class="field"><label data-en="Full name *" data-es="Nombre completo *">{'Nombre completo *' if PAGE_LANG=='es' else 'Full name *'}</label><input data-required autocomplete="name"><span class="err" data-en="Required." data-es="Requerido.">{'Requerido.' if PAGE_LANG=='es' else 'Required.'}</span></div>
        <div class="field"><label data-en="Email *" data-es="Correo electrónico *">{'Correo electrónico *' if PAGE_LANG=='es' else 'Email *'}</label><input type="email" data-required autocomplete="email"><span class="err" data-en="Enter a valid email." data-es="Ingrese un correo válido.">{'Ingrese un correo válido.' if PAGE_LANG=='es' else 'Enter a valid email.'}</span></div>
      </div>
      <div class="grid grid-2">
        <div class="field"><label data-en="Phone *" data-es="Teléfono *">{'Teléfono *' if PAGE_LANG=='es' else 'Phone *'}</label><input data-required data-validate="phone" autocomplete="tel"><span class="err" data-en="Enter a valid phone." data-es="Ingrese un teléfono válido.">{'Ingrese un teléfono válido.' if PAGE_LANG=='es' else 'Enter a valid phone.'}</span></div>
        <div class="field"><label data-en="Preferred date" data-es="Fecha preferida">{'Fecha preferida' if PAGE_LANG=='es' else 'Preferred date'}</label><input type="date"></div>
      </div>
      <div class="field"><label data-en="Visit type" data-es="Tipo de visita">{'Tipo de visita' if PAGE_LANG=='es' else 'Visit type'}</label>
        <select><option data-en="In person" data-es="En persona">{'En persona' if PAGE_LANG=='es' else 'In person'}</option><option data-en="Telehealth (where eligible)" data-es="Telesalud (donde sea elegible)">{'Telesalud (donde sea elegible)' if PAGE_LANG=='es' else 'Telehealth (where eligible)'}</option></select></div>
      <div class="field"><label data-en="Brief reason for visit" data-es="Motivo breve de la visita">{'Motivo breve de la visita' if PAGE_LANG=='es' else 'Brief reason for visit'}</label><textarea rows="3" {tph('e.g. lower back pain for 6 months', 'ej. dolor lumbar desde hace 6 meses')}></textarea></div>
      <div class="field"><label class="checkrow"><input type="checkbox" data-required><span data-en="I understand this is a demonstration booking and not a secure medical record." data-es="Entiendo que esta es una reserva de demostración y no un registro médico seguro.">{'Entiendo que esta es una reserva de demostración y no un registro médico seguro.' if PAGE_LANG=='es' else 'I understand this is a demonstration booking and not a secure medical record.'}</span></label><span class="err" data-en="Please acknowledge to continue." data-es="Por favor confirme para continuar.">{'Por favor confirme para continuar.' if PAGE_LANG=='es' else 'Please acknowledge to continue.'}</span></div>
      <button class="btn btn-gold" type="submit" data-en="Continue to Payment" data-es="Continuar al pago">{'Continuar al pago' if PAGE_LANG=='es' else 'Continue to Payment'}</button>
    </form>
  </div></div>
  <div id="bookStep3" style="display:none"><div class="form-card" style="text-align:center">
    {t('Booking registered!', '¡Reserva registrada!', 'h2')}
    {t('Service:', 'Servicio:', 'p')}<p><strong id="bookSvcEcho"></strong></p>
    {t('Your booking reference:', 'Su referencia de reserva:', 'p')}<div class="ref-number" id="bookRef">BPC-BOOK-…</div>
    <div id="payZone" style="margin-top:1rem"></div>
    <p class="kbd-hint" style="margin-top:1.2rem" data-en="We will contact you to confirm your appointment time." data-es="Nos pondremos en contacto para confirmar el horario de su cita.">{'Nos pondremos en contacto para confirmar el horario de su cita.' if PAGE_LANG=='es' else 'We will contact you to confirm your appointment time.'}</p>
  </div></div>
</div></section>
'''
    return page('Schedule & Pay | Boston Pain Center', 'Agendar y pagar | Boston Pain Center', 'booking', body,
                desc_en='Book your consultation and pay securely at booking through Stripe.',
                desc_es='Reserve su consulta y pague de forma segura al reservar a través de Stripe.')

def build_contact():
    body = page_hero('Contact', 'Contacto',
        'We are here to help', 'Estamos aquí para ayudarle',
        'Call, write, or send an inquiry — in English or Spanish.',
        'Llámenos, escríbanos o envíe una consulta — en inglés o español.')
    body += f'''
<section><div class="wrap"><div class="two-col"><div>
  <div class="grid grid-2">
    <div class="card">{t('Call us', 'Llámenos', 'h3')}<p><a href="tel:+16175550100" style="font-size:1.2rem;font-weight:700">{PHONE_DISPLAY}</a></p>{t('Number to be verified before launch.', 'Número por verificar antes del lanzamiento.', 'p', 'kbd-hint')}</div>
    <div class="card">{t('Visit us', 'Visítenos', 'h3')}{t('Boston, Massachusetts', 'Boston, Massachusetts', 'p')}{t('Street address to be verified before launch.', 'Dirección por verificar antes del lanzamiento.', 'p', 'kbd-hint')}</div>
  </div>
  <div class="notice notice-emergency" style="margin-top:22px"><h4 data-en="In an emergency" data-es="En una emergencia">{'En una emergencia' if PAGE_LANG=='es' else 'In an emergency'}</h4>
  {t('Call 911 or go to your nearest emergency department. Do not use this form for urgent medical needs.',
     'Llame al 911 o acuda al departamento de emergencias más cercano. No use este formulario para necesidades médicas urgentes.', 'p')}</div>
  <div class="form-card" style="margin-top:22px"><form class="bpc-form" data-ref-prefix="BPC" novalidate>
    {t('Send an inquiry', 'Envíe una consulta', 'h3')}
    <div class="grid grid-2">
      <div class="field"><label data-en="Full name *" data-es="Nombre completo *">{'Nombre completo *' if PAGE_LANG=='es' else 'Full name *'}</label><input data-required autocomplete="name"><span class="err" data-en="Required." data-es="Requerido.">{'Requerido.' if PAGE_LANG=='es' else 'Required.'}</span></div>
      <div class="field"><label data-en="Email *" data-es="Correo electrónico *">{'Correo electrónico *' if PAGE_LANG=='es' else 'Email *'}</label><input type="email" data-required autocomplete="email"><span class="err" data-en="Enter a valid email." data-es="Ingrese un correo válido.">{'Ingrese un correo válido.' if PAGE_LANG=='es' else 'Enter a valid email.'}</span></div>
    </div>
    <div class="field"><label data-en="Phone" data-es="Teléfono">{'Teléfono' if PAGE_LANG=='es' else 'Phone'}</label><input data-validate="phone" autocomplete="tel"><span class="err" data-en="Enter a valid phone." data-es="Ingrese un teléfono válido.">{'Ingrese un teléfono válido.' if PAGE_LANG=='es' else 'Enter a valid phone.'}</span></div>
    <div class="field"><label data-en="Topic *" data-es="Tema *">{'Tema *' if PAGE_LANG=='es' else 'Topic *'}</label>
      <select data-required><option value="">—</option>
      <option data-en="New appointment" data-es="Nueva cita">{'Nueva cita' if PAGE_LANG=='es' else 'New appointment'}</option>
      <option data-en="Telehealth" data-es="Telesalud">{'Telesalud' if PAGE_LANG=='es' else 'Telehealth'}</option>
      <option data-en="Second opinion" data-es="Segunda opinión">{'Segunda opinión' if PAGE_LANG=='es' else 'Second opinion'}</option>
      <option data-en="Billing / payment" data-es="Facturación / pago">{'Facturación / pago' if PAGE_LANG=='es' else 'Billing / payment'}</option>
      <option data-en="Other" data-es="Otro">{'Otro' if PAGE_LANG=='es' else 'Other'}</option></select>
      <span class="err" data-en="Please choose a topic." data-es="Elija un tema.">{'Elija un tema.' if PAGE_LANG=='es' else 'Please choose a topic.'}</span></div>
    <div class="field"><label data-en="Message *" data-es="Mensaje *">{'Mensaje *' if PAGE_LANG=='es' else 'Message *'}</label><textarea rows="5" data-required {tph('How can we help?', '¿Cómo podemos ayudarle?')}></textarea><span class="err" data-en="Required — please do not include sensitive medical details." data-es="Requerido — no incluya detalles médicos sensibles.">{'Requerido — no incluya detalles médicos sensibles.' if PAGE_LANG=='es' else 'Required — please do not include sensitive medical details.'}</span></div>
    <div class="field"><label class="checkrow"><input type="checkbox" data-required><span data-en="I understand this demonstration form is not a secure medical record." data-es="Entiendo que este formulario de demostración no es un registro médico seguro.">{'Entiendo que este formulario de demostración no es un registro médico seguro.' if PAGE_LANG=='es' else 'I understand this demonstration form is not a secure medical record.'}</span></label><span class="err" data-en="Please acknowledge to continue." data-es="Por favor confirme para continuar.">{'Por favor confirme para continuar.' if PAGE_LANG=='es' else 'Please acknowledge to continue.'}</span></div>
    <button class="btn btn-teal" type="submit" data-en="Send Inquiry" data-es="Enviar consulta">{'Enviar consulta' if PAGE_LANG=='es' else 'Send Inquiry'}</button>
  </form>
  <div class="form-confirm">{t('Inquiry received', 'Consulta recibida', 'h3')}
    {t('Thank you — we will be in touch. Your reference number:', 'Gracias — nos pondremos en contacto. Su número de referencia:', 'p')}
    <div class="ref-number">BPC-…</div></div></div>
</div><div>
  <div class="card">{t('Prefer to book directly?', '¿Prefiere reservar directamente?', 'h3')}
  {t('Choose your service and pay securely at booking.', 'Elija su servicio y pague de forma segura al reservar.', 'p')}
  <a class="btn btn-gold" href="booking.html" data-en="Schedule &amp; Pay" data-es="Agendar y pagar">{'Agendar y pagar' if PAGE_LANG=='es' else 'Schedule &amp; Pay'}</a></div>
  <div class="card" style="margin-top:18px">{t('Hours', 'Horario', 'h3')}
  {t('Hours to be verified before launch.', 'Horario por verificar antes del lanzamiento.', 'p', 'kbd-hint')}</div>
</div></div></div></section>
'''
    return page('Contact | Boston Pain Center', 'Contacto | Boston Pain Center', 'contact', body,
                desc_en='Contact Boston Pain Center — call, visit, or send an inquiry.',
                desc_es='Contacte a Boston Pain Center — llame, visítenos o envíe una consulta.')

def build_privacy():
    body = page_hero('Privacy & Medical Disclaimer', 'Privacidad y descargo médico',
        'How we handle information — and what this site is', 'Cómo manejamos la información — y qué es este sitio',
        'Plain-language privacy notice and medical disclaimer for bostonpaincenter.com.',
        'Aviso de privacidad y descargo médico en lenguaje claro para este sitio.')
    body += f'''
<section><div class="wrap" style="max-width:820px">
  <div class="card">{t('Privacy notice (website)', 'Aviso de privacidad (sitio web)', 'h3')}
  {t('This website is informational. Demonstration forms on this site do not transmit to a secure medical-record system. Please do not submit sensitive medical details through website forms until a HIPAA-compliant backend is connected and announced.',
     'Este sitio web es informativo. Los formularios de demostración de este sitio no se transmiten a un sistema seguro de registros médicos. Por favor no envíe detalles médicos sensibles a través de los formularios del sitio hasta que se conecte y anuncie un sistema compatible con HIPAA.', 'p')}
  {t('Payment information entered at booking is processed by Stripe on Stripe’s secure pages. Boston Pain Center does not see or store your card details.',
     'La información de pago ingresada al reservar es procesada por Stripe en las páginas seguras de Stripe. Boston Pain Center no ve ni almacena los datos de su tarjeta.', 'p')}</div>
  <div class="card" style="margin-top:18px">{t('Medical disclaimer', 'Descargo médico', 'h3')}
  {t('Content on this site — including articles, video tips, and podcast episodes — is for general education only and is not medical advice for your situation. It does not create a physician–patient relationship. Always seek the advice of your physician or another qualified health provider with questions about a medical condition.',
     'El contenido de este sitio — incluyendo artículos, consejos en video y episodios del podcast — es solo para educación general y no es consejo médico para su situación. No crea una relación médico–paciente. Siempre busque el consejo de su médico u otro proveedor de salud calificado si tiene preguntas sobre una condición médica.', 'p')}
  {t('Never disregard professional medical advice or delay seeking it because of something you read, heard, or saw here.',
     'Nunca ignore el consejo médico profesional ni demore en buscarlo por algo que leyó, escuchó o vio aquí.', 'p')}</div>
  <div class="card" style="margin-top:18px">{t('Investigational & off-label language', 'Lenguaje sobre investigación y uso fuera de indicación', 'h3')}
  {t('Some therapies discussed on this site — including certain stem cell, exosome, peptide, and ketamine applications — are investigational or used off-label. Availability follows careful physician evaluation and applicable law. Nothing on this site promises any outcome.',
     'Algunas terapias discutidas en este sitio — incluyendo ciertas aplicaciones de células madre, exosomas, péptidos y ketamina — son de investigación o de uso fuera de indicación. La disponibilidad sigue una cuidadosa evaluación médica y la ley aplicable. Nada en este sitio promete ningún resultado.', 'p')}</div>
  <div class="notice notice-emergency">{t('If you are experiencing a medical emergency, call 911 or go to your nearest emergency department immediately.',
     'Si está experimentando una emergencia médica, llame al 911 o acuda de inmediato al departamento de emergencias más cercano.', 'p')}</div>
</div></section>
'''
    return page('Privacy & Medical Disclaimer | Boston Pain Center', 'Privacidad y descargo | Boston Pain Center', 'privacy', body,
                desc_en='Privacy notice and medical disclaimer.',
                desc_es='Aviso de privacidad y descargo médico.')

# ============================ PRINTABLE GUIDES ============================
def guide_shell(title_en, title_es, inner):
    title = title_es if PAGE_LANG == 'es' else title_en
    return f'''<!DOCTYPE html>
<html lang="{PAGE_LANG}" data-default-lang="{PAGE_LANG}">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title data-en="{esc(title_en)}" data-es="{esc(title_es)}">{esc(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/css/style.css"></head>
<body>
<div class="wrap no-print" style="padding:18px 22px;display:flex;justify-content:space-between;align-items:center">
  <a href="../patient-resources.html" style="font-weight:700" data-en="← Back to Resources" data-es="← Volver a recursos">{'← Volver a recursos' if PAGE_LANG=='es' else '← Back to Resources'}</a>
  <div style="display:flex;gap:10px;align-items:center">
    <div class="lang-toggle" role="group" aria-label="Language"><button data-lang="en">EN</button><button data-lang="es">ES</button></div>
    <button class="btn btn-teal btn-sm" onclick="window.print()" data-en="Print / Save PDF" data-es="Imprimir / Guardar PDF">{'Imprimir / Guardar PDF' if PAGE_LANG=='es' else 'Print / Save PDF'}</button>
  </div>
</div>
<main class="wrap"><div class="guide" style="margin:10px 0 40px">
  <p><strong>Boston Pain Center</strong> · <span data-en="Boston, Massachusetts" data-es="Boston, Massachusetts">Boston, Massachusetts</span></p>
  {inner}
  <div class="notice notice-emergency no-print" style="margin-top:24px"><p style="margin:0" data-en="Medical emergency? Call 911." data-es="¿Emergencia médica? Llame al 911.">{'¿Emergencia médica? Llame al 911.' if PAGE_LANG=='es' else 'Medical emergency? Call 911.'}</p></div>
  <p class="kbd-hint" data-en="Educational material — not medical advice. Bring questions to your visit." data-es="Material educativo — no es consejo médico. Lleve sus preguntas a su visita.">{'Material educativo — no es consejo médico. Lleve sus preguntas a su visita.' if PAGE_LANG=='es' else 'Educational material — not medical advice. Bring questions to your visit.'}</p>
</div>
<div class="emergency-strip no-print" role="alert"><span data-en="Medical emergency? Call " data-es="¿Emergencia médica? Llame al ">¿Emergencia médica? Llame al </span><a href="tel:911">911</a></div>
</main>
<script src="../assets/js/main.js"></script>
</body></html>'''

def build_guide_crps():
    inner = f'''
{t('CRPS Preparation Checklist', 'Lista de verificación de preparación para CRPS', 'h2')}
{t('Bring these to your CRPS evaluation — the more complete your records, the more productive your visit.',
   'Traiga estos elementos a su evaluación de CRPS — mientras más completos sean sus registros, más productiva será su visita.', 'p', 'lead')}
<h3 data-en="Records &amp; imaging" data-es="Registros e imágenes">{'Registros e imágenes' if PAGE_LANG=='es' else 'Records &amp; imaging'}</h3>
<ul class="checklist">
  <li data-en="Prior diagnoses and physician notes related to your pain" data-es="Diagnósticos previos y notas médicas relacionadas con su dolor">{'Diagnósticos previos y notas médicas relacionadas con su dolor' if PAGE_LANG=='es' else 'Prior diagnoses and physician notes related to your pain'}</li>
  <li data-en="MRI, X-ray, CT, or nerve study reports (and discs/USBs if you have them)" data-es="Informes de resonancia, rayos X, tomografía o estudios de nervios (y discos/USB si los tiene)">{'Informes de resonancia, rayos X, tomografía o estudios de nervios (y discos/USB si los tiene)' if PAGE_LANG=='es' else 'MRI, X-ray, CT, or nerve study reports (and discs/USBs if you have them)'}</li>
  <li data-en="Surgical or procedure reports, if any" data-es="Informes quirúrgicos o de procedimientos, si los hay">{'Informes quirúrgicos o de procedimientos, si los hay' if PAGE_LANG=='es' else 'Surgical or procedure reports, if any'}</li>
  <li data-en="Physical or occupational therapy notes" data-es="Notas de terapia física u ocupacional">{'Notas de terapia física u ocupacional' if PAGE_LANG=='es' else 'Physical or occupational therapy notes'}</li>
</ul>
<h3 data-en="Medications &amp; history" data-es="Medicamentos e historial">{'Medicamentos e historial' if PAGE_LANG=='es' else 'Medications &amp; history'}</h3>
<ul class="checklist">
  <li data-en="Complete medication list with doses — including over-the-counter and supplements" data-es="Lista completa de medicamentos con dosis — incluyendo los de venta libre y suplementos">{'Lista completa de medicamentos con dosis — incluyendo los de venta libre y suplementos' if PAGE_LANG=='es' else 'Complete medication list with doses — including over-the-counter and supplements'}</li>
  <li data-en="Allergies (medications, latex, contrast dye)" data-es="Alergias (medicamentos, látex, medio de contraste)">{'Alergias (medicamentos, látex, medio de contraste)' if PAGE_LANG=='es' else 'Allergies (medications, latex, contrast dye)'}</li>
  <li data-en="What treatments you have tried and how each worked" data-es="Qué tratamientos ha probado y cómo funcionó cada uno">{'Qué tratamientos ha probado y cómo funcionó cada uno' if PAGE_LANG=='es' else 'What treatments you have tried and how each worked'}</li>
</ul>
<h3 data-en="Your symptom notes" data-es="Sus notas de síntomas">{'Sus notas de síntomas' if PAGE_LANG=='es' else 'Your symptom notes'}</h3>
<ul class="checklist">
  <li data-en="When the pain started and what triggered it" data-es="Cuándo comenzó el dolor y qué lo desencadenó">{'Cuándo comenzó el dolor y qué lo desencadenó' if PAGE_LANG=='es' else 'When the pain started and what triggered it'}</li>
  <li data-en="Skin changes: color, temperature, swelling, sweating" data-es="Cambios en la piel: color, temperatura, hinchazón, sudoración">{'Cambios en la piel: color, temperatura, hinchazón, sudoración' if PAGE_LANG=='es' else 'Skin changes: color, temperature, swelling, sweating'}</li>
  <li data-en="What makes it better or worse (movement, touch, weather, stress)" data-es="Qué lo mejora o empeora (movimiento, tacto, clima, estrés)">{'Qué lo mejora o empeora (movimiento, tacto, clima, estrés)' if PAGE_LANG=='es' else 'What makes it better or worse (movement, touch, weather, stress)'}</li>
  <li data-en="How pain affects sleep, work, and daily activities" data-es="Cómo el dolor afecta el sueño, el trabajo y las actividades diarias">{'Cómo el dolor afecta el sueño, el trabajo y las actividades diarias' if PAGE_LANG=='es' else 'How pain affects sleep, work, and daily activities'}</li>
</ul>'''
    return guide_shell('CRPS Preparation Checklist', 'Lista de preparación para CRPS', inner)

def build_guide_prp():
    inner = f'''
{t('PRP Preparation Guide', 'Guía de preparación para PRP', 'h2')}
{t('How to prepare for — and recover from — your platelet-rich plasma visit.',
   'Cómo prepararse para — y recuperarse de — su visita de plasma rico en plaquetas.', 'p', 'lead')}
<h3 data-en="Before your visit" data-es="Antes de su visita">{'Antes de su visita' if PAGE_LANG=='es' else 'Before your visit'}</h3>
<ul class="checklist">
  <li data-en="Tell your physician about all medications — especially blood thinners and anti-inflammatories" data-es="Informe a su médico sobre todos los medicamentos — especialmente anticoagulantes y antiinflamatorios">{'Informe a su médico sobre todos los medicamentos — especialmente anticoagulantes y antiinflamatorios' if PAGE_LANG=='es' else 'Tell your physician about all medications — especially blood thinners and anti-inflammatories'}</li>
  <li data-en="Stay hydrated the day before and the day of" data-es="Manténgase hidratado el día anterior y el día de la visita">{'Manténgase hidratado el día anterior y el día de la visita' if PAGE_LANG=='es' else 'Stay hydrated the day before and the day of'}</li>
  <li data-en="Eat normally unless instructed otherwise" data-es="Coma normalmente a menos que se le indique lo contrario">{'Coma normalmente a menos que se le indique lo contrario' if PAGE_LANG=='es' else 'Eat normally unless instructed otherwise'}</li>
  <li data-en="Bring prior imaging of the treatment area" data-es="Traiga imágenes previas del área de tratamiento">{'Traiga imágenes previas del área de tratamiento' if PAGE_LANG=='es' else 'Bring prior imaging of the treatment area'}</li>
  <li data-en="Arrange a ride if the treatment area affects driving comfort" data-es="Organice transporte si el área de tratamiento afecta su comodidad al conducir">{'Organice transporte si el área de tratamiento afecta su comodidad al conducir' if PAGE_LANG=='es' else 'Arrange a ride if the treatment area affects driving comfort'}</li>
</ul>
<h3 data-en="After your visit" data-es="Después de su visita">{'Después de su visita' if PAGE_LANG=='es' else 'After your visit'}</h3>
<ul class="checklist">
  <li data-en="Expect mild soreness for a few days — this is common" data-es="Espere una molestia leve por unos días — esto es común">{'Espere una molestia leve por unos días — esto es común' if PAGE_LANG=='es' else 'Expect mild soreness for a few days — this is common'}</li>
  <li data-en="Follow your physician’s guidance on activity and anti-inflammatory medications" data-es="Siga las indicaciones de su médico sobre actividad y medicamentos antiinflamatorios">{'Siga las indicaciones de su médico sobre actividad y medicamentos antiinflamatorios' if PAGE_LANG=='es' else 'Follow your physician’s guidance on activity and anti-inflammatory medications'}</li>
  <li data-en="Ice as directed; keep the area clean" data-es="Aplique hielo según lo indicado; mantenga el área limpia">{'Aplique hielo según lo indicado; mantenga el área limpia' if PAGE_LANG=='es' else 'Ice as directed; keep the area clean'}</li>
  <li data-en="Call us promptly for fever, severe swelling, or worsening pain" data-es="Llámenos de inmediato si tiene fiebre, hinchazón severa o empeoramiento del dolor">{'Llámenos de inmediato si tiene fiebre, hinchazón severa o empeoramiento del dolor' if PAGE_LANG=='es' else 'Call us promptly for fever, severe swelling, or worsening pain'}</li>
</ul>'''
    return guide_shell('PRP Preparation Guide', 'Guía de preparación para PRP', inner)

def build_guide_ketamine():
    inner = f'''
{t('Ketamine Visit Preparation Guide', 'Guía de preparación para la visita de ketamina', 'h2')}
{t('Screening, what to expect on infusion day, and aftercare.',
   'Evaluación, qué esperar el día de la infusión y cuidados posteriores.', 'p', 'lead')}
<h3 data-en="Screening" data-es="Evaluación">{'Evaluación' if PAGE_LANG=='es' else 'Screening'}</h3>
<ul class="checklist">
  <li data-en="Complete medical and psychiatric screening honestly — it determines safety and candidacy" data-es="Complete la evaluación médica y psiquiátrica con honestidad — determina la seguridad y la candidatura">{'Complete la evaluación médica y psiquiátrica con honestidad — determina la seguridad y la candidatura' if PAGE_LANG=='es' else 'Complete medical and psychiatric screening honestly — it determines safety and candidacy'}</li>
  <li data-en="List all medications, substances, and supplements" data-es="Liste todos los medicamentos, sustancias y suplementos">{'Liste todos los medicamentos, sustancias y suplementos' if PAGE_LANG=='es' else 'List all medications, substances, and supplements'}</li>
  <li data-en="Disclose heart, liver, bladder, or psychiatric history in detail" data-es="Informe en detalle antecedentes cardíacos, hepáticos, vesicales o psiquiátricos">{'Informe en detalle antecedentes cardíacos, hepáticos, vesicales o psiquiátricos' if PAGE_LANG=='es' else 'Disclose heart, liver, bladder, or psychiatric history in detail'}</li>
</ul>
<h3 data-en="On infusion day" data-es="El día de la infusión">{'El día de la infusión' if PAGE_LANG=='es' else 'On infusion day'}</h3>
<ul class="checklist">
  <li data-en="You MUST have a responsible adult drive you home — no driving after the session" data-es="DEBE tener un adulto responsable que le lleve a casa — no conduzca después de la sesión">{'DEBE tener un adulto responsable que le lleve a casa — no conduzca después de la sesión' if PAGE_LANG=='es' else 'You MUST have a responsible adult drive you home — no driving after the session'}</li>
  <li data-en="Follow fasting instructions given at screening" data-es="Siga las instrucciones de ayuno dadas en la evaluación">{'Siga las instrucciones de ayuno dadas en la evaluación' if PAGE_LANG=='es' else 'Follow fasting instructions given at screening'}</li>
  <li data-en="Wear comfortable clothing; bring a list of current medications" data-es="Use ropa cómoda; traiga una lista de sus medicamentos actuales">{'Use ropa cómoda; traiga una lista de sus medicamentos actuales' if PAGE_LANG=='es' else 'Wear comfortable clothing; bring a list of current medications'}</li>
  <li data-en="Plan a calm, restful remainder of the day" data-es="Planifique un resto del día tranquilo y de descanso">{'Planifique un resto del día tranquilo y de descanso' if PAGE_LANG=='es' else 'Plan a calm, restful remainder of the day'}</li>
</ul>
<h3 data-en="Aftercare" data-es="Cuidados posteriores">{'Cuidados posteriores' if PAGE_LANG=='es' else 'Aftercare'}</h3>
<ul class="checklist">
  <li data-en="Rest; avoid alcohol and driving for 24 hours" data-es="Descanse; evite el alcohol y conducir por 24 horas">{'Descanse; evite el alcohol y conducir por 24 horas' if PAGE_LANG=='es' else 'Rest; avoid alcohol and driving for 24 hours'}</li>
  <li data-en="Note your response — it guides the ongoing plan" data-es="Anote su respuesta — guía el plan continuo">{'Anote su respuesta — guía el plan continuo' if PAGE_LANG=='es' else 'Note your response — it guides the ongoing plan'}</li>
  <li data-en="Attend scheduled follow-ups; report side effects promptly" data-es="Asista a los seguimientos programados; reporte efectos secundarios de inmediato">{'Asista a los seguimientos programados; reporte efectos secundarios de inmediato' if PAGE_LANG=='es' else 'Attend scheduled follow-ups; report side effects promptly'}</li>
</ul>'''
    return guide_shell('Ketamine Visit Preparation Guide', 'Guía de preparación para ketamina', inner)

# ============================ MAIN ============================
def main():
    global PAGE_LANG
    os.makedirs(os.path.join(ROOT, 'guides'), exist_ok=True)
    jobs = [
        ('index.html', 'es', build_index),
        ('about.html', 'es', build_about),
        ('dr-roberto-feliz.html', 'es', build_roberto),
        ('dr-eddie-feliz.html', 'es', build_eddie),
        ('pain-management.html', 'es', build_pain),
        ('regenerative-medicine.html', 'es', build_regen_hub),
        ('prp-therapy.html', 'es', build_prp),
        ('stem-cell-therapy.html', 'es', build_stem),
        ('exosome-therapy.html', 'es', build_exosome),
        ('peptide-therapy.html', 'es', build_peptide),
        ('ketamine-infusion.html', 'es', build_ketamine),
        ('crps-center.html', 'es', build_crps),
        ('telehealth.html', 'es', build_telehealth),
        ('second-opinions.html', 'es', build_second),
        ('professional-portal.html', 'en', build_professional),
        ('patient-portal.html', 'es', build_patient_portal),
        ('podcast.html', 'es', build_podcast),
        ('video-tips.html', 'es', build_tips),
        ('patient-resources.html', 'es', build_resources),
        ('booking.html', 'es', build_booking),
        ('contact.html', 'es', build_contact),
        ('privacy-disclaimer.html', 'es', build_privacy),
    ]
    for name, lang, fn in jobs:
        PAGE_LANG = lang
        write(name, fn())
    PAGE_LANG = 'es'
    write('guides/crps-preparation-checklist.html', build_guide_crps())
    write('guides/prp-preparation-guide.html', build_guide_prp())
    write('guides/ketamine-preparation-guide.html', build_guide_ketamine())
    # 404 page
    PAGE_LANG = 'es'
    notfound = page('Page Not Found | Boston Pain Center', 'Página no encontrada | Boston Pain Center', 'home',
        '<section><div class="wrap" style="text-align:center;padding:80px 0">' +
        t('Page not found', 'Página no encontrada', 'h1') +
        t('The page you are looking for does not exist or has moved.', 'La página que busca no existe o ha sido movida.', 'p') +
        '<a class="btn btn-teal" href="index.html" data-en="Back to Home" data-es="Volver al inicio">Volver al inicio</a></div></section>')
    write('404.html', notfound)
    # favicon
    fav = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><circle cx="32" cy="32" r="30" fill="#0d2b45"/><text x="32" y="43" font-family="Georgia,serif" font-size="34" font-weight="bold" fill="#c19a5b" text-anchor="middle">B</text></svg>'''
    with open(os.path.join(ROOT, 'assets', 'favicon.svg'), 'w') as f:
        f.write(fav)
    print('build complete')

if __name__ == '__main__':
    main()
