import pandas as pd

df=pd.read_csv("F:/Work/AspirationAI/NCC.csv")

df=df[~df["Series"].isin(["BL"])]

print(df.head())
print(df.tail())
print(df.describe())

a=df["Close Price"].tail(90)

print("Maximun price for last 90 days=",max(a))
print("Minimum price for last 90 days=",min(a))
print("Mean price for last 90 days=",a.mean(axis=0))

print("Datatype of Date is",df.Date.dtype)
df["Date"]=pd.to_datetime(df["Date"])
print("Now datatype of Date is",df.Date.dtype)

print(max(df["Date"]-min(df["Date"])))

df["Month"]=df["Date"].dt.month
df["Year"]=df["Date"].dt.year
df["VWAP"]=df["Open Price"]+df["High Price"]+df["Close Price"]
df["VWAP"]=df["VWAP"]/3
df["VWAP"]=df["VWAP"]*df["Total Traded Quantity"]
df1=df[["Month","Year","Total Traded Quantity","VWAP"]].groupby(["Month","Year"]).sum()
df1["VWAP"]=df1["VWAP"]/df1["Total Traded Quantity"]

print(df1)

def avg(N):
    return ((df["Close Price"].tail(N).sum())/N)

print("Average Price for last")
print("1 week: ",avg(5))
print("2 weeks: ",avg(10))
print("1 month: ",avg(20))
print("3 months: ",avg(60))
print("6 months: ",avg(120))
print("1 year: ",avg(240))

def plp(N):
    diff=(df["Close Price"].tail(1).sum())-(df["Close Price"].tail(N).sum()-df["Close Price"].tail(N-1).sum())
    if diff==0:
        return 0
    elif diff<0:
        loss=(diff/df["Close Price"].tail(1).sum())*100
        return loss
    else:
        profit=(diff/df["Close Price"].tail(1).sum())*100
        return profit

print("Profit/Loss percentage for last")
print("1 week: ",plp(5))
print("2 weeks: ",plp(10))
print("1 month: ",plp(20))
print("3 months: ",plp(60))
print("6 months: ",plp(120))
print("1 year: ",plp(240))

df["Day_Perc_Change"]=df["Close Price"].pct_change()
df.dropna(axis=0, how="any", inplace=True)

for i in range(df.shape[0]):
    if (df["Day_Perc_Change"].values[i]>=-0.5 and df["Day_Perc_Change"].values[i]<0.5):
        df["Trend"]="Slight or No change"
    if (df["Day_Perc_Change"].values[i]>=0.5 and df["Day_Perc_Change"].values[i]<1):
       df["Trend"]="Slight positive"
    if (df["Day_Perc_Change"].values[i]>=-1 and df["Day_Perc_Change"].values[i]<-0.5):
        df["Trend"]="Slight negative"
    if (df["Day_Perc_Change"].values[i]>=1 and df["Day_Perc_Change"].values[i]<3):
        df["Trend"]="Positive"
    if (df["Day_Perc_Change"].values[i]>=-3 and df["Day_Perc_Change"].values[i]<-1):
        df["Trend"]="Negative"
    if (df["Day_Perc_Change"].values[i]>=3 and df["Day_Perc_Change"].values[i]<7):
        df["Trend"]="Among top gainers"
    if (df["Day_Perc_Change"].values[i]>=-7 and df["Day_Perc_Change"].values[i]<-3):
        df["Trend"]="Among top losers"
    if (df["Day_Perc_Change"].values[i]>=7):
        df["Trend"]="Bull run"
    if (df["Day_Perc_Change"].values[i]<-7):
        df["Trend"]="Bear drop"

print("Average of Total Traded Quantity for each type of Trend=",df.groupby(["Trend"]).mean()["Total Traded Quantity"])
print("Median of Total Traded Quantity for each type of Trend=",df.groupby(["Trend"]).median()["Total Traded Quantity"])
