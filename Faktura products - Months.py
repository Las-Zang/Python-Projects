from __future__ import nested_scopes
from tracemalloc import stop
import pandas as pd
import pandas
from datetime import datetime
from datetime import date
import requests, json
import time
df = pd.read_excel('faktura2020.xlsx')  


df['dato'] = pd.to_datetime(df['dato'],format='%Y-%m-%d') # Til datetime

#__________________skaf all produkter_______
payload = ""
reqUrl = "https://restapi.e-conomic.com/products?skippages=0&pagesize=1000"
headersList = {
 "X-AppSecretToken": "SECRET",
 "X-AgreementGrantToken": "SECRET",
 "Content-Type": "application/json" 
}
response = requests.request("GET", reqUrl, data=payload,  headers=headersList)
js = json.loads(response.text)
js
produktid = []
unitid =[]
produkt = []
unitname = []
for x in js["collection"]:
     if "unit" in x:
         print("yes")
         produkt.append(x["name"])
         produktid.append(x["productNumber"])
         unitid.append(x["unit"]['unitNumber'])
         unitname.append(x["unit"]['name'])
     else:
         print(x["productNumber"],"virker ikke")

len(produktid)

if len(unitid) == len(produkt) == len(produktid) == len(unitname):
    print("length ok")
else:
    print("length fked")

#___________________________________LAV DATO OM TIL MÅNED_______________________________________________

df["dato"] = df["dato"].dt.to_period('M') # lav om til 2021-01
df['dato'] = df['dato'].apply(str) # lav til string fra datetime object
datolist = df["dato"].tolist() # til list
datolist = list(dict.fromkeys(datolist)) # fjern duplicates
datolist = datolist[datolist.index('2021-01'):] # start fra 2021

#_______________________________________START MED DATA_________________________________________________

today = date.today()

stopmåned = (today.year - (today.year - 1) ) * 12 + today.month
årstart = (today.year - 1)
nytår = 0
antal = []
enhednavn = []
produktnavn = []
produktidx = []
produktdato = []
omsætning = []
stopprodukt = len(produkt)
stopmåned
måned = 0
while måned != stopmåned:
 pro = 0
 while stopprodukt != pro:
        antalx = (df[(df['produktnummer']==produktid[pro]) & (df['unitnumber']==unitid[pro]) & (df['dato']==datolist[måned]) ])['antal'].sum()
        antal.append(antalx)
        produktdato.append(datolist[måned])
        produktnavn.append(produkt[pro])
        enhednavn.append(unitname[pro])
        produktidx.append(produktid[pro])
        omsætningx = (df[(df['produktnummer']==produktid[pro]) & (df['unitnumber']==unitid[pro]) & (df['dato']==datolist[måned]) ])['totalnetamount'].sum()
        omsætning.append(omsætningx)
        pro = pro +1
 print(årstart + nytår,"måned",måned + 1,"done")
 måned = måned + 1
 if måned = 11:
     nytår = nytår + 1

len(produktnavn)

produktidx
df0 = pd.DataFrame (produktidx,columns=["ProduktID",])
df1 = pd.DataFrame (produktnavn,columns=["Produkt",])
df2 = pd.DataFrame (antal,columns=["Antal_Solgt",])
df3 = pd.DataFrame (enhednavn,columns=["Enhed",])
df4 = pd.DataFrame (produktdato,columns=["dato",])
df5 = pd.DataFrame (omsætning,columns=["Omsætning",])

produkter = pd.concat([df0,df1,df2,df3,df4,df5], axis=1, join="inner")
produkter
resultat = produkter[produkter.Antal_Solgt != 0]
resultat["Omsætning,"].sum()
produkter.to_excel("produktresultat.xlsx")
