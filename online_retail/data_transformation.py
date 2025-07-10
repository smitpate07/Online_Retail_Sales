import pandas as pd
import os

PROJECT_FOLDER = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(PROJECT_FOLDER, 'data','data.csv')

class DataTransformation:
    def data_transformation(self):
        try:
            self.df = pd.read_csv(DATA_FOLDER,sep=',')
            return self.df
        except Exception as e:
            raise e
    
    def clean_data(self):
        try:
            self.data = self.df.copy(deep=True) 
            self.data.dropna(inplace=True)
            self.data= self.data.loc[(self.data['Quantity']>0) & (self.data['UnitPrice']>0)] # Quantaties < 0 were dropped
            self.data['CustomerID'] = self.data['CustomerID'].astype('int32')
            self.data['InvoiceDate'] = pd.to_datetime(self.data['InvoiceDate'])
            self.data['Year'] = self.data['InvoiceDate'].dt.year
            self.data['Month'] = self.data['InvoiceDate'].dt.strftime('%b')
            self.data['Weekday'] = self.data['InvoiceDate'].dt.day_name()
            self.data['am_pm'] = self.data['InvoiceDate'].dt.strftime('%p')
            self.data['YearMonth'] = self.data['InvoiceDate'].dt.to_period('M').astype('category')    
            col = self.data.select_dtypes(include='object').columns
            self.data[col]  = self.data[col].astype('category')
            return self.data
        except Exception as e:
            raise e