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
            df2['FiscalYear'] = pd.to_numeric(df2['FiscalYear'], errors='coerce')
            df2['FiscalMonth'] = df1['Fiscal Year'].str.extract(month_pattern)
            df2['FiscalMonth'] = pd.to_numeric(df2['FiscalMonth'], errors='coerce')

            df2['Revenue'] = pd.to_numeric(df1['income_statement.Revenue'], errors='coerce')
            df2['CostOfGoodsSold'] = pd.to_numeric(df1['income_statement.Cost of Goods Sold'], errors='coerce')
            df2['GrossProfit'] = pd.to_numeric(df1['income_statement.Gross Profit'], errors='coerce')
            df2['SellingGeneralAndAdminExpense'] = pd.to_numeric(df1['income_statement.Selling, General, & Admin. Expense'], errors='coerce')
            df2['ResearchAndDevelopment'] = pd.to_numeric(df1['income_statement.Research & Development'], errors='coerce')
            df2['OtherOperatingExpense'] = pd.to_numeric(df1['income_statement.Other Operating Expense'], errors='coerce')
            df2['TotalOperatingExpense'] = pd.to_numeric(df1['income_statement.Total Operating Expense'], errors='coerce')
            df2['OperatingIncome'] = pd.to_numeric(df1['income_statement.Operating Income'], errors='coerce')
            df2['InterestExpense'] = pd.to_numeric(df1['income_statement.Interest Expense'], errors='coerce')
            df2['InterestIncome'] = pd.to_numeric(df1['income_statement.Interest Income'], errors='coerce')
            df2['NetInterestIncome'] = pd.to_numeric(df1['income_statement.Net Interest Income'], errors='coerce')
            df2['IncomeTaxExpense'] = pd.to_numeric(df1['income_statement.Tax Provision'], errors='coerce')
            df2['NetIncomeContinuingOperations'] = pd.to_numeric(df1['income_statement.Net Income (Continuing Operations)'], errors='coerce')
            df2['NetIncome'] = pd.to_numeric(df1['income_statement.Net Income'], errors='coerce')

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
            df2['FiscalYear'] = pd.to_numeric(df2['FiscalYear'], errors='coerce')
            df2['FiscalMonth'] = df1['Fiscal Year'].str.extract(month_pattern)
            df2['FiscalMonth'] = pd.to_numeric(df2['FiscalMonth'], errors='coerce')

            df2['CashAndEquivalents'] = pd.to_numeric(df1['balance_sheet.Cash and Cash Equivalents'], errors='coerce')
            df2['ShortTermInvestments'] = pd.to_numeric(df1['balance_sheet.Marketable Securities'], errors='coerce')
            df2['TotalShortTermCash'] = pd.to_numeric(df1['balance_sheet.Cash, Cash Equivalents, Marketable Securities'], errors='coerce')

            df2['AccountsReceivable'] = pd.to_numeric(df1['balance_sheet.Accounts Receivable'], errors='coerce')
            df2['TotalReceivable'] = pd.to_numeric(df1['balance_sheet.Total Receivables'], errors='coerce')
            df2['TotalInventories'] = pd.to_numeric(df1['balance_sheet.Total Inventories'], errors='coerce')
            df2['TotalCurrentAssets'] = pd.to_numeric(df1['balance_sheet.Total Current Assets'], errors='coerce')
            df2['GrossPropertyPlantAndEquipment'] = pd.to_numeric(df1['balance_sheet.Gross Property, Plant and Equipment'], errors='coerce')
            df2['NetPropertyPlantAndEquipment'] = pd.to_numeric(df1['balance_sheet.Property, Plant and Equipment'], errors='coerce')
            df2['TotalLongTermAssets'] = pd.to_numeric(df1['balance_sheet.Total Long-Term Assets'], errors='coerce')
            df2['TotalAssets'] = pd.to_numeric(df1['balance_sheet.Total Assets'], errors='coerce')

            df2['AccountsPayable'] = pd.to_numeric(df1['balance_sheet.Accounts Payable'], errors='coerce')
            df2['CurrentAccruedExpense'] = pd.to_numeric(df1['balance_sheet.Current Accrued Expense'], errors='coerce')
            df2['ShortTermDebt'] = pd.to_numeric(df1['balance_sheet.Short-Term Debt'], errors='coerce')
            df2['ShortTermCapitalLease'] = pd.to_numeric(df1['balance_sheet.Short-Term Capital Lease Obligation'], errors='coerce')
            df2['OtherCurrentLiabilities'] = pd.to_numeric(df1['balance_sheet.Other Current Liabilities'], errors='coerce')
            df2['TotalCurrentLiabilities'] = pd.to_numeric(df1['balance_sheet.Total Current Liabilities'], errors='coerce')
            df2['LongTermDebt'] = pd.to_numeric(df1['balance_sheet.Long-Term Debt'], errors='coerce')
            df2['LongTermCapitalLease'] = pd.to_numeric(df1['balance_sheet.Long-Term Capital Lease Obligation'], errors='coerce')
            df2['PensionBenefits'] = pd.to_numeric(df1['balance_sheet.Pension And Retirement Benefit'], errors='coerce')
            df2['OtherLongTermLiabilities'] = pd.to_numeric(df1['balance_sheet.Other Long-Term Liabilities'], errors='coerce')
            df2['TotalLiabilities'] = pd.to_numeric(df1['balance_sheet.Total Liabilities'], errors='coerce')

            df2['CommonStock'] = pd.to_numeric(df1['balance_sheet.Common Stock'], errors='coerce')
            df2['AdditionalPaidInCapital'] = pd.to_numeric(df1['balance_sheet.Additional Paid-In Capital'], errors='coerce')
            df2['TreasuryStock'] = pd.to_numeric(df1['balance_sheet.Treasury Stock'], errors='coerce')
            df2['TotalEquity'] = pd.to_numeric(df1['balance_sheet.Total Equity'], errors='coerce')

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
            df2['FiscalYear'] = pd.to_numeric(df2['FiscalYear'], errors='coerce')
            df2['FiscalMonth'] = df1['Fiscal Year'].str.extract(month_pattern)
            df2['FiscalMonth'] = pd.to_numeric(df2['FiscalMonth'], errors='coerce')

            df2['CashFromOperations'] = pd.to_numeric(df1['cashflow_statement.Cash Flow from Operations'], errors='coerce')

            df2['CapitalExpenditure'] = pd.to_numeric(df1['cashflow_statement.Capital Expenditure'], errors='coerce')
            df2['CashFromInvesting'] = pd.to_numeric(df1['cashflow_statement.Cash Flow from Investing'], errors='coerce')

            df2['StockIssuance'] = pd.to_numeric(df1['cashflow_statement.Issuance of Stock'], errors='coerce')
            df2['StockRepurchase'] = pd.to_numeric(df1['cashflow_statement.Repurchase of Stock'], errors='coerce')
            df2['DividendsPaid'] = pd.to_numeric(df1['cashflow_statement.Cash Flow for Dividends'], errors='coerce')
            df2['DebtIssuance'] = pd.to_numeric(df1['cashflow_statement.Issuance of Debt'], errors='coerce')
            df2['DebtPayments'] = pd.to_numeric(df1['cashflow_statement.Payments of Debt'], errors='coerce')
            df2['CashFromFinancing'] = pd.to_numeric(df1['cashflow_statement.Cash Flow from Financing'], errors='coerce')

            df2['FreeCashFlow'] = pd.to_numeric(df1['cashflow_statement.Free Cash Flow'], errors='coerce')

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
            df2['FiscalYear'] = pd.to_numeric(df2['FiscalYear'], errors='coerce')
            df2['FiscalMonth'] = df1['Fiscal Year'].str.extract(month_pattern)
            df2['FiscalMonth'] = pd.to_numeric(df2['FiscalMonth'], errors='coerce')

            df2['PerShareRevenue'] = pd.to_numeric(df1['per_share_data_array.Revenue per Share'], errors='coerce')
            df2['PerShareEarnings'] = pd.to_numeric(df1['per_share_data_array.Earnings per Share (Diluted)'], errors='coerce')
            df2['PerShareFreeCashFlow'] = pd.to_numeric(df1['per_share_data_array.Free Cash Flow per Share'], errors='coerce')
            df2['PerShareDividends'] = pd.to_numeric(df1['per_share_data_array.Dividends per Share'], errors='coerce')
            df2['PerShareBookValue'] = pd.to_numeric(df1['per_share_data_array.Book Value per Share'], errors='coerce')
            df2['PerSharePriceHigh'] = pd.to_numeric(df1['valuation_and_quality.Highest Stock Price'], errors='coerce')
            df2['PerSharePriceLow'] = pd.to_numeric(df1['valuation_and_quality.Lowest Stock Price'], errors='coerce')

            df2['SharesOutstandingDiluted'] = pd.to_numeric(df1['per_share_data_array.Shares Outstanding (Diluted Average)'], errors='coerce')
            df2['SharesOutstandingBasicAverage'] = pd.to_numeric(df1['valuation_and_quality.Shares Outstanding (Basic Average)'], errors='coerce')
            df2['SharesOutstandingEop'] = pd.to_numeric(df1['valuation_and_quality.Shares Outstanding (EOP)'], errors='coerce')
            df2['SharesOutstandingEop'] = pd.to_numeric(df1['valuation_and_quality.Shares Outstanding (EOP)'], errors='coerce')

            df2['RestatedFilingDate'] = df1['valuation_and_quality.Restated Filing Date']
            df2['FilingDate'] = df1['valuation_and_quality.Filing Date']
            df2['ShareHolderNumbers'] = pd.to_numeric(df1['valuation_and_quality.Number of Shareholders'], errors='coerce')
            df2['MarketCapitalization'] = pd.to_numeric(df1['valuation_and_quality.Market Cap'], errors='coerce')
            df2['EnterpriseValue'] = pd.to_numeric(df1['valuation_and_quality.Enterprise Value'], errors='coerce')

            return df2

        else:
            return "REIT"






