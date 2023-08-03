import streamlit as st
#import streamlit_tags as tags
st.set_page_config(
        page_title="Análisis de Textos",
        page_icon=":speech_balloon:",
        #layout="wide",
    )
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk, re
nltk.download('stopwords')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from textblob import TextBlob
import openpyxl
import pandas as pd


st.write("""
# Análisis de Sentimientos  

""")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
"""

st.markdown(hide_st_style, unsafe_allow_html=True)
#st.subheader('Interpreta y clasifica un texto según su polaridad en un rango de -1 a 1 y de subjetividad entre 0 y 1.')
#st.sidebar.write('Una polaridad cercana a 1 representa un sentimiento positivo y un valor cercano a -1 se asocia a un sentimiento negativo.')
#st.sidebar.write('Un valor cercano a 1 en la subjectividad indica una mayor implicación personal en el sentido del texto.')

st.set_option('deprecation.showPyplotGlobalUse', False)

#st.subheader("Ingresa un texto")


text = st.text_input("Ingresa un texto y presiona enter")



spanish_stopwords = stopwords.words('spanish')

if text:
    w = WordCloud(stopwords=spanish_stopwords).generate(text)
    st.subheader("Términos más usados")

    plt.imshow(w)
    plt.axis('off')
    st.pyplot()

with st.expander('Analizar el texto'):
    #text = st.text_input('Text here: ')
    if text:
        st.subheader('Análisis de sentimientos')
        blob = TextBlob(text)
        st.write('El texto tiene una polaridad de ', round(blob.sentiment.polarity,2), ' y una subjetividad de ', round(blob.sentiment.subjectivity,2),)
        #st.write('Un valor cercano a 1 en la subjectividad indica una mayor implicación personal en el sentido del texto.')
    blob = TextBlob(text)
    if round(blob.sentiment.polarity,2) >= 0.01:
        st.write('El texto tiene una connotación mayormente positiva')
        
    
    elif round(blob.sentiment.polarity,2) <= -0.01:
        st.write('El texto tiene una connotación mayormente negativa')
    
    
    else:
        st.write('El texto es mayoritariamnete neutral')

#Subir listado de literales
st.sidebar.header('Analiza un conjunto de textos')
st.sidebar.write('1. En un archivo Excel crea una columna con el nombre "Comentarios".')        
#st.sidebar.image('/Users/s1059121/Documents/python/ejemplo.png', width = 200)
st.sidebar.write('2. Incluye en cada fila el texto individual para analizar.')
st.sidebar.write('3. Guarda el archivo y súbelo a continuación.')

with st.sidebar.expander('Analizar Excel'):
    upl = st.file_uploader('Cargar el archivo excel')

    def score(x):
        blob1 = TextBlob(x)
        return blob1.sentiment.polarity

#
    def analyze(x):
        if x >= 0.01:
            return 'Positive'
        elif x <= -0.01:
            return 'Negative'
        else:
            return 'Neutral'

#
    if upl:
        df = pd.read_excel(upl)
        df['Puntaje'] = df['Comentario'].apply(score)
        df['Sentimiento'] = df['Puntaje'].apply(analyze)
        st.write(df.head(10))

        @st.cache_data
        def convert_df(df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode('utf-8')

        csv = convert_df(df)

        st.download_button(
            label="Descarga el archivo en formato CSV",
            data=csv,
            file_name='sentiment.csv',
            mime='text/csv',
        )
        
        st.write('El archivo creado incluye el análisis en la columna "Sentimineto" ')
