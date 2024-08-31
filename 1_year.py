#1_year

import yfinance as yf
import pandas as pd
import numpy as np


stock_tickers = ['AARTIIND.NS', 'ABB.NS', 'ABBOTINDIA.NS', 'ABCAPITAL.NS', 'ABFRL.NS', 'ACC.NS', 'ADANIENT.NS',
                 'ADANIPORTS.NS', 'AMBUJACEM.NS', 'APOLLOHOSP.NS', 'APOLLOTYRE.NS', 'ASHOKLEY.NS', 'ASTRAL.NS',
                 'ATUL.NS', 'AUBANK.NS', 'AUROPHARMA.NS', 'BAJAJFINSV.NS', 'BAJFINANCE.NS', 'BALKRISIND.NS',
                 'BALRAMCHIN.NS', 'BANDHANBNK.NS', 'BANKBARODA.NS', '^NSEBANK', 'BEL.NS', 'BHARATFORG.NS',
                 'BHARTIARTL.NS', 'BHEL.NS', 'BIOCON.NS', 'BOSCHLTD.NS', 'BPCL.NS', 'BRITANNIA.NS', 'BSOFT.NS',
                 'CANBK.NS', 'CHAMBLFERT.NS', 'CHOLAFIN.NS', 'CIPLA.NS', 'COALINDIA.NS', 'COFORGE.NS',
                 'CONCOR.NS', 'COROMANDEL.NS', 'CROMPTON.NS', 'CUB.NS', 'DABUR.NS', 'DALBHARAT.NS', 'DEEPAKNTR.NS',
                 'DLF.NS', 'EICHERMOT.NS', 'ESCORTS.NS', 'GAIL.NS', 'GLENMARK.NS', 'GMRINFRA.NS', 'GNFC.NS',
                 'GODREJCP.NS', 'GODREJPROP.NS', 'GRASIM.NS', 'GUJGASLTD.NS', 'HAL.NS', 'HDFCBANK.NS', 'HDFCLIFE.NS',
                 'HEROMOTOCO.NS', 'HINDPETRO.NS', 'HINDUNILVR.NS', 'ICICIBANK.NS', 'ICICIGI.NS', 'ICICIPRULI.NS',
                 'IDEA.NS', 'IDFC.NS', 'IDFCFIRSTB.NS', 'IEX.NS', 'INDHOTEL.NS', 'INDIACEM.NS', 'INDIAMART.NS',
                 'INDIGO.NS', 'INDUSINDBK.NS', 'INDUSTOWER.NS', 'IOC.NS', 'IPCALAB.NS', 'IRCTC.NS', 'ITC.NS',
                 'JINDALSTEL.NS', 'JKCEMENT.NS', 'JSWSTEEL.NS', 'JUBLFOOD.NS', 'KOTAKBANK.NS', 'LICHSGFIN.NS',
                 'LT.NS', 'LTF.NS', 'LTTS.NS', 'M&MFIN.NS', 'MANAPPURAM.NS', 'MARICO.NS', 'MARUTI.NS', 'MCX.NS',
                 'METROPOLIS.NS', 'MFSL.NS', 'MGL.NS', 'MOTHERSON.NS', 'MPHASIS.NS', 'NATIONALUM.NS', 'NAVINFLUOR.NS',
                 'NESTLEIND.NS', '^NSEI', 'NMDC.NS', 'NTPC.NS', 'OBEROIRLTY.NS', 'ONGC.NS', 'PEL.NS', 'PETRONET.NS',
                 'PFC.NS', 'PIDILITIND.NS', 'PIIND.NS', 'PNB.NS', 'POLYCAB.NS', 'POWERGRID.NS', 'PVRINOX.NS',
                 'RAMCOCEM.NS', 'RBLBANK.NS', 'RECLTD.NS', 'RELIANCE.NS', 'SAIL.NS', 'SBICARD.NS', 'SBILIFE.NS',
                 'SBIN.NS', 'SHRIRAMFIN.NS', 'SRF.NS', 'SUNTV.NS', 'TATACHEM.NS', 'TATACOMM.NS', 'TATACONSUM.NS',
                 'TATAMOTORS.NS', 'TATAPOWER.NS', 'TATASTEEL.NS', 'TCS.NS', 'TORNTPHARM.NS', 'UBL.NS', 'ULTRACEMCO.NS',
                 'UPL.NS', 'VEDL.NS', 'VOLTAS.NS', 'ZYDUSLIFE.NS']

market_ticker = '^NSEI'
period = '1y'


data = yf.download(stock_tickers, period=period, interval='1d')['Adj Close']
market_data = yf.download(market_ticker, period=period, interval='1d')['Adj Close']


daily_stock_returns = data.pct_change() * 100
daily_market_returns = market_data.pct_change() * 100


yearly_stock_returns = daily_stock_returns.resample('Y').mean()
yearly_market_returns = daily_market_returns.resample('Y').mean()


result_data = []


for ticker in stock_tickers:
    if ticker != market_ticker:
        stock_returns = yearly_stock_returns[ticker].dropna()
        market_returns = yearly_market_returns.dropna()

        
        aligned_returns = stock_returns.align(market_returns, join='inner', axis=0)
        stock_returns_aligned = aligned_returns[0]
        market_returns_aligned = aligned_returns[1]

        
        covariance_matrix = np.cov(stock_returns_aligned, market_returns_aligned)
        covariance = covariance_matrix[0, 1]
        variance = covariance_matrix[1, 1]

        
        beta = covariance / variance if variance != 0 else np.nan
        for date in stock_returns_aligned.index:
            result_data.append({'Datetime': date, 'Ticker': ticker, 'Yearly_Percent_Change': stock_returns_aligned.loc[date], 'Beta': beta})
            print(f"Calculated beta for {ticker} on {date}: {beta}")


result_df = pd.DataFrame(result_data)


if not result_df.empty:
    result_df.to_excel('stock_yearly_changes_with_beta.xlsx', index=False)
    print("Data saved to stock_yearly_changes_with_beta.xlsx")
else:
    print("No data to save.")