import io
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.platypus import Image
from online_retail.data_transformation import DataTransformation
import pandas as pd
import matplotlib.ticker as mtick

class ImageGenerator:
    def __init__(self,data_transformation: DataTransformation):
        try:
            self.data_transformation = data_transformation
        except Exception as e:
            raise e
    
    def create_top5_countries_chart(self):
        df  = self.data_transformation.data
        country_order = df['Country'].value_counts(ascending=False).nlargest(5).index        
        plt.figure(figsize=(6, 6))
        ax = sns.countplot(x='Country', data=df, order=country_order)
        plt.title('Record counts for the top 5 countries')
        ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{int(x):,}'))

        plt.xlabel('Countries')
        plt.ylabel('Count')
        plt.xticks(rotation=90)
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)

        return Image(buf, width=500, height=400)
    
    def create_year_chart(self):
        df  = self.data_transformation.data
        # Aggregate sum of Quantity by Year
        agg_df = df.groupby('Year')['Quantity'].sum().reset_index()

        # Plot using seaborn barplot
        ax = sns.barplot(data=agg_df, x='Year', y='Quantity')
        plt.title('Total Quantity sold per Year')
        plt.xlabel('Year')
        plt.ylabel('Total Quantity')
        ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{int(x):,}'))
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return Image(buf, width=400, height=300)
    
    def create_month_chart_2011(self):
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        df  = self.data_transformation.data
        df = df[df['Year'] == 2011].copy()
        agg_df = df.groupby('Month', observed=True)['Quantity'].sum().reset_index()
        agg_df['Month'] = pd.Categorical(agg_df['Month'], categories=months, ordered=True)
        plt.figure(figsize=(9, 8))
        ax = sns.barplot(data=agg_df, x='Month', y='Quantity')
        plt.title('Monthly Quantities Sold - 2011')
        plt.xlabel('Month')
        plt.ylabel('Quantity')
        ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{int(x):,}'))

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return Image(buf, width=400, height=400)
    
    def create_corr(self):
        df  = self.data_transformation.data
        month_str_to_num = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
                    'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
        df['MonthNum'] = df['Month'].map(month_str_to_num)
        relation = df.loc[df['MonthNum'].isin([9,10,11])]
        relation_qt_month = relation[['Quantity','UnitPrice']]
        correlation_matrix = relation_qt_month.corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return Image(buf, width=400, height=400)
    
    def create_highest_purchasing_customer(self):
        plt.figure(figsize=(9,9))
        df  = self.data_transformation.data
        agg_df = df.groupby('CustomerID')['Quantity'].sum().nlargest(5).reset_index().sort_values(by='Quantity',ascending=False)
        ax = sns.barplot(agg_df,x='CustomerID',y='Quantity',order=agg_df['CustomerID'])
        plt.title('Highest Purchasing Customers (by Quantity)')
        plt.xlabel('Customer ID')
        plt.ylabel('Total Quantity')
        ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{int(x):,}'))

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return Image(buf, width=500, height=400)
    
    def create_weekday_transaction(self):
        plt.figure(figsize=(9,9))
        df  = self.data_transformation.data
        ax= sns.countplot(data=df, x='Weekday', hue='am_pm', order=[
              'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
        plt.title('Transactions by Weekday and Time of Day')
        plt.xlabel('Day of the Week')
        plt.ylabel('Number of Transactions')
        ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{int(x):,}'))

        plt.legend(title='Time of Day')
        plt.xticks(rotation=45)
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return Image(buf, width=600, height=600)