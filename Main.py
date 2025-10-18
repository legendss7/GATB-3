# test_gatb_pro.py
import streamlit as st
import pandas as pd

# ---------------------------
# Configuración de la página
# ---------------------------
st.set_page_config(
    page_title="Simulador GATB Profesional",
    page_icon="🧠",
    layout="wide"
)

# ---------------------------
# Estilos (CSS)
# ---------------------------
st.markdown("""
<style>
    /* Ocultar "Made with Streamlit" */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Contenedor principal */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Tarjeta de bienvenida y resultados */
    .welcome-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 2.5rem;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #e0e0e0;
    }
    
    /* Tarjeta de pregunta */
    .question-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 20px 25px;
        margin-bottom: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border-left: 6px solid #007BFF; /* Azul profesional */
    }
    
    .question-card b {
        font-size: 1.15rem; /* Letra de pregunta más grande */
    }

    /* Radio buttons horizontales */
    div[role="radiogroup"] {
        flex-direction: row;
        justify-content: space-around;
        gap: 10px;
    }

    /* Estilo de botones en la barra lateral */
    .stSidebar .stButton>button {
        width: 100%;
        background-color: #007BFF;
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 8px 18px;
        border: none;
    }
    .stSidebar .stButton>button:hover {
        background-color: #0056b3;
    }
    
    /* Botón de Finalizar (Verde) */
    .stSidebar .stButton>button[kind="secondary"] {
        background-color: #28a745; /* Verde */
    }
    .stSidebar .stButton>button[kind="secondary"]:hover {
        background-color: #218838;
    }

</style>
""", unsafe_allow_html=True)


# ---------------------------
# Banco de Preguntas
# ---------------------------
def get_questions():
    """
    Retorna la lista completa de 50 preguntas.
    ¡Aquí es donde debes editar y agregar tus propias preguntas!
    """
    preguntas = [
        # --- Ejemplos Reales ---
        {
            "id": 1,
            "categoria": "Aritmética",
            "texto": "Si 3 operarios tardan 6 horas en cavar una zanja, ¿cuánto tardarían 2 operarios?",
            "opciones": ["4 horas", "8 horas", "9 horas", "12 horas"],
            "respuesta": "9 horas",
            "explicacion": "Es una proporción inversa. (3 operarios * 6 horas) = 18 horas-operario. 18 / 2 operarios = 9 horas."
        },
        {
            "id": 2,
            "categoria": "Verbal",
            "texto": "Elige el par de palabras que tenga una relación similar a: ÁRBOL es a BOSQUE como...",
            "opciones": ["LADRILLO es a PARED", "RÍO es a AGUA", "FLOR es a JARDÍN", "PÁJARO es a NIDO"],
            "respuesta": "LADRILLO es a PARED",
            "explicacion": "Un conjunto de árboles forma un bosque. Un conjunto de ladrillos forma una pared. (Relación parte-todo colectivo)."
        },
        {
            "id": 3,
            "categoria": "Problema",
            "texto": "Un tren viaja a 60 km/h y entra en un túnel de 1 km de largo. El tren mide 0.5 km de largo. ¿Cuánto tiempo tarda el tren en salir completamente del túnel?",
            "opciones": ["1 minuto", "1.5 minutos", "2 minutos", "3 minutos"],
            "respuesta": "1.5 minutos",
            "explicacion": "El tren debe recorrer la longitud del túnel (1 km) más su propia longitud (0.5 km) para salir por completo. Distancia total = 1.5 km. A 60 km/h (1 km/minuto), tarda 1.5 minutos."
        },
        {
            "id": 4,
            "categoria": "Aritmética",
            "texto": "¿Cuál es el 20% del 80% de 200?",
            "opciones": ["16", "32", "40", "64"],
            "respuesta": "32",
            "explicacion": "El 80% de 200 es (0.80 * 200) = 160. El 20% de 160 es (0.20 * 160) = 32."
        },
        {
            "id": 5,
            "categoria": "Verbal",
            "texto": "El antónimo de 'INOCUO' es:",
            "opciones": ["INOFENSIVO", "PERjudicial", "SALUDABLE", "APROPIADO"],
            "respuesta": "PERjudicial",
            "explicacion": "Inocuo significa que no hace daño (inofensivo). Su antónimo (lo opuesto) es algo que sí hace daño (perjudicial)."
        },
    ]

    # --- Relleno de Plantilla (Preguntas 6-50) ---
    for i in range(6, 51):
        cat = "Aritmética" if i % 3 == 1 else ("Verbal" if i % 3 == 2 else "Problema")
        preguntas.append({
            "id": i,
            "categoria": cat,
            "texto": f"Texto de ejemplo para la pregunta de {cat} número {i}. ¿Cuál es la opción correcta?",
            "opciones": ["Opción A", "Opción B", "Opción C", "Opción D"],
            "respuesta": "Opción A",
            "explicacion": f"Esta es la explicación de por qué la 'Opción A' es la correcta para la pregunta {i}."
        })
    
    return preguntas

# ---------------------------
# Funciones de la App
# ---------------------------

def initialize_state():
    """Inicializa el estado de la sesión."""
    if "test_started" not in st.session_state:
        st.session_state.test_started = False
    if "show_results" not in st.session_state:
        st.session_state.show_results = False
    if "page_idx" not in st.session_state:
        st.session_state.page_idx = 0
    if "questions" not in st.session_state:
        st.session_state.questions = get_questions()
    if "answers" not in st.session_state:
        st.session_state.answers = {str(q["id"]): "" for q in st.session_state.questions}

def get_option_index(question, stored_answer):
    """Obtiene el índice de la respuesta guardada, o None si no hay respuesta."""
    if stored_answer in question["opciones"]:
        return question["opciones"].index(stored_answer)
    return None

def show_welcome_screen():
    """Muestra la pantalla de bienvenida."""
    st.markdown('<div class="welcome-card">', unsafe_allow_html=True)
    st.title("🧠 Simulador Interactivo GATB Profesional")
    st.markdown("### Prueba de práctica de 50 preguntas")
    st.markdown("---")
    st.write("""
    Esta simulación está diseñada para familiarizarte con el formato de las preguntas 
    de aptitud verbal, aritmética y resolución de problemas.
    
    **Instrucciones:**
    - La prueba consta de **50 preguntas**.
    - Usa la navegación en la barra lateral izquierda para moverte entre las páginas.
    - Tu progreso se guardará automáticamente.
    - Puedes finalizar la prueba en cualquier momento para ver tus resultados.
    
    ¡Mucho éxito!
    """)
    if st.button("🚀 Comenzar Prueba", type="primary"):
        st.session_state.test_started = True
        st.session_state.show_results = False
        st.session_state.page_idx = 0
        st.session_state.answers = {str(q["id"]): "" for q in st.session_state.questions}
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def show_test_screen():
    """Muestra la interfaz del test (preguntas y barra lateral)."""
    preguntas = st.session_state.questions
    per_page = 5  # Preguntas por página
    total_pages = (len(preguntas) - 1) // per_page + 1

    # --- Barra Lateral (Sidebar) ---
    with st.sidebar:
        st.title("Progreso")
        
        # Barra de progreso
        total_questions = len(preguntas)
        answered_count = len([v for v in st.session_state.answers.values() if v])
        progress_percent = answered_count / total_questions
        
        st.progress(progress_percent)
        st.markdown(f"**{answered_count}** de **{total_questions}** respondidas")
        st.divider()

        st.subheader("Navegación")
        st.markdown(f"**Página {st.session_state['page_idx'] + 1} / {total_pages}**")

        # Botones de navegación
        col1, col2 = st.columns(2)
        if col1.button("⬅ Anterior", use_container_width=True):
            if st.session_state["page_idx"] > 0:
                st.session_state["page_idx"] -= 1
                st.rerun()

        if col2.button("Siguiente ➡", use_container_width=True):
            if st.session_state["page_idx"] < total_pages - 1:
                st.session_state["page_idx"] += 1
                st.rerun()
        
        st.divider()
        if st.button("✅ Finalizar y Corregir", type="secondary", use_container_width=True):
            st.session_state.show_results = True
            st.rerun()

    # --- Contenedor Principal (Preguntas) ---
    start = st.session_state["page_idx"] * per_page
    end = start + per_page
    
    st.header(f"Preguntas {start + 1} - {min(end, len(preguntas))}")

    for q in preguntas[start:end]:
        key = f"q_{q['id']}"
        st.markdown(f'<div class="question-card">', unsafe_allow_html=True)
        
        # Muestra la categoría y la pregunta
        st.caption(f"Categoría: {q['categoria']}")
        st.markdown(f"<b>{q['id']}. {q['texto']}</b>", unsafe_allow_html=True)
        
        # Obtiene la respuesta guardada
        prev_answer = st.session_state["answers"][str(q["id"])]
        
        # Muestra las opciones
        selected = st.radio(
            "Selecciona tu respuesta:",
            options=q["opciones"],
            index=get_option_index(q, prev_answer),
            key=key,
            horizontal=True,
            label_visibility="collapsed"
        )
        
        # Guarda la respuesta seleccionada
        if selected:
            st.session_state["answers"][str(q["id"])] = selected
            
        st.markdown('</div>', unsafe_allow_html=True)

def show_results_screen():
    """Muestra la pantalla de resultados detallados."""
    st.title("📈 Resultados de la Simulación")
    st.markdown("---")
    
    preguntas = st.session_state.questions
    respuestas = st.session_state.answers
    
    resultados_data = []
    categorias = {"Aritmética": {"correctas": 0, "total": 0},
                  "Verbal": {"correctas": 0, "total": 0},
                  "Problema": {"correctas": 0, "total": 0}}
    
    total_correctas = 0
    
    for q in preguntas:
        user_answer = respuestas[str(q["id"])]
        correct_answer = q["respuesta"]
        categoria = q["categoria"]
        
        es_correcta = user_answer == correct_answer
        
        if es_correcta:
            total_correctas += 1
            if categoria in categorias:
                categorias[categoria]["correctas"] += 1
                
        if categoria in categorias:
            categorias[categoria]["total"] += 1
            
        resultados_data.append({
            "ID": q["id"],
            "Pregunta": q["texto"],
            "Categoría": categoria,
            "Tu Respuesta": user_answer if user_answer else "Sin responder",
            "Respuesta Correcta": correct_answer,
            "Resultado": "✅ Correcta" if es_correcta else "❌ Incorrecta",
            "Explicación": q["explicacion"]
        })
    
    df = pd.DataFrame(resultados_data)
    
    # --- Métricas de Resumen ---
    st.subheader("Resumen de Puntaje")
    total_preguntas = len(preguntas)
    score_percent = (total_correctas / total_preguntas) * 100
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Puntaje Total", f"{total_correctas} / {total_preguntas}", f"{score_percent:.1f}%")
    
    try:
        col2.metric("Aritmética", 
                    f"{categorias['Aritmética']['correctas']} / {categorias['Aritmética']['total']}",
                    f"{ (categorias['Aritmética']['correctas'] / categorias['Aritmética']['total'])*100 :.1f}%")
    except ZeroDivisionError:
        col2.metric("Aritmética", "N/A")

    try:
        col3.metric("Verbal", 
                    f"{categorias['Verbal']['correctas']} / {categorias['Verbal']['total']}",
                    f"{ (categorias['Verbal']['correctas'] / categorias['Verbal']['total'])*100 :.1f}%")
    except ZeroDivisionError:
        col3.metric("Verbal", "N/A")

    try:
        col4.metric("Problemas", 
                    f"{categorias['Problema']['correctas']} / {categorias['Problema']['total']}",
                    f"{ (categorias['Problema']['correctas'] / categorias['Problema']['total'])*100 :.1f}%")
    except ZeroDivisionError:
        col4.metric("Problemas", "N/A")

    st.divider()

    # --- Detalle de Respuestas ---
    st.subheader("Revisión Detallada")
    st.dataframe(df.set_index('ID'), use_container_width=True)
    
    # Descargar resultados
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Descargar resultados (CSV)", csv, "resultados_gatb.csv", "text/csv")
    
    if st.button("🔄 Volver a intentar"):
        # Resetea el estado para volver a la pantalla de bienvenida
        st.session_state.test_started = False
        st.session_state.show_results = False
        st.rerun()

# ---------------------------
# Lógica Principal de la App
# ---------------------------

initialize_state()

if not st.session_state.test_started:
    show_welcome_screen()
elif st.session_state.show_results:
    show_results_screen()
else:
    show_test_screen()