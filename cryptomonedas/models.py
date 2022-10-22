from wtforms import HiddenField
import sqlite3
from config import *
import requests
from datetime import *
from cryptomonedas.routes import *

def filas_to_diccionario(filas, columnas):

    resultado = []
    for fila in filas:  
        posicion_columna = 0
        d = {}
        for campo in columnas:
            d[campo[0]] = fila[posicion_columna]
            posicion_columna += 1
        resultado.append(d)
    
    return resultado


def select_all():
    conn = sqlite3.connect(ORIGIN_DATA)
    cur = conn.cursor()
    cur.execute("SELECT id, Fecha, Hora, moneda_from, cantidad_from, Moneda_to, Cantidad_to, (cantidad_from/Cantidad_to) as PU from movements order by Fecha;")
    result = filas_to_diccionario(cur.fetchall(), cur.description)
    conn.close()
    return result


def insert(registro):
    conn = sqlite3.connect(ORIGIN_DATA)
    cur = conn.cursor()
    cur.execute("INSERT INTO movements (Fecha, Hora, Moneda_from, Cantidad_from, Moneda_to, cantidad_to) values(?,?,?,?,?,?)", registro)
    conn.commit()
    conn.close()

def peticion_crypto(moneda_from_data, moneda_to_data, apikey):
    url = requests.get(f"https://rest.coinapi.io/v1/exchangerate/{moneda_from_data}/{moneda_to_data}?&apikey={apikey}")
    resultado = url.json()
    return resultado

def invertido():
    conn = sqlite3.connect(ORIGIN_DATA)
    cur = conn.cursor()
    cur.execute("SELECT SUM(Cantidad_from) as Cantidad_from FROM movements WHERE Moneda_from = 'EUR'")
    result = filas_to_diccionario(cur.fetchall(), cur.description)
    conn.close()
    return result

def recuperado():
    conn= sqlite3.connect(ORIGIN_DATA)
    cur = conn.cursor()
    cur.execute("SELECT (CASE WHEN SUM(Cantidad_to) IS NULL THEN 0 ELSE SUM(Cantidad_to) end) as Cantidad_to FROM movements WHERE Moneda_to = 'EUR'")
    result = filas_to_diccionario(cur.fetchall(), cur.description)
    conn.close()
    return result


def cartera(moneda):
    consulta = f"SELECT ((SELECT (case when (SUM(Cantidad_to)) is null then 0 else SUM(Cantidad_to) end) as COMPRAR FROM movements WHERE Moneda_to = '{moneda}') - (SELECT (case when (SUM(Cantidad_from)) is null then 0 else SUM(Cantidad_from) end) as GASTAR FROM movements WHERE Moneda_from = '{moneda}')) AS {moneda}"
    #Calcular la cantidad total de cada tipo de moneda (EUR o BTC o ETH...) que tienes
    conn= sqlite3.connect(ORIGIN_DATA)
    cur = conn.cursor()
    cur.execute(consulta)
    result = filas_to_diccionario(cur.fetchall(), cur.description)
    conn.close()
    return result  


def traerTodasCartera(crypto):
    cryptosMonedas = {}
    conn= sqlite3.connect(ORIGIN_DATA)
    cur = conn.cursor()
    for moneda in crypto:
        consulta = f"SELECT ((SELECT (case when (SUM(Cantidad_to)) is null then 0 else SUM(Cantidad_to) end) as tot FROM movements WHERE Moneda_to = '{moneda}') - (SELECT (case when (SUM(Cantidad_from)) is null then 0 else SUM(Cantidad_from) end) as ee FROM movements WHERE Moneda_from = '{moneda}')) AS {moneda}"
        cur.execute(consulta)
        fila =cur.fetchall() 
        cryptosMonedas[moneda] = fila[0][0]
    conn.close()
     
    return cryptosMonedas

def totalActivo_una_consulta():    
    total = 0
    monederoActual = traerTodasCartera(cryptos)
    url = requests.get(f"https://rest.coinapi.io/v1/exchangerate/EUR?&apikey={apikey}")
    resultado = url.json()

    for a in monederoActual.keys(): #Para un valor en las claves de monederoActual
        for b in resultado['rates']: #Para un valor dentro de los resultados de las tasas
            if b['asset_id_quote'] == a: #Si el valor de la tasa de b = al valor de a
                total += 1/b['rate'] * monederoActual[a] #Al total se le suma 1/tasa de b multiplicado por el valor de a en monederoActual
                
    return total


def validador():
    error = [] #Error es una lista vacía
    registros = select_all() #Traemos todos los valores
    valorCantidad = request.values.get("inputCantidad") #Valor de valorCantidad
    valorMonedaFrom = request.values.get('moneda_from') #Valor de valorMonedaFrom
    valorMonedaTo = request.values.get('moneda_to') #Valor de valorMonedaTo
    valorCantidad2 = HiddenField #Valor de valorCantidad2, es un campo oculto. Es el que te obliga a que le des a aceptar una vez hayas calculado la tasa y te impide seguir.

    if registros == [] and valorMonedaFrom != "EUR": #Si los registros están vacíos y la moneda es distinta a €
        show_error = flash("En la primera compra de Cryptomonedas sólo pueden utilizarse Euros") #Lanza el mensaje de error
        error.append(show_error) #Añádelo
        return error #Devuélve el error
       
    if valorMonedaFrom == valorMonedaTo:
        show_error = flash("Las monedas no pueden ser las mismas")
        error.append(show_error)
        return error

    if valorCantidad2._value != valorCantidad: #Si el valor de valorCantidad se modifica o no se calcula
        show_error = flash("Es obligatorio obtener el valor en el botón 'Calcular' antes de comprar")
        error.append(show_error)
        return error

    monedero = cartera(valorMonedaFrom)
    if (valorMonedaFrom != 'EUR' and monedero[0][valorMonedaFrom] < float(valorCantidad)):
        #Si el valor de la moneda a gastar es distinto de € y el monedero (que lo calcula cartera) es más pequeño que el valor que se indica
        show_error = flash(f"No hay saldo suficiente de la moneda {valorMonedaFrom}") #Indica que no hay dinero
        error.append(show_error)
        return error
    
    return error