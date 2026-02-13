import streamlit as st
import pandas as pd

# 1. Configuración de la conexión
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT2AGLiMp7h2kwkpAz_r-VsG8k-Zvv7Pl46KrYpyLhixiCQ6_aZ1Exu8dgzbo00D99j0QZ9WKpIqgu6/pub?output=csv"

st.set_page_config(page_title="My Flashcards", page_icon="🧠")
st.title("My Flashcards App 🧠")

# Cargar datos
@st.cache_data
def load_data():
    return pd.read_csv(SHEET_URL)

df = load_data()
df.columns = df.columns.str.strip()

# 2. Selección de Categoría
categoria_select = st.sidebar.selectbox("¿Qué quieres estudiar hoy?", df['Categoría'].unique())
datos_filtrados = df[df['Categoría'] == categoria_select].reset_index(drop=True)

# --- LÓGICA DE ESTADO (IMPORTANTE) ---
# Inicializamos el índice si no existe o si cambiamos de categoría
if 'indice' not in st.session_state or 'cat_anterior' not in st.session_state:
    st.session_state.indice = 0
    st.session_state.cat_anterior = categoria_select

# Si cambias la categoría en el menú, reiniciamos el contador a 0
if st.session_state.cat_anterior != categoria_select:
    st.session_state.indice = 0
    st.session_state.cat_anterior = categoria_select

# 3. Mostrar la Flashcard actual
fila = datos_filtrados.iloc[st.session_state.indice]

st.markdown(f"<h1 style='text-align: center; font-size: 100px;'>{fila['Emoji']}</h1>", unsafe_allow_html=True)

# Formulario para manejar la respuesta y el Enter
with st.form(key='my_form', clear_on_submit=True):
    respuesta = st.text_input("¿Cómo se dice en francés?", placeholder="Escribe aquí...")
    submit = st.form_submit_button("Verificar")

if submit:
    if respuesta.lower().strip() == str(fila['Palabra']).lower().strip():
        st.success("¡Correcto! 🎉")
    else:
        st.error(f"Casi... la respuesta es: **{fila['Palabra']}**")

# 4. Botón de Siguiente (Fuera del form para que siempre funcione)
if st.button("Siguiente tarjeta ➡️"):
    st.session_state.indice = (st.session_state.indice + 1) % len(datos_filtrados)
    st.rerun()

# Mostrar progreso
st.write(f"Tarjeta {st.session_state.indice + 1} de {len(datos_filtrados)}")
