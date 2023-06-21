#import backtrader
import backtrader as bt

#import datetime
import datetime as dt

#Import yfinance
import yfinance as yf

#Import matplotlib
import matplotlib.pyplot as plt

# %%
# Define a simple moving average strategy
class TrendFollowingStrategy(bt.Strategy):
  def __init__(self):
    #Define the parameters to use
    self.sma = bt.indicators.SimpleMovingAverage(self.data, period=50)
    self.rsi = bt.indicators.RelativeStrengthIndex(self.data, period=14)
  
  def next(self):
    # Verifique as condições para abrir uma posição
    if self.data.close[0] > self.sma[0] and self.rsi[0] > 50:
      self.buy()
            
    # Verifique as condições para fechar uma posição
    if self.data.close[0] < self.sma[0] and self.rsi[0] < 50:
      self.sell()

# %%
#Cria uma instância do cerebro (backtest engine) e adiciona a estratégia:
cerebro = bt.Cerebro()
cerebro.addstrategy(TrendFollowingStrategy)

# %%
# Defina os símbolos das ações e o período desejado
symbols = ['BOVA11.SA']  # Exemplo de símbolos
start_date = '2010-01-01'
end_date = '2021-01-01'

# Baixe os dados do Yahoo Finance como objetos DataFrame
data = {}
for symbol in symbols:
    data[symbol] = yf.download(symbol, start=start_date, end=end_date)

# Converta os DataFrames para um formato compatível com o backtrader
for symbol, df in data.items():
    data_feed = bt.feeds.PandasData(dataname=df)
    df.to_csv(f'{symbol}.csv')  # Salve os dados em um arquivo CSV
    cerebro.adddata(data_feed, name=f'{symbol}.csv')

# %%
#Configurar o tamanho do lote e o valor inicial do portfólio:
cerebro.addsizer(bt.sizers.FixedSize, stake=10)  # Tamanho fixo do lote
cerebro.broker.setcash(100000)  # Valor inicial do portfólio


# %%
# Execute o backtest
cerebro.run()

# %%
#Plota os resultados
cerebro.plot()

input('Pressione ENTER para sair')