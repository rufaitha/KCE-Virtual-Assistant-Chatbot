from flask import Flask, render_template, request, jsonify
import requests
import re
from html import unescape

app = Flask(__name__)

# ============================================================
# KCE INFORMATION
# ============================================================

KCE_DATA = {
    "college": "Kings College of Engineering (KCE)",

    "location": (
        "Punalkulam, Near Thanjavur, "
        "Gandarvakottai Taluk, Pudukkottai District – 613 303, "
        "Tamil Nadu, India."
    ),

    "phone": "+91-6380989024",

    "email": "contact@kingsengg.edu.in",

    "website": "https://www.kingsengg.edu.in/",

    "founded": "2001",

    "management": (
        "Kings College of Engineering was founded in 2001 by "
        "Raj Educational Trust (RET), Chennai."
    ),

    "ug": [
        "B.E. Civil Engineering",
        "B.E. Computer Science and Engineering",
        "B.E. Electronics and Communication Engineering",
        "B.E. Electrical and Electronics Engineering",
        "B.E. Mechanical Engineering",
        "B.Tech Artificial Intelligence and Data Science",
        "B.Tech Information Technology"
    ],

    "pg": [
        "M.B.A. Master of Business Administration",
        "M.E. Computer Science and Engineering",
        "M.E. Power Electronics and Drives",
        "M.E. Thermal Engineering",
        "M.E. VLSI Design"
    ],

    "phd": [
        "Ph.D. Mechanical Engineering",
        "Ph.D. Electronics and Communication Engineering"
    ]
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def list_html(items):
    return "<ul>" + "".join(
        f"<li>{item}</li>" for item in items
    ) + "</ul>"


def get_latest_updates():
    """
    Fetch the latest announcements displayed on the
    official KCE website.
    """

    url = KCE_DATA["website"]

    try:
        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        response.raise_for_status()

        html = unescape(response.text)

        # Remove scripts and styles
        html = re.sub(
            r"<(script|style).*?</\1>",
            " ",
            html,
            flags=re.DOTALL | re.IGNORECASE
        )

        # Convert common HTML separators to spaces
        text = re.sub(r"<br\s*/?>", "\n", html, flags=re.IGNORECASE)
        text = re.sub(r"</(p|div|li|h1|h2|h3|h4|section)>", "\n",
                      text, flags=re.IGNORECASE)

        # Remove remaining HTML tags
        text = re.sub(r"<[^>]+>", " ", text)

        # Clean whitespace
        lines = [
            re.sub(r"\s+", " ", line).strip()
            for line in text.splitlines()
        ]

        lines = [line for line in lines if line]

        # Locate Latest Announcements
        start = None

        for i, line in enumerate(lines):
            if "latest announcements" in line.lower():
                start = i
                break

        if start is None:
            return (
                "<b>Latest KCE Updates</b><br>"
                "I could not retrieve the latest announcement section "
                "right now. Please check the official KCE website."
            )

        # Collect the following announcement lines
        updates = []

        for line in lines[start + 1:]:
            lower = line.lower()

            if "more about kce" in lower:
                break

            if "welcome to kings college" in lower:
                break

            if line not in updates:
                updates.append(line)

            if len(updates) >= 10:
                break

        if not updates:
            return (
                "<b>Latest KCE Updates</b><br>"
                "No announcement details could be retrieved right now. "
                "Please check the official KCE website."
            )

        result = "<b>Latest KCE Announcements</b><ul>"

        for update in updates:
            result += f"<li>{update}</li>"

        result += "</ul>"

        result += (
            f"<br><a href='{KCE_DATA['website']}' "
            "target='_blank'>View the official KCE website</a>"
        )

        return result

    except requests.RequestException:
        return (
            "<b>Latest KCE Updates</b><br>"
            "I could not connect to the official KCE website right now. "
            "Please try again later."
        )

    except Exception:
        return (
            "<b>Latest KCE Updates</b><br>"
            "The latest announcements could not be loaded right now. "
            "Please check the official KCE website."
        )


# ============================================================
# CHATBOT ANSWER LOGIC
# ============================================================

def answer(message):

    q = message.lower().strip()

    if not q:
        return (
            "Please type a question about "
            "Kings College of Engineering."
        )

    # --------------------------------------------------------
    # GREETING
    # --------------------------------------------------------

    if any(word in q for word in [
        "hello", "hi", "hey", "good morning",
        "good afternoon", "good evening"
    ]):
        return (
            "<b>Welcome to KCE Virtual Assistant</b><br>"
            "I can help you with information about Kings College "
            "of Engineering, including programmes, admissions, "
            "fees, management, placements, facilities, hostel, "
            "contact details and latest announcements."
        )

    # --------------------------------------------------------
    # LATEST / CURRENT UPDATES
    # --------------------------------------------------------

    latest_words = [
        "latest",
        "latest update",
        "latest updates",
        "current update",
        "current updates",
        "recent update",
        "recent updates",
        "today",
        "today's",
        "what is happening",
        "what's happening",
        "what is happening at kce",
        "what's happening at kce",
        "events",
        "event today",
        "college news",
        "college updates",
        "news"
    ]

    if any(word in q for word in latest_words):
        return get_latest_updates()

    # --------------------------------------------------------
    # FEES
    # --------------------------------------------------------

    if any(word in q for word in [
        "fee",
        "fees",
        "fee structure",
        "tuition fee",
        "college fee",
        "course fee",
        "fees structure"
    ]):
        return (
            "<b>KCE Fee Information</b><br>"
            "Fee amounts can vary by programme and admission category. "
            "I do not want to provide an unverified fee amount.<br><br>"
            "For the current 2026–27 fee details, please refer to "
            "the official KCE admission information or contact the "
            "admission office.<br><br>"
            f"<b>Admission Contact:</b> {KCE_DATA['phone']}<br>"
            f"<a href='{KCE_DATA['website']}' target='_blank'>"
            "Open Official KCE Website</a>"
        )

    # --------------------------------------------------------
    # MANAGEMENT
    # --------------------------------------------------------

    if any(word in q for word in [
        "management",
        "trust",
        "who manages kce",
        "who runs kce",
        "management details"
    ]):
        return (
            "<b>KCE Management</b><br>"
            "Kings College of Engineering was founded in 2001 by "
            "Raj Educational Trust (RET), Chennai.<br><br>"
            "For the current management and administrative details, "
            "please refer to the official KCE website."
        )

    # --------------------------------------------------------
    # ABOUT KCE
    # --------------------------------------------------------

    if any(word in q for word in [
        "about",
        "about kce",
        "history",
        "founded",
        "established",
        "when was kce founded"
    ]):
        return (
            "<b>About Kings College of Engineering</b><br>"
            "Kings College of Engineering (KCE) was founded in 2001 "
            "by Raj Educational Trust (RET), Chennai.<br><br>"
            "KCE is approved by AICTE, affiliated to Anna University, "
            "accredited by NAAC, and has autonomous status."
        )

    # --------------------------------------------------------
    # ALL COURSES
    # --------------------------------------------------------

    if any(word in q for word in [
        "course",
        "courses",
        "programme",
        "programmes",
        "program",
        "degree",
        "courses offered"
    ]):
        return (
            "<b>UG Programmes</b>"
            + list_html(KCE_DATA["ug"])
            + "<b>PG Programmes</b>"
            + list_html(KCE_DATA["pg"])
            + "<b>Ph.D. Programmes</b>"
            + list_html(KCE_DATA["phd"])
        )

    # --------------------------------------------------------
    # UG
    # --------------------------------------------------------

    if any(word in q for word in [
        "ug",
        "undergraduate",
        "b.e",
        "b.tech"
    ]):
        return (
            "<b>UG Programmes</b>"
            + list_html(KCE_DATA["ug"])
        )

    # --------------------------------------------------------
    # PG
    # --------------------------------------------------------

    if any(word in q for word in [
        "pg",
        "postgraduate",
        "post graduate",
        "m.e",
        "mba",
        "master"
    ]):
        return (
            "<b>PG Programmes</b>"
            + list_html(KCE_DATA["pg"])
        )

    # --------------------------------------------------------
    # Ph.D.
    # --------------------------------------------------------

    if any(word in q for word in [
        "phd",
        "ph.d",
        "research",
        "doctorate"
    ]):
        return (
            "<b>Ph.D. Programmes</b>"
            + list_html(KCE_DATA["phd"])
        )

    # --------------------------------------------------------
    # ADMISSION
    # --------------------------------------------------------

    if any(word in q for word in [
        "admission",
        "admissions",
        "apply",
        "application",
        "how to join",
        "join kce",
        "eligibility"
    ]):
        return (
            "<b>KCE Admission</b><br>"
            "KCE provides admission information and online registration "
            "for first-year UG and PG programmes.<br><br>"
            "Eligibility, application procedure and admission schedules "
            "can change by programme and academic year.<br><br>"
            f"<b>Admission Contact:</b> {KCE_DATA['phone']}<br>"
            f"<a href='{KCE_DATA['website']}' target='_blank'>"
            "Visit Official KCE Website</a>"
        )

    # --------------------------------------------------------
    # PLACEMENTS
    # --------------------------------------------------------

    if any(word in q for word in [
        "placement",
        "placements",
        "job",
        "recruitment",
        "recruit",
        "companies",
        "career"
    ]):
        return (
            "<b>Training and Placement</b><br>"
            "KCE's Placement Cell focuses on career readiness through "
            "soft-skill development, aptitude training, industry "
            "interaction, industrial exposure, projects and campus "
            "recruitment opportunities.<br><br>"
            "For current placement drives and placement records, "
            "please check the official KCE Training and Placement page."
        )

    # --------------------------------------------------------
    # HOSTEL
    # --------------------------------------------------------

    if any(word in q for word in [
        "hostel",
        "hostels",
        "accommodation",
        "stay"
    ]):
        return (
            "<b>KCE Hostel</b><br>"
            "KCE provides hostel-related information as part of its "
            "campus facilities.<br><br>"
            "For current hostel availability, rules, fees and facilities, "
            "please refer to the official KCE website or contact the college."
        )

    # --------------------------------------------------------
    # FACILITIES / INFRASTRUCTURE
    # --------------------------------------------------------

    if any(word in q for word in [
        "facility",
        "facilities",
        "infrastructure",
        "library",
        "laboratory",
        "lab",
        "campus",
        "classroom",
        "sports"
    ]):
        return (
            "<b>KCE Facilities</b><br>"
            "KCE provides campus facilities and infrastructure to support "
            "academic learning, student activities and professional development."
            "<br><br>"
            "For the latest details about specific facilities, please "
            "visit the official KCE website."
        )

    # --------------------------------------------------------
    # DEPARTMENTS
    # --------------------------------------------------------

    if any(word in q for word in [
        "department",
        "departments",
        "cse",
        "ece",
        "eee",
        "civil",
        "mechanical",
        "information technology",
        "aids",
        "artificial intelligence"
    ]):
        return (
            "<b>KCE Departments and Programmes</b><br>"
            "KCE offers programmes in:<ul>"
            "<li>Civil Engineering</li>"
            "<li>Computer Science and Engineering</li>"
            "<li>Electronics and Communication Engineering</li>"
            "<li>Electrical and Electronics Engineering</li>"
            "<li>Mechanical Engineering</li>"
            "<li>Artificial Intelligence and Data Science</li>"
            "<li>Information Technology</li>"
            "</ul>"
            "KCE also offers postgraduate and Ph.D. programmes."
        )

    # --------------------------------------------------------
    # CONTACT
    # --------------------------------------------------------

    if any(word in q for word in [
        "contact",
        "phone",
        "phone number",
        "mobile",
        "number",
        "email",
        "address",
        "location",
        "where is kce",
        "where is the college"
    ]):
        return (
            "<b>KCE Contact Details</b><br><br>"
            f"<b>Address:</b><br>{KCE_DATA['location']}<br><br>"
            f"<b>Phone:</b> {KCE_DATA['phone']}<br>"
            f"<b>Email:</b> {KCE_DATA['email']}<br><br>"
            f"<a href='{KCE_DATA['website']}' target='_blank'>"
            "Official KCE Website</a>"
        )

    # --------------------------------------------------------
    # WEBSITE
    # --------------------------------------------------------

    if any(word in q for word in [
        "website",
        "official website",
        "official site",
        "kce website"
    ]):
        return (
            f"<a href='{KCE_DATA['website']}' target='_blank'>"
            "Open the Official KCE Website →</a>"
        )

    # --------------------------------------------------------
    # THANK YOU
    # --------------------------------------------------------

    if any(word in q for word in [
        "thank",
        "thanks",
        "thank you"
    ]):
        return (
            "You're welcome. Feel free to ask me anything "
            "about Kings College of Engineering."
        )

    # --------------------------------------------------------
    # DEFAULT RESPONSE
    # --------------------------------------------------------

    return (
        "<b>KCE Virtual Assistant</b><br>"
        "I can help you with:<ul>"
        "<li>About KCE</li>"
        "<li>Courses and programmes</li>"
        "<li>Fee information</li>"
        "<li>Admissions</li>"
        "<li>Management</li>"
        "<li>Departments</li>"
        "<li>Placements</li>"
        "<li>Hostel and facilities</li>"
        "<li>Contact details</li>"
        "<li>Latest KCE announcements</li>"
        "</ul>"
        "Please ask your question."
    )


# ============================================================
# FLASK ROUTES
# ============================================================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json(silent=True) or {}

    message = data.get("message", "")

    return jsonify({
        "reply": answer(message)
    })


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)
