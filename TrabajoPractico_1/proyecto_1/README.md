# 🐍 Trivia de Películas

Breve descripción del proyecto:

“Esta es una aplicación web construida con el framework [Flask](https://flask.palletsprojects.com/). Permite intentar adivinar peliculas mediante frases celebres de estas, con seguimiento de resultados y visualización gráfica de estadisticas.

---
## 🏗Arquitectura General

Explica brevemente cómo está organizado el código (funciones y/o clases)
- **`server.py`**: Controlador principal (rutas Flask)
- **`modules/`**:
  - `peliculas.py`: Gestión del catálogo de películas
  - `trivia.py`: Lógica del juego
  - `resultados.py`: Manejo de estadísticas
- **`templates/`**: Vistas HTML
- **`static/`**: 
  - `pdf/`: Gráficos exportables
  - `graficas/`: Imágenes de gráficos

### Diagrama de flujo:
1. Usuario inicia juego → Trivia genera preguntas
2. Respuestas se verifican → Resultados se almacenan
3. Datos se visualizan → Gráficos exportables

El diagrama de relaciones entre clases está disponible en la carpeta [docs](./docs) del proyecto.
---
## 📑Dependencias

1. **Python 3.x**
2. **Flask** (`pip install flask`)
3. **SQLalchemy** (`pip install sqlalchemy`)
4. **Mathplotlib** (`pip install mathplotlib`)
5. **PyPDF4** (`pip install PyPDF4`)
6. Dependencias listadas en requierements.txt

---
## 🚀Cómo Ejecutar el Proyecto
1. **Clonar o descargar** el repositorio.

2. **Crear y activar** un entorno virtual.

3. **Instalar las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```
   El archivo `requirements.txt` se encuentran en la carpeta [deps](./deps) del proyecto.
---
4. **Ejecutar la aplicación**
   ```py server.py
   ```
5. **Copiar el link**
    ```Running on http://....
    ```
## 💻Uso de la aplicación


Explica la funcionalidad de tu aplicación:  
- Cómo se navega por las rutas o URLs.
Flujo típico:
-Ingresar nombre y número de preguntas
-Responder frases aleatorias
-Ver resultados finales
-Explorar estadísticas

Ruta	         Descripción
/	            Inicio con formulario de juego
/iniciar	      Comienza nueva trivia
/verificar	   Procesa respuestas
/resultados   	Historial de partidas
/graficas	   Visualización de estadísticas
/descargar  	Exporta gráficos a PDF


---

## 🙎‍♀️🙎‍♂️Autores

- Morello Deppeler Milagros Guadalupe
- Segovia Lucas Ezequiel

---

> **Consejo**: Mantén el README **actualizado** conforme evoluciona el proyecto, y elimina (o añade) secciones según necesites. Esta plantilla es sólo un punto de partida general.
