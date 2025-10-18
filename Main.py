# gatb_test_professional.py
import streamlit as st
import random
import pandas as pd

# ---------------------------
# Configuración de la página
# ---------------------------
st.set_page_config(
    page_title="Simulador GATB — Profesional",
    page_icon="🧠",
    layout="wide",
)

# ---------------------------
# Estilos profesionales
# ---------------------------
st.markdown(
    """
    <style>
    .question-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border-left: 6px solid #2E86C1;
    }
    .stButton>button {
        background-color: #2E86C1;
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 8px 18px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1B4F72;
    }
    h1,h2,h3,h4 { font-family: "Segoe UI", Roboto, Arial, sans-serif; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------
# Título
# ---------------------------
st.title("🧠 Simulador Interactivo GATB — 50 Preguntas")
st.markdown("Prueba profesional de práctica — Aritmética, Verbal y Problemas.")
st.markdown("---")

# ---------------------------
# Preguntas (50) — ejemplo
# ---------------------------
# Para simplificar, muestro solo 10; en producción agregar 50 como en el ejemplo anterior
preguntas = [
    {"id": 1, "categoria": "Aritmética", "texto": "58 + 34 =", "opciones": ["82","91","92","102"], "respuesta": "92", "explicacion": "58 + 34 = 92."},
    {"id": 2, "categoria": "Aritmética", "texto": "91 − 27 =", "opciones": ["64","74","76","66"], "respuesta": "64", "explicacion": "91 − 27 = 64."},
    {"id": 3, "categoria": "Verbal", "texto": "Sinónimo de Bonito:", "opciones": ["Feo","Lindo","Grande","Pequeño"], "respuesta": "Lindo", "explicacion": "Bonito y Lindo son sinónimos."},
    {"id": 4, "categoria": "Problema", "texto": "Si un trabajador hace 4 piezas/hora y trabaja 8 h/día durante 5 días, ¿cuántas piezas hace?", "opciones": ["32","40","160","200"], "respuesta": "160", "explicacion": "4×8×5=160."},
    {"id": 5, "categoria": "Aritmética", "texto": "81 ÷ 9 =", "opciones": ["7","8","9","6"], "respuesta": "9", "explicacion": "81 ÷ 9 = 9."},
    {"id": 6, "categoria": "Problema", "texto": "Juan compra 5 lápices a $0.8 y 3 cuadernos a $1.5. ¿Cuánto gasta?", "opciones": ["4","4.5","8.5","2.3"], "respuesta": "8.5", "explicacion": "5*0.8 + 3*1.5 = 8.5."},
    {"id": 7, "categoria": "Verbal", "texto": "Antónimo de Feliz:", "opciones": ["Contento","Triste","Alegre","Optimista"], "respuesta": "Triste", "explicacion": "Feliz y Triste son antónimos."},
    {"id": 8, "categoria": "Aritmética", "texto": "144 ÷ 12 =", "opciones": ["10","11","12","13"], "respuesta": "12", "explicacion": "144 ÷ 12 = 12."},
    {"id": 9, "categoria": "Problema", "texto": "Área de un rectángulo 10x5 m²:", "opciones": ["15","30","50","100"], "respuesta": "50", "explicacion": "10×5 = 50 m²."},
    {"id": 10, "categoria": "Verbal", "texto": "Palabra que no pertenece: Mesa, Silla, Computadora, Perro", "opciones": ["Mesa","Silla","Computadora","Perro"], "respuesta": "Perro", "explicacion": "Perro es un animal; los demás son muebles/electrónica."},
]

# ---------------------------
# Estado
# ---------------------------
if "answers" not in st.session_state:
    st.session_state["answers"] = {str(q["id"]): None for q in preguntas}
if "page_idx" not in st.session_state:
    st.session_state["page_idx"] = 0

per_page = 5
total_pages = (len(preguntas)-1)//per_page + 1

# ---------------------------
# Función mostrar preguntas
# ---------------------------
def mostrar_preguntas():
    start = st.session_state["page_idx"]*per_page
    end = start + per_page
    for q in preguntas[start:end]:
        key = f"q_{q['id']}"
        with st.container():
            st.markdown(f'<div class="question-card"><b>{q["id"]}. {q["texto"]}</b></div>', unsafe_allow_html=True)
            st.session_state["answers"][str(q["id"])] = st.radio(
                "Selecciona tu respuesta:",
                q["opciones"],
                index=q["opciones"].index(st.session_state["answers"][str(q["id"])]) if st.session_state["answers"][str(q["id"])] else 0,
                key=key
            )

# ---------------------------
# Mostrar preguntas
# ---------------------------
mostrar_preguntas()

# ---------------------------
# Navegación
# ---------------------------
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Anterior") and st.session_state["page_idx"] > 0:
        st.session_state["page_idx"] -= 1
        st.experimental_rerun()
with col2:
    st.markdown(f"Página {st.session_state['page_idx']+1} / {total_pages}")
with col3:
    if st.button("Siguiente") and st.session_state["page_idx"] < total_pages-1:
        st.session_state["page_idx"] += 1
        st.experimental_rerun()

# ---------------------------
# Finalizar prueba
# ---------------------------
if st.button("Finalizar prueba"):
    resultados = []
    correctas = 0
    for q in preguntas:
        user = st.session_state["answers"][str(q["id"])]
        correct = q["respuesta"]
        if user == correct:
            correctas += 1
        resultados.append({
            "ID": q["id"],
            "Pregunta": q["texto"],
            "Tu respuesta": user,
            "Respuesta correcta": correct,
            "Explicación": q["explicacion"]
        })
    df = pd.DataFrame(resultados)
    
    st.success(f"Has terminado la prueba! Puntaje: {correctas}/{len(preguntas)}")
    st.markdown("### Resultados detallados:")
    st.dataframe(df, use_container_width=True)
    
    # Descargar resultados
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Descargar resultados CSV", csv, "resultados_gatb.csv", "text/csv")
