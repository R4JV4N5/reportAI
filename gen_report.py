from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

def create_report_template(content_list, filename="report/reportai.pdf"):
    """
    Create a report with multiple sections and wrap text properly using SimpleDocTemplate.
    """
    # Check if the file exists, and create the directory if needed
    if not os.path.exists(filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)  # Create directory if it doesn't exist

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
        "1.Overall Payment Performance",
        "2.Payment Trends Across Batches and Courses",
        "3.Comparison of Payment Modes",
        "4.Installment Payment Analysis",
        "5.Revenue Projections Based on Payment Trends",
        "6.Semester-Wise Payment Overview",
        "7.Conclusion and Future Outlook"
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

