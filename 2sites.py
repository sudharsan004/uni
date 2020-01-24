from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

ETH=['ETH_ATOM', 'ETH_BTC', 'ETH_BCH', 'ETH_BAT', 'ETH_BNT', 'ETH_BLK', 'ETH_CVC', 'ETH_DASH', 'ETH_DGB', 'ETH_DNT', 'ETH_DOGE', 'ETH_ETC', 'ETH_FUN', 'ETH_GNO', 'ETH_GNT', 'ETH_LTC', 'ETH_MANA', 'ETH_MKR', 'ETH_OMG', 'ETH_POLY', 'ETH_RDD', 'ETH_RCN', 'ETH_RLC', 'ETH_SC', 'ETH_SNT', 'ETH_STORJ', 'ETH_TUSD', 'ETH_XMR', 'ETH_XRP', 'ETH_ZEC']
ETH2=['ATOM_ETH', 'BTC_ETH', 'BCH_ETH', 'BAT_ETH', 'BNT_ETH', 'BLK_ETH', 'CVC_ETH', 'DASH_ETH', 'DGB_ETH', 'DNT_ETH', 'DOGE_ETH', 'ETC_ETH', 'FUN_ETH', 'GNO_ETH', 'GNT_ETH', 'LTC_ETH', 'MANA_ETH', 'MKR_ETH', 'OMG_ETH', 'POLY_ETH', 'RDD_ETH', 'RCN_ETH', 'RLC_ETH', 'SC_ETH', 'SNT_ETH', 'STORJ_ETH', 'TUSD_ETH', 'XMR_ETH', 'XRP_ETH', 'ZEC_ETH']
u='https://shapeshift.io/marketinfo/'
#d={'pair', 'Exchange-Rate','MinerFee','limit','minimum','maximum'}
df = pd.DataFrame(columns=['pair', 'Exchange-Rate','Inverse-Rate'])
count=0



print("ETH EXCHANGE RATES")
print("Please wait I am scrapping from two websites shapeshift and flyp")
for pair in ETH:
    url=u+pair
    page=requests.get(url)
    html = bs(page.text, 'html.parser')
    my_dict=html.text
    lst=my_dict.split(',')
    rate=lst[1]
    #print(rate)
    p=pair.split('_')
    exchange_rate='1 ETH ='+rate[7:-2]+" "+p[1]
    inv=requests.get(u+ETH2[count]).text
    inve=inv.split(',')
    inver=inve[1]
    inverse_rate='1'+p[1]+'='+inver[7:-2]+p[0]
    df.loc[count]=(p[1],exchange_rate,inverse_rate)
    count=count+1
print("THIS IS FROM SHAPESHIFT ")
print(df)

df2 = pd.DataFrame(columns=['pair', 'Exchange-Rate','Inverse-Rate'])

flyp='https://flyp.me/api/v1/data/exchange_rates'
page2=requests.get(flyp)
data=page2.text
all=data.split(',')
eth_pair=[]
ETH_exchange_rate=[]
ETH_inverse_rate=[]
for element in all:
    if 'ETH' in element:
        eth_pair.append(element)
for pair in eth_pair:
    p=str(pair)
    if 'ETH-' in p:
        ETH_exchange_rate.append(p[1:-1])
    else:
        ETH_inverse_rate.append(p[1:-1])

for i in range(len(ETH_exchange_rate)):
    exchange_rate=str(ETH_exchange_rate[i])
    inverse_rate=str(ETH_inverse_rate[i])
    pair=exchange_rate.split(':')
    p2=str(pair[0])
    df2.loc[i]=(p2[0:-1],exchange_rate,inverse_rate)
print("THIS IS FROM FLYP")
print(df2)





