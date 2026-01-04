import streamlit as st
import os
from datetime import datetime, date
from PIL import Image
from pillow_heif import register_heif_opener
import pytz

# Habilitar soporte para fotos HEIC (iPhone)
register_heif_opener()

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Recuerdos",
    page_icon="❤️",
    layout="centered"
)

# # --- ESTILOS CSS (CSS HACKING PARA MEJORAR LA ESTÉTICA) ---
# st.markdown("""
#     <style>
#     /* Centrar títulos */
#     .main-title {
#         text-align: center;
#         font-family: 'Helvetica', sans-serif;
#         color: #ff4b4b;
#         font-size: 3em;
#         font-weight: bold;
#     }
#     .sub-title {
#         text-align: center;
#         font-family: 'Helvetica', sans-serif;
#         color: #555;
#         font-size: 1.5em;
#         margin-bottom: 20px;
#     }
#     /* Estilo del título de la canción */
#     .song-title {
#         text-align: center;
#         font-family: 'Helvetica', sans-serif;
#         color: #333;
#         font-size: 1.3em;
#         font-weight: bold;
#         margin-top: 20px;
#         margin-bottom: 10px;
#     }
#     /* Estilo del contenedor de la foto */
#     .stImage {
#         border-radius: 15px;
#         box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
#     }
#     /* Estilo para el desplegable de instrucciones */
#     .streamlit-expanderHeader {
#         font-weight: bold;
#         color: #ff4b4b;
#     }
#     </style>
# """, unsafe_allow_html=True)
# --- ESTILOS CSS (ESTILO LIMPIO + EFECTO POLAROID) ---
st.markdown("""
    <style>
    /* Centrar títulos */
    .main-title {
        text-align: center;
        font-family: 'Helvetica', sans-serif;
        color: #ff4b4b;
        font-size: 3em;
        font-weight: bold;
    }
    .sub-title {
        text-align: center;
        font-family: 'Helvetica', sans-serif;
        color: #555;
        font-size: 1.5em;
        margin-bottom: 20px;
    }
    /* Estilo del título de la canción */
    .song-title {
        text-align: center;
        font-family: 'Helvetica', sans-serif;
        color: #333;
        font-size: 1.3em;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    /* --- NUEVO: EFECTO POLAROID --- */
    /* Apuntamos a la imagen exacta para ponerle el marco blanco */
    div[data-testid="stImage"] img {
        border: 12px solid #ffffff; /* Marco blanco lateral y superior */
        border-bottom: 40px solid #ffffff; /* Marco inferior más grueso (donde se escribe) */
        box-shadow: 3px 3px 10px rgba(0,0,0,0.2); /* Sombra para dar profundidad */
        transform: rotate(-1.5deg); /* Pequeña inclinación "desenfadada" */
        border-radius: 2px; /* El papel fotográfico apenas tiene esquinas redondeadas */
        transition: transform 0.3s ease; /* Suaviza el movimiento si le pasas el ratón */
    }

    /* Opcional: que se enderece un poco al pasar el ratón */
    div[data-testid="stImage"] img:hover {
        transform: rotate(0deg) scale(1.01);
    }
    /* ----------------------------- */

    /* Estilo para el desplegable de instrucciones */
    .streamlit-expanderHeader {
        font-weight: bold;
        color: #ff4b4b;
    }
    </style>
""", unsafe_allow_html=True)

# --- CONFIGURACIÓN DE DATOS ---
zona_horaria = pytz.timezone('Europe/Madrid') 
hoy = datetime.now(zona_horaria).date()
# Descomenta la línea de abajo para probar fechas futuras:
# hoy = date(2024, 2, 14)

# Mapa para traducir el número del mes a tu carpeta
mapa_carpetas = {
    1: "01_Enero", 2: "02_Febrero", 3: "03_Marzo", 4: "04_Abril",
    5: "05_Mayo", 6: "06_Junio", 7: "07_Julio", 8: "08_Agosto",
    9: "09_Septiembre", 10: "10_Octubre", 11: "11_Noviembre", 12: "12_Diciembre"
}

# --- CONFIGURACIÓN DE MÚSICA ---
musica_por_mes = {
    1: "https://www.youtube.com/watch?v=kw5p7Azmh2Y&list=RDkw5p7Azmh2Y&start_radio=1",
    2: "https://www.youtube.com/watch?v=0qdDDFkheVw&list=RD0qdDDFkheVw&start_radio=1",
    3: "https://www.youtube.com/watch?v=5SXrZh03-pI&list=RD5SXrZh03-pI&start_radio=1",
    4: "https://www.youtube.com/watch?v=KgJzb_c2iiM&list=RDKgJzb_c2iiM&start_radio=1",
    5: "https://www.youtube.com/watch?v=fgLEhuSd64I&list=RDfgLEhuSd64I&start_radio=1",
    6: "https://www.youtube.com/watch?v=VEfkNHTjgs8&list=RDVEfkNHTjgs8&start_radio=1",
    7: "https://www.youtube.com/watch?v=PSjeJrDI4a4&list=RDPSjeJrDI4a4&start_radio=1",
    8: "https://www.youtube.com/watch?v=f41rIgQF-Mw&list=RDf41rIgQF-Mw&start_radio=1",
    9: "https://www.youtube.com/watch?v=BH8uWpXCLIM&list=RDBH8uWpXCLIM&start_radio=1",
    10: "https://www.youtube.com/watch?v=XM5DdGkRP40&list=RDXM5DdGkRP40&start_radio=1",
    11: "https://www.youtube.com/watch?v=TTzrFxeBiUQ&list=RDTTzrFxeBiUQ&start_radio=1",
    12: "https://www.youtube.com/watch?v=BaTM-84Akk8&list=RDBaTM-84Akk8&start_radio=1"
}

# --- LÓGICA INTELIGENTE DE URL (PARA LOS QRs) ---
params = st.query_params
fecha_defecto = hoy

if "mes" in params:
    try:
        mes_url = int(params["mes"])
        if 1 <= mes_url <= 12:
            fecha_defecto = date(hoy.year, mes_url, 1)
            if mes_url == hoy.month:
                fecha_defecto = hoy
    except:
        pass

# --- BARRA LATERAL (CALENDARIO + INSTRUCCIONES) ---
with st.sidebar:
    
    # --- NUEVO: BOTÓN DESPLEGABLE CON INSTRUCCIONES ---
    with st.expander("🎁 ¿Cómo funciona el regalo?"):
        st.markdown("""
        **¡Holii!** Bienvenido a tu calendario infinito. ❤️
        
        1. **📸 Foto Diaria:** Cada día se desbloquea una foto nueva automáticamente. La foto se ha tomado en el mes en el que se desbloquea :)
        2. **🚫 Sin Trampas:** Si intentas seleccionar un día futuro, el sistema no te dejará verlo jeje
        3. **🎶 Música:** Cada mes tiene su propia banda sonora. Dale al play debajo de la foto
        4. **🔙 Recuerdos:** Puedes usar el calendario de abajo para volver a ver días pasados
        """)
    
    st.write("---") # Separador visual

    st.header("📅 Navegación")
    st.write("Selecciona un día especial:")
    
    fecha_seleccionada = st.date_input(
        "Calendario",
        value=fecha_defecto,
        min_value=date(hoy.year, 1, 1),
        max_value=date(hoy.year, 12, 31)
    )
    
    st.write("---")
    st.caption("❤️ Hecho con cariño")

# --- PÁGINA PRINCIPAL ---

mes_nombre = fecha_seleccionada.strftime("%B")
nombres_meses_es = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
mes_esp = nombres_meses_es[fecha_seleccionada.month]

st.markdown(f"<div class='main-title'>Nuestros recuerdos</div>", unsafe_allow_html=True)
st.markdown(f"<div class='sub-title'>Fotito del <b>{fecha_seleccionada.day} de {mes_esp}</b></div>", unsafe_allow_html=True)

# 2. Lógica de BLOQUEO
if fecha_seleccionada > hoy:
    st.divider()
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.error("¡Alto ahí, viajera del tiempo! ⏳")
        st.write(f"Hoy es {hoy.day} de {nombres_meses_es[hoy.month]}. No puedes ver el futuro TRAMPOSA")
        st.image("https://media.giphy.com/media/tXL4FHPSnVJ0A/giphy.gif")

else:
    carpeta = mapa_carpetas.get(fecha_seleccionada.month)
    dia = fecha_seleccionada.day
    
    ruta_carpeta = os.path.join("Fotos", carpeta)
    foto_encontrada = None
    
    if os.path.exists(ruta_carpeta):
        archivos = os.listdir(ruta_carpeta)
        for archivo in archivos:
            # Convertimos el nombre a minúsculas para comparar
            if archivo.lower().startswith(f"{dia}."):
                foto_encontrada = os.path.join(ruta_carpeta, archivo)
                break
    st.divider()
    
    if foto_encontrada:
        image = Image.open(foto_encontrada)
        st.image(image, use_column_width=True)
        
        # --- AQUI VA LA MÚSICA ---
        link_cancion = musica_por_mes.get(fecha_seleccionada.month)
        if link_cancion and len(link_cancion) > 5:
            # 1. Añadimos espacio (salto de línea)
            st.markdown("<br>", unsafe_allow_html=True)
            
            # 2. Título más grande y con estilo propio
            st.markdown(f"<div class='song-title'>🎶 Nuestra canción de {mes_esp}</div>", unsafe_allow_html=True)
            
            # 3. Vídeo más pequeño usando columnas
            col_izq, col_centro, col_der = st.columns([1, 2, 1])
            with col_centro:
                st.video(link_cancion)

        if fecha_seleccionada == hoy:
            st.balloons()
            
        txt_path = foto_encontrada.rsplit('.', 1)[0] + ".txt"
        if os.path.exists(txt_path):
            with open(txt_path, "r", encoding="utf-8") as f:
                st.info(f.read())
                
    else:
        st.warning(f"Ups, parece que para el día {dia} de {mes_esp} se me olvidó subir la foto... ¡Pídeme un beso de compensación! 😘")