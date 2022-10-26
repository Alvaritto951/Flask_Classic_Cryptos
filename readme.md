# PROYECTO WEB CRYPTOMONEDAS 👛
- Proyecto fin Bootcamp Aprender a programar desde cero - Edición XII ~~ KeepCoding

- Flask classic

- Registro de inversiones y compra/venta de Cryptomonedas

# Compra-venta y tradeo de Cryptomonedas 💱

Programa hecho en Python como lenguaje principal. También se ha utilizado: Flask, HTML5, CSS3 y Jinja.
Para consultar y recuperar el valor de las cryptomonedas, se utiliza la API de Coinapi.io

## Instalación 🤓💬

- Realizar gitclone desde la dirección de GitHub: https://github.com/Alvaritto951/Flask_Classic_Cryptos.git
- Obtener la apikey en https://www.coinapi.io/ 
- Obtener una Secret Key en https://randomkeygen.com/ 
- Hacer una copia del fichero `config_template.py`:
    - En apikey indicar tu clave personal e intransferible
    - En el SECRET_KEY poner tu Secret Key

### EJEMPLOS DE KEY🖥️🔐
```
apikey = "45gt76u67ii8i"

SECRET_KEY = "4rfEw65hg45y6h4g4"
```

- Renombrar al fichero `config_template.py` como `config.py`
- Descargar la app DB Browser for SQLite: https://sqlitebrowser.org/
- En la carpeta `data` se encuentra un fichero llamado `create.sql` que tiene la estructura para crear la tabla de la base de datos en  DB Browser
- Hacer una copia del fichero `.env_template` y renombrar como `.env`
- Dentro del fichero, en el apartado `FLASK_DEBUG` indicar `True` o `False`

#### Instalacion de dependencias 🛠️🖥️

- Ejecutar `pip install -r requirements.txt`

- Por ultimo ejecutar

```
flask run
```
- Si el servidor 5000 está ocupado ejecutar entonces
```
flask run -p 5001
```

💱¡¡Y listo!! Ya tienes tus consultas, compras y tradeos de cryptomonedas!! 💱🔚
