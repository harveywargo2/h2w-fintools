import requests
import pandas as pd


class GuruPriceHistory:

    def __init__(self, **kwargs):
        self.token = kwargs.get('token', 'error')
        self.ticker = kwargs.get('ticker', 'error')
        self.api_data = self._price_api_data()
        self.df = self._price_df()
        self.df_normalized = self._price_df_normalized()


    def _price_api_data(self):
        return requests.get(f'https://api.gurufocus.com/public/user/{str(self.token)}/stock/{str(self.ticker)}/price').json()


    def _price_df(self):

        price_list = self.api_data
        price_df = pd.DataFrame(price_list, columns=['price_date', 'share_price'])

        return price_df


    def _price_df_normalized(self):

        price_list = self.api_data
        price_df = pd.DataFrame(price_list, columns=['price_date', 'share_price'])

        return price_df