from flask import Flask, render_template, request, redirect, url_for, session, render_template_string, flash
import os
import folium
import random

# --- Configuración de la app ---
app = Flask(__name__)
app.secret_key = "supersecreto123"  # Necesario para sesiones

# --- Archivo para guardar resultados ---
ARCHIVO_RESULTADOS = "resultados.txt"

adivinanzas_emojis = [
    {"emojis": "🔥🌳", "opciones": ["Incendio forestal", "Deforestación", "Cambio climático", "Reciclaje"], "respuesta": "Incendio forestal"},
    {"emojis": "🌊🏝️⬆️", "opciones": ["Aumento del nivel del mar", "Huracán", "Sequía", "Reciclaje"], "respuesta": "Aumento del nivel del mar"},
    {"emojis": "🚗💨🌍", "opciones": ["Contaminación del aire", "Deforestación", "Reciclaje", "Energía solar"], "respuesta": "Contaminación del aire"},
    {"emojis": "🧊🐧🌡️", "opciones": ["Derretimiento de glaciares", "Reciclaje", "Energía solar", "Huracán"], "respuesta": "Derretimiento de glaciares"},
    {"emojis": "🌳✂️🚫", "opciones": ["Deforestación", "Plantar árboles", "Compostaje", "Energía solar"], "respuesta": "Deforestación"},
    {"emojis": "♻️🌱", "opciones": ["Reciclaje", "Contaminación", "Incendio", "Energía solar"], "respuesta": "Reciclaje"},
    {"emojis": "💧🚱", "opciones": ["Escasez de agua", "Inundación", "Sequía", "Huracán"], "respuesta": "Escasez de agua"},
    {"emojis": "🌪️🏠", "opciones": ["Huracán", "Tornado", "Sequía", "Inundación"], "respuesta": "Huracán"},
    {"emojis": "🐠💀", "opciones": ["Muerte de corales", "Contaminación del aire", "Deforestación", "Reciclaje"], "respuesta": "Muerte de corales"},
    {"emojis": "🌞☀️", "opciones": ["Energía solar", "Energía eólica", "Incendio", "Huracán"], "respuesta": "Energía solar"},
    {"emojis": "💨⚡", "opciones": ["Energía eólica", "Huracán", "Contaminación", "Deforestación"], "respuesta": "Energía eólica"},
    {"emojis": "🚴🌿", "opciones": ["Transporte sostenible", "Contaminación del aire", "Deforestación", "Huracán"], "respuesta": "Transporte sostenible"},
    {"emojis": "🛢️💥", "opciones": ["Derrame de petróleo", "Incendio forestal", "Deforestación", "Reciclaje"], "respuesta": "Derrame de petróleo"},
    {"emojis": "🥵🌡️", "opciones": ["Olas de calor", "Huracán", "Sequía", "Reciclaje"], "respuesta": "Olas de calor"},
    {"emojis": "❄️📉", "opciones": ["Reducción de glaciares", "Reciclaje", "Huracán", "Deforestación"], "respuesta": "Reducción de glaciares"},
    {"emojis": "🍃🏡", "opciones": ["Casas ecológicas", "Deforestación", "Incendio", "Reciclaje"], "respuesta": "Casas ecológicas"},
    {"emojis": "🚯🌍", "opciones": ["Basura en el planeta", "Reciclaje", "Incendio forestal", "Huracán"], "respuesta": "Basura en el planeta"},
    {"emojis": "🌱🌎", "opciones": ["Cuidar el planeta", "Deforestación", "Contaminación", "Huracán"], "respuesta": "Cuidar el planeta"},
    {"emojis": "🌊🌡️", "opciones": ["Calentamiento de océanos", "Huracán", "Deforestación", "Reciclaje"], "respuesta": "Calentamiento de océanos"},
    {"emojis": "🦈💀", "opciones": ["Extinción de especies", "Reciclaje", "Deforestación", "Contaminación"], "respuesta": "Extinción de especies"},
]

# --- Lista de consejos ---
CONSEJOS = [
    "Usa transporte público o bicicleta.",
    "Reduce el consumo de agua y energía.",
    "Evita productos plásticos de un solo uso.",
    "Recicla y reutiliza siempre que puedas.",
    "Compra productos locales y de temporada.",
    "Usa productos de limpieza ecológicos.",
    "Reutiliza botellas y envases."
]

consejos = [
    "Usa transporte público o bicicleta.",
    "Reduce el consumo de agua.",
    "Evita productos plásticos de un solo uso.",
    "Recicla todo lo que puedas.",
    "Compra productos locales.",
    "Apaga las luces cuando no las necesites.",
    "Reutiliza bolsas y envases.",
    "Consume menos carne.",
    "Evita el desperdicio de alimentos.",
    "Usa energía renovable si es posible.",
    "Dúchate en lugar de bañarte.",
    "Cierra el grifo mientras te cepillas los dientes.",
    "Usa electrodomésticos eficientes.",
    "Planta árboles en tu comunidad.",
    "Participa en campañas de limpieza.",
    "Evita la contaminación acústica.",
    "Usa productos de limpieza ecológicos.",
    "Compra ropa de segunda mano.",
    "Reduce el uso de papel.",
    "Separa la basura para reciclar.",
    "Evita productos con demasiado embalaje.",
    "Ahorra energía usando bombillas LED.",
    "No quemes basura.",
    "Usa bolsas de tela.",
    "Cambia tu coche por uno eléctrico o híbrido.",
    "Cierra bien la puerta de la nevera.",
    "Evita comprar productos desechables.",
    "Recoge la basura de tu entorno.",
    "Educa a otros sobre el medio ambiente.",
    "Usa menos plásticos.",
    "Evita el uso de aerosoles dañinos.",
    "Haz compost de los restos orgánicos.",
    "Consume productos de temporada.",
    "Ahorra papel digitalizando documentos.",
    "Usa menos detergente químico.",
    "Evita contaminar ríos y lagos.",
    "Apaga los aparatos electrónicos cuando no los uses.",
    "Compra menos, reutiliza más.",
    "Usa la bicicleta para trayectos cortos.",
    "Evita el uso excesivo del aire acondicionado.",
    "Promueve huertos comunitarios.",
    "Usa el transporte compartido.",
    "Participa en campañas de plantación.",
    "Evita el uso innecesario de agua caliente.",
    "Repara antes de tirar.",
    "Usa cubiertos y vajilla reutilizable.",
    "Aprovecha la luz natural durante el día.",
    "No tires basura al suelo.",
    "Evita el uso de químicos en el jardín.",
    "Involucra a tus amigos en hábitos sostenibles."
]

# --- Preguntas del quiz completo ---
PREGUNTAS_QUIZ = [
    {
        "pregunta": "¿Cuál es el principal gas de efecto invernadero responsable del cambio climático?",
        "opciones": ["Dióxido de carbono (CO2)", "Metano (CH4)", "Óxido nitroso (N2O)"],
        "respuesta": "Dióxido de carbono (CO2)",
        "justificacion": "El CO2 es el gas de efecto invernadero más abundante y contribuye significativamente al calentamiento global."
    },
    {
        "pregunta": "¿Qué porcentaje de la energía mundial proviene de fuentes renovables?",
        "opciones": ["Alrededor del 10%", "Alrededor del 30%", "Alrededor del 50%"],
        "respuesta": "Alrededor del 10%",
        "justificacion": "Actualmente, solo una pequeña fracción de la energía mundial proviene de fuentes renovables, aunque está en aumento."
    },
    {
        "pregunta": "¿Cuál de las siguientes acciones ayuda a reducir la huella de carbono?",
        "opciones": ["Usar transporte público", "Comer más carne", "Comprar productos importados"],
        "respuesta": "Usar transporte público",
        "justificacion": "El transporte público emite menos CO2 por persona en comparación con los automóviles privados."
    },
    {
        "pregunta": "¿Qué es la deforestación?",
        "opciones": ["La plantación de árboles", "La tala masiva de bosques", "El reciclaje de papel"],
        "respuesta": "La tala masiva de bosques",
        "justificacion": "La deforestación se refiere a la eliminación de grandes áreas de bosques, lo que contribuye al cambio climático."
    },
    {
        "pregunta": "¿Cuál es el efecto del aumento de la temperatura global?",
        "opciones": ["Aumento del nivel del mar", "Disminución de la biodiversidad", "Ambos"],
        "respuesta": "Ambos",
        "justificacion": "El aumento de la temperatura global provoca el derretimiento de los glaciares y altera los ecosistemas, lo que resulta en la pérdida de biodiversidad."
    },
    {
        "pregunta": "¿Qué es el reciclaje?",
        "opciones": ["Reutilizar materiales para hacer nuevos productos", "Tirar basura al suelo", "Comprar productos nuevos"],
        "respuesta": "Reutilizar materiales para hacer nuevos productos",
        "justificacion": "El reciclaje implica procesar materiales usados para convertirlos en nuevos productos, reduciendo así la necesidad de extraer recursos naturales."
    },
    {
        "pregunta": "¿Cuál es una fuente de energía renovable?",
        "opciones": ["Carbón", "Energía solar", "Petróleo"],
        "respuesta": "Energía solar",
        "justificacion": "La energía solar es una fuente de energía renovable que no se agota y tiene un impacto ambiental mínimo."
    },
    {
        "pregunta": "¿Qué impacto tiene el uso excesivo de plásticos?",
        "opciones": ["Contaminación de océanos", "Daño a la vida marina", "Ambos"],
        "respuesta": "Ambos",
        "justificacion": "El uso excesivo de plásticos contribuye a la contaminación de los océanos y causa daño a la vida marina."
    },
    {
        "pregunta": "¿Qué es la huella de carbono?",
        "opciones": ["La cantidad de CO2 que una persona emite", "El espacio que ocupa una persona", "La cantidad de agua que consume una persona"],
        "respuesta": "La cantidad de CO2 que una persona emite",
        "justificacion": "La huella de carbono mide el impacto ambiental de una persona en términos de emisiones de CO2."
    },
    {
        "pregunta": "¿Cuál es una forma efectiva de conservar el agua?",
        "opciones": ["Dejar el grifo abierto mientras te cepillas los dientes", "Reparar fugas de agua", "Regar el jardín en horas de sol"],
        "respuesta": "Reparar fugas de agua",
        "justificacion": "Reparar fugas de agua es crucial para conservar este recurso vital."
    }
]

# --- Preguntas Verdadero/Falso ---
PREGUNTAS_VF = [
    {"pregunta": "El deshielo de los polos aumenta el nivel del mar.", "respuesta": "Verdadero"},
    {"pregunta": "Las energías renovables contaminan más que combustibles fósiles.", "respuesta": "Falso"},
    {"pregunta": "Plantar árboles ayuda a reducir CO2.", "respuesta": "Verdadero"},
    {"pregunta": "El transporte público contamina más que viajar en auto.", "respuesta": "Falso"},
    {"pregunta": "El reciclaje no impacta el cambio climático.", "respuesta": "Falso"},
    {"pregunta": "Los incendios forestales contribuyen al calentamiento global.", "respuesta": "Verdadero"},
    {"pregunta": "El CO2 es un gas de efecto invernadero.", "respuesta": "Verdadero"}
]


# --- Funciones ---
def guardar_resultados(texto):
    """Guarda el texto en un archivo de resultados"""
    with open(ARCHIVO_RESULTADOS, "a", encoding="utf-8") as f:
        f.write(texto + "\n")

# --- Rutas ---
@app.route("/")
def inicio():
    """Página de inicio"""
    return render_template("index.html")

@app.route("/informacion")
def informacion():
    return render_template("informacion.html")

@app.route("/vivencias")
def vivencias():
    return render_template("vivencias.html")

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    """Página del quiz principal"""
    # Inicializar sesión
    if "indice" not in session:
        session["indice"] = 0
        session["respuestas"] = []
        session["consejos_quiz"] = random.sample(CONSEJOS, 5)

    indice = session["indice"]

    if request.method == "POST":
        accion = request.form.get("accion")
        seleccion = request.form.get("respuesta")

        if accion == "siguiente" and seleccion:
            session["respuestas"].append(seleccion)
            session["indice"] += 1
        elif accion == "atras" and session["indice"] > 0:
            session["indice"] -= 1
            if session["respuestas"]:
                session["respuestas"].pop()

        indice = session["indice"]
        if indice >= len(PREGUNTAS_QUIZ):
            return redirect(url_for("resultado_quiz"))

    return render_template(
        "quiz.html",
        pregunta=PREGUNTAS_QUIZ[indice],
        indice=indice + 1,
        total=len(PREGUNTAS_QUIZ)
    )


@app.route("/resultado_quiz")
def resultado_quiz():
    """Mostrar resultado del quiz"""
    respuestas = session.get("respuestas", [])
    puntaje = 0
    errores = []

    for i, respuesta in enumerate(respuestas):
        correcta = PREGUNTAS_QUIZ[i]["respuesta"]
        if respuesta == correcta:
            puntaje += 1
        else:
            errores.append({
                "pregunta": PREGUNTAS_QUIZ[i]["pregunta"],
                "correcta": correcta,
                "justificacion": PREGUNTAS_QUIZ[i].get("justificacion", "")
            })

    total = len(PREGUNTAS_QUIZ)
    porcentaje = int((puntaje / total) * 100) if total > 0 else 0

    if porcentaje == 100:
        mensaje = "¡Perfecto! Todas correctas."
    elif porcentaje >= 70:
        mensaje = "¡Muy bien! Algunos errores."
    elif porcentaje >= 40:
        mensaje = "Moderado, puedes mejorar."
    else:
        mensaje = "Necesitas repasar más."

    consejos_aleatorios = random.sample(consejos, 5)

    session.clear()  # Limpiar sesión al terminar

    # Guardar resultado en archivo
    with open("resultados.txt", "a", encoding="utf-8") as f:
        f.write(f"Quiz: {puntaje}/{total} puntos\n")

    return render_template(
        "resultado_quiz.html",
        puntaje=puntaje,
        total=total,
        errores=errores,
        porcentaje=porcentaje,
        mensaje=mensaje,
        consejos=consejos_aleatorios
    )

@app.route("/minijuego", methods=["GET", "POST"])
def minijuego():
    """Mini juego de verdadero/falso"""
    if request.method == "POST":
        puntaje = 0
        errores = []

        for i, pregunta in enumerate(PREGUNTAS_VF):
            seleccion = request.form.get(f"p{i}")
            if seleccion == pregunta["respuesta"]:
                puntaje += 1
            else:
                errores.append(
                    f"Pregunta {i+1}: '{pregunta['pregunta']}' → Correcto: {pregunta['respuesta']}"
                )
        # Después de calcular puntaje y errores
        email_usuario = "anonimo"
        with open("resultados.txt", "a", encoding="utf-8") as f:
            f.write(f"{email_usuario} - Minijuego VF: {puntaje}/{len(PREGUNTAS_VF)} puntos\n")

        return render_template(
            "resultado_minijuego.html",
            puntaje=puntaje,
            total=len(PREGUNTAS_VF),
            errores=errores
        )

    return render_template("minijuego.html", preguntas=PREGUNTAS_VF)

@app.route("/emojis", methods=["GET", "POST"])
def emojis():
    if "indice" not in session:
        session["indice"] = 0
        session["puntaje"] = 0
        session["respuestas"] = []
        session["seleccionadas"] = random.sample(adivinanzas_emojis, 5)  # solo 5 aleatorias

    indice = session["indice"]
    actual = session["seleccionadas"][indice]

    if request.method == "POST":
        seleccion = request.form.get("respuesta")
        if seleccion == actual["respuesta"]:
            session["puntaje"] += 1
            resultado = "✅ Correcto"
        else:
            resultado = f"❌ Incorrecto, era: {actual['respuesta']}"

        session["respuestas"].append(resultado)
        session["indice"] += 1
        indice = session["indice"]

        if indice >= len(session["seleccionadas"]):
            return redirect(url_for("resultado_emojis"))

        actual = session["seleccionadas"][indice]

    return render_template("emojis.html", adivinanza=actual, indice=indice+1, total=5)

@app.route("/resultado-emojis")
def resultado_emojis():
    puntaje = session.get("puntaje", 0)
    respuestas = session.get("respuestas", [])
    session.clear()
    return render_template("resultado_emojis.html", puntaje=puntaje, total=5, respuestas=respuestas)

@app.route("/mapa")
def mapa():
    # Crear mapa centrado en Uruguay
    mapa = folium.Map(location=[-32.5, -55.8], zoom_start=6)

    # Lista de 100 eventos
    eventos = [
        # Bendiciones de Salto (dorado)
        ("Salto", -31.3885, -57.9601, "Ciudad bendecida por Dios ✨", "gold"),
        ("Salto", -31.4000, -57.9600, "Aguas termales curativas 💧", "gold"),
        ("Salto", -31.4200, -57.9700, "Naturaleza hermosa 🌳", "gold"),
        ("Salto", -31.4500, -57.9500, "Cielos despejados 🌌", "gold"),
        ("Salto", -31.4700, -57.9300, "Frutas frescas y abundantes 🍊", "gold"),
        ("Salto", -31.4800, -57.9200, "Familias felices 👨‍👩‍👦", "gold"),
        ("Salto", -31.4900, -57.9100, "Campo fértil 🌱", "gold"),
        ("Salto", -31.5000, -57.9000, "Aire puro 🌬️", "gold"),
        ("Salto", -31.5100, -57.8900, "Sol brillante ☀️", "gold"),
        ("Salto", -31.5200, -57.8800, "Gente solidaria 🤝", "gold"),
        # Otros departamentos con desastres
        ("Montevideo", -34.9011, -56.1645, "Inundación costera 🌊", "blue"),
        ("Paysandú", -32.3214, -58.0756, "Tormenta eléctrica ⛈️", "darkblue"),
        ("Rivera", -30.9053, -55.5508, "Sequía prolongada 🌵", "yellow"),
        ("Maldonado", -34.9011, -54.9500, "Incendio forestal 🔥", "orange"),
        ("Colonia", -34.4625, -57.8381, "Contaminación del río 🏭", "gray"),
        ("Durazno", -33.3806, -56.5236, "Pérdida de cosechas 🌾", "lightgreen"),
        ("Tacuarembó", -31.7333, -55.9833, "Plaga de langostas 🦗", "lightgreen"),
        ("Florida", -34.0956, -56.2142, "Contaminación del agua 🚱", "gray"),
        ("Artigas", -30.4167, -56.4667, "Deforestación 🌲❌", "darkred"),
        ("Cerro Largo", -32.3333, -54.1667, "Erosión del suelo ⛏️", "beige"),
        ("Treinta y Tres", -33.2333, -54.3833, "Enfermedades respiratorias 😷", "purple"),
        ("Rocha", -34.4833, -54.3333, "Mareas altas 🌊", "blue"),
        ("Soriano", -33.5306, -58.2028, "Tormenta con rayos ⛈️", "darkblue"),
        ("Flores", -33.5333, -56.9000, "Incendio rural 🔥", "orange"),
        ("Río Negro", -32.8167, -58.0833, "Contaminación industrial 🏭", "gray"),
        ("Canelones", -34.5228, -56.2777, "Sequía agrícola 🌵", "yellow"),
        ("Lavalleja", -33.5167, -54.9167, "Pérdida de pasturas 🐄", "lightgreen"),
        ("Colonia Histórica", -34.4700, -57.8500, "Patrimonio protegido 🏛️", "green"),
        ("Rocha Costa", -34.4000, -54.3000, "Avistamiento de tortugas 🐢", "green"),
        ("Maldonado Costa", -34.9500, -54.9500, "Playas limpias 🏖️", "green"),
        # Rellenar hasta 100
    ]

    # Llenar el resto hasta 100 eventos con bendiciones de Salto
    while len(eventos) < 100:
        eventos.append(("Salto", -31.3885, -57.9601, "Bendecido por Dios ✨", "gold"))

    # Agregar marcadores al mapa
    for ciudad, lat, lon, texto, color in eventos:
        folium.Marker(
            location=[lat, lon],
            popup=f"{ciudad}: {texto}",
            icon=folium.Icon(color=color, icon="info-sign")
        ).add_to(mapa)

    # Guardar mapa temporal
    mapa.save("templates/mapa_temp.html")

    # Leer mapa y armar HTML final
    with open("templates/mapa_temp.html", "r", encoding="utf-8") as f:
        mapa_html = f.read()

    html_completo = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
    <meta charset="UTF-8">
    <title>GCambio - Mapa</title>
    <link rel="icon" href="static/img/icono1.png" type="image/png">
    <link rel="stylesheet" href="static/css/style.css">
        <meta charset="UTF-8">
        <title>Mapa de desastres en Uruguay</title>
        <style>
            body {{ font-family: 'Arial', sans-serif; background: linear-gradient(135deg,#e0f7fa,#d0f4de); margin:0; padding:20px; }}
            h1 {{ text-align: center; color: #0277bd; font-weight: 600;font-size: 3rem; }}
        </style>
    </head>
    <body>
        <h1 class="header h1">Mapa de desastres en Uruguay</h1>
        <button class="mi-boton" onclick="window.location.href='/'">Volver al inicio</button>
        {mapa_html}
    </body>
    </html>
    """
    return render_template_string(html_completo)

# Formulario de compromiso / vivencia
@app.route("/compromiso", methods=["GET", "POST"])
def compromiso():
    if request.method == "POST":
        email = request.form.get("email")
        vivencia = request.form.get("vivencia")
        # Guardar vivencia en archivo
        with open("vivencias.txt", "a", encoding="utf-8") as f:
            f.write(f"{email}: {vivencia}\n")
        return redirect(url_for("inicio"))
    
    # Renderiza HTML desde archivo
    return render_template("compromiso.html")

# Ver vivencias
@app.route("/ver_vivencias")
def ver_vivencias():
    try:
        with open("vivencias.txt", "r", encoding="utf-8") as f:
            vivencias = f.readlines()
    except FileNotFoundError:
        vivencias = []

    return render_template("ver_vivencias.html", vivencias=vivencias)

# Preguntas educativas sobre cambio climático
preguntas_edu = [
    {
        "pregunta": "¿Qué energía es limpia?",
        "opciones": ["Solar ", "Carbón", "Gasolina"],
        "respuesta": "Solar "
    },
    {
        "pregunta": "Para ahorrar agua, podemos:",
        "opciones": ["Dejar la llave abierta", "Cerrar la llave al cepillarnos los dientes ", "Lavar todo con manguera"],
        "respuesta": "Cerrar la llave al cepillarnos los dientes "
    },
    {
        "pregunta": "¿Qué ayuda al planeta?",
        "opciones": ["Plantar árboles ", "Tirar basura al río", "Quemar hojas secas"],
        "respuesta": "Plantar árboles "
    }
]

# Colores y emojis para bebés
colores_bebes = ["yellow", "blue", "green"]
emojis_bebes = ["☀️", "🌧️", "🍃", "🐝"]

@app.route("/educativa", methods=["GET"])
def educativa():
    return render_template("educativa.html", preguntas_edu=preguntas_edu, colores_bebes=colores_bebes, emojis_bebes=emojis_bebes)

@app.route("/educativa/check_answer", methods=["POST"])
def check_answer():
    pregunta_index_str = request.form.get("pregunta_index")
    if pregunta_index_str is None:
        flash("No se seleccionó ninguna pregunta.", "error")
        return redirect(url_for("educativa"))
    pregunta_index = int(pregunta_index_str)
    seleccion = request.form.get("opcion")
    correcta = preguntas_edu[pregunta_index]["respuesta"]

    if seleccion == correcta:
        flash("✅ Correcto! Muy bien hecho.", "success")
    else:
        flash(f"❌ Incorrecto! La respuesta correcta es: {correcta}", "error")
    return redirect(url_for("educativa"))

@app.route("/donaciones")
def donaciones():
    return render_template("donaciones.html")

@app.route("/procesar_donacion", methods=["POST"])
def procesar_donacion():
    nombre = request.form.get("nombre")
    email = request.form.get("email")
    cantidad = request.form.get("cantidad")

    if not cantidad or int(cantidad) <= 0:
        return "Debes ingresar una cantidad válida. <a href='/donaciones'>Volver</a>"

    cantidad = int(cantidad)

    # Mensaje según cantidad
    if cantidad <= 5:
        mensaje = "¡Gracias por tu granito de arena! 🌱"
    elif cantidad <= 10:
        mensaje = "¡Tu apoyo hace la diferencia! 🌿"
    elif cantidad <= 20:
        mensaje = "¡Wow, gracias por tu generosidad! 🌎"
    else:
        mensaje = "¡Eres un héroe del planeta! 💚"

    return render_template("checkout.html", nombre=nombre, cantidad=cantidad, mensaje=mensaje)

@app.route("/salir")
def salir():
    """Volver al inicio"""
    return redirect(url_for("inicio"))

# --- Ejecutar la app ---
if __name__ == "__main__":
    if not os.path.exists(ARCHIVO_RESULTADOS):
        open(ARCHIVO_RESULTADOS, "w", encoding="utf-8").close()
    app.run(debug=True)