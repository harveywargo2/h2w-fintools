import requests
import pandas as pd



class GuruFinancials:
    def __init__(self, **kwargs):
        self.token = kwargs.get('token', 'error')
        self.ticker = kwargs.get('ticker', 'error')
        self.api_data = self._fin_api()
        self.financials_properties = self.api_data['financials']['financial_template_parameters']
        self.reit = self.financials_properties['REITs']
        self.df_financials_annual = self._annuals()
        self.df_annual_income_normalized = self._income_normalized()
        self.df_annual_balance_normalized = self._balance_normalized()


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

    def _income_normalized(self):
        df1 = self.df_financials_annual
        df2 = pd.DataFrame()

        # Normalize Fiscal Year
        fy_pattern = r"([\d]{4})-"
        month_pattern = r"-([\d]{2})"

        if self.reit == 'N':
            df2['FiscalYear'] = df1['Fiscal Year']

            # Drop TTM
            df2 = df2.loc[df2['FiscalYear'] != 'TTM']

            # Normalize Date
            df2['FiscalYear'] = df1['Fiscal Year'].str.extract(fy_pattern)
            df2['FiscalMonth'] = df1['Fiscal Year'].str.extract(month_pattern)

            df2['Revenue'] = df1['income_statement.Revenue']
            df2['CostOfGoodsSold'] = df1['income_statement.Cost of Goods Sold']
            df2['GrossProfit'] = df1['income_statement.Gross Profit']
            df2['SellingGeneralAndAdminExpense'] = df1['income_statement.Selling, General, & Admin. Expense']
            df2['ResearchAndDevelopment'] = df1['income_statement.Research & Development']
            df2['OtherOperatingExpense'] = df1['income_statement.Other Operating Expense']
            df2['TotalOperatingExpense'] = df1['income_statement.Total Operating Expense']
            df2['OperatingIncome'] = df1['income_statement.Operating Income']
            df2['InterestExpense'] = df1['income_statement.Interest Expense']
            df2['InterestIncome'] = df1['income_statement.Interest Income']
            df2['NetInterestIncome'] = df1['income_statement.Net Interest Income']
            df2['IncomeTaxExpense'] = df1['income_statement.Tax Provision']
            df2['NetIncomeContinuingOperations'] = df1['income_statement.Net Income (Continuing Operations)']
            df2['NetIncome'] = df1['income_statement.Net Income']

            return df2

        else:
            return "REIT"


    def _balance_normalized(self):
        df1 = self.df_financials_annual
        df2 = pd.DataFrame()

        # Normalize Fiscal Year
        fy_pattern = r"([\d]{4})-"
        month_pattern = r"-([\d]{2})"

        if self.reit == 'N':
            df2['FiscalYear'] = df1['Fiscal Year']

            # Drop TTM
            df2 = df2.loc[df2['FiscalYear'] != 'TTM']

            # Normalize Date
            df2['FiscalYear'] = df1['Fiscal Year'].str.extract(fy_pattern)
            df2['FiscalMonth'] = df1['Fiscal Year'].str.extract(month_pattern)



            return df2

        else:
            return "REIT"
