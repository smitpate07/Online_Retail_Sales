import pandas as pd
import os
from sqlalchemy import create_engine, text 

PROJECT_FOLDER = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(PROJECT_FOLDER, 'data','data.csv')
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

# Construct the SQLAlchemy connection string
DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

class DataTransformation:
    def data_transformation(self):
        try:
            self.df = pd.read_sql(text("SELECT * FROM public.online_retail_sales"), con=engine)
            print("DB Connection Sucessful!")
            print(type(self.df))
            print(self.df)
            return self.df
        except Exception as e:
            raise e
    
    def clean_data(self):
        try:
            self.data = self.df.copy(deep=True)
            print(self.data.dtypes)
            self.data.dropna(inplace=True)
            self.data['UnitPrice'] = self.data['UnitPrice'].astype('float')
            self.data= self.data.loc[(self.data['Quantity']>0) & (self.data['UnitPrice']>0)] # Quantaties < 0 were dropped
            self.data['CustomerID'] = self.data['CustomerID'].astype('float')
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