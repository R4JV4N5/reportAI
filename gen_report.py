from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def create_report_template(content_list, filename="report/reportai.pdf"):
    """
    Create a report with multiple sections and wrap text properly using SimpleDocTemplate.
    """
    # Define the document and its size
    doc = SimpleDocTemplate(filename, pagesize=letter)
    doc.title = "ReportAI"
    # Styles for the report
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    heading_style = styles['Heading1']
    body_style = styles['BodyText']

    # Content container (list of elements to add to the document)
    story = []

    # Title of the report
    story.append(Paragraph("Financial Report", title_style))
    story.append(Spacer(1, 12))  # Add space after the title

    # Section Titles and Content
    section_titles = [
        "1. Overall Financial Performance",
        "2. Revenue Breakdown",
        "3. Expense Analysis",
        "4. Profit Margins",
        "5. Key Financial Ratios",
        "6. Conclusion and Outlook"
    ]

    # Loop through each content and section title
    for i, content in enumerate(content_list):
        # Add section title
        story.append(Paragraph(section_titles[i], heading_style))
        story.append(Spacer(1, 6))  # Space between title and content
        
        # Add section content (wrapped text)
        content_paragraph = Paragraph(content.replace(r'\n', '<br/>').replace(r'\t', '&nbsp;&nbsp;&nbsp;&nbsp;'), body_style)
        story.append(content_paragraph)
        story.append(Spacer(1, 12))  # Add space between sections

    # Build the document
    doc.build(story)

# Content for each section
# content_list = [
#     """Government segment led sales with $56.4 million, followed by Small Business ($45.9 million),
# Enterprise ($21.1 million), Midmarket ($2.6 million), and Channel Partners ($1.9 million).
# Total Cost of Goods Sold (COGS) reached $101,832,648.
# Unable to determine overall net revenue due to unavailability of data.
# Outlook: Focus on growing Government and Small Business segments, optimizing COGS, and potentially exploring opportunities in Enterprise and Midmarket.
# Risks: Increasing COGS, stagnating sales in slower-growing segments.
# Recommendations: Analyze Government and Small Business customer needs, optimize supply chain to reduce COGS, and explore strategic partnerships in Enterprise and Midmarket""",
    
#     """Government segment led sales with $56.4 million, followed by Small Business ($45.9 million),
# Enterprise ($21.1 million), Midmarket ($2.6 million), and Channel Partners ($1.9 million).
# Total Cost of Goods Sold (COGS) reached $101,832,648.
# Unable to determine overall net revenue due to unavailability of data.
# Outlook: Focus on growing Government and Small Business segments, optimizing COGS, and potentially exploring opportunities in Enterprise and Midmarket.
# Risks: Increasing COGS, stagnating sales in slower-growing segments.
# Recommendations: Analyze Government and Small Business customer needs, optimize supply chain to reduce COGS, and explore strategic partnerships in Enterprise and Midmarket""",
    
#     """Government segment led sales with $56.4 million, followed by Small Business ($45.9 million),
# Enterprise ($21.1 million), Midmarket ($2.6 million), and Channel Partners ($1.9 million).
# Total Cost of Goods Sold (COGS) reached $101,832,648.
# Unable to determine overall net revenue due to unavailability of data.
# Outlook: Focus on growing Government and Small Business segments, optimizing COGS, and potentially exploring opportunities in Enterprise and Midmarket.
# Risks: Increasing COGS, stagnating sales in slower-growing segments.
# Recommendations: Analyze Government and Small Business customer needs, optimize supply chain to reduce COGS, and explore strategic partnerships in Enterprise and Midmarket""",
    
#     """Government segment led sales with $56.4 million, followed by Small Business ($45.9 million),
# Enterprise ($21.1 million), Midmarket ($2.6 million), and Channel Partners ($1.9 million).
# Total Cost of Goods Sold (COGS) reached $101,832,648.
# Unable to determine overall net revenue due to unavailability of data.
# Outlook: Focus on growing Government and Small Business segments, optimizing COGS, and potentially exploring opportunities in Enterprise and Midmarket.
# Risks: Increasing COGS, stagnating sales in slower-growing segments.
# Recommendations: Analyze Government and Small Business customer needs, optimize supply chain to reduce COGS, and explore strategic partnerships in Enterprise and Midmarket""",
    
#     """Government segment led sales with $56.4 million, followed by Small Business ($45.9 million),
# Enterprise ($21.1 million), Midmarket ($2.6 million), and Channel Partners ($1.9 million).
# Total Cost of Goods Sold (COGS) reached $101,832,648.
# Unable to determine overall net revenue due to unavailability of data.
# Outlook: Focus on growing Government and Small Business segments, optimizing COGS, and potentially exploring opportunities in Enterprise and Midmarket.
# Risks: Increasing COGS, stagnating sales in slower-growing segments.
# Recommendations: Analyze Government and Small Business customer needs, optimize supply chain to reduce COGS, and explore strategic partnerships in Enterprise and Midmarket""",
    
#     """Government segment led sales with $56.4 million, followed by Small Business ($45.9 million),
# Enterprise ($21.1 million), Midmarket ($2.6 million), and Channel Partners ($1.9 million).
# Total Cost of Goods Sold (COGS) reached $101,832,648.
# Unable to determine overall net revenue due to unavailability of data.
# Outlook: Focus on growing Government and Small Business segments, optimizing COGS, and potentially exploring opportunities in Enterprise and Midmarket.
# Risks: Increasing COGS, stagnating sales in slower-growing segments.
# Recommendations: Analyze Government and Small Business customer needs, optimize supply chain to reduce COGS, and explore strategic partnerships in Enterprise and Midmarket"""
# ]

# # Call the function to generate the report
# create_report_template(content_list)
