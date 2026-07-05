"""
Generates Project3_SQL_Insights_Report.pdf
Steel-blue, minimal style consistent with Bhumi's Project 1 & 2 deliverables.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image, Table,
                                 TableStyle, PageBreak, HRFlowable)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

STEEL_BLUE = colors.HexColor("#4682B4")
DARK_BLUE = colors.HexColor("#1f4e79")
LIGHT_TINT = colors.HexColor("#EAF2F8")
TEXT_GREY = colors.HexColor("#333333")
CODE_BG = colors.HexColor("#F4F6F8")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="ReportTitle", fontName="Helvetica-Bold", fontSize=20,
                           textColor=DARK_BLUE, spaceAfter=8, leading=24))
styles.add(ParagraphStyle(name="SubTitle", fontName="Helvetica", fontSize=10,
                           textColor=TEXT_GREY, spaceAfter=14, leading=13))
styles.add(ParagraphStyle(name="SectionHead", fontName="Helvetica-Bold", fontSize=14,
                           textColor=DARK_BLUE, spaceBefore=16, spaceAfter=8,
                           leftIndent=8))
styles.add(ParagraphStyle(name="Body", fontName="Helvetica", fontSize=9.5,
                           textColor=TEXT_GREY, leading=14, spaceAfter=6))
styles.add(ParagraphStyle(name="InsightItem", fontName="Helvetica", fontSize=9.5,
                           textColor=TEXT_GREY, leading=14, spaceAfter=8, leftIndent=10))
styles.add(ParagraphStyle(name="Caption", fontName="Helvetica-Oblique", fontSize=8.5,
                           textColor=colors.grey, alignment=TA_CENTER, spaceAfter=14))
styles.add(ParagraphStyle(name="FooterText", fontName="Helvetica", fontSize=8,
                           textColor=colors.grey, alignment=TA_CENTER))
styles.add(ParagraphStyle(name="SQLCode", fontName="Courier", fontSize=8,
                           textColor=colors.HexColor("#1f1f1f"), leading=11,
                           backColor=CODE_BG, borderPadding=8, spaceAfter=10))

def section_bar(text):
    t = Table([[Paragraph(text, styles["SectionHead"])]], colWidths=[480])
    t.setStyle(TableStyle([
        ("LINEBEFORE", (0, 0), (0, 0), 4, STEEL_BLUE),
        ("BACKGROUND", (0, 0), (0, 0), LIGHT_TINT),
        ("LEFTPADDING", (0, 0), (0, 0), 10),
        ("TOPPADDING", (0, 0), (0, 0), 4),
        ("BOTTOMPADDING", (0, 0), (0, 0), 4),
    ]))
    return t

def code_block(code_text):
    safe = code_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    safe = safe.replace("\n", "<br/>")
    return Paragraph(safe, styles["SQLCode"])

def result_table(data, col_widths=None):
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), STEEL_BLUE),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_TINT]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t

def build_pdf(output_path):
    doc = SimpleDocTemplate(output_path, pagesize=A4,
                             topMargin=1.3*cm, bottomMargin=1.3*cm,
                             leftMargin=1.6*cm, rightMargin=1.6*cm)
    elements = []

    elements.append(Paragraph("Project 3: SQL Data Analysis", styles["ReportTitle"]))
    elements.append(Paragraph(
        "DecodeLabs Industrial Training Kit &middot; Batch 2026 &middot; "
        "Prepared by Bhumi Singh &middot; Database: orders.db (SQLite) &middot; 1,200 records",
        styles["SubTitle"]))
    elements.append(HRFlowable(width="100%", thickness=1.2, color=STEEL_BLUE, spaceAfter=10))

    # 1. Overview
    elements.append(section_bar("1. Project Overview"))
    elements.append(Paragraph(
        "This project applies SQL to the same cleaned e-commerce orders dataset used in "
        "Projects 1 and 2 (1,200 records, 14 fields), loaded into a SQLite database "
        "(<font face='Courier'>orders.db</font>). 21 queries were written and executed, "
        "covering SELECT, WHERE filtering, GROUP BY aggregation, HAVING, ORDER BY, and "
        "COUNT/SUM/AVG functions, plus business-focused queries like revenue contribution "
        "percentages and repeat-customer identification.", styles["Body"]))

    # 2. Execution order
    elements.append(section_bar("2. Understanding SQL Execution Order"))
    elements.append(Paragraph(
        "Although SQL is written as SELECT &rarr; FROM &rarr; WHERE &rarr; GROUP BY &rarr; "
        "ORDER BY, the database engine actually executes it as: "
        "<b>FROM/JOIN &rarr; WHERE &rarr; GROUP BY &rarr; HAVING &rarr; SELECT &rarr; ORDER BY</b>. "
        "This explains the &ldquo;Alias Trap&rdquo;: a column alias created in SELECT (e.g. "
        "<font face='Courier'>TotalPrice AS rev</font>) cannot be referenced inside WHERE, "
        "because WHERE runs before SELECT and the alias does not exist yet. It CAN, however, "
        "be used in ORDER BY, since ORDER BY runs after SELECT.", styles["Body"]))
    elements.append(code_block(
        "-- This FAILS (alias used before it exists):\n"
        "SELECT TotalPrice AS rev FROM orders WHERE rev > 1000;\n\n"
        "-- This WORKS (condition repeated in WHERE, alias used only in ORDER BY):\n"
        "SELECT TotalPrice AS rev\nFROM orders\nWHERE TotalPrice > 1000\nORDER BY rev DESC;"
    ))

    elements.append(PageBreak())

    # 3. Query Highlights
    elements.append(section_bar("3. Query Highlights & Results"))

    elements.append(Paragraph("<b>3.1 Total Revenue by Product</b> (SUM + GROUP BY + ORDER BY)", styles["Body"]))
    elements.append(code_block(
        "SELECT Product, COUNT(*) AS num_orders, SUM(TotalPrice) AS total_revenue\n"
        "FROM orders\nGROUP BY Product\nORDER BY total_revenue DESC;"
    ))
    elements.append(Image("outputs/chart1_revenue_by_product.png", width=440, height=270))
    elements.append(Paragraph("Fig 1: Chair leads revenue at Rs. 195,620, narrowly ahead of Printer.", styles["Caption"]))

    elements.append(Paragraph("<b>3.2 Average Order Value by Payment Method</b> (AVG + GROUP BY)", styles["Body"]))
    elements.append(code_block(
        "SELECT PaymentMethod, COUNT(*) AS num_orders, ROUND(AVG(TotalPrice),2) AS avg_order_value\n"
        "FROM orders\nGROUP BY PaymentMethod\nORDER BY avg_order_value DESC;"
    ))
    elements.append(Image("outputs/chart2_avg_order_value_payment.png", width=420, height=233))
    elements.append(Paragraph("Fig 2: Credit Card orders carry the highest average value at Rs. 1,127.55.", styles["Caption"]))

    elements.append(PageBreak())

    elements.append(Paragraph("<b>3.3 Monthly Revenue Trend</b> (SUM + GROUP BY on date substring)", styles["Body"]))
    elements.append(code_block(
        "SELECT substr(Date,1,7) AS year_month, COUNT(*) AS num_orders, SUM(TotalPrice) AS total_revenue\n"
        "FROM orders\nGROUP BY year_month\nORDER BY year_month;"
    ))
    elements.append(Image("outputs/chart3_monthly_revenue.png", width=460, height=209))
    elements.append(Paragraph("Fig 3: Monthly revenue trend, Jan 2023 to Jun 2025.", styles["Caption"]))

    elements.append(Paragraph("<b>3.4 Filtering Aggregated Results with HAVING</b>", styles["Body"]))
    elements.append(code_block(
        "SELECT Product, SUM(TotalPrice) AS total_revenue\n"
        "FROM orders\nGROUP BY Product\nHAVING SUM(TotalPrice) > 180000\nORDER BY total_revenue DESC;"
    ))
    elements.append(result_table([
        ["Product", "Total Revenue"],
        ["Chair", "195,620.11"],
        ["Printer", "195,612.61"],
        ["Laptop", "192,126.56"],
        ["Tablet", "186,568.95"],
    ], col_widths=[200, 200]))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(
        "HAVING filters groups AFTER aggregation (unlike WHERE, which filters individual rows "
        "before grouping) &mdash; only products clearing Rs. 180,000 in total revenue appear here.",
        styles["Body"]))

    elements.append(PageBreak())

    # 4. Business Insights
    elements.append(section_bar("4. Key Business Insights"))
    insights = [
        "<b>Chair</b> and <b>Printer</b> are statistically tied for top revenue generator "
        "(Rs. 195,620 vs Rs. 195,613) &mdash; both deserve equal inventory priority.",
        "<b>41.4% of all orders</b> are Cancelled or Returned, calculated directly via SQL "
        "CASE/SUM logic &mdash; confirming the same finding from the Project 2 EDA and "
        "validating the analysis across two different methods.",
        "<b>Credit Card</b> orders have the highest average value (Rs. 1,127.55); "
        "<b>Debit Card</b> the lowest (Rs. 1,001.56) &mdash; a 12.6% spread worth investigating "
        "for targeted payment-method promotions.",
        "Revenue is fairly evenly distributed across products (12&ndash;15.5% each) &mdash; "
        "no single category dominates, which lowers business risk from any one product underperforming.",
        "Only <b>11 customers</b> placed more than 1 order in the dataset &mdash; repeat purchase "
        "rate is low, suggesting an opportunity for loyalty/retention campaigns.",
        "Coupon usage has a small POSITIVE association with order value (Rs. 1,057.64 used vs "
        "Rs. 1,043.37 not used) &mdash; consistent with the Project 2 finding that discounts "
        "are not eroding margin via smaller baskets.",
    ]
    for i, ins in enumerate(insights, 1):
        elements.append(Paragraph(f"{i}. {ins}", styles["InsightItem"]))

    elements.append(Spacer(1, 10))
    elements.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#CCCCCC"), spaceAfter=8))
    elements.append(Paragraph(
        "Full set of 21 queries available in queries.sql. Complete raw output for every query "
        "is available in outputs/Project3_SQL_Results.txt.",
        styles["Body"]))
    elements.append(Paragraph(
        "Prepared as part of the DecodeLabs Industrial Training Kit (Batch 2026) &mdash; Project 3 checkpoint submission.",
        styles["FooterText"]))

    doc.build(elements)
    print(f"PDF saved to {output_path}")

if __name__ == "__main__":
    build_pdf("outputs/Project3_SQL_Insights_Report.pdf")
