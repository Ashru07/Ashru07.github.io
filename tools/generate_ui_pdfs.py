from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer


PAGE_WIDTH, PAGE_HEIGHT = A4


def build_pdf(output_path: str, title: str, subtitle: str, paragraphs: list[str]) -> None:
    document = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#0f1724"),
        spaceAfter=8,
    )
    subtitle_style = ParagraphStyle(
        "CustomSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=14,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#475569"),
        spaceAfter=14,
    )
    body_style = ParagraphStyle(
        "CustomBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=11,
        leading=16,
        spaceAfter=10,
        textColor=colors.HexColor("#111827"),
    )

    story = [
        Paragraph(title, title_style),
        Paragraph(subtitle, subtitle_style),
    ]

    for paragraph in paragraphs:
        story.append(Paragraph(paragraph, body_style))

    document.build(story)


best_ui_paragraphs = [
    "The best user interface I have used is <b>W3Schools</b>. I think it is successful because it respects the way many people actually learn: by trying something, seeing the result immediately, and then adjusting based on feedback. The page layout is simple, the tutorials are separated into small pieces, and the examples are easy to scan. That reduces the cognitive load for beginners and makes the site feel approachable instead of intimidating.",
    "Its most useful feature is the live editor. A learner can read a short explanation on one side and instantly test code on the other side. This is a strong example of good interaction design because the interface keeps the user in control. It gives clear feedback, supports experimentation, and does not force the learner to switch between many different tools. The navigation is also predictable, so once you understand one page, the rest of the site feels familiar.",
    "The visual design is not flashy, but it is practical. Headings, examples, and buttons are easy to recognize. The contrast is readable, the page structure is consistent, and the site does not bury important content under unnecessary decoration. That consistency is one of the main reasons it works so well. A good interface does not need to be complicated if its goal is to help users finish a task quickly.",
    "If I could improve it, I would make the learning path more personalized. For example, the site could remember which topics a student has already practiced and suggest the next logical lesson. It could also offer stronger progress tracking, a cleaner mobile-first practice mode, and more context-sensitive hints for absolute beginners. Even with those improvements, the current design is already a strong example of a useful, user-centered educational interface.",
]

worst_ui_paragraphs = [
    "The worst user interface I have used is the Bangladesh Railway e-ticketing website, <b>https://eticket.railway.gov.bd/</b>. The main issue is that the site often feels overloaded and stressful to use, especially when users are trying to book tickets quickly. The interface puts too many steps in front of a simple task, and the journey from searching to payment can feel fragile and confusing. Instead of guiding the user smoothly, it often makes the user worry about whether the next action will work.",
    "A major weakness is the lack of clarity in the booking flow. Important actions are not always visually emphasized, the page structure can feel crowded, and error messages are not always helpful enough for a first-time user. When a ticketing system is under heavy demand, good interaction design becomes even more important. The interface should reduce uncertainty, but here it often does the opposite by making users guess what is happening or what to do next.",
    "Another problem is consistency. Some parts of the website feel dated, while other parts look like they were added later without fully matching the rest of the system. That creates a disjointed experience. The site also seems to assume that users already understand the process, which is a mistake for a public service. A railway booking site should support a wide range of users, including people with low digital experience and people using slow connections.",
    "It could have been made much better by simplifying the workflow, improving the visibility of each step, and giving users clearer feedback after every action. The site should also be faster, more accessible, and better tested on mobile devices. I think it turned out this way because the project likely had to balance many constraints: high traffic, legacy systems, complex business rules, and limited time for redesign. Even so, a more user-centered approach would have made the system far less frustrating to use.",
]


if __name__ == "__main__":
    build_pdf(
        "e:/Desk/Ashru07/assets/best_ui.pdf",
        "Best User Interface I Have Used",
        "W3Schools as a practical, beginner-friendly learning interface",
        best_ui_paragraphs,
    )
    build_pdf(
        "e:/Desk/Ashru07/assets/worst_ui.pdf",
        "Worst User Interface I Have Used",
        "Bangladesh Railway e-ticketing site as an example of a frustrating booking flow",
        worst_ui_paragraphs,
    )
