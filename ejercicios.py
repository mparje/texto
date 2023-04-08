import os
import base64
import streamlit as st
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title='Generador de Ejercicios Resueltos',
                   layout="centered",
                   initial_sidebar_state='auto')

st.title("Generador de Ejercicios Resueltos")

left_column = st.sidebar

left_column.title("Instrucciones")
left_column.markdown("""
1. Esta aplicación es un complemento de laa generadora de capítulos. Ponga en esta los mismos datos que en aquella.
2. Escribe 5-8 palabras clave en el área de texto.
3. Ingresa el tema del ejercicio resuelto en la caja de texto provista.
4. Selecciona cuántas fuentes de Google Scholar quieres utilizar.
5. Haz clic en el botón 'Generar ejercicios' para crear los ejercicios resueltos.
""")

left_column.warning("""
- Verifica la información generada por el asistente antes de usarla.
- Utiliza esta herramienta de manera responsable y ten en cuenta las implicaciones éticas de su uso.
""")

palabras_clave = left_column.text_area("Ingrese 5-8 palabras clave aquí:", height=75)

edad_destinatarios = st.sidebar.number_input('Edad de los destinatarios', min_value=1, max_value=100, value=18, step=1)

tema_ejercicio = st.text_input('Ingresa el tema del ejercicio resuelto:', max_chars=500)

num_fuentes = left_column.slider("Número de fuentes de Google Scholar:", min_value=1, max_value=10, value=5, step=1)

def generar_ejercicios(prompt, max_tokens):
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

def crear_ejercicios(tema, contenido, edad_destinatarios, num_ejercicios=10):
    prompt = f"Escribe {num_ejercicios} ejercicios resueltos sobre {tema} utilizando palabras clave del siguiente contenido proporcionado:\n{contenido}\n\nTen en cuenta que la edad de los destinatarios es {edad_destinatarios}.\n\n---\n\nEjercicios resueltos:\n\n"

    max_tokens = num_ejercicios * 50

    ejercicios = generar_ejercicios(prompt, max_tokens)
    return ejercicios

ejercicios_generados = None

if st.button('Generar ejercicios', key='generar_ejercicios'):
    if palabras_clave and tema_ejercicio:
        ejercicios_generados = crear_ejercicios(tema_ejercicio, palabras_clave, edad_destinatarios)
        st.write("Ejercicios generados:")
        st.write(ejercicios_generados)
    else:
        st.warning("Por favor, ingrese las palabras clave y escriba un tema para los ejercicios.")

def descargar_markdown(ejercicios, nombre_archivo="ejercicios_generados.md"):
    b64 = base64.b64encode(ejercicios.encode()).decode()
    enlace = f'<a href="data:file/markdown;base64,{b64}" download="{nombre_archivo}">Descargar ejercicios en formato Markdown</a>'
    return enlace

if ejercicios_generados:
    st.markdown(descargar_markdown(ejercicios_generados), unsafe_allow_html=True)

left_column.markdown("Copyright © 2023 [ibmonograph.com](https://www.ibmonograph.com)")
