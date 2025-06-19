from modules.text_vectorizer import TextVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted


class ClaimsClassifier(BaseEstimator, ClassifierMixin):

    def __init__(self):
        pass
   
    def fit(self, X, y):
        # X, y = check_X_y(X, y, accept_sparse=True) #No lo puedo usar con strings
        self.encoder_ = LabelEncoder()
        y = self.encoder_.fit_transform(y)
        pipe = Pipeline([
            ('vectorizer', TextVectorizer()),
            ('scaler', StandardScaler()),
            ('classifier', RandomForestClassifier(max_depth=20, max_features='log2', n_estimators=10))
        ])
        self.clf_ = pipe.fit(X, y)
        if self.clf_:
            self.is_fitted_ = True
        return self

#X (list of str): Una lista de cadenas de texto, donde cada cadena es un reclamo.
#y (list of str): Una lista de cadenas, donde cada cadena es la etiqueta (categoría) correspondiente al reclamo en X.

    def predict(self, X):
        check_is_fitted(self)
        # X = check_array(X, accept_sparse=True)
        return self.encoder_.inverse_transform(self.clf_.predict(X))
#X (list of str): Una lista de cadenas de texto (reclamos) a clasificar.

        #Returns:
            #list of str: Una lista de cadenas, donde cada cadena es la etiqueta predicha (en su formato original de texto) para el reclamo correspondiente.
  
    def clasificar(self, X):
        """Clasifica una lista de reclamos
        Args:
            X (List): Lista de reclamos a clasificar, el formato de cada reclamo debe ser un string
        Returns:
            clasificación: Lista con las clasificaciones de los reclamos, el formato de cada clasificación es un string
            los valores posibles dependen de las etiquetas en y usadas en el entrenamiento
        """
        return self.predict(X)
    

if __name__ == "__main__":
    from modules.create_csv import crear_csv
    datos = crear_csv("./data/frases.json")
    X = datos['reclamo']
    y = datos['etiqueta']
    clf = ClaimsClassifier()
    clf.fit(X, y)
    print(clf.clasificar(["La computadora 1 del laboratorio 3 no enciende", \
                          "El proyector del aula 2 no proyecta la imagen", \
                          "El piso del aula 5 está muy sucio", \
                          "No puedo enviar mi trabajo por correo electrónico porque la red no funciona"]))
    
"""
Bloque de prueba para la clase ClaimsClassifier.
Este código se ejecuta solo cuando 'classifier.py' es ejecutado directamente
(no cuando es importado como un módulo). Carga datos de ejemplo, entrena
el clasificador y luego lo utiliza para clasificar algunos reclamos de prueba,
imprimiendo los resultados en la consola.
"""
"""
Clasificador personalizado para reclamos, implementando la interfaz de scikit-learn.
Esta clase encapsula un pipeline de procesamiento de texto y un modelo de clasificación
(RandomForestClassifier por defecto) para categorizar reclamos textuales.
Permite el entrenamiento con datos de reclamos y etiquetas, y la posterior clasificación
de nuevos reclamos.
Atributos:
encoder_ (LabelEncoder): Objeto para codificar y decodificar las etiquetas de clase.
clf_ (Pipeline): Pipeline de scikit-learn que contiene el vectorizador de texto,
el escalador y el clasificador final.
is_fitted_ (bool): Indica si el clasificador ha sido entrenado.
"""
