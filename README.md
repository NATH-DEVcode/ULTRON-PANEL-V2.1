## ║ MAPAMUNDI ║

![Mapamundi ULTRON](./mapamundi%20uis.png)


## ║ PERSONALIZACIÓN ║

![Preferencias ULTRON](./Preferencias%20ui.png)

## ║ ADMINISTRACIÓN DE USUARIOS ║

![Usuarios ULTRON](./Usuarios%20ui.png)


ULTRON PANEL V2.1

ULTRON-PANEL 


║               CREADO POR                 
               @NATH-DEVcode (así me encuentras en ig y tiktok)            ║


ULTRON PANEL V2 es un proyecto experimental desarrollado principalmente con Python. Su objetivo es reunir herramientas de administración, inteligencia artificial, diagnóstico y control en una interfaz modular.

Actualmente, esta versión está diseñada para funcionar en Windows.

---

║ ¿QUÉ ES ULTRON? ║

ULTRON es un panel modular que integra diferentes herramientas en una sola interfaz.

Su estructura está organizada mediante módulos independientes que permiten acceder a distintas funciones sin necesidad de abrir múltiples aplicaciones.

El proyecto busca ofrecer una experiencia centralizada, personalizable y ampliable.

║ ¿CÓMO FUNCIONA? ║

ULTRON utiliza una interfaz gráfica que conecta diferentes módulos con los componentes internos del programa.

Su funcionamiento se divide en:

- ULTRON CORE: núcleo principal desde donde se controla la interfaz y sus funciones.
- Módulos: herramientas independientes que amplían las capacidades del panel.
- Usuarios: administración de cuentas y autenticación local.
- CONCIENCIA: interacción mediante inteligencia artificial y voz.
- Configuración: administración de preferencias y servicios externos.

Algunas funciones requieren conexión a internet o credenciales de servicios externos.

---

║ REQUISITOS ║

Para utilizar ULTRON PANEL V2 se necesita:

- Windows 10 u 11 de 64 bits.
- Conexión a internet para las funciones que utilizan servicios externos.
- Micrófono para las funciones de interacción por voz.
- Espacio disponible para la instalación y sus dependencias.
- API Key de Groq para las funciones de inteligencia artificial que utilizan este servicio.

---

║ INSTALACIÓN ║

Método 1 — Instalador

1. Descarga ULTRON PANEL V2 desde el repositorio oficial.
2. Extrae los archivos si descargaste un ZIP.
3. Ejecuta el instalador de ULTRON.
4. Sigue las instrucciones del asistente de instalación.
5. Espera a que finalice la configuración.
6. Inicia ULTRON desde el acceso disponible.

Método 2 — Instalación desde el código fuente

1. Instala Python y Git en Windows.
2. Descarga o clona el repositorio.
3. Abre una terminal dentro de la carpeta del proyecto.
4. Instala las dependencias:

pip install -r requirements-windows.txt

5. Ejecuta el programa:

python main.py

Si utilizas el instalador automático incluido en el proyecto, sigue sus instrucciones en lugar de repetir la instalación manual.

---

║ CONFIGURACIÓN DE INTELIGENCIA ARTIFICIAL ║

ULTRON permite integrar servicios de inteligencia artificial mediante API Keys.

Actualmente, la integración con Groq permite utilizar funciones de IA relacionadas con texto y voz.

¿Cómo configurar la IA?

1. Crea una cuenta en Groq.
2. Accede a la plataforma oficial:
   https://console.groq.com/
3. Genera una API Key desde tu cuenta.
4. Abre ULTRON PANEL V2.
5. Entra a el módulo de conciencia
6. ahí te pedirá introducir la api key que creaste
7. Introduce tu API Key en el campo correspondiente.
8. Guarda la configuración.
9. Comprueba la conexión con el servicio.

Importante:

- La API Key es personal.
- No compartas tus credenciales.
- No publiques tu API Key en GitHub.
- Las funciones de IA dependen de la disponibilidad del proveedor y de tu conexión a internet.
- El uso del servicio puede estar sujeto a los límites de Groq.

---

║ CONCIENCIA ║

CONCIENCIA permite interactuar mediante voz con ULTRON.

Por razones de privacidad permanece desactivada inicialmente.

Para activarla:
Presiona ULTRON CORE.

Para desactivarla:
Presiona nuevamente ULTRON CORE.

Cuando está desactivada, el sistema bloquea la captura del micrófono.

La interacción mediante IA requiere la configuración correspondiente del servicio externo.

---

║ USUARIOS ║

ULTRON PANEL V2 incorpora un sistema de administración local de usuarios.

Cada usuario dispone de autenticación propia.

El sistema permite:

- Crear usuarios.
- Iniciar sesión.
- Cerrar sesión.
- Cambiar de usuario.
- Evitar nombres duplicados.
- Establecer contraseñas.
- Recuperar el acceso mediante un código de recuperación
- El cual solo seuestra una vez al crear la cuenta o reestablecer la contraseñas
- (se recomienda guardarla en un lugar seguro sin compartirla a nadie)

Desde la interfaz principal puede utilizarse el icono de usuario para cambiar de cuenta sin necesidad de cerrar completamente ULTRON.

Recuperación de contraseña

En caso de olvidar una contraseña, el sistema dispone de un mecanismo de recuperación mediante un código.

Se recomienda conservar este código en un lugar seguro.

---

║ MÓDULOS ║

La arquitectura modular permite incorporar herramientas independientes dentro del panel.

Entre sus categorías se encuentran:

- CONCIENCIA
- GESTIÓN
- SISTEMA
- RED
- SEGURIDAD
- DIAGNÓSTICO
- PREFERENCIAS
- ESTADO
- CHAT LOCAL

Los módulos han recibido modificaciones en su estructura, presentación y funcionamiento.

Se ha trabajado especialmente en los módulos más complejos, reduciendo información innecesaria y mejorando la organización de sus interfaces.

---

║ ACTUALIZACIONES DE V2 ║

Esta versión incorpora diferentes mejoras respecto a versiones anteriores.

Interfaz y diseño

- Cambios en el diseño general del panel.
- Mejoras en la interfaz de usuarios.
- Ajustes en la distribución de elementos.
- Organización visual de los módulos.

- Sistema de usuarios

- Mejoras en la administración de cuentas.
- Gestión de contraseñas.
- Incorporación de códigos de recuperación.
- Ajustes en el cambio de usuario.

Inteligencia artificial

- Cambios en la administración de API Keys.
- Ajustes en la integración de servicios de IA.
- Mejoras en la configuración de los servicios externos.

Módulos

- Modificaciones en módulos complejos.
- Optimización de su estructura.
- Reducción de información innecesaria.
- Mejor organización de las herramientas.

Sistema general

- Corrección de errores.
- Ajustes internos.
- Mejoras de funcionamiento.
- Incorporación del mapa mundi.

---

║ PERSONALIZACIÓN ║

• Se pueden personalizar diferentes elementos:

- Colores.a
- Componentes visuales.

Antes de modificar archivos importantes se recomienda crear una copia de seguridad o utilizar Git.

---

║ COMPATIBILIDAD ║

Plataforma actual: Windows.

Esta versión está orientada al entorno Windows. La compatibilidad con otros sistemas operativos no está garantizada.

ULTRON continúa en desarrollo, por lo que algunas funciones pueden cambiar o recibir modificaciones.

---

║ AUTOR Y DESARROLLO ║

NATH-DEVcode

Desarrollador y creador de ULTRON PANEL.

Repositorio oficial:

https://github.com/NATH-DEVcode/ULTRON-PANEL-V2

Demostración web:

https://nath-devcode.github.io/webdemo/

Blog:

https://nath-devcode.blogspot.com/

---


║             ULTRON-PANEL V2.1              ║                                   
             @NATH-DEVcode                 ║
