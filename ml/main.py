import yfinance as yf
import matplotlib.pyplot as plt
#import seaborn
import pandas
from predict import predict


def download(name):
    df = yf.download(name, start='2021-01-01', auto_adjust=False, actions=False)
    df.to_csv(name+'.csv')


def ema(s, n):
    """
    returns an n period exponential moving average for
    the time series s

    s is a list ordered from oldest (index 0) to most
    recent (index -1)
    n is an integer

    returns a numeric array of the exponential
    moving average
    """
    s = list(s)
    ema = []
    j = 1

    #get n sma first and calculate the next n period ema
    sma = sum(s[:n]) / n
    multiplier = 2 / float(1 + n)
    ema.append(sma)

    #EMA(current) = ( (Price(current) - EMA(prev) ) x Multiplier) + EMA(prev)
    ema.append(( (s[n] - sma) * multiplier) + sma)

    #now calculate the rest of the values
    for i in s[n+1:]:
        tmp = ( (i - ema[j]) * multiplier) + ema[j]
        j = j + 1
        ema.append(tmp)

    return ema


def run(name):
    # Milestone 1
    df = pandas.read_csv(name+'.csv')
    # Step 1
    data_top = df.loc[df['Volume'].idxmax()]
    print('Largest volume:', end='')
    print(data_top['Date'])
    # Step 2
    change = []
    for index, row in df.iterrows():
        open_p = row['Open']
        close_p = row['Close']
        c = (close_p - open_p) / open_p * 100
        change.append(c)
    df['change'] = change
    # Step 3
    q_low = df.quantile(0.01)
    q_hi  = df.quantile(0.99)
    df_filtered = df[df["Volume"] > q_hi["Volume"]]
    # Step 4
    months = {'01':0,'02':0,'03':0,'04':0,'05':0,'06':0,'07':0,'08':0, \
            '09':0, '10':0, '11':0, '12':0}
    for index, row in df.iterrows():
        m = row['Date'].split('-')[1]
        v = row['Volume']
        months[m] += v
    print('Month with largest volume transferred: ', end='')
    print(max(months, key=months.get))

    # Step 5
    for period in [20, 50, 100]:
        ema_20 = ema(df['Open'].tolist(), period)
        #plt.plot(df['Open'].tolist(), label="Stock Values", color="blue")
        #plt.plot(ema_20, label="EMA Values", color="green")
        #plt.xlabel("Days")
        #plt.ylabel("Price")
        #plt.legend()
        #plt.show()
    low_dates = []
    for index, row in df.iterrows():
        if index == len(ema_20) - 1:
            break
        if row['Open'] < ema_20[index]:
            low_dates.append(row['Date'])
    #print(low_dates)
    
    return df['change'].tolist()
    

def distance(c1, c2):
    # c1 1%, c2 2.5%
    d = 0
    for i in range(min(len(c1), len(c2))):
        d += (c1[i] - c2[i])*(c1[i] - c2[i])
    return d
 

def runAll():
    # Milestone 1
    aapl = run('AAPL')
    tsla = run('TSLA')
    nvda = run('NVDA') 
    nflx = run('NFLX')
    msft = run('MSFT')
    companies = [aapl,tsla,nvda,nflx,msft]
    diff = {}
    for i in range(len(companies)):
        for j in range(i+1, len(companies)):
            diff[(i,j)] = distance(companies[i],companies[j])
    key = min(diff, key=diff.get)
    companies_str = ['AAPL','TSLA','NVDA','NFLX','MSFT']
    print(companies_str[key[0]]+' and ' + companies_str[key[1]] + ' are closest')

    # Milestone 2
    predict('AAPL', aapl)

if __name__ == '__main__':
    runAll()
    #download('NFLX')
