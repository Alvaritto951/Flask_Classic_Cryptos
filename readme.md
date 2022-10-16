# WEB CRYPTOMONEDAS
- Proyecto Final BootCamp Zero - XII Edición | KeepCoding

- Aplicación web en Flask

- Simulador de conversión, tradeo e inversión en Criptomonedas

# Compra-ventas y tradeo de Cryptomonedas

Programa hecho en como lenguaje principal python. Tambien se ha usado Flask, Html5, CSS3 y Jinja.
Para consultar y recuperar el valor de las criptomonedas, hemos utilizado la API de Coinapi.io

## Instalación 🔧

- Obtener la apikey en https://www.coinapi.io/ 
- Obtener una Scret Key en https://randomkeygen.com/ 
- Hacer una copia del fichero `config_template.py`:
    - En apikey  poner tu clave
    - En el SECRET_KEY poner tu Secret Key

```
apikey = "45gt76u67ii8i"
```
   

```
SECRET_KEY = "4rfEw65hg45y6h4g4"
```

- Renombrar al fichero copia como `config.py`
- Descargar la app DB Browser for SQLite
- En la carpeta data hay un fichero llamado create.sql que tiene la estructura para crear la tabla de la base de datos en DB Browser
- Hacer una copia del fichero `.env_template` y el FLASK_DEBUG poner True o False
- Renombrar la copia `.env_template` a el nombre `.env`


### Instalacion de dependencias

- Ejecutar `pip install -r requirements.txt``

- Por ultimo ejecutar

```
flask run
```
- Si el servidor 5000 esta ocupado ejecutar entonces
```
flask run -p 5001
```

