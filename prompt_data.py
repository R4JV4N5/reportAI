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
You do not include any introductory phrases like "Here are..." or similar statements.

Categorization: Organize questions into these categories:

Performance Analysis (e.g., "How has revenue changed over recent quarters?")
Comparisons (e.g., "What are the profit margin differences across product lines?")
Future Projections (e.g., "What is the projected revenue based on current growth rates?")
Clarity and Precision:MAKE SURE QUESTIONS ARE CLEAR, specific, and directly related to the data.

Output: Provide 5 insightful questions in a strictly " + " separated format to guide report generation.
Do not generate anything else

Do not generate anything else 
"""

report_summary_prompt = """ You are an AI tasked with summarizing a financial report based on a provided list of questions and answers.Your goal is to extract key insights, trends, and highlights from the information given in the format of a brief summary.1.Analyze the content of the provided Q&A text for important financial metrics, performance indicators, and any notable developments.2.Focus on clarity, coherence, and conciseness in your summary.3.Ensure that the summary is structured logically, emphasizing the most critical information first.4.Your output should be a well-organized paragraph or two that encapsulates the essence of the Q&A content, highlighting any significant changes or outlooks.5.Maintain a professional tone appropriate for a financial audience.Input: {qa_text} Output: """


report_code_generation = """
"Create a basic financial report using Python based on the provided summary of financial data.
"""

ast_sum_prompt = "You are good at generating summaries based on question answers on financial data "


code_template="""

import subprocess
import sys

subprocess.check_call([sys.executable, "-m", "pip", "install -q", "reportlab"])

# Ensure proper imports from reportlab
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def create_report_template(filename="report/reportai.pdf"):
    # Create the PDF document
    pdf = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()

    # Define styles
    title_style = styles['Title']
    heading_style = styles['Heading2']
    body_style = styles['BodyText']

    # Content elements
    elements = []

    # Title
    elements.append(Paragraph("Financial Report", title_style))
    elements.append(Spacer(1, 20))

    # Section 1: Overall Financial Performance
    elements.append(Paragraph("1. Overall Financial Performance", heading_style))
    elements.append(Paragraph("<Insert summary of overall financial performance here>", body_style))
    elements.append(Spacer(1, 12))

    # Section 2: Revenue Breakdown
    elements.append(Paragraph("2. Revenue Breakdown", heading_style))
    # Placeholder for a table or chart
    elements.append(Paragraph("<Insert revenue breakdown table or chart here>", body_style))
    elements.append(Spacer(1, 12))

    # Section 3: Expense Analysis
    elements.append(Paragraph("3. Expense Analysis", heading_style))
    # Placeholder for a table or chart
    elements.append(Paragraph("<Insert expense analysis table or chart here>", body_style))
    elements.append(Spacer(1, 12))

    # Section 4: Profit Margins
    elements.append(Paragraph("4. Profit Margins", heading_style))
    elements.append(Paragraph("<Insert gross margin and net profit margin details here>", body_style))
    elements.append(Spacer(1, 12))

    # Section 5: Cash Flow
    elements.append(Paragraph("5. Cash Flow", heading_style))
    elements.append(Paragraph("<Insert cash flow details and analysis here>", body_style))
    elements.append(Spacer(1, 12))

    # Section 6: Key Financial Ratios
    elements.append(Paragraph("6. Key Financial Ratios", heading_style))
    # Placeholder for a table or chart
    elements.append(Paragraph("<Insert financial ratios table or details here>", body_style))
    elements.append(Spacer(1, 12))

    # Section 7: Conclusion and Outlook
    elements.append(Paragraph("7. Conclusion and Outlook", heading_style))
    elements.append(Paragraph("<Insert summary of financial position and future outlook here>", body_style))
    elements.append(Spacer(1, 12))

    # Build the PDF
    pdf.build(elements)

# Call the function to generate the template
create_report_template()



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


Based on this information, please generate a structured report with clear, concise sections, and ensure the format is appropriate. Prevent overlapping or overflow of content in the PDF by handling layout, spacing, and pagination properly. 
savepath = 'report/'
FILE_NAME = reportai

use following Summary: {report_summary}

handle following errors : {error}

"""




# Prompts for report contents

ast_report_prompt = "you are good at generating report contents from financial summaries"

Overall_Financial_Performance_prompt = """Analyze the overall financial performance from the following summary \n{report_summary}\n . Include key metrics such as total sales, gross sales, and net profit. Identify how these figures have changed over time, focusing on trends by year and month. Discuss the impact of segments, countries, and discount bands on overall performance."""

Revenue_Breakdown_prompt = """Break down total revenue by market segment, country, and product. For each category, calculate the total sales, gross sales, and average sales price. Identify which products or segments have contributed the most to the revenue and highlight any geographic or discount-related trends from the following summary \n{report_summary}\n"""

Expense_Analysis_prompt = """Examine the costs associated with sales, including COGS (cost of goods sold) and manufacturing prices. Compare the manufacturing cost with the sale price for each product, and identify any products that are underperforming or generating lower margins. Analyze how COGS trends vary by segment, country, or product from the following summary \n{report_summary}\n."""

Profit_Margins_prompt = """Evaluate the profit margins for each market segment, country, and product. Calculate the gross profit margin (profit/sales) and net profit margin (profit/gross sales) for each category. Compare these margins across different time periods (month, year) and discuss factors that have contributed to any significant changes in profitability from the following summary \n{report_summary}\n."""

Key_Financial_Ratios_prompt = """Identify and analyze key financial ratios such as gross profit margin, net profit margin, and cost-to-sale ratios for different market segments, countries, and products. Compare these ratios by month or year, and discuss any areas of concern or notable improvements in financial efficiency from the following summary \n{report_summary}\n."""

Conclusion_and_Outlook_prompt = """Summarize the key financial insights, focusing on overall sales, profitability, and performance by segment, country, and product. Provide an outlook for the next period, highlighting any potential risks or opportunities based on trends in sales, margins, and costs. Recommend strategic actions for improving profitability or optimizing sales efforts from the following summary \n{report_summary}\n."""


prompt_list = [Overall_Financial_Performance_prompt,Revenue_Breakdown_prompt,Expense_Analysis_prompt,Profit_Margins_prompt,Key_Financial_Ratios_prompt,Conclusion_and_Outlook_prompt,]