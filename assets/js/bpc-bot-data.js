/* Boston Pain Center — visitor assistant knowledge base (v1, FAQ rules-based, $0).
   Every answer is grounded in the site's own published content. No prices,
   hours, insurance acceptance, or physician credentials are asserted here,
   because the site does not publish them yet: contact details are flagged
   "to be verified" exactly as the site flags them. Nothing here is medical
   advice for an individual case. No network requests are made by the bot. */
window.BPC_BOT_DATA = {
  ui: {
    en: {
      title: "Boston Pain Center Assistant",
      placeholder: "Ask about services, booking, telehealth…",
      send: "Send",
      close: "Close chat",
      open: "Chat with the visitor assistant",
      disclaimer: "Educational information only — not medical advice.",
      chips: ["Services", "Request a consultation", "Contact", "Telehealth", "Second opinion"]
    },
    es: {
      title: "Asistente de Boston Pain Center",
      placeholder: "Pregunte sobre servicios, consultas, telesalud…",
      send: "Enviar",
      close: "Cerrar chat",
      open: "Chatear con el asistente",
      disclaimer: "Solo información educativa — no es consejo médico.",
      chips: ["Servicios", "Solicitar una consulta", "Contacto", "Telesalud", "Segunda opinión"]
    }
  },
  /* Entry order is the tie-break order: specific topics first, general last. */
  faq: [
    {
      id: "greeting",
      kw: { en: ["hello", "hi", "hey", "help", "what can you do", "who are you"],
            es: ["hola", "buenas", "ayuda", "qué puedes hacer", "quién eres"] },
      a: { en: "Hello! I am the Boston Pain Center visitor assistant. I can answer questions about our services, telehealth, second opinions, and how to request a consultation — in English or Spanish. Use the EN/ES toggle at the top of the site to switch my language too. What would you like to know?",
           es: "¡Hola! Soy el asistente de Boston Pain Center. Puedo responder preguntas sobre nuestros servicios, telesalud, segundas opiniones y cómo solicitar una consulta — en inglés o español. Use el botón EN/ES en la parte superior del sitio para cambiar mi idioma también. ¿Qué desea saber?" }
    },
    {
      id: "ketamine",
      kw: { en: ["ketamine", "infusion", "infusion therapy"],
            es: ["ketamina", "infusión", "infusion"] },
      a: { en: "We offer evaluated and monitored infusion care for selected pain and mood conditions. When properly evaluated and monitored, ketamine infusion has an established safety history in clinical settings — but it is not without risks, which your doctor will review with you. Treatment courses vary, and your doctor will propose a plan and reevaluate it based on your response. After each session, a responsible adult must take you home — you cannot drive yourself.",
           es: "Ofrecemos cuidado de infusión evaluado y monitoreado para condiciones seleccionadas de dolor y del estado de ánimo. Cuando se evalúa y monitorea adecuadamente, la infusión de ketamina tiene un historial de seguridad establecido en entornos clínicos — pero no está exenta de riesgos, que su médico revisará con usted. Los cursos de tratamiento varían; su médico le propondrá un plan y lo reevaluará según su respuesta. Después de cada sesión, un adulto responsable debe llevarle a casa — no puede conducir usted mismo." },
      link: { href: "ketamine-infusion.html", en: "Ketamine Infusion Center", es: "Centro de infusión de ketamina" }
    },
    {
      id: "crps",
      kw: { en: ["crps", "complex regional pain", "regional pain syndrome"],
            es: ["crps", "síndrome de dolor regional complejo", "dolor regional complejo"] },
      a: { en: "We provide specialized evaluation and management for complex regional pain syndrome (CRPS). There is no single cure, but early, coordinated care can improve function and reduce pain in many patients — we focus on realistic, measurable goals. Bringing complete records, imaging, medication lists, and symptom notes makes your evaluation more productive.",
           es: "Ofrecemos evaluación y manejo especializados para el síndrome de dolor regional complejo (CRPS). No existe una cura única, pero el cuidado temprano y coordinado puede mejorar la función y reducir el dolor en muchos pacientes — nos enfocamos en objetivos realistas y medibles. Traer registros completos, imágenes, listas de medicamentos y notas de síntomas hace su evaluación más productiva." },
      link: { href: "crps-center.html", en: "CRPS Center", es: "Centro de CRPS" }
    },
    {
      id: "regenerative",
      kw: { en: ["regenerative", "prp", "platelet", "stem cell", "exosome", "peptide"],
            es: ["regenerativa", "regenerativo", "prp", "células madre", "exosomas", "péptidos"] },
      a: { en: "Our regenerative medicine care includes education on PRP, stem cells, exosomes, and peptides, with clear and honest regulatory guidance. Whether regenerative care fits you is decided through an individualized evaluation — never a guarantee.",
           es: "Nuestro cuidado de medicina regenerativa incluye educación sobre PRP, células madre, exosomas y péptidos, con orientación regulatoria clara y honesta. Si el cuidado regenerativo es adecuado para usted se decide mediante una evaluación individualizada — nunca es una garantía." },
      link: { href: "regenerative-medicine.html", en: "Regenerative Medicine", es: "Medicina regenerativa" }
    },
    {
      id: "telehealth",
      kw: { en: ["telehealth", "video visit", "virtual visit", "online visit", "remote visit"],
            es: ["telesalud", "videoconsulta", "consulta por video", "visita virtual", "consulta virtual"] },
      a: { en: "We offer secure video visits for consultations, follow-ups, and second opinions when clinically appropriate. Telehealth availability depends on where you are, physician licensure, and applicable law — we confirm eligibility before scheduling your video visit. You need a smartphone, tablet, or computer with a camera, plus a quiet, private space. Some evaluations and all procedures require an in-person visit; your doctor will tell you the right setting for your case.",
           es: "Ofrecemos visitas por video seguro para consultas, seguimientos y segundas opiniones cuando es clínicamente apropiado. La disponibilidad de telesalud depende de dónde se encuentre usted, la licencia del médico y la ley aplicable — confirmamos la elegibilidad antes de agendar su visita por video. Necesita un teléfono inteligente, tableta o computadora con cámara, además de un espacio tranquilo y privado. Algunas evaluaciones y todos los procedimientos requieren una visita en persona; su médico le indicará el entorno adecuado para su caso." },
      link: { href: "telehealth.html", en: "Telehealth", es: "Telesalud" }
    },
    {
      id: "second-opinion",
      kw: { en: ["second opinion", "second opinions", "independent review"],
            es: ["segunda opinión", "segundas opiniones", "revisión independiente"] },
      a: { en: "We offer a structured, documented review of your diagnosis and options — for patients, physicians, and international cases. If your diagnosis is unclear or recommendations conflict, we review your records and imaging and give you a clear written evaluation with options. The steps are: request a second-opinion review, share your records and imaging through our secure process, and receive a documented evaluation with recommendations — by video or in person. For international patients without insurance, second opinions are offered on a self-pay basis, with fees confirmed before your review begins.",
           es: "Ofrecemos una revisión estructurada y documentada de su diagnóstico y opciones — para pacientes, médicos y casos internacionales. Si su diagnóstico no está claro o las recomendaciones son contradictorias, revisamos sus registros e imágenes y le damos una evaluación clara y escrita con opciones. Los pasos son: solicitar una revisión de segunda opinión, compartir sus registros e imágenes a través de nuestro proceso seguro, y recibir una evaluación documentada con recomendaciones — por video o en persona. Para pacientes internacionales sin seguro, las segundas opiniones se ofrecen con pago directo, y los honorarios se confirman antes de comenzar su revisión." },
      link: { href: "second-opinions.html", en: "Second Opinions", es: "Segundas opiniones" }
    },
    {
      id: "pain",
      kw: { en: ["pain management", "pain", "back pain", "chronic pain", "treat my condition", "do you treat", "conditions"],
            es: ["manejo del dolor", "dolor", "dolor crónico", "dolor lumbar", "tratan mi condición", "condiciones"] },
      a: { en: "Our pain management starts with a careful evaluation — history, examination, and review of imaging and prior treatments — then a coordinated plan that may include image-guided interventional procedures, rehabilitation, and carefully monitored medication, always discussing benefits, risks, and alternatives. Procedures are one tool among several; your doctor will recommend only what fits your evaluation. We evaluate a wide range of painful conditions — a consultation is the right way to determine whether our care fits your situation.",
           es: "Nuestro manejo del dolor comienza con una evaluación cuidadosa — historial, examen y revisión de imágenes y tratamientos previos — y luego un plan coordinado que puede incluir procedimientos intervencionistas guiados por imagen, rehabilitación y manejo cuidadoso y monitoreado de medicamentos, siempre discutiendo beneficios, riesgos y alternativas. Los procedimientos son una herramienta entre varias; su médico recomendará solo lo que corresponda a su evaluación. Evaluamos una amplia gama de condiciones dolorosas — una consulta es la forma correcta de determinar si nuestro cuidado se adapta a su situación." },
      link: { href: "pain-management.html", en: "Pain Management", es: "Manejo del dolor" }
    },
    {
      id: "services",
      kw: { en: ["services", "what do you do", "what do you offer", "specialties", "centers", "treatments"],
            es: ["servicios", "qué hacen", "qué ofrecen", "especialidades", "centros", "tratamientos"] },
      a: { en: "Boston Pain Center offers comprehensive pain management, regenerative medicine, and image-guided interventional care, centered on you and your goals — including a specialized CRPS center, monitored infusion care, telehealth, and second opinions. Care is physician-led and fully bilingual in English and Spanish.",
           es: "Boston Pain Center ofrece manejo integral del dolor, medicina regenerativa y cuidado intervencionista guiado por imagen, centrados en usted y sus objetivos — incluyendo un centro especializado de CRPS, cuidado de infusión monitoreado, telesalud y segundas opiniones. La atención está dirigida por médicos y es completamente bilingüe en inglés y español." },
      link: { href: "index.html", en: "Our services", es: "Nuestros servicios" }
    },
    {
      id: "first-visit",
      kw: { en: ["first visit", "what to expect", "what to bring", "new patient", "consultation process", "how does it work"],
            es: ["primera visita", "qué esperar", "qué debo llevar", "qué llevar", "paciente nuevo", "cómo funciona"] },
      a: { en: "Your care follows four steps: a comprehensive evaluation (history, examination, and review of prior imaging and records), a diagnosis explained in plain language, an individualized plan with options, benefits, risks, and alternatives discussed openly, and coordinated follow-up with communication to your care team. Please bring prior images, procedure reports, a complete medication list, and notes on what has helped — and what has not. If a treatment is unlikely to help you, we will tell you, and explain what might.",
           es: "Su cuidado sigue cuatro pasos: una evaluación integral (historial, examen y revisión de imágenes y registros previos), un diagnóstico explicado en lenguaje claro, un plan individualizado con opciones, beneficios, riesgos y alternativas discutidos abiertamente, y un seguimiento coordinado con comunicación a su equipo de cuidado. Por favor traiga imágenes previas, informes de procedimientos, una lista completa de medicamentos y notas sobre lo que ha ayudado — y lo que no. Si es poco probable que un tratamiento le ayude, se lo diremos y le explicaremos qué podría ayudar." },
      link: { href: "about.html", en: "About our approach", es: "Nuestro enfoque" }
    },
    {
      id: "booking",
      kw: { en: ["book", "booking", "appointment", "schedule", "consultation", "request a consultation", "make an appointment"],
            es: ["reservar", "reserva", "cita", "agendar", "consulta", "solicitar una consulta", "pedir una cita"] },
      a: { en: "You can request a consultation or second opinion on our booking page — for local and international patients, including patients without insurance. Please note honestly: that request form is currently a demonstration. Nothing you enter there is sent to the clinic, and it does not reserve an appointment, so please do not enter sensitive medical details there. Live, HIPAA-connected intake has not been announced yet.",
           es: "Puede solicitar una consulta o segunda opinión en nuestra página de reservas — para pacientes locales e internacionales, incluyendo quienes no tienen seguro. Tenga en cuenta con honestidad: ese formulario de solicitud es actualmente una demostración. Nada de lo que ingrese allí se envía a la clínica, y no reserva una cita, así que por favor no ingrese detalles médicos sensibles allí. La recepción en vivo conectada a HIPAA aún no se ha anunciado." },
      link: { href: "booking.html", en: "Request a Consultation", es: "Solicitar una consulta" }
    },
    {
      id: "contact",
      kw: { en: ["contact", "phone", "call", "email", "address", "where are you", "location", "hours", "open"],
            es: ["contacto", "teléfono", "llamar", "correo", "dirección", "dónde están", "ubicación", "horario", "abren"] },
      a: { en: "You can reach us in English or Spanish. Our listed phone is (617) 555-0100 — please note this number is marked “to be verified” before launch. We are in Boston, Massachusetts; the street address is also marked “to be verified,” as are our hours. Our contact form is a demonstration and does not send your inquiry or trigger follow-up.",
           es: "Puede comunicarse con nosotros en inglés o español. Nuestro teléfono publicado es (617) 555-0100 — tenga en cuenta que este número está marcado como “por verificar” antes del lanzamiento. Estamos en Boston, Massachusetts; la dirección también está marcada como “por verificar”, al igual que nuestro horario. Nuestro formulario de contacto es una demostración y no envía su consulta ni genera seguimiento." },
      link: { href: "contact.html", en: "Contact Us", es: "Contáctenos" }
    },
    {
      id: "insurance",
      kw: { en: ["insurance", "coverage", "cost", "price", "fees", "self-pay", "uninsured", "payment"],
            es: ["seguro", "cobertura", "costo", "precio", "honorarios", "pago directo", "sin seguro", "pago"] },
      a: { en: "The site does not list which insurance plans are accepted. Consultations and second opinions are offered for local and international patients, including patients without insurance. For international patients without insurance, consultations and second opinions are offered on a self-pay basis, with fees confirmed before your review begins.",
           es: "El sitio no publica qué planes de seguro se aceptan. Las consultas y segundas opiniones se ofrecen para pacientes locales e internacionales, incluyendo quienes no tienen seguro. Para pacientes internacionales sin seguro, las consultas y segundas opiniones se ofrecen con pago directo, y los honorarios se confirman antes de comenzar su revisión." },
      link: { href: "booking.html", en: "Request a Consultation", es: "Solicitar una consulta" }
    },
    {
      id: "international",
      kw: { en: ["international", "abroad", "overseas", "travel", "foreign patient", "from another country"],
            es: ["internacional", "extranjero", "viajar", "otro país", "paciente internacional"] },
      a: { en: "We welcome international patients: consultations and second opinions are offered for patients abroad, including patients without insurance on a self-pay basis. Telehealth consultations are available for international patients without insurance, and a second-opinion review can include guidance on whether traveling for care is justified.",
           es: "Damos la bienvenida a pacientes internacionales: las consultas y segundas opiniones se ofrecen para pacientes en el extranjero, incluyendo quienes no tienen seguro con pago directo. Las consultas por telesalud están disponibles para pacientes internacionales sin seguro, y una revisión de segunda opinión puede incluir orientación sobre si viajar para recibir cuidado está justificado." },
      link: { href: "second-opinions.html", en: "Second Opinions", es: "Segundas opiniones" }
    },
    {
      id: "doctors",
      kw: { en: ["doctor", "doctors", "physician", "feliz", "roberto", "eddie", "who are the doctors"],
            es: ["médico", "médicos", "doctor", "feliz", "roberto", "eddie", "quiénes son los médicos"] },
      a: { en: "Our physicians listed on this site are Dr. Roberto Feliz and Dr. Eddie Feliz. Physician profiles are published after verification, so I will not state credentials here beyond what the site publishes. Care here is physician-led, with listening first and a plan shaped around your history, goals, and prior treatment response.",
           es: "Nuestros médicos publicados en este sitio son el Dr. Roberto Feliz y el Dr. Eddie Feliz. Los perfiles de los médicos se publican después de la verificación, así que no afirmaré credenciales aquí más allá de lo que publica el sitio. La atención aquí está dirigida por médicos, escuchando primero y con un plan basado en su historial, objetivos y respuesta a tratamientos previos." },
      link: { href: "about.html", en: "Meet the physicians", es: "Conozca a los médicos" }
    },
    {
      id: "spanish",
      kw: { en: ["spanish", "español", "speak spanish", "bilingual", "language"],
            es: ["español", "hablan español", "bilingüe", "idioma", "inglés"] },
      a: { en: "Yes — care here is fully bilingual in English and Spanish, because understanding your plan matters. This assistant follows the EN/ES toggle at the top of the site: switch it and I switch too.",
           es: "Sí — la atención aquí es completamente bilingüe en inglés y español, porque entender su plan es importante. Este asistente sigue el botón EN/ES en la parte superior del sitio: cámbielo y yo cambio también." }
    },
    {
      id: "resources",
      kw: { en: ["resources", "guides", "checklist", "prepare", "preparation", "questions to ask", "podcast", "video tips"],
            es: ["recursos", "guías", "lista de verificación", "prepararse", "preparación", "preguntas para hacer", "podcast", "consejos en video"] },
      a: { en: "Our patient resources page offers checklists, preparation guides, and education to make the most of each visit — including what to bring (prior images, procedure reports, a full medication list, and symptom notes) and questions worth asking, such as: What is the diagnosis? What are my options, with benefits and risks? What happens if I do nothing? What is a realistic timeline? You will also find the Dr. Feliz podcast and daily video tips.",
           es: "Nuestra página de recursos para pacientes ofrece listas de verificación, guías de preparación y educación para aprovechar cada visita — incluyendo qué traer (imágenes previas, informes de procedimientos, una lista completa de medicamentos y notas de síntomas) y preguntas que vale la pena hacer, como: ¿Cuál es el diagnóstico? ¿Cuáles son mis opciones con beneficios y riesgos? ¿Qué pasa si no hago nada? ¿Cuál es el plazo realista? También encontrará el podcast del Dr. Feliz y consejos diarios en video." },
      link: { href: "patient-resources.html", en: "Patient Resources", es: "Recursos para pacientes" }
    },
    {
      id: "privacy",
      kw: { en: ["privacy", "hipaa", "secure", "medical records", "my information", "personal information", "data"],
            es: ["privacidad", "hipaa", "seguro", "registros médicos", "mi información", "información personal", "datos"] },
      a: { en: "This website is informational. Its demonstration forms are not transmitted to a secure medical-record system, so please do not submit patient-identifiable information through this site's forms until a HIPAA-connected system is connected and announced. I do not collect or store anything you type here — this chat runs entirely in your browser and nothing leaves it.",
           es: "Este sitio web es informativo. Sus formularios de demostración no se transmiten a un sistema seguro de registros médicos, así que por favor no envíe información identificable de pacientes a través de los formularios de este sitio hasta que se conecte y anuncie un sistema compatible con HIPAA. No recopilo ni guardo nada de lo que escriba aquí — este chat funciona completamente en su navegador y nada sale de él." },
      link: { href: "privacy-disclaimer.html", en: "Privacy & Medical Disclaimer", es: "Privacidad y descargo médico" }
    }
  ],
  emergency: {
    en: "If this is a medical emergency, call 911 or go to your nearest emergency department right now. Do not use this site's forms for urgent medical needs — they are demonstrations and no one follows up from them.",
    es: "Si esto es una emergencia médica, llame al 911 o acuda al departamento de emergencias más cercano ahora mismo. No use los formularios de este sitio para necesidades médicas urgentes — son demostraciones y nadie les da seguimiento."
  },
  guard: {
    en: "I can't assess your individual case or give medical advice for your situation — that is what a consultation is for. What I can do is explain our services and how care here works in general, and point you to requesting a consultation, where a physician can evaluate you properly.",
    es: "No puedo evaluar su caso individual ni darle consejo médico para su situación — para eso es una consulta. Lo que sí puedo hacer es explicarle nuestros servicios y cómo funciona la atención aquí en general, y dirigirle a solicitar una consulta, donde un médico puede evaluarle adecuadamente."
  },
  fallback: {
    en: "I don't have an answer for that in the site's published information. Try asking about our services, telehealth, second opinions, what to bring to a first visit, or how to request a consultation — or use the Contact page. I can also only share general educational information, not advice for an individual case.",
    es: "No tengo una respuesta para eso en la información publicada del sitio. Intente preguntar sobre nuestros servicios, telesalud, segundas opiniones, qué llevar a una primera visita o cómo solicitar una consulta — o use la página de Contacto. Además, solo puedo compartir información educativa general, no consejos para un caso individual."
  }
};
