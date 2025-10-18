import streamlit as st
import random

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Test GATB Profesional",
    page_icon="🧠",
    layout="wide"
)

# --- ESTILOS CSS PARA DISEÑO PROFESIONAL ---
st.markdown("""
    <style>
        .main {
            background-color: #f8f9fa;
            font-family: 'Segoe UI', sans-serif;
        }
        .stButton>button {
            background-color: #2E86C1;
            color: white;
            font-weight: 600;
            border-radius: 8px;
            border: none;
            padding: 10px 24px;
        }
        .stButton>button:hover {
            background-color: #1B4F72;
            color: white;
        }
        .question-card {
            background-color: white;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

# --- ENCABEZADO ---
st.title("🧠 Test de Aptitudes GATB")
st.subheader("Evaluación general de aptitudes — versión profesional (50 preguntas)")
st.markdown("---")

# --- GENERACIÓN DE PREGUNTAS ---
preguntas_base = [
    ("Identifique la figura diferente en la serie.", ["A", "B", "C", "D"], "C"),
    ("Complete la secuencia numérica: 2, 4, 8, 16, ?", ["18", "24", "32", "36"], "32"),
    ("¿Qué palabra no pertenece al grupo?", ["Perro", "Gato", "Loro", "Mesa"], "Mesa"),
    ("Si todos los A son B y algunos B son C, entonces:", 
     ["Todos los A son C", "Algunos C son A", "Ningún C es A", "No se puede determinar"], "No se puede determinar"),
    ("¿Cuál es el sinónimo de 'iniciar'?", ["Terminar", "Comenzar", "Ignorar", "Cancelar"], "Comenzar"),
    ("Si 5 trabajadores hacen una tarea en 10 días, ¿cuántos la harán en 5 días?", 
     ["10", "5", "15", "20"], "10"),
    ("¿Qué número completa la serie? 3, 6, 9, 12, ?", ["13", "14", "15", "16"], "15"),
    ("Si un tren recorre 60 km en 1 hora, ¿cuánto recorrerá en 3 horas?", ["90", "120", "150", "180"], "180"),
    ("¿Cuál es el antónimo de 'rápido'?", ["Veloz", "Ágil", "Lento", "Fuerte"], "Lento"),
    ("¿Qué figura completa la serie lógica?", ["A", "B", "C", "D"], "B"),
]

# --- DUPLICAR ALEATORIAMENTE PARA LLEGAR A 50 ---
preguntas = []
for i in range(50):
    base = random.choice(preguntas_base)
    preguntas.append((f"{i+1}. {base[0]}", base[1], base[2]))

# --- INICIALIZAR ESTADO ---
if "respuestas" not in st.session_state:
    st.session_state.respuestas = {}
if "pagina" not in st.session_state:
    st.session_state.pagina = 0

# --- LÓGICA DE PÁGINAS ---
total_preguntas = len(preguntas)
preguntas_por_pagina = 5
total_paginas = total_preguntas // preguntas_por_pagina

pagina_actual = st.session_state.pagina
inicio = pagina_actual * preguntas_por_pagina
fin = inicio + preguntas_por_pagina

# --- BARRA DE PROGRESO ---
progreso = len(st.session_state.respuestas) / total_preguntas
st.progress(progreso)
st.write(f"Progreso: {int(progreso*100)}% completado")

# --- MOSTRAR PREGUNTAS ---
for i in range(inicio, fin):
    pregunta, opciones, correcta = preguntas[i]
    with st.container():
        st.markdown(f"<div class='question-card'><h5>{pregunta}</h5>", unsafe_allow_html=True)
        seleccion = st.radio("Selecciona una respuesta:", opciones, key=f"pregunta_{i}")
        st.markdown("</div>", unsafe_allow_html=True)
        st.session_state.respuestas[i] = seleccion

# --- NAVEGACIÓN ENTRE PÁGINAS ---
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if pagina_actual > 0:
        if st.button("⬅️ Anterior"):
            st.session_state.pagina -= 1
            st.rerun()

with col3:
    if pagina_actual < total_paginas - 1:
        if st.button("Siguiente ➡️"):
            st.session_state.pagina += 1
            st.rerun()

# --- FINALIZAR Y MOSTRAR RESULTADOS ---
if pagina_actual == total_paginas - 1:
    st.markdown("---")
    if st.button("✅ Finalizar Test"):
        correctas = 0
        for i, (pregunta, opciones, correcta) in enumerate(preguntas):
            if st.session_state.respuestas.get(i) == correcta:
                correctas += 1
        puntaje = int((correctas / total_preguntas) * 100)

        st.success(f"Has finalizado el test. Tu puntaje es: **{puntaje}%**")
        if puntaje >= 80:
            st.balloons()
            st.info("¡Excelente desempeño! Alta capacidad de razonamiento general.")
        elif puntaje >= 60:
            st.warning("Buen resultado, con margen de mejora en análisis lógico.")
        else:
            st.error("Nivel bajo. Se recomienda reforzar habilidades cognitivas básicas.")

        st.markdown("---")
        st.subheader("🔎 Resumen de Respuestas")
        for i, (pregunta, opciones, correcta) in enumerate(preguntas):
            resp = st.session_state.respuestas.get(i, "No respondida")
            resultado = "✅" if resp == correcta else "❌"
            st.write(f"{resultado} **{pregunta}** — Tu respuesta: {resp} | Correcta: {correcta}")
