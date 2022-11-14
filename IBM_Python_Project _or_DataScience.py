#Extracting and Visualizing Stock Data
#Description
#Extracting essential data from a dataset and #displaying it is a necessary part of data #science; therefore individuals can make correct #decisions based on the data. In this assignment, #you will extract some stock data, you will then #display this data in a graph.

!pip install yfinance==0.1.67
!mamba install bs4==4.10.0 -y
!pip install nbformat==5.1.3

import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots


#Define Graphing Function
def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()

#Use yfinance to Extract Stock Data
Tesla=yf.Ticker('TSLA')
tesla_data= Tesla.history(period='max')
tesla_data.reset_index(inplace=True)

#Use Webscraping to Extract Tesla Revenue Data
html_data =requests.get('https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue').text
beautiful_soup=BeautifulSoup(html_data,'html5lib')
tesla_revenue=pd.read_html(str(beautiful_soup))[1]
tesla_revenue.columns=['Date','Revenue'] 
tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"") #remove the comma and dollar sign from the Revenue column

 #Remove an null or empty strings in the Revenue column.
tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]

tesla_revenue.tail() #Display the last 5 row of the tesla_revenue dataframe using the tail function

#Use yfinance to Extract Stock Data
GameStop=yf.Ticker('GME')
gme_data = GameStop.history(period='max')
gme_data.reset_index(inplace=True)

#Use Webscraping to Extract GME Revenue Data
html_data = requests.get('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html').text
beautiful_soup=BeautifulSoup(html_data,'html5lib')
gme_revenue=pd.read_html(str(beautiful_soup))[1]

gme_revenue.columns=['Date','Revenue']
gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace(',|\$',"")

#Plot Tesla Stock Graph
make_graph(tesla_data, tesla_revenue, 'Tesla')

#Plot GameStop Stock Graph
make_graph(gme_data, gme_revenue, 'GameStop')