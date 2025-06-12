# 🐍Sistema de Reclamos

Breve descripción del proyecto:

Esta es una aplicación de secretaría de la FIUNERque sirve para la gestion de reclamos.

---
## 🏗Arquitectura General

Explica brevemente cómo está organizado el código (funciones y/o clases)
El codigo esta organizado de la siguiente manera:
Modelos: Las clases de SQLAlchemy (modelos.py) definen la estructura de la base de datos (por ejemplo, Reclamo, Usuario) y manejan la lógica de interacción con la misma.
Visualizacion: Las plantillas HTML (templates/) se encargan de la presentación de la información al usuario.
Controladores: Las funciones de ruta en app.py llevan a cabo la lógica de la aplicación, manejando las solicitudes del usuario, interactuando con los modelos y renderizando las vistas apropiadas.

El diagrama de relaciones entre clases está disponible en la carpeta [docs](./docs) del proyecto.

---
## 📑Dependencias

1. **Python 3.x**
2. **Flask** (`pip install flask`)
3. **SQLalchemy** (`pip install sqlalchemy`)
4. **Flask-Login** ('pip install Flsk-Login')
5. **Flask-WTF** ('pip install Flask-WTF') 
5. Dependencias listadas en requierements.txt

---
## 🚀Cómo Ejecutar el Proyecto
1. **Clonar o descargar** el repositorio.

2. **Crear y activar** un entorno virtual.

3. **Instalar las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```
   El archivo `requirements.txt` se encuentran en la carpeta [deps](./deps) del proyecto.

4. **Ejecutar la aplicacion**
   ´´´bash
   flask run
---

## 💻Uso de la aplicación

Explica la funcionalidad de tu aplicación:  
- Cómo se navega por las rutas o URLs.
- Si requiere autenticación, describe el flujo de login o registro.

- **Ruta principal** (`/`): muestra la página de inicio.
- **Ruta de usuario** (`/user/<id>`): muestra información del usuario.
-Registro de usuario (/register): Permite a nuevos usuarios crear una cuenta en el sistema. Requiere un nombre de usuario y contraseña.
-Inicio de sesión (/login): Permite a los usuarios existentes autenticarse para acceder a funcionalidades restringidas.
-Cerrar sesión (/logout): Finaliza la sesión del usuario actual.
-Crear nuevo reclamo (/new_claim): Los usuarios autenticados pueden acceder a un formulario para enviar un nuevo reclamo, especificando un título y una descripción.
-Mis reclamos (/my_claims): Los usuarios autenticados pueden ver un listado de todos los reclamos que han enviado, junto con su estado actual.
-Detalle del reclamo (/claim/<id>): Muestra los detalles de un reclamo específico, incluyendo el título, descripción, estado y cualquier respuesta o comentario.
-Gestión de reclamos (Solo administradores) (/admin/claims): Los usuarios con rol de administrador pueden ver todos los reclamos, filtrar por estado y acceder a la edición.
-Actualizar estado del reclamo (Solo administradores) (/admin/claim/<id>/update_status): Permite a los administradores cambiar el estado de un reclamo (por ejemplo, "Pendiente", "En progreso", "Resuelto").
-Responder a reclamo (Solo administradores) (/admin/claim/<id>/respond): Los administradores pueden añadir una respuesta o comentario a un reclamo específico.

---

## 🙎‍♀️🙎‍♂️Autores

- Morello Deppeler, Milagros Guadalupe
- Segovia, Lucas Ezequiel

---

> **Consejo**: Mantén el README **actualizado** conforme evoluciona el proyecto, y elimina (o añade) secciones según necesites. Esta plantilla es sólo un punto de partida general.
