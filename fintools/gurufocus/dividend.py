import requests
import pandas as pd


class GuruDividendHistory:

    def __init__(self, **kwargs):
        self.token = kwargs.get('token', 'error')
        self.ticker = kwargs.get('ticker', 'error')
        self.api_data = self._div_api_data()
        self.df = self._div_api_df()
        self.df_normalized = self._div_normalized()


    def _div_api_data(self):
        return requests.get(f'https://api.gurufocus.com/public/user/{str(self.token)}/stock/{str(self.ticker)}/dividend').json()

    def _div_api_df(self):
        div_list = self.api_data
        div_df = pd.DataFrame(div_list)

        return div_df

    def _div_normalized(self):

        div_list = self.api_data
        div_df = pd.DataFrame(div_list)
        div_df = div_df.rename(columns={
            'amount': 'dividend_amount',
            'type': 'dividend_type'
        })
        div_df['dividend_type'] = div_df['dividend_type'].replace('Cash Div.', 'regular')
        div_df['dividend_type'] = div_df['dividend_type'].replace('Special Div.', 'special')

        div_df['dividend_amount'] = div_df['dividend_amount']


        return div_df