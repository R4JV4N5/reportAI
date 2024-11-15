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


report_format = """

"""
user_prompt = """
You are a Python code generator that creates a comprehensive financial report based on a provided summary of data.Your task is to take the following input summary and generate a Python script that will produce a well-structured report, including key financial metrics, visualizations, and interpretations.

The report should contain sections for an executive summary, financial highlights, detailed analysis of revenues and expenses, graphical representations of financial growth, and a conclusion.

Input Summary:
{report_summary}

"Write a Python script that accomplishes the following:

Import necessary libraries such as reportlab and pandas.
* Define variables to represent financial data, such as sales, expenses, profits, and other summary metrics.
* Use pandas to create a DataFrame for organizing and managing the financial data.
* Compile a structured financial report in PDF format using reportlab. Ensure the report includes sections such as:
       Financial Summary
       Key Metrics and Ratios
* Add comments in the code to explain each step for better understanding.
* Ensure the report is stakeholder-friendly, with neatly formatted tables, headings, and descriptions.
* Prevent overlapping or overflow of content in the PDF by handling layout, spacing, and pagination properly. 
* Ensure the content fits neatly on the page without cutting off or overcrowding."
* Use times roman font from reportlab with the following specifications:
       Title font size: 18
       Heading font size: 14
       Body text font size: 10
Additional Notes:

Include a clear table of financial data with columns like "Metric," "Value," and "Description."
Add an introduction page summarizing the purpose of the report and a conclusion section highlighting key insights.

# handle following errors : {error}

you can use this template to fill specific sections based oon the summary handdle the errors above in following code:{code_template}



"""

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


# user_prompt = """
# Your output should be a complete Python script ready for execution, with comments explaining each section of the code for clarity. The script should follow best practices for coding standards and include any necessary imports or function definitions required for creating the report using ReportLab.

# I need you to help me generate a one-page report. The report should include the following sections:

# 1. **Title**: A concise, descriptive title for the report.
# 2. **Executive Summary**: A brief summary of the report, including key points and outcomes.
# 3. **Introduction**: A section that introduces the purpose and scope of the report.
# 4. **Findings/Results**: List the key findings or results from the research or project. Each finding should be numbered.
# 5. **Conclusion/Recommendations**: Provide conclusions and actionable recommendations based on the findings.

# Conclusion/Recommendations
# Based  on  these  findings,  we  recommend  reviewing  our  sales  strategies  and  profit  margins  to
# identify  areas  for  improvement.  Additionally,  we  should  prioritize  collecting  data  on  the  Montana
# product to inform future business decisions.


# Based on this information, please generate a structured report with clear, concise sections, and ensure the format is appropriate. ensure each section is evenly spaced and do not overlap eact other

# savepath = 'report/'
# FILE_NAME = reportai

# use following Summary: {report_summary}

# handle following errors : {error}

# """




