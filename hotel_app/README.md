# Sistema de Reservas de Hotel

Este proyecto es un sistema de reservas de hotel que permite a los usuarios registrarse, iniciar sesión, buscar habitaciones disponibles y realizar reservas. El sistema está diseñado utilizando una arquitectura en capas para garantizar escalabilidad y facilidad de mantenimiento.

---

## Tabla de Contenido

1. [Descripción General](#descripción-general)
2. [Arquitectura del Proyecto](#arquitectura-del-proyecto)
3. [Tecnologías Utilizadas](#tecnologías-utilizadas)
4. [Instalación y Configuración](#instalación-y-configuración)
5. [Ejecución del Proyecto](#ejecución-del-proyecto)
6. [Contribuciones](#contribuciones)

---

## Descripción General

El Sistema de Reservas de Hotel permite a los usuarios:
- Registrarse y gestionar sus cuentas.
- Buscar habitaciones disponibles en tiempo real.
- Realizar reservas con fechas específicas.
- Consultar sus reservas activas.

---

## Arquitectura del Proyecto

El sistema utiliza una arquitectura en tres capas:

1. **Capa de Presentación**:
   - Desarrollo en HTML, CSS, Bootstrap y jQuery.
   - Se conecta con la API RESTful para mostrar datos dinámicos.

2. **Capa de Lógica de Negocio**:
   - Implementada en Python con el framework Flask.
   - Proporciona las rutas y la lógica principal de la aplicación.
   - Incluye autenticación de usuarios y manejo de sesiones.

3. **Capa de Datos**:
   - Utiliza MariaDB como base de datos relacional.
   - Gestiona las tablas `Clientes`, `Habitaciones` y `Reservas`.

---

## Tecnologías Utilizadas

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, Bootstrap, jQuery
- **Base de Datos**: MariaDB
- **Servidor Web**: NGINX
- **Despliegue Remoto**: Serveo

---

## Instalación y Configuración

### Prerrequisitos

1. Tener instalados:
   - Python 3.8 o superior
   - pip (gestor de paquetes de Python)
   - MariaDB
   - NGINX

2. Clonar el repositorio del proyecto:
   ```bash
   git clone https://github.com/usuario/proyecto-reservas-hotel.git
   cd proyecto-reservas-hotel
   ```

### Configuración de la Base de Datos

1. Iniciar MariaDB y crear las tablas:
   ```sql
   CREATE DATABASE hotel;
   USE hotel;

   CREATE TABLE clientes (
       id INT AUTO_INCREMENT PRIMARY KEY,
       nombre VARCHAR(100),
       email VARCHAR(100) UNIQUE,
       password_hash VARCHAR(255)
   );

   CREATE TABLE habitaciones (
       id INT AUTO_INCREMENT PRIMARY KEY,
       numero INT,
       tipo VARCHAR(50),
       precio DECIMAL(10,2),
       estado VARCHAR(50)
   );

   CREATE TABLE reservas (
       id INT AUTO_INCREMENT PRIMARY KEY,
       cliente_id INT,
       habitacion_id INT,
       fecha_inicio DATE,
       fecha_fin DATE,
       estado VARCHAR(50),
       FOREIGN KEY (cliente_id) REFERENCES clientes(id),
       FOREIGN KEY (habitacion_id) REFERENCES habitaciones(id)
   );
   ```

2. Poblar la base de datos con datos de prueba si es necesario.

### Instalación de Dependencias

1. Crear un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

2. Instalar las dependencias del proyecto:
   ```bash
   pip install -r requirements.txt
   ```

### Configuración del Servidor Web

1. Configurar NGINX para servir la aplicación Flask:
   ```nginx
   server {
       listen 80;
       server_name localhost;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

2. Reiniciar NGINX:
   ```bash
   sudo systemctl restart nginx
   ```

---

## Ejecución del Proyecto

1. Iniciar la aplicación Flask:
   ```bash
   flask run
   ```

2. Acceder a la aplicación en el navegador:
   ```
   http://localhost
   ```

---

## Contribuciones

Las contribuciones son bienvenidas. Si deseas colaborar, crea un `fork` del repositorio y envía tus cambios a través de un `pull request`. Recuerda seguir las buenas prácticas de desarrollo.

---

**Autor:** [Javier]

**Licencia:** Este proyecto está licenciado bajo los términos de la [MIT License](LICENSE).
