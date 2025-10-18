# gatb_test_50.py
import streamlit as st
import pandas as pd

# ---------------------------
# Configuración de la página
# ---------------------------
st.set_page_config(
    page_title="Simulador GATB — Profesional",
    page_icon="🧠",
    layout="wide"
)

# ---------------------------
# Estilos profesionales
# ---------------------------
st.markdown("""
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
""", unsafe_allow_html=True)

# ---------------------------
# Título
# ---------------------------
st.title("🧠 Simulador Interactivo GATB — 50 Preguntas")
st.markdown("Prueba profesional de práctica — Aritmética, Verbal y Problemas.")
st.markdown("---")

# ---------------------------
# Preguntas (ejemplo: 50)
# ---------------------------
preguntas = []
for i in range(1, 51):
    preguntas.append({
        "id": i,
        "categoria": "Aritmética" if i % 3 == 1 else ("Verbal" if i % 3 == 2 else "Problema"),
        "texto": f"Pregunta de ejemplo número {i}: ¿Cuál es la respuesta correcta?",
        "opciones": ["A", "B", "C", "D"],
        "respuesta": "A",
        "explicacion": f"Explicación de la pregunta {i}: la respuesta correcta es A."
    })

# ---------------------------
# Inicializar session_state
# ---------------------------
if "answers" not in st.session_state:
    st.session_state["answers"] = {str(q["id"]): "" for q in preguntas}
if "page_idx" not in st.session_state:
    st.session_state["page_idx"] = 0

per_page = 5
total_pages = (len(preguntas)-1)//per_page + 1

# ---------------------------
# Función mostrar preguntas
# ---------------------------
def mostrar_preguntas(start, end):
    for q in preguntas[start:end]:
        key = f"q_{q['id']}"
        with st.container():
            st.markdown(f'<div class="question-card"><b>{q["id"]}. {q["texto"]}</b></div>', unsafe_allow_html=True)
            prev_answer = st.session_state["answers"][str(q["id"])]
            selected = st.radio(
                "Selecciona tu respuesta:",
                q["opciones"],
                index=q["opciones"].index(prev_answer) if prev_answer in q["opciones"] else 0,
                key=key
            )
            st.session_state["answers"][str(q["id"])] = selected

# ---------------------------
# Mostrar preguntas actuales
# ---------------------------
start = st.session_state["page_idx"] * per_page
end = start + per_page
mostrar_preguntas(start, end)

# ---------------------------
# Navegación
# ---------------------------
col1, col2, col3 = st.columns([1,2,1])
with col1:
    if st.button("⬅ Anterior") and st.session_state["page_idx"] > 0:
        st.session_state["page_idx"] -= 1
with col3:
    if st.button("Siguiente ➡") and st.session_state["page_idx"] < total_pages-1:
        st.session_state["page_idx"] += 1

st.markdown(f"**Página {st.session_state['page_idx']+1} / {total_pages}**")

# ---------------------------
# Finalizar prueba
# ---------------------------
if st.button("✅ Finalizar prueba"):
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
