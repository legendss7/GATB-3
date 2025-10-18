# gatb_test_professional.py
import streamlit as st
import random
import math
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
# Estilos (profesional)
# ---------------------------
st.markdown(
    """
    <style>
    /* Fondo y caja principal */
    .app-container {
        background: linear-gradient(180deg, #f4f8fb 0%, #e9f2fb 100%);
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 6px 24px rgba(14,30,37,0.06);
    }
    /* Cards de pregunta */
    .question-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 18px 20px;
        margin-bottom: 14px;
        box-shadow: 0 4px 12px rgba(14,30,37,0.04);
        border-left: 6px solid #2E86C1;
    }
    /* Botones */
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
    /* Títulos */
    h1, h2, h3, h4 { font-family: "Segoe UI", Roboto, Arial, sans-serif; }
    /* Small caption */
    .small { font-size: 0.9em; color: #6b7280; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------
# Encabezado
# ---------------------------
st.markdown('<div class="app-container">', unsafe_allow_html=True)
st.title("🧠 Simulador Interactivo GATB — 50 Preguntas")
st.markdown("Prueba de práctica profesional — Aritmética, Verbal y Problemas. Responde, revisa explicaciones y descarga resultados.")
st.markdown("---")

# ---------------------------
# Preguntas (50) — definidas y revisadas
# ---------------------------
# Nota: mantuvimos variedad: Aritmética / Verbal / Problemas
preguntas = [
    # Aritmética (Parte 2)
    {"id": 1,  "categoria": "Aritmética", "texto": "¿Cuánto es 58 + 34?", "opciones": ["82","91","92","102"], "respuesta": "92", "explicacion": "58 + 34 = 92."},
    {"id": 2,  "categoria": "Aritmética", "texto": "¿Cuánto es 91 − 27?", "opciones": ["64","74","76","66"], "respuesta": "64", "explicacion": "91 − 27 = 64."},
    {"id": 3,  "categoria": "Aritmética", "texto": "¿Cuánto es 15 × 6?", "opciones": ["75","80","90","95"], "respuesta": "90", "explicacion": "15 × 6 = 90."},
    {"id": 4,  "categoria": "Aritmética", "texto": "¿Cuánto es 81 ÷ 9?", "opciones": ["7","8","9","6"], "respuesta": "9", "explicacion": "81 ÷ 9 = 9."},
    {"id": 5,  "categoria": "Aritmética", "texto": "¿Cuánto es 129 + 87?", "opciones": ["206","216","226","196"], "respuesta": "216", "explicacion": "129 + 87 = 216."},
    {"id": 6,  "categoria": "Aritmética", "texto": "¿Cuánto es 153 − 78?", "opciones": ["75","85","87","65"], "respuesta": "75", "explicacion": "153 − 78 = 75."},
    {"id": 7,  "categoria": "Aritmética", "texto": "¿Cuánto es 42 × 7?", "opciones": ["284","294","296","304"], "respuesta": "294", "explicacion": "42 × 7 = 294."},
    {"id": 8,  "categoria": "Aritmética", "texto": "¿Cuánto es 132 ÷ 11?", "opciones": ["10","11","12","13"], "respuesta": "12", "explicacion": "132 ÷ 11 = 12."},
    {"id": 9,  "categoria": "Aritmética", "texto": "¿Cuánto es 788 + 325?", "opciones": ["1013","1103","1113","1123"], "respuesta": "1113", "explicacion": "788 + 325 = 1113."},
    {"id": 10, "categoria": "Aritmética", "texto": "¿Cuánto es 804 − 139?", "opciones": ["765","675","665","705"], "respuesta": "665", "explicacion": "804 − 139 = 665."},

    # Verbal (Parte 4)
    {"id": 11, "categoria": "Verbal", "texto": "Selecciona los sinónimos: Bonito, Feo, Lindo, Grande.", "opciones": ["Bonito y Feo","Bonito y Lindo","Feo y Grande","Grande y Lindo"], "respuesta": "Bonito y Lindo", "explicacion": "Bonito y Lindo son sinónimos."},
    {"id": 12, "categoria": "Verbal", "texto": "Selecciona los sinónimos: Cansado, Agotado, Fuerte, Rápido.", "opciones": ["Cansado y Agotado","Fuerte y Rápido","Agotado y Rápido","Cansado y Fuerte"], "respuesta": "Cansado y Agotado", "explicacion": "Cansado y Agotado significan falta de energía."},
    {"id": 13, "categoria": "Verbal", "texto": "Selecciona el par opuesto: Abrir, Cerrar, Entrar, Salir.", "opciones": ["Abrir y Cerrar","Entrar y Cerrar","Salir y Abrir","Entrar y Salir"], "respuesta": "Abrir y Cerrar", "explicacion": "Abrir y Cerrar son antónimos directos."},
    {"id": 14, "categoria": "Verbal", "texto": "Selecciona los sinónimos: Alegre, Contento, Enojado, Triste.", "opciones": ["Alegre y Triste","Contento y Alegre","Enojado y Alegre","Triste y Alegre"], "respuesta": "Contento y Alegre", "explicacion": "Contento y Alegre expresan felicidad."},
    {"id": 15, "categoria": "Verbal", "texto": "Selecciona el par opuesto: Frío, Caliente, Tibio, Helado.", "opciones": ["Frío y Caliente","Tibio y Helado","Frío y Helado","Caliente y Tibio"], "respuesta": "Frío y Caliente", "explicacion": "Frío y Caliente son antónimos en temperatura."},
    {"id": 16, "categoria": "Verbal", "texto": "Selecciona los sinónimos: Empezar, Terminar, Iniciar, Pausar.", "opciones": ["Empezar y Terminar","Iniciar y Pausar","Empezar e Iniciar","Terminar y Pausar"], "respuesta": "Empezar e Iniciar", "explicacion": "Empezar e Iniciar son sinónimos."},
    {"id": 17, "categoria": "Verbal", "texto": "Selecciona el par opuesto: Reír, Llorar, Sonreír, Gritar.", "opciones": ["Reír y Llorar","Sonreír y Gritar","Reír y Sonreír","Llorar y Gritar"], "respuesta": "Reír y Llorar", "explicacion": "Reír y Llorar son antónimos en emoción."},
    {"id": 18, "categoria": "Verbal", "texto": "Selecciona los sinónimos: Antiguo, Moderno, Nuevo, Viejo.", "opciones": ["Antiguo y Moderno","Antiguo y Viejo","Nuevo y Viejo","Moderno y Viejo"], "respuesta": "Antiguo y Viejo", "explicacion": "Antiguo y Viejo comparten significado."},
    {"id": 19, "categoria": "Verbal", "texto": "Selecciona el par opuesto: Vacío, Lleno, Roto, Completo.", "opciones": ["Vacío y Lleno","Roto y Completo","Vacío y Roto","Lleno y Completo"], "respuesta": "Vacío y Lleno", "explicacion": "Vacío y Lleno son antónimos."},
    {"id": 20, "categoria": "Verbal", "texto": "Selecciona los sinónimos: Triste, Deprimido, Alegre, Contento.", "opciones": ["Triste y Alegre","Deprimido y Triste","Alegre y Deprimido","Contento y Triste"], "respuesta": "Deprimido y Triste", "explicacion": "Depr
