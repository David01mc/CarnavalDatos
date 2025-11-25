# Guía del Script: Cómo subimos los datos a la Nube

Esta guía explica paso a paso qué hace el archivo `upload_to_mongo.py`. Piensa en este script como un "robot de mudanza" que coge las cajas (archivos JSON) de tu habitación (tu ordenador) y las lleva a un almacén gigante y seguro (MongoDB Atlas).

## Paso 1: Las Herramientas (Imports)

Al principio del archivo, le decimos a Python qué herramientas necesita:
- `json`: Para poder leer nuestros archivos de datos.
- `glob`: Es como un buscador, nos ayuda a encontrar todos los archivos que terminen en `.json`.
- `pymongo`: Es la herramienta oficial para hablar con la base de datos MongoDB.
- `dotenv`: Nos ayuda a leer las contraseñas secretas desde el archivo `.env` para no escribirlas directamente en el código.

## Paso 2: Las Llaves de Seguridad

```python
load_dotenv()
username = os.getenv("USERNAME_MONGODB")
password = os.getenv("PASSWORD_MONGODB")
```
Aquí el robot busca las llaves del almacén. En lugar de tener la contraseña escrita a la vista de todos, la busca en un archivo especial (`.env`) que es privado. Si no encuentra la contraseña, se para y nos avisa.

## Paso 3: Conectando el Puente

```python
uri = f"mongodb+srv://{username}:{password}@carnavalrag..."
client = MongoClient(uri)
```
Con el usuario y la contraseña, creamos una dirección segura (URI) y establecemos la conexión. Es como llamar por teléfono al almacén y decir "Hola, soy yo, ábreme la puerta".

## Paso 4: Eligiendo el Estante

```python
db = client["CarnavalDatos"]
collection = db["agrupaciones"]
```
Una vez dentro de MongoDB (el almacén), vamos a una habitación específica llamada `CarnavalDatos` (Base de Datos) y dentro de esa habitación, a una estantería concreta llamada `agrupaciones` (Colección). Ahí es donde guardaremos todo.

## Paso 5: Buscando las Cajas

```python
json_files = glob.glob("carnavalJSON/*.json")
```
Aquí usamos la herramienta `glob` para buscar en la carpeta `carnavalJSON` todos los archivos que terminen en `.json`. El robot hace una lista de todo lo que tiene que llevarse.

## Paso 6: La Mudanza (El Bucle)

```python
for json_file in json_files:
    with open(json_file, 'r') as f:
        data = json.load(f)
    collection.insert_many(data)
```
Esta es la parte más importante. El robot va archivo por archivo (caja por caja):
1.  **Abre** el archivo.
2.  **Lee** lo que hay dentro.
3.  **Lo envía** a la nube (`insert_many`), guardando todas las agrupaciones de ese año de golpe.
4.  Nos avisa por pantalla: "He insertado X documentos...".

## ¡Listo!

Al final, cuando ha terminado con todos los archivos, nos dice "Upload complete". Ahora todos tus datos están seguros en Internet y listos para ser usados por cualquier aplicación.
