Sistema de Control de Cinta Transportadora

Descripción del proyecto: Aplicación web que simula y controla una cinta transportadora de alimentos, calculando métricas clave como actividad acuosa (aw) y generando advertencias cuando los valores exceden los límites seguros.

Arquitectura General
El sistema está organizado en una estructura de carpetas provista por la cátedra, con las siguientes componentes principales:
proyecto_2/
├── .vscode/
├── apps/
├── data/
├── deps/
│ └── requirements.txt
├── docs/
│ └── UML.jpeg
├── modules/
│ ├── init.py
│ ├── alimento.py # Clases base de alimentos (Alimento, Fruta, Verdura, etc.)
│ ├── cajon.py # Clase Cajon y sus métricas
│ ├── control_cinta.py # Lógica de control de la cinta transportadora
│ └── detector_alimento.py # Simulador de detección de alimentos
├── static/
│ └── images/
│ └── smart-belt.jpg
├── templates/
│ └── index.html
├── tests/
│ ├── init.py
│ └── test_app.py
├── README.md
└── server.py # Aplicación Flask principal

El diagrama de relaciones entre clases está disponible en [docs/UML.jpeg](./docs/UML.jpeg).

---

📑 Dependencias

1. Python 3.8+
2. Flask (para la interfaz web)
3. Numpy (para cálculos matemáticos)
4. Pytest (para pruebas unitarias)

Instalación:
```bash
pip install -r deps/requirements.txt

Interfaz principal:
Configurar el número de alimentos por cajón (N)
Botón "INICIAR CARGA" para comenzar el proceso

Resultados:
Peso total del cajón
Actividad acuosa (aw) promedio por tipo de alimento
Actividad acuosa promedio total
Advertencias cuando aw > 0.90

Visualización:
Listado detallado de todos los alimentos en el cajón
Alertas visuales según los valores calculados


Autores
Morello Deppeler, Milagros Guadalupe
Segovia, Lucas Ezequiel