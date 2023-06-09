import os
import base64
import streamlit as st
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title='Generador de Capítulos de Libro',
                   layout="centered",
                   initial_sidebar_state='auto')

st.title("Generador de Capítulos de Libro")

left_column = st.sidebar

left_column.title("Instrucciones")
left_column.markdown("""
1. Escribe 5-8 palabras clave en el área de texto.
2. Ingresa el tema del capítulo de libro en la caja de texto provista.
3. Selecciona cuántas fuentes de Google Scholar quieres utilizar.
4. Haz clic en el botón 'Generar capítulo' para crear el capítulo.
""")

left_column.warning("""
- Verifica la información generada por el asistente antes de usarla.
- Utiliza esta herramienta de manera responsable y ten en cuenta las implicaciones éticas de su uso.
""")

palabras_clave = left_column.text_area("Ingrese 5-8 palabras clave aquí:", height=75)

edad_destinatarios = st.sidebar.number_input('Edad de los destinatarios', min_value=1, max_value=100, value=18, step=1)

tema_capitulo = st.text_input('Ingresa el tema del capítulo:', max_chars=500)

num_fuentes = left_column.slider("Número de fuentes de Google Scholar:", min_value=1, max_value=10, value=5, step=1)

def generar_capitulo(prompt, max_tokens):
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

def crear_capitulo(tema, contenido, edad_destinatarios, max_palabras=1800):
    prompt = f"Escribe un capítulo de {max_palabras} palabras sobre {tema} utilizando palabras clave del siguiente contenido proporcionado:\n{contenido}\n\nTen en cuenta que la edad de los destinatarios es {edad_destinatarios}.\n\n---\n\nCapítulo:\n\n"

    max_tokens = max_palabras * 4

    capitulo = generar_capitulo(prompt, max_tokens)
    return capitulo


capitulo_generado = None

if st.button('Generar capítulo', key='generar_capitulo'):
    if palabras_clave and tema_capitulo:
        capitulo_generado = crear_capitulo(tema_capitulo, palabras_clave, edad_destinatarios)
        st.write("Capítulo generado:")
        st.write(capitulo_generado)
    else:
        st.warning("Por favor, ingrese las palabras clave y escriba un tema para el capítulo.")

def descargar_markdown(capitulo, nombre_archivo="capitulo_generado.md"):
    b64 = base64.b64encode(capitulo.encode()).decode()
    enlace = f'<a href="data:file/markdown;base64,{b64}" download="{nombre_archivo}">Descargar capítulo en formato Markdown</a>'
    return enlace

if capitulo_generado:
    st.markdown(descargar_markdown(capitulo_generado), unsafe_allow_html=True)

left_column.markdown("Copyright © 2023 [ibmonograph.com](https://www.ibmonograph.com)")
