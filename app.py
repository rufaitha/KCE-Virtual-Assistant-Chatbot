from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# KCE information compiled from the official college website.
KCE_DATA = {
    "college": "Kings College of Engineering (KCE)",
    "location": "Punalkulam, Near Thanjavur, Gandarvakottai Taluk, Pudukkottai District – 613 303, Tamil Nadu, India.",
    "phone": "+91-6380989024",
    "email": "contact@kingsengg.edu.in",
    "website": "https://www.kingsengg.edu.in/",
    "founded": "2001",
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

def list_html(items):
    return "<ul>" + "".join(f"<li>{x}</li>" for x in items) + "</ul>"

def answer(message):
    q = message.lower().strip()

    if not q:
        return "Please type a question about Kings College of Engineering."

    if any(w in q for w in ["hello", "hi", "hey", "vanakkam"]):
        return ("Hello! 👋 I’m the KCE Chatbot. I can answer questions about "
                "courses, admissions, departments, placements, contact details and more.")

    if any(w in q for w in ["course", "courses", "programme", "program", "degree"]):
        return ("<b>UG Programmes</b>" + list_html(KCE_DATA["ug"]) +
                "<b>PG Programmes</b>" + list_html(KCE_DATA["pg"]) +
                "<b>Ph.D. Programmes</b>" + list_html(KCE_DATA["phd"]))

    if "ug" in q or "undergraduate" in q:
        return "<b>UG Programmes</b>" + list_html(KCE_DATA["ug"])

    if "pg" in q or "postgraduate" in q or "master" in q or "mba" in q:
        return "<b>PG Programmes</b>" + list_html(KCE_DATA["pg"])

    if "phd" in q or "research" in q:
        return "<b>Ph.D. Programmes</b>" + list_html(KCE_DATA["phd"])

    if any(w in q for w in ["admission", "admissions", "apply", "application"]):
        return ("KCE's official website currently provides an online admission registration "
                "option for first-year UG and PG programmes. For the latest eligibility, "
                "application procedure and admission updates, please check the official website.")

    if any(w in q for w in ["placement", "placements", "job", "recruit"]):
        return ("<b>Training & Placement</b><br>"
                "KCE's Training and Placement department focuses on career readiness through "
                "soft-skill and aptitude training, orientation programmes, industry interaction, "
                "industrial exposure and campus recruitment opportunities. "
                "For current placement drives and records, check the official Training & Placement page.")

    if any(w in q for w in ["contact", "phone", "number", "email", "address", "location", "where"]):
        return (f"<b>KCE Contact Details</b><br>"
                f"📍 {KCE_DATA['location']}<br>"
                f"📞 {KCE_DATA['phone']}<br>"
                f"✉️ {KCE_DATA['email']}<br>"
                f"🌐 <a href='{KCE_DATA['website']}' target='_blank'>Official Website</a>")

    if any(w in q for w in ["about", "history", "founded", "established"]):
        return (f"<b>About KCE</b><br>"
                f"Kings College of Engineering was founded in {KCE_DATA['founded']} by Raj Educational Trust. "
                "The college is approved by AICTE, affiliated to Anna University, accredited by NAAC, "
                "and has autonomous status.")

    if any(w in q for w in ["department", "departments", "cse", "ece", "eee", "civil", "mechanical", "it", "aids"]):
        return ("KCE offers departments/programmes in Civil Engineering, Computer Science and Engineering, "
                "Electronics and Communication Engineering, Electrical and Electronics Engineering, "
                "Mechanical Engineering, Artificial Intelligence and Data Science, and Information Technology, "
                "along with postgraduate programmes.")

    if any(w in q for w in ["facility", "facilities", "library", "lab", "hostel", "infrastructure"]):
        return ("KCE's official website provides information about its facilities and infrastructure. "
                "You can use the <b>Facilities</b> section of the official website for the latest details.")

    if any(w in q for w in ["website", "official site", "official website"]):
        return f"<a href='{KCE_DATA['website']}' target='_blank'>Open the official KCE website →</a>"

    if any(w in q for w in ["thank", "thanks"]):
        return "You're welcome! 😊 Ask me anything about KCE."

    return ("I’m designed for Kings College of Engineering information. "
            "Try asking about <b>courses, admissions, departments, placements, facilities, "
            "college history, or contact details</b>.")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")
    return jsonify({"reply": answer(message)})

if __name__ == "__main__":
    app.run(debug=True)
