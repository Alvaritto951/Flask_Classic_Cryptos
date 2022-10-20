from flask import redirect, render_template, request, url_for, flash
from cryptomonedas import app
import sqlite3
from cryptomonedas.forms import Moneda
from config import *
from cryptomonedas.models import select_all, insert, peticion_crypto, invertido, recuperado, totalActivo_una_consulta, validador
from datetime import datetime, date
from wtforms import HiddenField



@app.route("/")
def index():
    try:
        registros = select_all()
        return render_template("index.html", pageTitle = "Cryptomonedas", data = registros, cabecera = 'index.html')
    except sqlite3.Error as e:
        flash("Se ha producido un error en la base datos, inténtelo de nuevo")
        return render_template("index.html", pageTitle="Todos", data = [])

        

@app.route("/purchase", methods=["GET", "POST"])
def comprar():
    moneda = Moneda()
    #registros = select_all()
    valorCantidad = request.values.get("inputCantidad") 
    #valorMonedaFrom = request.values.get('moneda_from')
    #valorMonedaTo = request.values.get('moneda_to')
    valorCantidad2 = HiddenField
    if request.method == "GET":
        return render_template("/purchase.html", PageTitle = "Comprar", formulario = moneda, cabecera = 'purchase.html', cantidad = "input")
    
    else:
        try:
            if request.values.get("submitCalcular"):
                
                try:
                    if moneda.inputCantidad.data == None:
                        flash("Introduce solo datos numéricos en la casilla Cantidad y, si es decimal utiliza el . (punto) (no la , (coma))")
                        return redirect(url_for("comprar"))
                    resultado = peticion_crypto(moneda.moneda_from.data, moneda.moneda_to.data, apikey)
                    total = resultado['rate'] * float(valorCantidad) #Importe
                    total = ("{:.8f}".format(total))
                    tasa = resultado['rate'] #Precio unitario
                    tasa = ("{:.8f}".format(tasa))
                    valorCantidad2._value = valorCantidad
                

                    return render_template("/purchase.html", resultado = total, Tasa = tasa, formulario = moneda, cabecera = "purchase.html", cantidad = "texto", valorinput = valorCantidad )
                except Exception as e:
                    print(e)
                    flash("No se ha podido conectar con la Api, por favor, inténtelo de nuevo pasados unos minutos")
                    return redirect(url_for("index"))
        
      

            elif request.values.get("submitCompra"):
                
                try:
                    validar = validador()
                    if validar != []:
                        return redirect (url_for('comprar'))
                    

                    if moneda.validate():
                        resultado = peticion_crypto(moneda.moneda_from.data, moneda.moneda_to.data, apikey)
                        total = resultado['rate'] * float(valorCantidad)
                        insert([datetime.now().date().isoformat(), str(datetime.now().time().isoformat())[:8], resultado["asset_id_base"], valorCantidad, resultado["asset_id_quote"], total])
                        flash("Compra realizada correctamente")
                        return redirect(url_for('index'))
                except sqlite3.Error as e:
                    print(e)
                    flash("Se ha producido error en la base datos")
                    return redirect(url_for('index'))
                
                
            else:
                flash('Error inesperado, vuelva a intentarlo'), 404
                return redirect(url_for('index'))
        
        except Exception as e:
            print(e)
            flash("Error, vuelva a intentarlo")
            return redirect(url_for("index"))


@app.route("/status")
def estado():
    invest = invertido()
    if invest[0]['Cantidad_from'] == None:
        flash("No hay ninguna compra de Cryptomonedas")
        return render_template("status.html", inv = [{'Cantidad_from': 0}], rec = [{'Cantidad_to': 0}], vComp = 0, vAct = 0, ganancia = 0, cabecera = 'status.html')
        
    else:
        
        try:
            inv = invertido()
            rec = recuperado()
            vCompra = inv[0]['Cantidad_from'] - rec[0]['Cantidad_to']
            vActivo = totalActivo_una_consulta()


            return render_template("status.html", inv = inv, rec = rec, vComp = vCompra , vAct = vActivo, ganancia = vActivo - vCompra, cabecera = 'status.html')
        except Exception as e:
            print(e)
            flash("Error de cálculo, inténtelo de nuevo más tarde")
            return redirect(url_for('index'))

