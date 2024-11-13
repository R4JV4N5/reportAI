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

report_summary_prompt = """ You are an AI tasked with summarizing a financial report based on a provided list of questions and answers.Your goal is to extract key insights, trends, and highlights from the information given in the format of a brief summary.1.Analyze the content of the provided Q&A text for important financial metrics, performance indicators, and any notable developments.2.Focus on clarity, coherence, and conciseness in your summary.3.Ensure that the summary is structured logically, emphasizing the most critical information first.4.Your output should be a well-organized paragraph or two that encapsulates the essence of the Q&A content, highlighting any significant changes or outlooks.5.Maintain a professional tone appropriate for a financial audience.Input: {qa_text} Output: """


report_code_generation = """
"Create a basic financial report using Python based on the provided summary of financial data.
"""

ast_sum_prompt = "You are good at generating summaries based on question answers on financial data "


report_format = """

"""


user_prompt = """
Your output should be a complete Python script ready for execution, with comments explaining each section of the code for clarity. The script should follow best practices for coding standards and include any necessary imports or function definitions required for creating the report using ReportLab.

I need you to help me generate a one-page report. The report should include the following sections:

1. **Title**: A concise, descriptive title for the report.
2. **Executive Summary**: A brief summary of the report, including key points and outcomes.
3. **Introduction**: A section that introduces the purpose and scope of the report.
4. **Findings/Results**: List the key findings or results from the research or project. Each finding should be numbered.
5. **Conclusion/Recommendations**: Provide conclusions and actionable recommendations based on the findings.

Conclusion/Recommendations
Based  on  these  findings,  we  recommend  reviewing  our  sales  strategies  and  profit  margins  to
identify  areas  for  improvement.  Additionally,  we  should  prioritize  collecting  data  on  the  Montana
product to inform future business decisions.


Based on this information, please generate a structured report with clear, concise sections, and ensure the format is appropriate. ensure each section is evenly spaced and do not overlap eact other

savepath = 'report/'
FILE_NAME = reportai

use following Summary: {report_summary}

handle following errors : {error}

"""



