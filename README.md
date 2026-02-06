# Requisitos

- Instalar Python 3.14

# Instrucciones de uso

1. Instalar dependencias: `pip install -r requirements.txt`.
2. Correr limpieza: `python main.py`.
3. Se generará un archivo `data/clean_data.csv` con los datos limpios y convertidos a COP.

El código usa el archivo `cache/conversion_cache.json` para guardar las tasas de cambio y evitar llamadas a la API de conversión. 

Si se quiere usar las tasas de cambio más recientes, se puede borrar el archivo `conversion_cache.json` y volver a correr el script. Esto requiere reemplazar el archivo `api_key.py` con una API key válida del sitio [ExchangeRate-api](https://www.exchangerate-api.com/docs/free-api-key).
