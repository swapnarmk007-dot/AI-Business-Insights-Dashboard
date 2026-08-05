from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


def generate_pdf_report(

    filepath,

    rows,

    columns,

    missing,

    duplicates,

    best_model,

    score

):

    doc = SimpleDocTemplate(filepath)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "<b><font size=18>AI Business Intelligence Report</font></b>",
            styles["Title"]
        )
    )

    elements.append(Spacer(1,20))

    data = [

        ["Rows", rows],

        ["Columns", columns],

        ["Missing Values", missing],

        ["Duplicate Rows", duplicates],

        ["Best Model", best_model],

        ["Score", score]

    ]

    table = Table(data)

    table.setStyle(

        TableStyle([

            ("BACKGROUND",(0,0),(-1,0),colors.darkblue),

            ("TEXTCOLOR",(0,0),(-1,0),colors.white),

            ("GRID",(0,0),(-1,-1),1,colors.grey),

            ("BACKGROUND",(0,1),(-1,-1),colors.beige),

            ("BOTTOMPADDING",(0,0),(-1,0),10)

        ])

    )

    elements.append(table)

    elements.append(Spacer(1,25))

    elements.append(

        Paragraph(

            "This report was generated automatically by the AI Business Intelligence Platform.",

            styles["BodyText"]

        )

    )

    doc.build(elements)