import nltk
nltk.download("punkt")
nltk.download('punkt_tab')
nltk.download("stopwords")
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import string
from collections import Counter
from sklearn.base import BaseEstimator, TransformerMixin

class TextVectorizer(BaseEstimator, TransformerMixin):
    """
    Vectorizador de texto personalizado para convertir cadenas de texto en vectores numéricos.

    Este transformador preprocesa el texto (tokenización, minúsculas, eliminación de
    stopwords, stemming) y luego construye un vocabulario. Finalmente, representa
    cada texto como un vector de "bolsa de palabras" (bag-of-words) donde cada
    elemento del vector cuenta la frecuencia de las palabras del vocabulario.

    Hereda de `BaseEstimator` y `TransformerMixin` de scikit-learn,
    lo que permite que se use dentro de pipelines de scikit-learn.

    Atributos:
        __word2idx (dict): Mapeo de palabras del vocabulario a sus índices numéricos.
        stop_words (set): Conjunto de palabras vacías (stopwords) en español para filtrar.
        spanish_stemmer (SnowballStemmer): Objeto para realizar stemming en español.
        vocabulario_ (list): Lista de palabras únicas que forman el vocabulario aprendido.
    """
    def __init__(self):
        """
        Inicializa el vectorizador de texto.
        Configura las stopwords en español y el stemmer.
        """
        self.__word2idx = {}
        self.stop_words = set(stopwords.words('spanish'))
        self.spanish_stemmer = SnowballStemmer('spanish')

    def __get_tokens(self, texto): 
        """
        Procesa una cadena de texto para tokenizarla, convertirla a minúsculas,
        eliminar stopwords y aplicar stemming.

        Args:
            texto (str): La cadena de texto de entrada.

        Returns:
            str: La cadena de texto procesada, con tokens separados por espacios.
        """       
        texto = texto.lower()
        tokens = word_tokenize(texto)    
        word_tokens = [self.spanish_stemmer.stem(token) for token in tokens\
                            if token not in self.stop_words and token not in string.punctuation]
        return ' '.join(word_tokens)

    # Text to Vector
    def __text_to_vector(self, texto):
        """
        Convierte una cadena de texto procesada en un vector numérico (bag-of-words).

        El vector resultante tiene la misma longitud que el vocabulario aprendido
        y sus elementos representan la frecuencia de cada palabra del vocabulario
        en el texto de entrada.

        Args:
            texto (str): La cadena de texto ya preprocesada (tokenizada y stemmed).

        Returns:
            numpy.ndarray: Un array NumPy que representa el vector del texto.
        """
        word_vector = np.zeros(len(self.vocabulario_))
        texto = self.__get_tokens(texto) #agrego esta linea
        for word in texto.split(" "):
            if self.__word2idx.get(word) is None:
                continue
            else:
                word_vector[self.__word2idx.get(word)] += 1
        return np.array(word_vector)

    def fit(self, X, y=None):
        """
        Aprende el vocabulario a partir de una colección de documentos (reclamos).

        Itera sobre todos los reclamos, los preprocesa y construye un contador
        de frecuencias de palabras para identificar el vocabulario único.

        Args:
            X (list[str]): Una lista de cadenas de texto (los reclamos).
            y (any, opcional): Ignorado, se mantiene para compatibilidad con la API de scikit-learn.

        Returns:
            self: La instancia del vectorizador entrenado.
        """
        X_procesado = []
        for reclamo in X:
            X_procesado.append(self.__get_tokens(reclamo))

        total_counts = Counter()
        for reclamo in X_procesado:
            for word in reclamo.split(" "):
                total_counts[word] += 1
        self.vocabulario_ = [elem[0] for elem in total_counts.most_common()]
        for i, word in enumerate(self.vocabulario_):
            self.__word2idx[word] = i 

        return self

    def transform(self, X, y=None): 
        """
        Transforma una colección de documentos (reclamos) en una matriz de vectores numéricos.

        Cada fila de la matriz representa un reclamo, y cada columna representa
        la frecuencia de una palabra del vocabulario en ese reclamo.

        Args:
            X (list[str]): Una lista de cadenas de texto (los reclamos a transformar).
            y (any, opcional): Ignorado, se mantiene para compatibilidad con la API de scikit-learn.

        Returns:
            numpy.ndarray: Una matriz donde cada fila es el vector del reclamo correspondiente.
                           Los elementos son enteros que representan frecuencias.
        """       
        word_vectors = np.zeros((len(X), len(self.vocabulario_)), dtype=np.int_)
        for i, texto in enumerate(X):
            word_vectors[i] = self.__text_to_vector(texto)

        return word_vectors
    
if __name__ == "__main__":
    """
    Bloque de prueba para la clase TextVectorizer.

    Este código se ejecuta solo cuando 'text_vectorizer.py' es ejecutado directamente.
    Carga datos de ejemplo, entrena el vectorizador y luego lo usa para transformar
    los datos, imprimiendo el resultado vectorizado.
    """

    from modules.create_csv import crear_csv
    from sklearn.preprocessing import LabelEncoder

    datos = crear_csv("./data/frases.json")
    X = datos['reclamo']
    y = LabelEncoder().fit_transform(datos['etiqueta'])

    vectorizer = TextVectorizer()
    X_vectorizado = vectorizer.fit_transform(X)
    print(X_vectorizado)    