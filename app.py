from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


# =========================================================
# KCE BASIC INFORMATION
# =========================================================

KCE_DATA = {
    "college": "Kings College of Engineering (KCE)",

    "location": (
        "Punalkulam, Near Thanjavur, "
        "Gandarvakottai Taluk, Pudukkottai District – 613303, "
        "Tamil Nadu, India."
    ),

    "phone": "+91-6380989024",

    "email": "contact@kingsengg.edu.in",

    "website": "https://www.kingsengg.edu.in/",

    "founded": "2001",

    "management": "Raj Educational Trust",

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
        "M.E. VLSI Design",
        "M.E. Thermal Engineering",
        "M.E. Power Electronics and Drives",
        "M.E. Computer Science and Engineering",
        "M.B.A. Master of Business Administration"
    ],

    "phd": [
        "Ph.D. Mechanical Engineering",
        "Ph.D. Electronics and Communication Engineering"
    ]
}


# =========================================================
# HELPER FUNCTION
# =========================================================

def list_html(items):
    return "<ul>" + "".join(
        f"<li>{item}</li>" for item in items
    ) + "</ul>"


# =========================================================
# CHATBOT ANSWER FUNCTION
# =========================================================

def answer(message):

    q = message.lower().strip()

    # Empty message
    if not q:
        return "Please type a question about Kings College of Engineering."


    # =====================================================
    # GREETING
    # =====================================================

    if any(word in q for word in [
        "hello",
        "hi",
        "hey",
        "good morning",
        "good afternoon",
        "good evening"
    ]):

        return (
            "Hello! 👋<br><br>"
            "I’m the <b>KCE Virtual Assistant</b>.<br>"
            "I can help you with information about "
            "courses, admissions, fees, departments, "
            "placements, facilities, hostel, management, "
            "contact details and more."
        )


    # =====================================================
    # COLLEGE NAME
    # =====================================================

    if any(word in q for word in [
        "what is kce",
        "what does kce stand for",
        "college name",
        "name of the college"
    ]):

        return (
            "<b>KCE</b><br>"
            "KCE stands for <b>Kings College of Engineering</b>."
        )


    # =====================================================
    # ABOUT KCE
    # =====================================================

    if any(word in q for word in [
        "about kce",
        "tell me about kce",
        "about college",
        "about kings college",
        "history of kce"
    ]):

        return (
            "<b>About Kings College of Engineering</b><br><br>"
            "Kings College of Engineering (KCE) was founded in "
            "<b>2001</b> by Raj Educational Trust.<br><br>"
            "The college offers undergraduate, postgraduate "
            "and research programmes in various engineering "
            "and management disciplines."
        )


    # =====================================================
    # FOUNDED / ESTABLISHED
    # =====================================================

    if any(word in q for word in [
        "when was kce founded",
        "when was kce established",
        "founded",
        "established"
    ]):

        return (
            "<b>KCE Founded</b><br>"
            "Kings College of Engineering was founded in "
            "<b>2001</b>."
        )


    # =====================================================
    # MANAGEMENT
    # =====================================================

    if any(word in q for word in [
        "management",
        "who manages kce",
        "managed by",
        "who runs kce",
        "trust",
        "owner"
    ]):

        return (
            "<b>Management</b><br>"
            "Kings College of Engineering is managed by "
            "<b>Raj Educational Trust</b>."
        )


    # =====================================================
    # ALL COURSES
    # =====================================================

    if any(word in q for word in [
        "courses",
        "course",
        "programmes",
        "programs",
        "degrees",
        "what can i study"
    ]):

        return (
            "<b>UG Programmes</b>"
            + list_html(KCE_DATA["ug"])
            +
            "<b>PG Programmes</b>"
            + list_html(KCE_DATA["pg"])
            +
            "<b>Ph.D. Programmes</b>"
            + list_html(KCE_DATA["phd"])
        )


    # =====================================================
    # UG
    # =====================================================

    if any(word in q for word in [
        "ug",
        "undergraduate",
        "b.e",
        "btech",
        "b.tech"
    ]):

        return (
            "<b>UG Programmes</b>"
            + list_html(KCE_DATA["ug"])
        )


    # =====================================================
    # PG
    # =====================================================

    if any(word in q for word in [
        "pg",
        "postgraduate",
        "m.e",
        "mba",
        "master"
    ]):

        return (
            "<b>PG Programmes</b>"
            + list_html(KCE_DATA["pg"])
        )


    # =====================================================
    # Ph.D
    # =====================================================

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


    # =====================================================
    # DEPARTMENTS
    # =====================================================

    if any(word in q for word in [
        "department",
        "departments",
        "cse",
        "ece",
        "eee",
        "civil",
        "mechanical",
        "information technology",
        "artificial intelligence"
    ]):

        return (
            "<b>KCE Departments / Academic Areas</b><br><br>"
            "• Civil Engineering<br>"
            "• Computer Science and Engineering<br>"
            "• Electronics and Communication Engineering<br>"
            "• Electrical and Electronics Engineering<br>"
            "• Mechanical Engineering<br>"
            "• Artificial Intelligence and Data Science<br>"
            "• Information Technology<br>"
            "• Postgraduate programmes<br>"
            "• Management studies"
        )


    # =====================================================
    # FEES
    # =====================================================

    if any(word in q for word in [
        "fee",
        "fees",
        "fee structure",
        "tuition fee",
        "college fees",
        "cost"
    ]):

        return (
            "<b>KCE Fee Information</b><br><br>"
            "The fee structure can vary depending on the "
            "programme and admission category.<br><br>"
            "For the latest and exact fee details, please "
            "contact the KCE admission office or visit the "
            "official KCE website.<br><br>"
            f"<a href='{KCE_DATA['website']}' target='_blank'>"
            "Visit Official KCE Website →</a>"
        )


    # =====================================================
    # ADMISSION
    # =====================================================

    if any(word in q for word in [
        "admission",
        "admissions",
        "apply",
        "application",
        "how to join",
        "join kce",
        "how can i get admission"
    ]):

        return (
            "<b>KCE Admissions</b><br><br>"
            "KCE provides admission opportunities for its "
            "undergraduate and postgraduate programmes.<br><br>"
            "For current eligibility criteria, application "
            "procedure, important dates and admission updates, "
            "please check the official KCE website."
            "<br><br>"
            f"<a href='{KCE_DATA['website']}' target='_blank'>"
            "Open Official Admission Information →</a>"
        )


    # =====================================================
    # PLACEMENTS
    # =====================================================

    if any(word in q for word in [
        "placement",
        "placements",
        "job",
        "recruitment",
        "recruit",
        "career"
    ]):

        return (
            "<b>Training & Placement</b><br><br>"
            "KCE's Training and Placement department supports "
            "students through career-readiness activities such "
            "as aptitude training, soft-skill development, "
            "orientation programmes, industry interaction and "
            "campus recruitment opportunities.<br><br>"
            "For current placement drives and latest records, "
            "please check the official KCE website."
        )


    # =====================================================
    # HOSTEL
    # =====================================================

    if any(word in q for word in [
        "hostel",
        "hostels",
        "accommodation",
        "stay"
    ]):

        return (
            "<b>KCE Hostel</b><br><br>"
            "KCE provides hostel facilities for students.<br><br>"
            "For current hostel availability, rules, facilities "
            "and fee details, please contact the college directly."
        )


    # =====================================================
    # FACILITIES
    # =====================================================

    if any(word in q for word in [
        "facility",
        "facilities",
        "infrastructure",
        "campus"
    ]):

        return (
            "<b>KCE Facilities</b><br><br>"
            "KCE provides academic and campus facilities "
            "including classrooms, laboratories, library and "
            "other student-support facilities.<br><br>"
            "For the latest facility information, please visit "
            "the official KCE website."
        )


    # =====================================================
    # LIBRARY
    # =====================================================

    if any(word in q for word in [
        "library",
        "books",
        "reading"
    ]):

        return (
            "<b>KCE Library</b><br><br>"
            "KCE provides library facilities to support "
            "students' academic and learning needs."
        )


    # =====================================================
    # LABORATORIES
    # =====================================================

    if any(word in q for word in [
        "lab",
        "labs",
        "laboratory",
        "laboratories"
    ]):

        return (
            "<b>KCE Laboratories</b><br><br>"
            "KCE provides department-related laboratory "
            "facilities for practical learning, academic "
            "sessions and student projects."
        )


    # =====================================================
    # INFRASTRUCTURE
    # =====================================================

    if any(word in q for word in [
        "classroom",
        "classrooms",
        "building",
        "infrastructure"
    ]):

        return (
            "<b>KCE Infrastructure</b><br><br>"
            "KCE provides academic infrastructure including "
            "classrooms, laboratories, library and other "
            "campus facilities."
        )


    # =====================================================
    # AUTONOMOUS STATUS
    # =====================================================

    if any(word in q for word in [
        "autonomous",
        "autonomous status"
    ]):

        return (
            "<b>Autonomous Status</b><br><br>"
            "Kings College of Engineering has "
            "<b>autonomous status</b>."
        )


    # =====================================================
    # ACCREDITATION / APPROVAL
    # =====================================================

    if any(word in q for word in [
        "aicte",
        "anna university",
        "naac",
        "accreditation",
        "accredited",
        "affiliation",
        "approved"
    ]):

        return (
            "<b>Recognition & Accreditation</b><br><br>"
            "KCE is approved by AICTE, affiliated to "
            "Anna University, accredited by NAAC and has "
            "autonomous status."
        )


    # =====================================================
    # LOCATION
    # =====================================================

    if any(word in q for word in [
        "location",
        "located",
        "where is kce",
        "where is the college",
        "address"
    ]):

        return (
            "<b>KCE Location</b><br><br>"
            f"📍 {KCE_DATA['location']}"
        )


    # =====================================================
    # CONTACT
    # =====================================================

    if any(word in q for word in [
        "contact",
        "phone",
        "phone number",
        "mobile",
        "email",
        "mail"
    ]):

        return (
            "<b>KCE Contact Details</b><br><br>"
            f"📞 {KCE_DATA['phone']}<br>"
            f"✉️ {KCE_DATA['email']}<br>"
            f"📍 {KCE_DATA['location']}<br><br>"
            f"🌐 <a href='{KCE_DATA['website']}' "
            "target='_blank'>Official Website</a>"
        )


    # =====================================================
    # WEBSITE
    # =====================================================

    if any(word in q for word in [
        "website",
        "official website",
        "official site"
    ]):

        return (
            "<b>KCE Official Website</b><br><br>"
            f"<a href='{KCE_DATA['website']}' "
            "target='_blank'>Open Official KCE Website →</a>"
        )


    # =====================================================
    # TRANSPORT
    # =====================================================

    if any(word in q for word in [
        "transport",
        "bus",
        "college bus"
    ]):

        return (
            "<b>KCE Transport</b><br><br>"
            "For current college bus routes, timings and "
            "availability, please contact the college directly."
        )


    # =====================================================
    # STUDENT ACTIVITIES
    # =====================================================

    if any(word in q for word in [
        "student activities",
        "activities",
        "clubs",
        "events",
        "extracurricular",
        "extra curricular"
    ]):

        return (
            "<b>Student Activities</b><br><br>"
            "Students can participate in academic activities, "
            "projects, events and extracurricular activities "
            "conducted by the college."
        )


    # =====================================================
    # THANK YOU
    # =====================================================

    if any(word in q for word in [
        "thank",
        "thanks",
        "thank you"
    ]):

        return (
            "You're welcome! 😊<br><br>"
            "Feel free to ask me anything about KCE."
        )


    # =====================================================
    # DEFAULT ANSWER
    # =====================================================

    return (
        "I'm the <b>KCE Virtual Assistant</b>.<br><br>"
        "I can help you with:<br>"
        "• Courses & Programmes<br>"
        "• Fees<br>"
        "• Admissions<br>"
        "• Departments<br>"
        "• Management<br>"
        "• Placements<br>"
        "• Hostel<br>"
        "• Facilities<br>"
        "• Library & Laboratories<br>"
        "• Infrastructure<br>"
        "• Contact Details<br>"
        "• Location<br>"
        "• College Information<br><br>"
        "Please ask me a question about KCE."
    )


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():
    return render_template("index.html")


# =========================================================
# CHAT API
# =========================================================

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json(silent=True) or {}

    message = data.get("message", "")

    reply = answer(message)

    return jsonify({
        "reply": reply
    })


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)
