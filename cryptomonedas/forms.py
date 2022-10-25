from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, Label, FloatField
from wtforms.validators import DataRequired, InputRequired, NumberRange, Length
import requests
class Moneda(FlaskForm):
    moneda_from = SelectField('From', choices=[('EUR', 'EUR - EURO'), ('BTC', 'BTC - Bitcoin'), ('ETH', 'ETH - Ethereum'), ('USDT', 'USDT - Tether'), ('BNB', 'BNB - Binance Coin'), ('XRP', 'XRP - Ripple'), ('ADA', 'ADA - Cardano'),('SOL', 'SOL -'), ('DOT', 'DOT -'), ('MATIC', 'MATIC -')])
    moneda_to = SelectField('To', choices=[('EUR', 'EUR - EURO'), ('BTC', 'BTC - Bitcoin'), ('ETH', 'ETH - Ethereum'), ('USDT', 'USDT - Tether'), ('BNB', 'BNB - Binance Coin'), ('XRP', 'XRP - Ripple'), ('ADA', 'ADA - Cardano'),('SOL', 'SOL -'), ('DOT', 'DOT -'), ('MATIC', 'MATIC -')])
    inputCantidad = FloatField('Cantidad', validators=[InputRequired(), NumberRange(min=0.00001, max=99999999), DataRequired()])

    submitCalcular = SubmitField('Calculate' 'Calcular') #Agregado en styles posición del botón
    submitCompra = SubmitField('done_outline' 'Aceptar')
