#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gettingstarted.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
    import os
    import requests
    import datetime
    from datetime import date
    from datetime import datetime
    from bs4 import BeautifulSoup
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages


    nbAppleStock = 189
    nbMicrosoftStock = 100
    AppleInit = 127.84
    MicrosoftInit = 228.0599
    EURUSDInit = 1.19517400 
    InitialWalletInvested = (nbAppleStock * AppleInit + nbMicrosoftStock * MicrosoftInit)/EURUSDInit
    fees = 0.0047 * InitialWalletInvested
    feesApple = 0.0047 * AppleInit*nbAppleStock / EURUSDInit
    feesMicrosoft = 0.0047 * MicrosoftInit*nbMicrosoftStock / EURUSDInit
    fees = 0
    feesApple = 0
    feesMicrosoft = 0

    url1='https://fr.finance.yahoo.com/quote/AAPL/history/'
    url2='https://fr.finance.yahoo.com/quote/MSFT/history/'
    url3='https://fr.finance.yahoo.com/quote/EURUSD=X/'
    url4='https://finance.yahoo.com/quote/AAPL/history?p=AAPL'
    url5='https://finance.yahoo.com/quote/MSFT/history?p=MSFT'
    url6='https://finance.yahoo.com/quote/EURUSD%3DX/history?p=EURUSD%3DX'
    url7='https://www.boursedirect.fr/fr/marche/nasdaq-ngs-global-select-market/apple-inc-AAPL-USD-XNGS/seance'
    url8='https://www.boursedirect.fr/fr/marche/nasdaq-ngs-global-select-market/microsoft-corporation-MSFT-USD-XNGS/seance'
    page1 = requests.get(url1)
    page2 = requests.get(url2)
    page3 = requests.get(url3)
    page4 = requests.get(url4)
    page5 = requests.get(url5)
    page6 = requests.get(url6)
    page7 = requests.get(url7)
    page8 = requests.get(url8)
    soup1 = BeautifulSoup(page1.text, 'html.parser')
    soup2 = BeautifulSoup(page2.text, 'html.parser') 
    soup3 = BeautifulSoup(page3.text, 'html.parser')
    soup4 = BeautifulSoup(page4.text, 'html.parser')
    soup5 = BeautifulSoup(page5.text, 'html.parser')
    soup6 = BeautifulSoup(page6.text, 'html.parser')
    soup7 = BeautifulSoup(page7.text, 'html.parser')
    soup8 = BeautifulSoup(page8.text, 'html.parser')
    #print(soup7.prettify())

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_time_pdf_name = now.strftime("%H_%M_%S")
    print("Current Time =", current_time)

    if  (int(now.strftime("%H"))<15 or (int(now.strftime("%H"))==15 and int(now.strftime("%M"))<=30)) or (int(now.strftime("%H"))>=22 and int(now.strftime("%M"))>=15) or (int(now.strftime("%H"))>22):
        AppleStockPriceString = soup7.find('tbody',{'class':"bd-streaming-select-value-trades"}).findAll("td")[2:3][0]
        AppleStockPriceString = str(AppleStockPriceString)
        AppleStockPriceString=AppleStockPriceString.replace("<td>","").replace("</td>","")
        MicrosoftStockPriceString = soup8.find('tbody',{'class':"bd-streaming-select-value-trades"}).findAll("td")[2:3][0]
        MicrosoftStockPriceString = str(MicrosoftStockPriceString)
        MicrosoftStockPriceString=MicrosoftStockPriceString.replace("<td>","").replace("</td>","")
    else :
        AppleStockPriceString = soup1.find('div',{'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span').text
        MicrosoftStockPriceString = soup2.find('div',{'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span').text

    EURUSDString = soup3.find('div',{'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span').text
    AppleStockPriceString = AppleStockPriceString.replace(",",".")
    MicrosoftStockPriceString = MicrosoftStockPriceString.replace(",",".")
    EURUSDString = EURUSDString.replace(",",".")
    AppleStockPrice = float(AppleStockPriceString)
    MicrosoftStockPrice = float(MicrosoftStockPriceString)
    EURUSD = float(EURUSDString)
    print("EURUSD: " + EURUSDString)
    print("AppleStockPrice: " + str(AppleStockPrice) + "$")
    print("MicrosoftStockPrice: " + str(MicrosoftStockPrice) + "$")
    EURUSDPerformance = 1/(1 + (EURUSD/EURUSDInit)-1) - 1
    print("EURUSD Performance SI: " + str(round(EURUSDPerformance * 100,2)) + "%")
    WalletPresentValue = (nbAppleStock * AppleStockPrice + nbMicrosoftStock * MicrosoftStockPrice)/EURUSD
    Performance =(WalletPresentValue/(InitialWalletInvested) - 1)
    print("Overall Performance SI: " + str(round((Performance)*100,2)) + "%")
    print("Apple Performance SI: " + str(round((((1 + AppleStockPrice/(AppleInit) - 1))*(1-feesApple/(nbAppleStock*AppleInit))*(1+EURUSDPerformance)-1)*100,2))+ "%")
    PNLApple = round(nbAppleStock* AppleStockPrice/EURUSD - nbAppleStock*AppleInit/EURUSDInit, 2)
    print("P&L on Apple: " + str(PNLApple) + "€")
    print("Microsoft Performance SI: " + str(round((((1 + MicrosoftStockPrice/(MicrosoftInit) - 1))*(1-feesMicrosoft/(nbMicrosoftStock*MicrosoftInit))*(1+EURUSDPerformance)-1)*100,2)) + "%")
    PNLMicrosoft = round(nbMicrosoftStock* MicrosoftStockPrice/EURUSD - nbMicrosoftStock*MicrosoftInit/EURUSDInit, 2)
    print("P&L on Microsoft: " + str(PNLMicrosoft) + "€")
    print("P&L: " + str(round(PNLApple + PNLMicrosoft,2)))
    print("Invested Wallet Present Value in €: " + str(round(WalletPresentValue,2)))
    Cash = 11569.54
    print("Total Compte Titres in €: " + str(round(Cash + WalletPresentValue,2)))

    text=""
    text += "Current Time =" + current_time + "\n"
    text += "EURUSD: " + EURUSDString + "\n"
    text +="AppleStockPrice: " + str(AppleStockPrice) + "$" + "\n"
    text +="MicrosoftStockPrice: " + str(MicrosoftStockPrice) + "$" + "\n"
    text +="EURUSD Performance SI: " + str(round(EURUSDPerformance * 100,2)) + "%" + "\n"
    text +="Overall Performance SI: " + str(round((Performance)*100,2)) + "%" + "\n"
    text +="Apple Performance SI: " + str(round((((1 + AppleStockPrice/(AppleInit) - 1))*(1-feesApple/(nbAppleStock*AppleInit))*(1+EURUSDPerformance)-1)*100,2))+ "%" + "\n"
    text +="P&L on Apple: " + str(PNLApple) + "€" + "\n"
    text +="Microsoft Performance SI: " + str(round((((1 + MicrosoftStockPrice/(MicrosoftInit) - 1))*(1-feesMicrosoft/(nbMicrosoftStock*MicrosoftInit))*(1+EURUSDPerformance)-1)*100,2)) + "%" + "\n"
    text +="P&L on Microsoft: " + str(PNLMicrosoft) + "€" + "\n"
    text +="Overall P&L: " + str(round(PNLApple + PNLMicrosoft,2)) +"€" + "\n"
    text +="Invested Wallet Present Value in €: " + str(round(WalletPresentValue,2)) + "\n"
    text +="Total Compte Titres in €: " + str(round(Cash + WalletPresentValue,2)) + "\n"

    table = soup4.find('table')
    table_rows = table.find_all('tr')
    res = []
    for tr in table_rows:
        td = tr.find_all('td')
        row = [tr.text.strip() for tr in td if tr.text.strip()]
        if row:
            res.append(row)
    df1 = pd.DataFrame(res, columns=["Date", "Ouverture", "Élevé ", "Faible ","Clôture*","Cours de clôture ajusté**","Volume"])
    df1 = df1.drop(["Ouverture", "Élevé ", "Faible ","Cours de clôture ajusté**","Volume"], axis=1)
    df1 = df1.drop_duplicates("Date", keep='first', inplace=False)
    df1['Clôture*'] = df1['Clôture*'].str.replace(',','.')
    df1["Clôture*"] = pd.to_numeric(df1["Clôture*"], downcast="float")
    df1["Rendement"] = df1['Clôture*'].pct_change()
    df1["Date"] = df1["Date"].astype(str)
    indexNames = df1[ df1['Date'].str.contains("split") ].index
    df1.drop(indexNames , inplace=True)
    df1['Date'] = df1['Date'].astype('datetime64[ns]')
    df1["Date"] = pd.to_datetime(df1["Date"])
    df1 = df1.sort_values(by="Date")
    df1RSI=df1.tail(15)
    df1RSI=df1.head(14)
    df1rendementspositifs = df1RSI[df1RSI["Rendement"]>0]
    df1rendementsnegatifs = df1RSI[df1RSI["Rendement"]<0]
    AVG1=float(df1rendementspositifs["Rendement"].mean())*100
    AVG2=-float(df1rendementsnegatifs["Rendement"].mean())*100
    p= AVG1 / AVG2
    RSIApple= 100 - 100/(1+p)
    print("RSI Apple: " + str(RSIApple))
    df1["Date"] = df1["Date"].astype(str)
    indexNames = df1[ df1['Date'].str.contains("split") ].index
    df1.drop(indexNames , inplace=True)
    df1['Date'] = df1['Date'].astype('datetime64[ns]')
    df1temp = pd.read_csv("AppleData.csv",index_col=False)
    df1temp["Date"]= df1temp['Date'].astype('datetime64[ns]')
    df1["Clôture*"]=df1["Clôture*"].astype(float).round(2)
    df1["Rendement"]=df1["Rendement"].astype(float).round(2)
    df1temp["Clôture*"]=df1temp["Clôture*"].astype(float).round(2)
    df1temp["Rendement"]=df1temp["Rendement"].astype(float).round(2)
    df1=pd.merge(df1, df1temp, on = ["Date","Clôture*","Rendement" ], right_index=False, how='outer')
    df1=df1.drop_duplicates('Date', keep="first", inplace=False)
    df1['Date'] = df1['Date'].astype('datetime64[ns]')
    df1.to_csv("AppleData.csv",index=False)
    df1.plot(figsize=(10,2), x ='Date', y='Clôture*', kind = 'line')
    plt.title('Apple Stock Prices in $')
    plt.xlabel('Dates')
    plt.ylabel('Stock Price in $')
    plt.show()
    df1Wallet = df1[df1["Date"] >= '2020-09-01']
    table = soup5.find('table')
    table_rows = table.find_all('tr')
    res = []
    for tr in table_rows:
        td = tr.find_all('td')
        row = [tr.text.strip() for tr in td if tr.text.strip()]
        if row:
            res.append(row)
    df2 = pd.DataFrame(res, columns=["Date", "Ouverture", "Élevé ", "Faible ","Clôture*","Cours de clôture ajusté**","Volume"])
    df2 = df2.drop(["Ouverture", "Élevé ", "Faible ","Cours de clôture ajusté**","Volume"], axis=1)
    df2 = df2.drop_duplicates("Date", keep='first', inplace=False)
    df2['Clôture*'] = df2['Clôture*'].str.replace(',','.')
    df2["Clôture*"] = pd.to_numeric(df2["Clôture*"], downcast="float")
    df2["Rendement"] = df2['Clôture*'].pct_change()
    df2["Date"] = df2["Date"].astype(str)
    indexNames = df2[ df2['Date'].str.contains("split") ].index
    df2.drop(indexNames , inplace=True)
    df2['Date'] = df2['Date'].astype('datetime64[ns]')
    df2["Date"] = pd.to_datetime(df2["Date"])
    df2 = df2.sort_values(by="Date")
    df2RSI=df2.tail(15)
    df2RSI=df2.head(14)
    df2rendementspositifs = df2RSI[df2RSI["Rendement"]>0]
    df2rendementsnegatifs = df2RSI[df2RSI["Rendement"]<0]
    AVG1=float(df2rendementspositifs["Rendement"].mean())*100
    AVG2=-float(df2rendementsnegatifs["Rendement"].mean())*100
    p= AVG1 / AVG2
    RSIMicrosoft= 100 - 100/(1+p)
    print("RSI Microsoft: " + str(RSIMicrosoft))
    df2["Date"] = df2["Date"].astype(str)
    indexNames = df2[ df2['Date'].str.contains("split") ].index
    df2.drop(indexNames , inplace=True)
    df2['Date'] = df2['Date'].astype('datetime64[ns]')
    df2temp = pd.read_csv("MicrosoftData.csv",index_col=False)
    df2temp["Date"]= df2temp['Date'].astype('datetime64[ns]')
    df2["Clôture*"]=df2["Clôture*"].astype(float).round(2)
    df2["Rendement"]=df2["Rendement"].astype(float).round(2)
    df2temp["Clôture*"]=df2temp["Clôture*"].astype(float).round(2)
    df2temp["Rendement"]=df2temp["Rendement"].astype(float).round(2)
    df2=pd.merge(df2, df2temp, on = ["Date","Clôture*","Rendement" ], right_index=False, how='outer')
    df2=df2.drop_duplicates('Date', keep="first", inplace=False)
    df2['Date'] = df2['Date'].astype('datetime64[ns]')
    df2.to_csv("MicrosoftData.csv",index=False)
    df2.plot(figsize=(10,2), x ='Date', y='Clôture*', kind = 'line')
    plt.title('Microsfot Stock Prices in $')
    plt.xlabel('Dates')
    plt.ylabel('Stock Price in $')
    plt.show()
    df2Wallet = df2[df2["Date"] >= '2020-09-01']

    table = soup6.find('table')
    table_rows = table.find_all('tr')
    res = []
    for tr in table_rows:
        td = tr.find_all('td')
        row = [tr.text.strip() for tr in td if tr.text.strip()]
        if row:
            res.append(row)
    df3 = pd.DataFrame(res, columns=["Date", "Ouverture", "Élevé ", "Faible ","Clôture*","Cours de clôture ajusté**","Volume"])
    df3 = df3.drop(["Ouverture", "Élevé ", "Faible ","Cours de clôture ajusté**","Volume"], axis=1)
    df3 = df3.drop_duplicates("Date", keep='first', inplace=False)
    df3['Clôture*'] = df3['Clôture*'].str.replace(',','.')
    df3['Clôture*'] = df3["Clôture*"].apply (pd.to_numeric, errors='coerce')
    df3 = df3.dropna()
    df3["Clôture*"] = pd.to_numeric(df3["Clôture*"], downcast="float")
    df3["Date"] = df3["Date"].astype(str)
    df3["Date"].describe()

    df3['Date'] = df3['Date'].astype('datetime64[ns]')
    df3.plot(figsize=(10,2), x ='Date', y='Clôture*', kind = 'line')
    plt.title('EURUSD Exchange Rate')
    plt.xlabel('Dates')
    plt.ylabel('EURUSD Exchange Rate')
    plt.show()
    df3Wallet = df3[df3["Date"] >= '2020-09-01']
    Wallet = pd.merge(df1Wallet, df2Wallet, on='Date')
    Wallet = pd.merge(Wallet, df3Wallet, on = 'Date')
    Wallet['Wallet'] = (Wallet["Clôture*_x"]*nbAppleStock + Wallet["Clôture*_y"]*nbMicrosoftStock)/Wallet["Clôture*"]
    Wallet['Performance SI'] = (Wallet['Wallet']-InitialWalletInvested)/InitialWalletInvested
    Wallet['Date'] =pd.to_datetime(Wallet.Date)
    Wallet = Wallet.drop(["Clôture*_x","Clôture*_y","Clôture*","Rendement_x","Rendement_y"], axis=1)
    Wallet = pd.concat([pd.DataFrame([[pd.to_datetime('2020-08-31'), float(InitialWalletInvested), float(0)]],columns=Wallet.columns),Wallet],ignore_index=True)
    Wallet = pd.concat([pd.DataFrame([[pd.to_datetime(date.today()), float(WalletPresentValue), Performance,]],columns=Wallet.columns),Wallet],ignore_index=True)
    Wallet['Performance SI']=Wallet['Performance SI']*100
    Wallet = Wallet.sort_values(by='Date')
    plot1=Wallet.plot(figsize=(10,2), x ='Date', y='Wallet', kind = 'line')

    plt.title('Ludo Wallet')
    plt.xlabel('Dates')
    plt.ylabel('Value in €')
    plt.show()
    plot2=Wallet.plot(figsize=(10,2), x ='Date', y='Performance SI', kind = 'line')


    plt.title('Ludo Wallet Performance SI')
    plt.xlabel('Dates')
    plt.ylabel('Performance in %')
    plt.show()
    y2=[]
    for i in Wallet["Date"]:
        y2.append(0)

    x=Wallet["Date"]
    y1=Wallet["Performance SI"]
    fig, (ax, ax1) = plt.subplots(2, 1, sharex= True, figsize=(10,4))
    ax.plot(x, y1, x, y2, color='black')
    ax.fill_between(x, y1, y2, where=y2 >= y1, facecolor='red', interpolate=True)
    ax.fill_between(x, y1, y2, where=y2 <= y1, facecolor='green', interpolate=True)
    ax.set_title('Ludo Wallet Performance SI')
    plt.xlabel("Dates")
    plt.ylabel("Ludo Wallet in €/Performance SI in %")
    plt.xticks(rotation=45) 
    y1 = Wallet["Wallet"]
    y2=[]
    for i in Wallet["Date"]:
        y2.append(InitialWalletInvested)
    ax1.plot(x, y1, x, y2, color='black')
    ax1.fill_between(x, y1, y2, where=y2 >= y1,
                     facecolor='red', interpolate=True)
    ax1.fill_between(x, y1, y2, where=y2 <= y1,
                     facecolor='green', interpolate=True)
    ax1.set_title('Ludo Wallet SI')


    y2=[]
    for i in df1["Date"]:
        y2.append(AppleInit)
    x=df1["Date"]
    x2=df2["Date"]
    y1=df1["Clôture*"]
    fig2, (ax2, ax21) = plt.subplots(2, 1, sharex= True, figsize=(10,4))
    ax2.plot(x, y1, x, y2, color='black')
    #ax2.fill_between(x, y1, y2, where=y2 >= y1, facecolor='red', interpolate=True)
    ax2.fill_between(x, y1, y2, where=y2 <= y1, facecolor='green', interpolate=True)
    ax2.set_title('Apple Stock Price Time Series')
    plt.xlabel("Dates")
    plt.ylabel("Stock Price in $")
    plt.xticks(rotation=45) 
    y1 = df2["Clôture*"]
    y2=[]
    for i in df2["Date"]:
        y2.append(MicrosoftInit)
    ax21.plot(x2, y1, x2, y2, color='black')
    #ax21.fill_between(x2, y1, y2, where=y2 >= y1,facecolor='red', interpolate=True)
    ax21.fill_between(x2, y1, y2, where=y2 <= y1, facecolor='green', interpolate=True)
    ax21.set_title('Microsoft Stock Price Time Series')

    y2=[]
    for i in df3["Date"]:
        y2.append(EURUSDInit)
    x=df3["Date"]
    y1=df3["Clôture*"]
    fig3, (ax3) = plt.subplots(1, 1, sharex= True, figsize=(10,4))
    ax3.plot(x, y1, x, y2, color='black')
    #ax2.fill_between(x, y1, y2, where=y2 >= y1, facecolor='red', interpolate=True)
    ax3.fill_between(x, y1, y2, where=y2 >= y1, facecolor='green', interpolate=True)
    ax3.set_title('EURUSD Spot Price Time Series')
    plt.xlabel("Dates")
    plt.ylabel("Exchange rate in $")
    plt.xticks(rotation=45) 


    filenamestring = "Wallet " + str(current_time_pdf_name)+ ".pdf"
    pp = PdfPages(filenamestring)
    pp.savefig(fig)
    pp.savefig(fig2)
    pp.savefig(fig3)

    firstPage = plt.figure(figsize=(11.69,8.27))
    firstPage.clf()
    txt = text
    firstPage.text(0.5,0.5,txt, transform=firstPage.transFigure, size=15, ha="center")
    pp.savefig()
    pp.close()
    ##os.system('jupyter-nbconvert --to PDFviaHTML Wallet12latest.ipynb')
    os.system("explorer.exe " + filenamestring)


    
