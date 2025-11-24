# Guía para Principiantes: Proyecto de Scraping de Carnaval

¡Hola! Esta guía está pensada para explicar cómo funciona este proyecto "por dentro", ideal si estás empezando en el mundo de la programación con Python.

El objetivo del proyecto es entrar en la web `letrasdecarnaval.com` y descargar automáticamente la información de las agrupaciones (chirigotas, comparsas, coros...) y sus letras.

---

## 1. Las Herramientas (Librerías)

Para que Python pueda navegar por internet y entender las páginas web, usamos unas "herramientas" extra llamadas **librerías**. Aquí usamos dos muy famosas:

### `requests` (El Cartero)
Imagina que `requests` es un cartero. Su trabajo es ir a una dirección web (URL) que tú le digas, llamar a la puerta y traerte lo que haya allí (el código HTML de la página).
*   **¿Qué hace en el código?**: Cuando ves `requests.get(url)`, le estamos diciendo: "Ve a esta web y tráeme el contenido".

### `BeautifulSoup` (El Traductor)
Cuando el "cartero" (`requests`) nos trae la página, nos da un montón de código HTML desordenado. `BeautifulSoup` (de la librería `bs4`) es como un traductor que ordena ese caos.
*   **¿Qué hace en el código?**: Nos permite buscar cosas específicas, como "dame todos los títulos" (`h4`) o "busca los enlaces" (`a`).

### `json` (El Archivador)
Esta viene con Python. Nos sirve para guardar la información que hemos conseguido en un archivo de texto ordenado que cualquier ordenador puede leer fácilmente.

---

## 2. El Script Principal: `scraper_historical.py`

Este es el cerebro del proyecto. Es un archivo único que hace todo el trabajo, desde 2025 hacia atrás hasta 2017. Vamos a ver sus partes (funciones):

### `get_soup(session, url)`
*   **¿Qué es?**: Es una función ayudante.
*   **¿Qué hace?**: Combina al "cartero" y al "traductor". Le das una dirección web y te devuelve la página lista para buscar cosas en ella. Si hay un error (la web no carga), te avisa.

### `scrape_year(session, year)`
*   **¿Qué es?**: El encargado de un año concreto.
*   **¿Qué hace?**:
    1.  Entra en la página del año (ej. `.../anyo/2025`).
    2.  Busca todas las "tarjetas" de agrupaciones.
    3.  Filtra solo las de "Adultos".
    4.  Apunta lo básico: Nombre, autor, imagen y el enlace a su página.

### `scrape_details(session, grouping)`
*   **¿Qué es?**: El investigador de detalles.
*   **¿Qué hace?**:
    1.  Entra en el enlace de la agrupación que conseguimos antes.
    2.  Va a la pestaña de "Información".
    3.  Apunta quiénes son los autores (letra, música) y sus fotos.

### `scrape_lyrics(session, grouping)`
*   **¿Qué es?**: El recolector de letras.
*   **¿Qué hace?**:
    1.  Busca en la página de la agrupación los botones que dicen "Ver letra".
    2.  Para cada botón, entra y copia el texto de la letra.
    3.  También se fija en qué **tipo** es (Pasodoble, Cuplé...) y cuántas **visitas** tiene.

### `main()`
*   **¿Qué es?**: El jefe de orquesta.
*   **¿Qué hace?**:
    1.  Prepara la sesión de navegación.
    2.  Hace un bucle (un ciclo) que va contando hacia atrás: 2025, 2024, 2023...
    3.  Para cada año, llama a las funciones anteriores en orden: "Busca agrupaciones" -> "Busca detalles" -> "Busca letras".
    4.  Al final de cada año, guarda todo en un archivo `.json`.

---

## 3. Otros Scripts (Versiones Anteriores)

Verás otros archivos en la carpeta que fueron nuestros "borradores" o primeros pasos:

*   **`scraper_details.py`**: Fue nuestro primer intento. Solo sacaba la lista de agrupaciones y sus autores, pero no las letras.
*   **`scraper_lyrics.py`**: Fue el segundo paso. Aprendimos a sacar las letras de un año concreto.

**Recomendación**: Para usar el proyecto, solo necesitas ejecutar `scraper_historical.py`. Los otros puedes guardarlos de recuerdo o borrarlos.

---

## ¿Cómo ejecutarlo?

1.  Abre tu terminal (consola).
2.  Asegúrate de estar en la carpeta del proyecto.
3.  Escribe: `python scraper_historical.py`
4.  ¡Verás cómo empieza a trabajar año por año!
