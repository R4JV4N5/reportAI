db_columns_info = '''
segment (VARCHAR): Indicates the market segment ('Government', 'Midmarket', 'Channel Partners', 'Enterprise',
       'Small Business'), useful for analyzing performance based on the type of client.
country (VARCHAR): Represents the country where the sale occurred, important for geographic sales analysis.
product (VARCHAR): Specifies the product sold, in this case, Carretera','Montana','Paseo','Velo ','VTT','Amarilla', which helps in tracking product-specific sales performance.
discount_band (VARCHAR): Shows the discount band applied to the product (if any), useful for analyzing the impact of discounts on sales.
units_sold (FLOAT): Represents the number of units sold, useful for tracking sales volume.
manufacturing_price (FLOAT): Indicates the price to produce one unit of the product, critical for cost and profit analysis.
sale_price (FLOAT): The price at which the product was sold, essential for calculating gross revenue and profit margins.
gross_sales (FLOAT): The total revenue before any discounts, representing overall sales value.
discounts (FLOAT): The total discount amount, useful for assessing the impact of discounts on gross revenue.
sales (FLOAT): The actual sales amount after applying any discounts, used for understanding net revenue.
cogs (FLOAT): The cost of goods sold, critical for calculating profitability and assessing the efficiency of sales.
profit (FLOAT): The net profit, calculated as sales minus COGS, showing the actual profitability of each sale.
date (DATE): The date the sale occurred, useful for time-based analysis and trends.
month_number (INTEGER): The numerical representation of the month, aiding in month-wise analysis.
month_name (VARCHAR): The name of the month, useful for reporting and visualizing data trends across months.
year (INTEGER): The year of the sale,in this case(2013,2014) useful for analyzing performance over time.
'''

questions_prompt = """
You are an AI expert in generating financial questions based on table data for comprehensive company reports.

Follow these steps:

Context Understanding: Identify the report’s purpose and focus on key financial aspects.

Key Info Extraction: Examine table columns for metrics like revenue, expenses, or growth rates.

Question Generation: Formulate questions that encourage in-depth analysis of trends, comparisons, and financial health.

Categorization: Organize questions into these categories:

Performance Analysis (e.g., "How has revenue changed over recent quarters?")
Comparisons (e.g., "What are the profit margin differences across product lines?")
Future Projections (e.g., "What is the projected revenue based on current growth rates?")
Clarity and Precision:MAKE SURE QUESTIONS ARE CLEAR, specific, and directly related to the data.

Output: Provide 5 insightful questions in a strictly " + " separated format to guide report generation.
Do not generate anything else 
"""

