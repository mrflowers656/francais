import streamlit as st
import pandas as pd
import random

# 1. Configuración de la conexión (Pega aquí tu link de "Publicar en la web")
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT2AGLiMp7h2kwkpAz_r-VsG8k-Zvv7Pl46KrYpyLhixiCQ6_aZ1Exu8dgzbo00D99j0QZ9WKpIqgu6/pub?output=csv"

st.title("My Flashcards App 🧠")

# Cargar datos
@st.cache_data
def load_data():
    return pd.read_csv(SHEET_URL)

df = load_data()

# 2. Menú de Categorías
categoria_select = st.sidebar.selectbox("¿Qué quieres estudiar hoy?", df['Categoria'].unique())
datos_filtrados = df[df['Categoria'] == categoria_select].reset_index()

# 3. Lógica de la Flashcard
if 'indice' not in st.session_state:
    st.session_state.indice = 0

fila = datos_filtrados.iloc[st.session_state.indice]

# Mostrar Emoji gigante
st.markdown(f"<h1 style='text-align: center; font-size: 100px;'>{fila['Emoji']}</h1>", unsafe_allow_html=True)

# Input del usuario
respuesta = st.text_input("¿Cómo se dice en francés?", key=f"input_{st.session_state.indice}")

if st.button("Verificar"):
    if respuesta.lower().strip() == fila['Palabra'].lower().strip():
        st.success("¡Correcto! 🎉")
        if st.button("Siguiente"):
            st.session_state.indice = (st.session_state.indice + 1) % len(datos_filtrados)
            st.rerun()
    else:
        st.error(f"Casi... la respuesta es: {fila['Palabra']}")
