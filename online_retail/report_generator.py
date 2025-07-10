from online_retail.data_transformation import DataTransformation
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, PageBreak,KeepTogether, Paragraph, Table, TableStyle,ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from online_retail.image_generator import ImageGenerator
import time


class ReportGenerator:
    def __init__(self,data_transformation:DataTransformation,image_generator:ImageGenerator):
        try:
            self.data_transformation = data_transformation
            self.image_generator = image_generator
        except Exception as e:
            raise e
    
    def report_generator(self, mode = 1):
        try:
            print('>>>'*10+'Generating Report'+'<<<'*10)
            doc = SimpleDocTemplate("Report.pdf")
            story = []
            styles = getSampleStyleSheet()

            # Add a title
            t1 = time.time()
            story.append(Paragraph("Online Retail Sales Report", styles['h1']))
            story.append(Paragraph("Dataset Description", styles['h2']))

            dataset_description = (
    "This is a transactional dataset that includes all purchases made between 01/12/2010 and 09/12/2011 by customers "
    "of a UK-based and registered non-store online retailer. The company primarily sells unique, gift-related products "
    "through its online platform, with the majority of its customers being wholesalers. "
    "Each transaction includes details such as invoice number, stock code, item description, quantity, invoice date, "
    "unit price, customer ID, and country of purchase. "
    "<br/><br/>"
    "This dataset was generously donated to the UCI Machine Learning Repository by Daqing Chen on November 5, 2015. "
    "It is made publicly available under the Creative Commons Attribution 4.0 International (CC BY 4.0) license, allowing "
    "free use, distribution, and adaptation of the data provided proper attribution is given. "
    "The dataset serves as a rich resource for exploring customer segmentation, sales trends, and data preprocessing techniques."
    "The following is a description of the dataset columns."
)
            story.append(Paragraph(dataset_description, styles['Normal']))
            # Add a table
            # Define table data
            data = [
                ['Variable Name', 'Type', 'Description'],
                ['InvoiceNo', 'Categorical', 'a 6-digit integral number uniquely assigned to each transaction. If this code starts with letter "c", it indicates a cancellation'],
                ['StockCode', 'Categorical', 'a 5-digit integral number uniquely assigned to each distinct product'],
                ['Description', 'Categorical', 'product name'],
                ['Quantity', 'Integer', 'the quantities of each product (item) per transaction'],
                ['InvoiceDate', 'Date', 'the day and time when each transaction was generated'],
                ['UnitPrice', 'Continuous', 'product price per unit'],
                ['CustomerID', 'Catgeorical', 'a 5-digit integral number uniquely assigned to each customer'],
                ['Country', 'Categorical', 'the name of the country where each customer resides']
            ]

            col_widths = [80, 80, 280]  # sum ~500-550 points max (A4 width minus margins)

            # Wrap cell contents using Paragraph for better control and word wrapping
            table_data_wrapped = [[
                     Paragraph(cell, styles['BodyText']) if isinstance(cell, str) else cell
                    for cell in row
                ] for row in data]

            # Create a Table object with fixed widths
            table = Table(table_data_wrapped, colWidths=col_widths)


            # Apply table style (optional)
            style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header row background
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white), # Header row text color
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all cells
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'), # Header font
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Header padding
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Data rows background
                ('GRID', (0, 0), (-1, -1), 1, colors.black)  # Add grid lines
            ])

            table.setStyle(style)

            # Add the table to the story
            story.append(KeepTogether(table))
            unique_countries = ", ".join(self.data_transformation.df['Country'].unique())
            story.append(Paragraph("Key Takeaways:", styles['h1']))

            missing_df = (
                self.data_transformation.df.isnull().sum() / len(self.data_transformation.df) * 100
            ).reset_index()

            missing_df.columns = ['Column Name', 'Missing Values (%)']

            missing_df = missing_df.sort_values(by='Missing Values (%)', ascending=False)
            missing_df['Missing Values (%)'] = missing_df['Missing Values (%)'].round(2) 
            missing_table_data = [missing_df.columns.tolist()] + missing_df.values.tolist()

            missing_table = Table(missing_table_data)

            # Create bullet points
            bullet_points = [
                 f"The dataset contains {self.data_transformation.df.shape[0]:,} rows and {self.data_transformation.df.shape[1]} columns",
                f"The dataset contains {len(self.data_transformation.df['Country'].unique())} unique countries.",
                f"Unique Countries are: {', '.join(self.data_transformation.df['Country'].unique())}"]

            # Create a bullet list
            bullet_list = ListFlowable(
                [ListItem(Paragraph(point, styles['Normal'])) for point in bullet_points],
                bulletType='bullet',
                start='bulletchar',  # You can use '1' for numbered list
                bulletFontName='Helvetica'
            )

            # Add the list to the story
            story.append(bullet_list)

            story.append(Paragraph("Missing Values Summary Table:", styles['h4']))
            story.append(missing_table)

            story.append(Paragraph("**Above report provides a raw overview of the dataset and has not been fully cleaned or finalized.", styles['h5']))

            
            if mode >= 2:
                story.append(Paragraph(
                "The following visualizations have been generated after applying key data cleaning steps. "
                 "Specifically, all records with null values were removed,and only transactions with positive quantities and unit prices (i.e., Quantity > 0 and UnitPrice > 0) "
                "were retained to ensure data accuracy.",
                 styles['h3']
                ))
                story.append(Paragraph("Top 5 Countries by Record Count:", styles['h2']))
                chart_image = self.image_generator.create_top5_countries_chart()
                story.append(chart_image)

                story.append(Paragraph("<b>Analysis:</b> Most transactions occurred in the United Kingdom, followed by Germany and other countries.", styles['Normal']))

                story.append(PageBreak())
                story.append(Paragraph("Total Quantaties Sold Per Year:", styles['h2']))
                chart_image = self.image_generator.create_year_chart()
                story.append(chart_image)
                story.append(Paragraph("<b>Analysis:</b> The majority of transactions occurred in 2011, showing a significant increase compared to 2010. This suggests a rising customer base and growing business activity during that period, possibly due to seasonal demand and improved online retail presence. The trend highlights the importance of maintaining inventory and marketing strategies to meet peak demand periods effectively.", styles['Normal']))

                story.append(PageBreak())
                story.append(Paragraph("Monthly Sales Quantities (2011):", styles['h2']))
                chart_image = self.image_generator.create_month_chart_2011()
                story.append(chart_image)
                story.append(Paragraph(
    "<b>Analysis:</b> Most quantities were sold between September and November of 2011, indicating a seasonal surge in product demand. "
    "This peak may be driven by holiday shopping behavior, promotional campaigns, or bulk purchasing by wholesalers. "
    "Recognizing such patterns is essential for aligning inventory planning, sales strategies, and customer targeting during high-demand periods.",
    styles['Normal']))
            
            if mode >= 3:
                story.append(PageBreak())
                story.append(Paragraph("Correlation between Quantity & Unit Price (For Sep,Oct,Nov):", styles['h2']))
                chart_image = self.image_generator.create_corr()
                story.append(chart_image)
                story.append(Paragraph(
    "<b>Analysis:</b> The correlation analysis between Quantity and UnitPrice for the months of September, October, and November revealed a negative relationship. "
    "This suggests that lower-priced items were typically purchased in higher quantities, which is common in wholesale or promotional buying behavior. "
    "Understanding this inverse correlation can help optimize pricing strategies, especially during high-volume sales periods.",
    styles['Normal']))

                story.append(PageBreak())
                story.append(Paragraph("Highest Purchasing Customers (by Quantity):", styles['h2']))
                chart_image = self.image_generator.create_highest_purchasing_customer()
                story.append(chart_image)
                story.append(Paragraph(
    "<b>Analysis:</b> The analysis of top purchasing customers by quantity reveals that a small subset of customers contributes a disproportionately large share of total sales volume. "
    "These high-volume buyers are likely to be wholesale or repeat customers. Identifying and nurturing such key accounts can help strengthen customer loyalty and significantly impact revenue through targeted marketing, personalized offers, or bulk purchase incentives.",
    styles['Normal']))

                story.append(PageBreak())
                story.append(Paragraph("Transactions by Weekday and Time of Day:", styles['h2']))
                chart_image = self.image_generator.create_weekday_transaction()
                story.append(chart_image)
                story.append(Paragraph(
    "<b>Analysis:</b> Most purchases occurred on Thursday afternoons, indicating a mid-to-late week surge in customer activity. "
    "This trend may reflect business-driven buying cycles, as many wholesale customers place bulk orders before the weekend. "
    "The consistent spike on Thursdays could also be aligned with marketing campaigns or restocking behaviors. "
    "Understanding this peak period enables better planning for inventory management, customer support staffing, and targeted promotions to capitalize on high-engagement time windows. "
    "Additionally, scheduling system maintenance or data updates outside of these peak hours could ensure seamless customer experience.",
    styles['Normal']))

            # Build the PDF document
            doc.build(story)
            t2 = time.time()
            t3 = t2-t1
            print(f'Report generated in {t3:.2f} secs.Open "Report.pdf"')
        except Exception as e:
            raise e
        