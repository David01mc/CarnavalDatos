# ¿Qué es MongoDB y MongoDB Atlas?

Esta es una pequeña guía para entender las tecnologías que estamos usando para guardar los datos del Carnaval.

## 1. ¿Qué es MongoDB?

Imagina que tienes un montón de fichas o documentos con información (como nuestros archivos JSON del carnaval). En una base de datos tradicional (como SQL), tendrías que obligar a que toda esa información encaje en tablas muy rígidas, como una hoja de Excel donde no puedes escribir si no hay una columna para ello.

**MongoDB** es diferente. Es una base de datos **NoSQL** (No solo SQL) orientada a documentos.
- **Flexible**: Guarda la información en un formato muy parecido a nuestros JSON (llamado BSON).
- **Sin esquemas rígidos**: Si un año una agrupación tiene "autor de música" y al año siguiente solo "autor", no pasa nada. MongoDB lo acepta sin problemas.
- **Ideal para nuestros datos**: Como nosotros ya tenemos la información en archivos JSON, guardarlos en MongoDB es casi directo. No tenemos que transformar nada complejo.

## 2. ¿Qué es MongoDB Atlas?

Si MongoDB es el "programa" o el motor de la base de datos, **MongoDB Atlas** es el lugar donde vive en la nube.

- **La Nube**: En lugar de tener que instalar MongoDB en tu propio ordenador y dejarlo encendido todo el día para que funcione, Atlas lo aloja en servidores de internet (como los de Google, Amazon o Azure).
- **Servicio Gestionado**: Ellos se encargan de que el servidor funcione, de las copias de seguridad y de la seguridad. Nosotros solo nos conectamos y usamos los datos.
- **Gratuito y Accesible**: Tiene una capa gratuita que es perfecta para proyectos como este, y nos permite conectarnos a nuestra base de datos desde cualquier sitio (desde tu casa, desde mi casa, o desde una aplicación web).

## 3. ¿Por qué lo usamos en este proyecto?

1.  **Naturaleza de los datos**: Nuestros datos del Carnaval son variados y vienen en formato JSON. MongoDB es la "casa" natural para este tipo de datos.
2.  **Facilidad**: Es mucho más fácil subir nuestros archivos JSON directamente a MongoDB que intentar crear tablas complejas en otro tipo de base de datos.
3.  **Conectividad**: Al usar Atlas, podemos conectar futuras aplicaciones (como una web o una app móvil) a estos datos muy fácilmente, sin depender de que tu ordenador esté encendido.

En resumen: Usamos **MongoDB** porque habla el mismo idioma que nuestros datos (JSON) y usamos **Atlas** para tener esos datos seguros y accesibles en internet.
