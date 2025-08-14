import pandas as pd
from datetime import date


class DividendPriceDataFrame:


    def __init__(self, **kwargs):
        self.dividend_df = kwargs.get('dividend_df', 'error')
        self.frequency = kwargs.get('dividend_frequency', 4)
        self.price_df = kwargs.get('price_df', 'error')
        self.lookback = kwargs.get('lookback_years', 20)
        self.dividend_price_df = self._dividend_price()


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

    