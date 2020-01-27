#python code to scrape live exchange rates 
#From the websites shapeshift.io and flyp
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

print("ETH EXCHANGE RATES ")
print("Please wait a minute, I am scrapping from this websites shapeshift, flyp, simpleswap, morphtoken, blocktrade, godex")

ETH=['ETH_ATOM', 'ETH_BTC', 'ETH_BCH', 'ETH_BAT', 'ETH_BNT', 'ETH_BLK', 'ETH_CVC', 'ETH_DASH', 'ETH_DGB', 'ETH_DNT', 'ETH_DOGE', 'ETH_ETC', 'ETH_FUN', 'ETH_GNO', 'ETH_GNT', 'ETH_LTC', 'ETH_MANA', 'ETH_MKR', 'ETH_OMG', 'ETH_POLY', 'ETH_RDD', 'ETH_RCN', 'ETH_RLC', 'ETH_SC', 'ETH_SNT', 'ETH_STORJ', 'ETH_TUSD', 'ETH_XMR', 'ETH_XRP', 'ETH_ZEC']
ETH2=['ATOM_ETH', 'BTC_ETH', 'BCH_ETH', 'BAT_ETH', 'BNT_ETH', 'BLK_ETH', 'CVC_ETH', 'DASH_ETH', 'DGB_ETH', 'DNT_ETH', 'DOGE_ETH', 'ETC_ETH', 'FUN_ETH', 'GNO_ETH', 'GNT_ETH', 'LTC_ETH', 'MANA_ETH', 'MKR_ETH', 'OMG_ETH', 'POLY_ETH', 'RDD_ETH', 'RCN_ETH', 'RLC_ETH', 'SC_ETH', 'SNT_ETH', 'STORJ_ETH', 'TUSD_ETH', 'XMR_ETH', 'XRP_ETH', 'ZEC_ETH']
u='https://shapeshift.io/marketinfo/'
#d={'pair', 'Exchange-Rate','MinerFee','limit','minimum','maximum'}
df = pd.DataFrame(columns=['pair', 'Exchange-Rate','Inverse-Rate'])
count=0




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

l_simpleswap=["xmr","btc","zec","etc","ltc","bch","dash","xlm","xrp","omg","doge","trx","eos","nano","tusd","tusd","dgd","neo","pax","usdc","xtz","bnbmainnet","btg","eth","usdt","ada","xem","zrx","waves","xvg","rep","icx","usdttrc20"]
url_simpleswap='https://api.simpleswap.io/fixed/get_estimated?currency_from=eth&currency_to='
base_simpleswap='https://api.simpleswap.io/fixed/get_estimated?currency_from='
df_simpleswap = pd.DataFrame(columns=['pair', 'Exchange-Rate','inverse-pair','inverse-rate'])
count=0
for pair in l_simpleswap:
    full_pair=pair+'&amount=1'
    new_url=url_simpleswap+full_pair
    pair_rate=requests.get(new_url)
    #print('eth-'+pair+':'+pair_rate.text)
    inverse_url=base_simpleswap+pair+'&currency_to=eth&amount=1'
    inverse_response=requests.get(inverse_url)
    inverse_pair=pair+'-eth'
    inverse_rate=inverse_response.text
    df_simpleswap.loc[count]=('eth-'+pair,pair_rate.text,inverse_pair,inverse_rate)
    count=count+1
print("THIS IS FROM SIMPLESWAP")
print(df_simpleswap)
print("null- not available in simpleswap website")


p = requests.get('https://api.morphtoken.com/rates')
#print(p.text)
html = bs(p.text, 'html.parser')
my_html=html.text
page=str(my_html)
morp=page[:-20]
dat=page.split('},')
df1_morph= pd.DataFrame(columns=['pair', 'Exchange-Rate'])
cot=0
ne=[]
for i in range(len(dat)):
    s=str(dat[i])
    ne.append(s.split('": {'))  
for element in ne:
    a=element[0]
    b=(element[1]).split(',')
    
    for pair in b:
        if 'ETH' in pair:
            inverse_pair=a[2:]+' to'
            inverse_rate=pair[2:-1]
            df1_morph.loc[cot]=(inverse_pair,inverse_rate)
            cot=cot+1

v=5
for element in ne:
    a=element[0]
    b=(element[1]).split(',')
    if 'ETH' in a:
        #print(b)
        for el in b:
            df1_morph.loc[v]=('ETH to',el)
            #print(el)
            v=v+1
print("THIS IS FROM MORPH-TOKENS")
print(df1_morph)

base_block="https://blocktrades.us/api/v2/estimate-input-amount?outputAmount=1&inputCoinType="
url_blocktrade="https://blocktrades.us/api/v2/estimate-input-amount?outputAmount=1&inputCoinType=eth&outputCoinType=" 
#l=[, 'affiliate_btc', 'affiliate_bchabc', 'affiliate_bchsv', 'affiliate_trade.usdlabor', 'affiliate_dash', 'affiliate_dgd', 'affiliate_doge', 'affiliate_eos', 'affiliate_eth', 'affiliate_ltc', 'affiliate_xmr', 'affiliate_nbt', 'affiliate_nsr', 'affiliate_open.btc', 'affiliate_open.dash', 'affiliate_omg', 'affiliate_ppc', 'affiliate_steem', 'affiliate_sbd', 'affiliate_trade.btc', 'affiliate_trade.ltc', 'affiliate_usdc', 'affiliate_usdt_erc20', 'affiliate_usdt_omni', 'bitshares.beos', 'bitbtc', 'bitcny', 'biteur', 'bitgold', 'bts', 'bitshares_mkr', 'bitusd', 'trade.usdlabor', 'brownie.pts', 'open.btc', 'open.dao', 'open.dash', 'open.dgd', 'open.eth', 'open.mkr', 'open.sbd', 'open.steem', 'open.usd', 'open.usdt', 'rudex.steem', 'tester.btc', 'tester.ltc', 'trade.btc', 'trade.dash', 'trade.doge', 'trade.ltc', 'trade.nbt', 'trade.nsr', 'trade.ppc', 'trade.muse', 'whaleshare', 'bts1.bitbtc', 'bts1.bitcny', 'bts1.biteur', 'bts1.bitgold', 'bts1.bts', 'bts1.bitusd', 'bts1.brownie.pts', 'bts1.note', 'bts1.tester.btc', 'bts1.tester.ltc', 'bts1.trade.btc', 'bts1.trade.ltc', 'btc', 'peerplays_ico',  'cpu_eos', 'network_eos', 'bat', 'dao', 'dgd', 'eth', 'ethereum_mkr', 'kin', 'mit_ito', 'omg', 'usdc', 'usdt_erc20', 'ltc', 'muse', 'xmr', 'nbt', 'nsr', 'agrs', 'eurt', 'maid', 'omni', 'amp', 'usdt_omni', 'ppc', 'delegatable_vests', ]
new_l=['bchabc', 'bchsv', 'dash', 'doge', 'eos','btc','ltc','steem', 'steem_account_creation', 'sbd', 'steem_power','usdt_omni']
nw=['bchabc', 'bchsv', 'dash', 'doge', 'eos','btc','ltc','steem', 'usdt_omni']
df1_blocktrade= pd.DataFrame(columns=['pair', 'Exchange-Rate'])
var=0
for i in new_l:
    final_url=url_blocktrade+i
    pg=requests.get(final_url)
    d=(pg.text).split(',')
    dc=(d[0]).split(':')
    rate=dc[1]
    pair='eth-'+i
    df1_blocktrade.loc[var]=(pair,rate[1:-1])
    var=var+1
vari=9
for i in nw:
    final_url=base_block+i+'&outputCoinType=eth'
    pg=requests.get(final_url)
    d=(pg.text).split(',')
    dc=(d[0]).split(':')
    rate=dc[1]
    pair=i+'-eth'
    df1_blocktrade.loc[vari]=(pair,rate[1:-1])
    vari=vari+1
    #print(res)
print("THIS IS FROM BLOCK-TRADE")
print(df1_blocktrade)

godex_lst=['BTC', 'XMR', 'ZEC', 'BCH', 'BSV',  'DASH']
df1_godex= pd.DataFrame(columns=['pair', 'Exchange-Rate'])
godex_ct=0
url="https://api.godex.io/api/v1/info"
for element in  godex_lst:
    d= {
            "from": element,
            "to": "ETH",
            "amount": 1}
    r = requests.post(url, data=d)
    l=r.text
    la=l.split(',')
    rate=la[-1]
    df1_godex.loc[godex_ct]=(element+'-ETH',rate[1:-1])
    godex_ct=godex_ct+1
    
godex_ct2=6
for element in  godex_lst:
    d= {
            "from": 'ETH',
            "to": element,
            "amount": 1}
    r = requests.post(url, data=d)
    l=r.text
    la=l.split(',')
    rate=la[-1]
    df1_godex.loc[godex_ct2]=('ETH-'+element,rate[1:-1])
    godex_ct2=godex_ct2+1
print("THIS IS FROM GODEX")
print(df1_godex)

