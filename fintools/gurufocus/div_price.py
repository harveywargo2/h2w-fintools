import pandas as pd
from datetime import date
from fintools.gurufocus.dividend import GuruDividendHistory
from fintools.gurufocus.price import GuruPriceHistory


class GuruDividendPriceDf:


    def __init__(self, **kwargs):
        self.token = kwargs.get('token', 'error')
        self.ticker = kwargs.get('ticker', 'error')
        self.frequency = kwargs.get('dividend_frequency', 4)
        self.lookback = kwargs.get('lookback_years', 20)
        self.dividend_df = GuruDividendHistory(token=self.token, ticker=self.ticker).df_normalized
        self.price_df = GuruPriceHistory(token=self.token, ticker=self.ticker).df_normalized
        self.dividend_price_df = self._dividend_price()
        self.dividend_price_df_aggr = self._dividend_price_aggr()


    def _dividend_price(self):

        div_var = 0.0
        current_year = date.today().year
        cutoff = 20 + 1

        div_df1 = self.dividend_df
        # Trim out special dividend
        div_df2 = div_df1.loc[div_df1['DividendType'] == 'regular']

        # Drop Unused Columns, Convert DataTypes & Rename Date Column
        div_df2 = div_df2.drop(['RecordDate', 'PayDate'], axis=1)
        div_df2['ExDate'] = pd.to_datetime(div_df2['ExDate'])
        div_df2['DividendAmount'] = pd.to_numeric(div_df2['DividendAmount'])
        div_df2 = div_df2.rename(columns={'ExDate': 'Date'})

        price_df1 = self.price_df
        price_df1['PriceDate'] = pd.to_datetime(price_df1['PriceDate'])
        price_df1 = price_df1.rename(columns={'PriceDate': 'Date'})

        merged_df1 = pd.merge(price_df1, div_df2, on='Date', how='left')
        merged_df1['DividendAmount'] = merged_df1['DividendAmount'].fillna(0)
        merged_df1['DividendPaid'] = merged_df1['DividendAmount']

        for index, row in merged_df1.iterrows():
            if row['DividendAmount'] > 0:
                div_var = row['DividendAmount']

            else:
                merged_df1.at[index, 'DividendAmount'] = div_var

        merged_df1['ForwardDividend'] = merged_df1['DividendAmount'] * 4
        merged_df1['ForwardDividendYield'] = merged_df1['ForwardDividend'] / merged_df1['PricePerShare']

        for index, row in merged_df1.iterrows():
            if current_year - row['Date'].year >= cutoff:
                merged_df1.drop(index, inplace=True)

        return merged_df1


    def _dividend_price_aggr(self):
        df1 = self.dividend_price_df
        df1 = df1.set_index('Date')

        df2 = df1.groupby(df1.index.year).agg(
            SharePriceMin=pd.NamedAgg(column='PricePerShare', aggfunc='min'),
            SharePriceMax=pd.NamedAgg(column='PricePerShare', aggfunc='max'),
            SharePriceMean=pd.NamedAgg(column='PricePerShare', aggfunc='mean'),
            SharePriceMedian=pd.NamedAgg(column='PricePerShare', aggfunc='median'),
            DivYieldMin=pd.NamedAgg(column='ForwardDividendYield', aggfunc='min'),
            DivYieldMax=pd.NamedAgg(column='ForwardDividendYield', aggfunc='max'),
            DivYieldMean=pd.NamedAgg(column='ForwardDividendYield', aggfunc='mean'),
            DivYieldMedian=pd.NamedAgg(column='ForwardDividendYield', aggfunc='median'),
            DividendPaidCy=pd.NamedAgg('DividendPaid', aggfunc='sum')
        )

        return df2

