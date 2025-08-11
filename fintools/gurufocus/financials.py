import requests
import pandas as pd



class GuruFinancials:
    def __init__(self, **kwargs):
        self.token = kwargs.get('token', 'error')
        self.ticker = kwargs.get('ticker', 'error')
        self.api_data = self._fin_api()
        self.financials_properties = self.api_data['financials']['financial_template_parameters']
        self.df_financials_annual = self._annuals()

    def _fin_api(self):
        return requests.get(f'https://api.gurufocus.com/public/user/{str(self.token)}/stock/{str(self.ticker)}/financials').json()


    def _annuals(self):
        an_df1 = pd.DataFrame.from_dict(self.api_data)
        an_df2 = pd.json_normalize(an_df1.loc['annuals'])
        x_loc = 0
        an_df3 = pd.DataFrame()

        for item, values in an_df2.items():
            series_expand = pd.Series(values, name=item).explode(ignore_index=True)
            series_df = series_expand.to_frame()
            an_df3 = pd.concat([an_df3, series_df], axis=1)
            x_loc += 1

        return an_df3

