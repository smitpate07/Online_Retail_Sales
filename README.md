## 🛍️ Online Retail Report Generator

Automatically generate insightful PDF reports from the UCI Online Retail Dataset, complete with data summaries, visualizations, and analysis.

## 📌 Features

📄 Generates a PDF report with:

Dataset overview and structure

Summary of missing values

Key metrics and bullet points

Auto-generated visualizations (charts, trends, correlations).

Insightful written analysis for each section.

## 📊 Charts include:

Top countries by transaction volume.

Quantity sold by year and month.

Correlation between quantity and unit price.

Highest purchasing customers.

Transactions by weekday & time of day.

🧼Handles null values, filters invalid data (e.g. negative quantity or unit price).

🧠Modular design using DataTransformation and ImageGenerator classes.

## 🔧 Requirements

Python 3.8+

Libraries:

    pandas

    matplotlib

    seaborn

    reportlab



## 🚀 How to Run

1. Clone this repo.
2. Run the main.py.
3. Choose the report level.
4.🎉 A PDF file (Report.pdf) will be generated in the root directory.

## 📁 Project Structure
    .
    ├── online_retail/
    |   ├── data/
    │   |   └── data.csv
    │   ├── data_transformation.py
    │   ├── image_generator.py
    │   └── report_generator.py
    ├── main.py
    ├── requirements.txt
    └── README.md

## 📌 Example Insights

Most transactions occurred in 2011, especially between September and November.

Peak purchases happened on Thursday afternoons.

Top purchasing customers and countries identified.

Negative correlation between quantity and unit price in peak months.

## 📬 Feedback & Contributions

Feel free to open issues, suggest improvements.