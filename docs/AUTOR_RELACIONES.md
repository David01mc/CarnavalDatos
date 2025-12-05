# Script: add_author_relationships.py

## Descripción

Este script añade un campo `agrupaciones_relacionadas` a cada objeto de autor dentro del array `authors` de cada agrupación en MongoDB. El campo contiene una lista de todas las agrupaciones donde ese autor ha participado.

## Ubicación

```
src/database/add_author_relationships.py
```

## Funcionamiento

El script opera en dos fases:

### Fase 1: Construcción del Índice
- Lee todas las agrupaciones de MongoDB
- Construye un diccionario que mapea cada autor a todas sus agrupaciones
- Ejemplo: `"Martínez Ares" → ["Los Sonrisillas", "Los Sumisos", "Los Cobardes"]`

### Fase 2: Actualización de Documentos
- Para cada agrupación, actualiza el array `authors`
- Añade el campo `agrupaciones_relacionadas` a cada autor
- Si un autor solo tiene 1 agrupación, el campo será `["No hay"]`

## Estructura de Datos Resultante

Antes:
```json
{
  "name": "Los Sonrisillas",
  "authors": [
    {
      "name": "Martínez Ares",
      "role": "Autor",
      "image": "...",
      "link": "..."
    }
  ]
}
```

Después:
```json
{
  "name": "Los Sonrisillas",
  "authors": [
    {
      "name": "Martínez Ares",
      "role": "Autor",
      "image": "...",
      "link": "...",
      "agrupaciones_relacionadas": ["Los Sonrisillas", "Los Sumisos", "Los Cobardes"]
    }
  ]
}
```

Si el autor solo tiene una agrupación:
```json
{
  "agrupaciones_relacionadas": ["No hay"]
}
```

## Uso

### Requisitos
- Archivo `.env` con credenciales de MongoDB
- Conexión a internet
- Base de datos `CarnavalDatos` con colección `agrupaciones`

### Ejecución

```bash
cd C:\Users\Usuario\Desktop\Scripts\Carnaval\CarnavalDatos
python src/database/add_author_relationships.py
```

### Salida Esperada

```
✓ Successfully connected to MongoDB!

=== Phase 1: Building author-agrupaciones index ===
Found 2333 agrupaciones in database
✓ Indexed 974 unique authors

Example authors and their agrupaciones:
  - Antonio Rodríguez Martínez (Tio de la Tiza): 18 agrupaciones
  - ...

=== Phase 2: Updating documents ===
✓ Updated 2328 documents

=== Verification ===
Sample agrupacion: ...
Authors with related agrupaciones:
  - Martínez Ares (Autor)
    → 15 agrupaciones relacionadas: ...

✓ Process completed successfully!
```

## Características

- ✅ **Idempotente**: Puede ejecutarse múltiples veces sin problemas
- ✅ **Seguro**: Solo actualiza el array `authors`, no elimina datos
- ✅ **Informativo**: Muestra progreso y ejemplos durante la ejecución
- ✅ **Verificación**: Muestra un ejemplo al final para confirmar

## Notas

- El script procesa ~2300 documentos, puede tardar 1-2 minutos
- Los nombres de autores deben coincidir exactamente para agruparse
- Si un autor solo aparece en una agrupación, se marca como `["No hay"]`
