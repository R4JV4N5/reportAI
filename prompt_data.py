# db_columns_info = '''
# Table:university_data

# Price units are in 'INR',

# 1. University (VARCHAR):
#    - Description: Represents the name of the university offering the course. This is used to identify the institution within the data.
#    - Unique Values: ['JAIN (DEEMED-TO-BE UNIVERSITY)']

# 2. UniversityCode (VARCHAR):
#    - Description: The code representing the university.

# 3. Batch (VARCHAR):
#    - Description: Indicates the batch or cohort in which a student is enrolled, with details like start date and course duration.
#    - Unique Values: ['July 2020 - 3 Years', 'July 2020 - 2 Years', 'July 2019 - 2 Years', 'July 2019 - 3 Years', 'WorkX - 2020', 
#                       'July 2020 - 1 Year', 'Jan 2020 - 2 Years', 'Jan 2019 - 2 Years', 'Jan 2021 -3 Years', 'Jan 2021 - 2 Year', 
#                       'Jan 2020 - 3 Years', 'July 2021 - 2 Years', 'July 2019 - 1 Year', 'July 2021 - 3 Years', 'Jan 2019 - 3 Years', 
#                       'Jan 2022 - 2 Years', 'Jan 2022 - 3 Years']

# 4. Course (VARCHAR):
#    - Description: Indicates the name of the course a student is enrolled in.
#    - Unique Values: ['Bachelor of Science', 'Bachelor of Business Administration', 'Master of Science Psychology', 
#                      'Master of Commerce', 'Bachelor of Arts', 'Bachelor of Commerce', 'Bachelors in Computer Application', 
#                      'WorkX Diploma Program', 'Post Graduate Diploma Program in Banking & Finance Management', 
#                      'MA in Economics', 'Bachelor of Business Administration with Apprenticeship', 
#                      'Master of Science (Psychology) with Apprenticeship', 'Bachelor of Arts with Apprenticeship', 
#                      'Post Graduate Diploma Program in Human Resource Management', 'Post Graduate Diploma Program in Finance Management',
#                      'Master of Commerce with Apprenticeship', 'Bachelor of Commerce with Apprenticeship', 
#                      'MA in Economics with Apprenticeship', 'Post Graduate Diploma Program in Information Technology', 
#                      'M.A. (English)']

# 5. Semester (VARCHAR):
#    - Description: Denotes the semester within the academic year.
#    - Unique Values: ['Semester 1', 'Semester 3', 'Registration', 'Semester 5']

# 6. InstallmentNo (INTEGER):
#    - Description: Represents the installment number for payment.

# 7. EnrollmentNo (VARCHAR):
#    - Description: The unique identifier for each student’s enrollment.

# 8. Name (VARCHAR):
#    - Description: The name of the student.

# 9. PaymentId (INTEGER):
#    - Description: The unique identifier for each payment made.

# 10. Amount (FLOAT):
#     - Description: The total payment amount made by the student.

# 11. Mode (VARCHAR):
#     - Description: The mode of payment used by the student, such as online payment or demand draft.
#     - Unique Values: ['Net Banking', 'DD']

# 12. Provider (VARCHAR):
#     - Description: The payment service provider used to process the payment.
#     - Unique Values: ['ATOM TECHNOLOGIES LTD.', 'CITRUS PAYMENT SOLUTIONS PVT. LTD.', 'AGGREPAY', 'CCAvenue']

# 13. Status (VARCHAR):
#     - Description: The status of the payment.
#     - Unique Values: ['C']

# 14. PaidOn (VARCHAR):
#     - Description: The date when the payment was made.

# '''
db_columns_info = '''
Table:university_data

Price units are in 'INR',

1. University (VARCHAR):
   - Description: Represents the name of the university offering the course. This is used to identify the institution within the data.

2. UniversityCode (VARCHAR):
   - Description: The code representing the university.

3. Batch (VARCHAR):
   - Description: Indicates the batch or cohort in which a student is enrolled, with details like start date and course duration.

4. Course (VARCHAR):
   - Description: Indicates the name of the course a student is enrolled in.

5. Semester (VARCHAR):
   - Description: Denotes the semester within the academic year.


6. InstallmentNo (INTEGER):
   - Description: Represents the installment number for payment.

7. EnrollmentNo (VARCHAR):
   - Description: The unique identifier for each student’s enrollment.

8. Name (VARCHAR):
   - Description: The name of the student.

9. PaymentId (INTEGER):
   - Description: The unique identifier for each payment made.

10. Amount (FLOAT):
    - Description: The total payment amount made by the student.

11. Mode (VARCHAR):
    - Description: The mode of payment used by the student, such as online payment or demand draft.
  
12. Provider (VARCHAR):
    - Description: The payment service provider used to process the payment.
    
13. Status (VARCHAR):
    - Description: The status of the payment.
   

14. PaidOn (VARCHAR):
    - Description: The date when the payment was made.

'''

questions_prompt = """
You are an AI expert in generating financial questions based on table data for comprehensive company reports.
You do not include any introductory phrases like "Here are..." or similar statements.

Categorization: Organize questions into these categories:

Performance Analysis:
"How have payment amounts changed across different batches and courses over time?"

Comparisons:
"What are the differences in payment amounts across various payment modes (Net Banking vs. DD)?"

Future Projections:
"What is the projected revenue based on current installment payment trends?"

Output: Provide 5 insightful questions in a strictly " + " separated format to guide report generation.
Do not generate anything else

Do not generate anything else 
"""

report_summary_prompt = """ You are an AI tasked with summarizing a financial report based on a provided list of questions and answers.Your goal is to extract key insights, trends, and highlights from the information given in the format of a brief summary.1.Analyze the content of the provided Q&A text for important financial metrics, performance indicators, and any notable developments.2.Focus on clarity, coherence, and conciseness in your summary.3.Ensure that the summary is structured logically, emphasizing the most critical information first.4.Your output should be a well-organized paragraph or two that encapsulates the essence of the Q&A content, highlighting any significant changes or outlooks.5.Maintain a professional tone appropriate for a financial audience.Input: {qa_text} Output: """


report_code_generation = """
"Create a basic financial report using Python based on the provided summary of financial data.
"""

ast_sum_prompt = "You are good at generating summaries based on question answers on financial data "




# Prompts for report contents

ast_report_prompt = "you are good at generating report contents from financial summaries"

Payment_Performance_prompt = """Analyze the overall payment performance from the following summary \n{report_summary}\n. Include key metrics such as total payment amount, number of payments, and payment trends over time. Identify how these figures have changed across different time periods (year, month). Discuss the impact of different market segments, countries, and products on payment performance."""

Payment_Trends_by_Batch_and_Course_prompt = """Examine the payment trends by batch and course from the following summary \n{report_summary}\n. Break down the payment amounts and number of payments for each batch and course. Identify which batches or courses have the highest payment volumes and whether any specific trends or anomalies exist across different periods."""

Payment_Mode_Comparison_prompt = """Compare the payment amounts and payment volumes across different payment modes (e.g., Net Banking, DD) from the following summary \n{report_summary}\n. Analyze the contribution of each payment mode to total revenue and identify any trends or shifts in preference for payment methods over time."""

Installment_Analysis_prompt = """Analyze the payment data related to installments from the following summary \n{report_summary}\n. Examine the number of installment payments, total installment amount, and frequency of installment payments. Identify trends in installment usage and any correlations with specific batches, courses, or payment modes."""

Revenue_Projections_prompt = """Provide projections for future revenue based on current payment trends from the following summary \n{report_summary}\n. Analyze historical payment data to estimate future payment volumes and total revenue. Include considerations for changes in market segments, countries, payment modes, and other key factors that may influence revenue growth."""

Semester_Payment_Overview_prompt = """Summarize the payment performance by semester from the following summary \n{report_summary}\n. Break down the payment amounts and trends across different semesters. Identify which semesters have seen the highest or lowest payment volumes and analyze any trends or patterns in payment behavior by semester."""

Conclusion_and_Outlook_prompt = """Summarize the key payment performance insights from the following summary \n{report_summary}\n. Focus on payment volumes, trends by batch and course, and payment modes. Provide an outlook for the next period, highlighting any potential risks or opportunities based on current payment trends. Recommend strategies to optimize payment collection and improve revenue generation."""



prompt_list = [Payment_Performance_prompt,Payment_Trends_by_Batch_and_Course_prompt,Payment_Mode_Comparison_prompt,Installment_Analysis_prompt,Revenue_Projections_prompt,Semester_Payment_Overview_prompt,Conclusion_and_Outlook_prompt]





