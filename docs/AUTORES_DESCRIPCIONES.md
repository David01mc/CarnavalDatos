# 👤 Sistema de Descripciones de Autores

Implementación de descripciones de autores con propagación automática usando denormalización.

## 🎯 Problema Resuelto

**Antes**: Los autores se repetían en múltiples agrupaciones sin información adicional.

**Ahora**: Cada autor puede tener una descripción que se propaga automáticamente a todas sus apariciones.

## 📁 Archivos Creados

### Frontend (CarnavalWEB)

- **AgrupacionForm.jsx** (modificado)
  - Añadido campo `descripcion` en la sección de autores
  - Textarea de 3 líneas para descripción del autor

### Scripts Python (CarnavalDatos)

1. **list_authors.py**
   - Lista todos los autores únicos
   - Muestra estadísticas (número de apariciones)
   - Indica cuáles tienen descripción
   - Identifica autores prioritarios

2. **update_author_description.py**
   - Actualiza la descripción de un autor manualmente
   - Propaga el cambio a TODAS las agrupaciones
   - Pide confirmación antes de ejecutar

3. **generate_author_descriptions.py** (CarnavalOpenAI)
   - Genera descripciones automáticas con IA
   - Analiza trayectoria del autor
   - Propaga a todas las agrupaciones
   - Solo procesa autores sin descripción

## 🚀 Uso

### 1. Ver Lista de Autores

```bash
cd CarnavalDatos
python list_authors.py
```

**Salida:**
```
📊 AUTORES EN LA BASE DE DATOS
Total de autores únicos: 450

Autor                                    Apariciones  Descripción
---------------------------------------- ------------ ------------
David Corrales González                 15           ❌ No
Juan Carlos Aragón                       12           ❌ No
Antonio Martínez Ares                    10           ✅ Sí
...

🎯 TOP 10 AUTORES MÁS FRECUENTES:
1. David Corrales González - 15 agrupaciones ❌
2. Juan Carlos Aragón - 12 agrupaciones ❌
...
```

### 2. Actualizar Descripción Manualmente

```bash
cd CarnavalDatos
python update_author_description.py
```

**Proceso interactivo:**
```
Nombre del autor (exacto): David Corrales González

Escribe la descripción del autor:
Autor gaditano reconocido por su estilo innovador...

📊 Encontradas 15 agrupaciones con el autor 'David Corrales González'
⚠️  Esto actualizará la descripción en TODAS las 15 agrupaciones

¿Continuar? (yes/no): yes

✅ Actualización completada!
   Documentos modificados: 15
```

### 3. Generar Descripciones con IA

```bash
cd CarnavalOpenAI
python generate_author_descriptions.py
```

**Proceso:**
```
📊 Encontrados 120 autores sin descripción (con 2+ agrupaciones)

🎯 TOP 20 AUTORES A PROCESAR:
1. David Corrales González - 15 agrupaciones
2. Juan Carlos Aragón - 12 agrupaciones
...

⚠️  Esto generará descripciones usando OpenAI API
   Estimated cost: ~$0.24 USD

¿Continuar? (yes/no): yes

[1/120] Generando descripción para: David Corrales González
   📊 15 agrupaciones
   📝 Descripción: Autor gaditano con amplia trayectoria en el carnaval...
   ✅ Actualizado en 15 agrupaciones
...
```

## 📊 Estructura de Datos

### Antes
```json
{
  "authors": [
    {
      "name": "David Corrales González",
      "role": "Autor de letra y música",
      "image": "url",
      "link": "url"
    }
  ]
}
```

### Después
```json
{
  "authors": [
    {
      "name": "David Corrales González",
      "role": "Autor de letra y música",
      "descripcion": "Autor gaditano reconocido por su estilo innovador y su capacidad para fusionar tradición con modernidad. Con más de 15 agrupaciones en su haber, destaca por sus letras cargadas de crítica social y humor inteligente.",
      "image": "url",
      "link": "url"
    }
  ]
}
```

## 🔄 Cómo Funciona la Propagación

Cuando actualizas la descripción de un autor:

1. **Búsqueda**: Encuentra todas las agrupaciones con ese autor
2. **Actualización**: Usa MongoDB array filters para actualizar solo ese autor
3. **Propagación**: El cambio se refleja en TODAS las apariciones

**Comando MongoDB usado:**
```javascript
db.agrupaciones.update_many(
  {"authors.name": "David Corrales González"},
  {"$set": {"authors.$[elem].descripcion": "Nueva descripción"}},
  array_filters=[{"elem.name": "David Corrales González"}]
)
```

## ✨ Ventajas de Este Enfoque

### ✅ Pros
- **Simple**: No requiere cambios estructurales grandes
- **Rápido**: Actualización en una sola operación
- **Flexible**: Puedes tener descripciones diferentes si es necesario
- **Compatible**: Funciona con la estructura actual

### ⚠️ Consideraciones
- **Duplicación**: Los datos se duplican (trade-off de NoSQL)
- **Sincronización**: Hay que ejecutar script para propagar cambios
- **Consistencia**: Debes usar el nombre exacto del autor

## 🎯 Casos de Uso

### Caso 1: Autor Nuevo
1. Añades autor en el formulario web
2. Escribes su descripción
3. Se guarda en esa agrupación
4. Si el autor aparece en otras, ejecutas `update_author_description.py`

### Caso 2: Generar Todas las Descripciones
1. Ejecutas `generate_author_descriptions.py`
2. La IA analiza la trayectoria de cada autor
3. Genera descripciones automáticas
4. Las propaga a todas las agrupaciones

### Caso 3: Actualizar Descripción Existente
1. Ejecutas `update_author_description.py`
2. Escribes la nueva descripción
3. Se actualiza en todas las agrupaciones

## 💰 Costos de IA

- **Por autor**: ~$0.002 USD
- **120 autores**: ~$0.24 USD
- **Total estimado**: Menos de $1 USD para todos los autores

## 🔍 Verificación

Después de actualizar, verifica en:

1. **Web**: http://localhost:5173 - Edita una agrupación y verás la descripción
2. **MongoDB Compass**: Busca un autor y verifica el campo `descripcion`

## 📝 Recomendaciones

1. **Ejecuta primero** `list_authors.py` para ver quiénes necesitan descripción
2. **Prioriza** autores con más apariciones (mayor impacto)
3. **Usa IA** para generar descripciones base, luego refina manualmente
4. **Mantén consistencia** en el nombre del autor (exacto)

---

**Implementado**: 26/11/2025
**Enfoque**: Denormalización con propagación automática
