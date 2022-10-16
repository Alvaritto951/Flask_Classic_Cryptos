from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, Label, FloatField
from wtforms.validators import DataRequired, InputRequired, NumberRange, Length
import requests
class Moneda(FlaskForm):
    moneda_from = SelectField('From', choices=[('EUR', 'EUR - EURO'), ('BTC', 'BTC - Bitcoin'), ('ETH', 'ETH - Ether'), ('USDT', 'USDT - Tether'), ('BNB', 'BNB - Binance Coin'), ('XRP', 'XRP - Ripple'), ('ADA', 'ADA - Cardano'),('SOL', 'SOL -'), ('DOT', 'DOT -'), ('MATIC', 'MATIC -')])
    moneda_to = SelectField('To', choices=[('EUR', 'EUR - EURO'), ('BTC', 'BTC - Bitcoin'), ('ETH', 'ETH - Ether'), ('USDT', 'USDT - Tether'), ('BNB', 'BNB - Binance Coin'), ('XRP', 'XRP - Ripple'), ('ADA', 'ADA - Cardano'),('SOL', 'SOL -'), ('DOT', 'DOT -'), ('MATIC', 'MATIC -')])
    inputCantidad = FloatField('Cantidad', validators=[InputRequired(), NumberRange(min=0.00001, max=99999999), DataRequired()])

    submitCalcular = SubmitField('Calculate' 'Calcular')
    submitCompra = SubmitField('done_outline' 'Aceptar')


class todoCoinApiIo:
    def __init__(self):
        self.criptos= []
        self.no_criptos = []
    
    def trae(self, apikey):
        
        r = requests.get("https://rest.coinapi.io/v1/assets?apikey={}". format(apikey))
        if r.status_code != 200:
            raise Exception("error en consulta de assets: {}". format(r.status_code))

        lista_candidatas = r.json()
        for candidata in lista_candidatas:
            if candidata["type_is_crypto"] == 1:
                self.criptos.append(candidata["asset_id"])
            else:
                self.no_criptos.append(candidata["asset_id"])

#Cambia de cripto a moneda deseada
class Cambio:
    def __init__(self, cripto):
        self.cripto = cripto
        self.tasa = None
        self.horefecha = None

    def actualiza(self, apikey):
        r = requests.get("https://rest.coinapi.io/v1/exchangerate/{}/EUR?apikey={}". format(self.cripto, apikey))
        resultado = r.json()
        if r.status_code == 200 :
            self.tasa = resultado["rate"]
            self.horefecha = resultado["time"]
        else:
            pass
            #raise ModelError("{} : {}" .format(r.status_code, resultado["error"]))