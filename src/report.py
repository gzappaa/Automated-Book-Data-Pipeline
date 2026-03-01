from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import pandas as pd

def generate_pdf(stats, output_path="data/book_report.pdf"):
    """
    Generates a PDF report containing:
    - Summary statistics (total, average, max, min)
    - Most expensive book
    - Cheapest book
    - Complete list of books
    """

    books = stats["books"]  # Extract the list of books from stats
    doc = SimpleDocTemplate(output_path)  # Create PDF document
    elements = []  # This will hold all PDF elements
    styles = getSampleStyleSheet()  # Load default styles

    # ===== Title =====
    elements.append(Paragraph("<b>Book Data Report</b>", styles["Title"]))
    elements.append(Spacer(1, 0.5*inch))  # Add spacing after title

    # ===== Summary =====
    elements.append(Paragraph("<b>Summary</b>", styles["Heading2"]))
    elements.append(Paragraph(f"Total Books: {stats['total_books']}", styles["Normal"]))
    elements.append(Paragraph(f"Average Price: £{stats['average_price']}", styles["Normal"]))
    elements.append(Paragraph(f"Max Price: £{stats['max_price']}", styles["Normal"]))
    elements.append(Paragraph(f"Min Price: £{stats['min_price']}", styles["Normal"]))
    elements.append(Spacer(1, 0.3*inch))

    # ===== Most Expensive Book =====
    me = stats["most_expensive"]
    elements.append(Paragraph("<b>Most Expensive Book</b>", styles["Heading3"]))
    elements.append(Paragraph(f"{me['title']} - £{me['price']}", styles["Normal"]))
    elements.append(Spacer(1, 0.3*inch))

    # ===== Cheapest Book =====
    ch = stats["cheapest"]
    elements.append(Paragraph("<b>Cheapest Book</b>", styles["Heading3"]))
    elements.append(Paragraph(f"{ch['title']} - £{ch['price']}", styles["Normal"]))
    elements.append(Spacer(1, 0.3*inch))

    # ===== Complete Book List =====
    elements.append(Paragraph("<b>Book List</b>", styles["Heading2"]))

    # Convert each book into a bullet list item with title, price, and rating
    book_items = [
        ListItem(Paragraph(f"{b['title']} | £{b['price']} | {b['rating']} stars", styles["Normal"]))
        for b in books
    ]
    elements.append(ListFlowable(book_items, bulletType="bullet"))

    # ===== Build PDF =====
    doc.build(elements)  # Generate the final PDF file

    import pandas as pd

def generate_excel(stats, output_path="data/book_report.xlsx"):
    """
    Generates an Excel file with all book data.
    """
    books = stats["books"]
    df = pd.DataFrame(books)
    df.to_excel(output_path, index=False)