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
        self.df_annual_cashflow_normalized = self._cashflow_normalized()
        self.df_annual_supplemental = self._annual_supplemental()


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

            df2['CashAndEquivalents'] = df1['balance_sheet.Cash and Cash Equivalents']
            df2['ShortTermInvestments'] = df1['balance_sheet.Marketable Securities']
            df2['TotalShortTermCash'] = df1['balance_sheet.Cash, Cash Equivalents, Marketable Securities']

            df2['AccountsReceivable'] = df1['balance_sheet.Accounts Receivable']
            df2['TotalReceivable'] = df1['balance_sheet.Total Receivables']
            df2['TotalInventories'] = df1['balance_sheet.Total Inventories']
            df2['TotalCurrentAssets'] = df1['balance_sheet.Total Current Assets']
            df2['GrossPropertyPlantAndEquipment'] = df1['balance_sheet.Gross Property, Plant and Equipment']
            df2['NetPropertyPlantAndEquipment'] = df1['balance_sheet.Property, Plant and Equipment']
            df2['TotalLongTermAssets'] = df1['balance_sheet.Total Long-Term Assets']
            df2['TotalAssets'] = df1['balance_sheet.Total Assets']

            df2['AccountsPayable'] = df1['balance_sheet.Accounts Payable']
            df2['CurrentAccruedExpense'] = df1['balance_sheet.Current Accrued Expense']
            df2['ShortTermDebt'] = df1['balance_sheet.Short-Term Debt']
            df2['ShortTermCapitalLease'] = df1['balance_sheet.Short-Term Capital Lease Obligation']
            df2['OtherCurrentLiabilities'] = df1['balance_sheet.Other Current Liabilities']
            df2['TotalCurrentLiabilities'] = df1['balance_sheet.Total Current Liabilities']
            df2['LongTermDebt'] = df1['balance_sheet.Long-Term Debt']
            df2['LongTermCapitalLease'] = df1['balance_sheet.Long-Term Capital Lease Obligation']
            df2['PensionBenefits'] = df1['balance_sheet.Pension And Retirement Benefit']
            df2['OtherLongTermLiabilities'] = df1['balance_sheet.Other Long-Term Liabilities']
            df2['TotalCurrentLiabilities'] = df1['balance_sheet.Total Current Liabilities']

            df2['CommonStock'] = df1['balance_sheet.Common Stock']
            df2['AdditionalPaidInCapital'] = df1['balance_sheet.Additional Paid-In Capital']
            df2['TreasuryStock'] = df1['balance_sheet.Treasury Stock']
            df2['TotalEquity'] = df1['balance_sheet.Total Equity']


            return df2

        else:
            return "REIT"


    def _cashflow_normalized(self):
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

            df2['CashFromOperations'] = df1['cashflow_statement.Cash Flow from Operations']

            df2['CapitalExpenditure'] = df1['cashflow_statement.Capital Expenditure']
            df2['CashFromInvesting'] = df1['cashflow_statement.Cash Flow from Investing']

            df2['StockIssuance'] = df1['cashflow_statement.Issuance of Stock']
            df2['StockRepurchase'] = df1['cashflow_statement.Repurchase of Stock']
            df2['DividendsPaid'] = df1['cashflow_statement.Cash Flow for Dividends']
            df2['DebtIssuance'] = df1['cashflow_statement.Issuance of Debt']
            df2['DebtPayments'] = df1['cashflow_statement.Payments of Debt']
            df2['CashFromFinancing'] = df1['cashflow_statement.Cash Flow from Financing']

            df2['FreeCashFlow'] = df1['cashflow_statement.Free Cash Flow']

            return df2

        else:
            return "REIT"


    def _annual_supplemental(self):
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

            df2['PerShareRevenue'] = df1['per_share_data_array.Revenue per Share']
            df2['PerShareEarnings'] = df1['per_share_data_array.Earnings per Share (Diluted)']
            df2['PerShareFreeCashFlow'] = df1['per_share_data_array.Free Cash Flow per Share']
            df2['PerShareDividends'] = df1['per_share_data_array.Dividends per Share']
            df2['PerShareBookValue'] = df1['per_share_data_array.Book Value per Share']
            df2['PerSharePriceHigh'] = df1['valuation_and_quality.Highest Stock Price']
            df2['PerSharePriceLow'] = df1['valuation_and_quality.Lowest Stock Price']

            df2['SharesOutstandingDiluted'] = df1['per_share_data_array.Shares Outstanding (Diluted Average)']
            df2['SharesOutstandingBasicAverage'] = df1['valuation_and_quality.Shares Outstanding (Basic Average)']
            df2['SharesOutstandingEop'] = df1['valuation_and_quality.Shares Outstanding (EOP)']
            df2['SharesOutstandingEop'] = df1['valuation_and_quality.Shares Outstanding (EOP)']

            df2['RestatedFilingDate'] = df1['valuation_and_quality.Restated Filing Date']
            df2['FilingDate'] = df1['valuation_and_quality.Filing Date']
            df2['ShareHolderNumbers'] = df1['valuation_and_quality.Number of Shareholders']
            df2['MarketCapitalization'] = df1['valuation_and_quality.Market Cap']
            df2['EnterpriseValue'] = df1['valuation_and_quality.Enterprise Value']

            return df2

        else:
            return "REIT"






