import os
import base64
import streamlit as st
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title='Expansor de Secciones de Texto',
                   layout="centered",
                   initial_sidebar_state='auto')

st.title("Expansor de Secciones de Texto")

left_column = st.sidebar

left_column.title("Instrucciones")
left_column.markdown("""
1. Escribe el texto que deseas expandir en el área de texto.
2. Ingresa el tema de la sección en la caja de texto provista.
3. Selecciona cuántas fuentes de Google Scholar quieres utilizar.
4. Haz clic en el botón 'Expandir sección' para expandir la sección.
""")

left_column.warning("""
- Verifica la información generada por el asistente antes de usarla.
- Utiliza esta herramienta de manera responsable y ten en cuenta las implicaciones éticas de su uso.
""")

texto_a_expandir = left_column.text_area("Ingrese el texto que desea expandir aquí:", height=75)

edad_destinatarios = st.sidebar.number_input('Edad de los destinatarios', min_value=1, max_value=100, value=18, step=1)

tema_seccion = st.text_input('Ingresa el tema de la sección:', max_chars=500)

num_fuentes = left_column.slider("Número de fuentes de Google Scholar:", min_value=1, max_value=10, value=5, step=1)

def generar_seccion(prompt, max_tokens):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4-0314",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0.5,
            presence_penalty=0.5,
        )
        return completion.choices[0].message['content']
    except Exception as e:
        return str(e)

def expandir_seccion(tema, contenido, edad_destinatarios, max_palabras=1800):
    prompt = f"Expande el siguiente texto sobre {tema} teniendo en cuenta la edad de los destinatarios {edad_destinatarios} y utilizando palabras clave de este contenido proporcionado:\n{contenido}\n\n---\n\nTexto expandido:\n\n"

    max_tokens = max_palabras * 4

    seccion_expandida = generar_seccion(prompt, max_tokens)
    return seccion_expandida


seccion_expandida = None

if st.button('Expandir sección', key='expandir_seccion'):
    if texto_a_expandir and tema_seccion:
        seccion_expandida = expandir_seccion(tema_seccion, texto_a_expandir, edad_destinatarios)
        st.write("Sección expandida:")
        st.write(seccion_expandida)
    else:
        st.warning("Por favor, ingrese el texto que desea expandir y escriba un tema para la sección.")

def descargar_markdown(seccion, nombre_archivo="seccion_expandida.md"):
    b64 = base64.b64encode(seccion.encode()).decode()
    enlace = f'<a href="data:file/markdown;base64,{b64}" download="{nombre_archivo}">Descargar sección en formato Markdown</a>'
    return enlace

if seccion_expandida: st.markdown(descargar_markdown(seccion_expandida), unsafe_allow_html=True)

left_column.markdown(“Copyright © 2023 ibmonograph.com”)

