"""
Database setup for the Nandha Arts and Science College Admission Chatbot.
Creates admission.db (SQLite) and seeds it with sample college data
modeled on Nandha Arts and Science College (NASC), Erode.
Run: python3 database/db_setup.py
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "admission.db")


def create_and_seed():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # ---------- Schema ----------
    cur.execute("""
        CREATE TABLE courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_name TEXT NOT NULL,
            course_code TEXT NOT NULL,
            department TEXT NOT NULL,
            duration TEXT NOT NULL,
            eligibility TEXT NOT NULL,
            annual_fee INTEGER NOT NULL,
            seats INTEGER NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE scholarships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            eligibility TEXT NOT NULL,
            benefit TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE important_dates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event TEXT NOT NULL,
            event_date TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_name TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE faqs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE chat_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            user_message TEXT,
            detected_intent TEXT,
            confidence REAL,
            bot_response TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ---------- Seed data ----------
    # Course catalog modeled on Nandha Arts and Science College (NASC), Erode —
    # affiliated to Bharathiar University, Coimbatore. Fees are illustrative,
    # based on the college's publicly reported annual fee range (~Rs 32,000-50,000).
    courses = [
        ("B.A. English", "BAENG", "Arts & Humanities", "3 Years", "10+2 in any stream, min 45%", 34000, 60),
        ("B.A. Tamil", "BATAM", "Arts & Humanities", "3 Years", "10+2 in any stream, min 45%", 34000, 60),
        ("B.Sc. Computer Science", "BSCCS", "Science", "3 Years", "10+2 with Mathematics/Science, min 50%", 42000, 60),
        ("B.Sc. Mathematics", "BSCMAT", "Science", "3 Years", "10+2 with Mathematics, min 45%", 38000, 60),
        ("B.Sc. Biotechnology", "BSCBIO", "Science", "3 Years", "10+2 with Biology/Science, min 45%", 40000, 60),
        ("B.Sc. Physics", "BSCPHY", "Science", "3 Years", "10+2 with Physics & Mathematics, min 45%", 38000, 60),
        ("B.Com (General)", "BCOM", "Commerce", "3 Years", "10+2 in any stream, min 45%", 50000, 80),
        ("BCA (Bachelor of Computer Applications)", "BCA", "Computer Applications", "3 Years", "10+2 with Mathematics, min 45%", 45000, 60),
        ("BBA (Bachelor of Business Administration)", "BBA", "Management", "3 Years", "10+2 in any stream, min 45%", 42000, 60),
        ("M.Sc. Computer Science", "MSCCS", "Science", "2 Years", "B.Sc. Computer Science or related, min 50%", 46000, 30),
        ("M.Sc. Mathematics", "MSCMAT", "Science", "2 Years", "B.Sc. Mathematics, min 50%", 40000, 30),
        ("M.A. English", "MAENG", "Arts & Humanities", "2 Years", "B.A. English or related, min 50%", 36000, 30),
        ("M.Com", "MCOM", "Commerce", "2 Years", "B.Com, min 50%", 44000, 30),
    ]
    cur.executemany(
        "INSERT INTO courses (course_name, course_code, department, duration, eligibility, annual_fee, seats) VALUES (?,?,?,?,?,?,?)",
        courses,
    )

    scholarships = [
        ("Merit Scholarship", "Score above 90% in the qualifying exam", "Up to 50% tuition fee waiver"),
        ("Sports Scholarship", "State/National level sports achievement", "Up to 25% tuition fee waiver"),
        ("Economically Weaker Section (EWS) Scholarship", "Family income below Rs. 2,50,000 per annum", "Up to 40% tuition fee waiver"),
        ("Single Parent / Women Empowerment Scholarship", "Applicants from single-parent households", "Fee concession as assessed by the college committee"),
        ("Alumni Ward Scholarship", "Children of NASC alumni", "15% tuition fee waiver"),
    ]
    cur.executemany(
        "INSERT INTO scholarships (name, eligibility, benefit) VALUES (?,?,?)",
        scholarships,
    )

    important_dates = [
        ("Application Portal Opens", "1 March 2026"),
        ("Last Date to Apply Online", "15 June 2026"),
        ("Personal Interview & Counselling", "18-26 June 2026"),
        ("Merit List Release", "30 June 2026"),
        ("Document Verification", "1-10 July 2026"),
        ("Fee Payment Deadline", "15 July 2026"),
        ("Classes Commence", "1 August 2026"),
    ]
    cur.executemany(
        "INSERT INTO important_dates (event, event_date) VALUES (?,?)",
        important_dates,
    )

    documents = [
        ("10th Mark Sheet and Certificate",),
        ("12th Mark Sheet and Certificate",),
        ("Transfer Certificate (TC)",),
        ("Migration Certificate (if applicable)",),
        ("Passport-size Photographs (4 copies)",),
        ("Aadhaar Card / Government ID Proof",),
        ("Community Certificate (if applicable)",),
        ("Income Certificate (for scholarship applicants)",),
        ("Conduct Certificate from previous institution",),
    ]
    cur.executemany("INSERT INTO documents (document_name) VALUES (?)", documents)

    faqs = [
        ("Is hostel accommodation available?",
         "Yes, separate hostel facilities are available for men and women with mess, Wi-Fi, and 24x7 security. Hostel fee is approximately Rs. 45,000 per year, payable separately from tuition fee."),
        ("What is the placement record?",
         "NASC has a dedicated Placement Cell that organizes campus recruitment drives, internships, and skill-development / personality-development programs throughout the year. Contact the Placement Cell directly for the latest recruiter list and package details."),
        ("Is there a management quota?",
         "As a self-financed institution, a limited number of seats may be available under the management quota, subject to eligibility criteria. Please contact the admission office for current availability."),
        ("Can I apply for more than one course?",
         "Yes, applicants can apply for a maximum of 3 courses in a single application. Preference order should be indicated during the application process."),
        ("Is there an entrance exam for admission?",
         "No national entrance exam is required. Admission is primarily based on your Class 12 (10+2) marks, followed by a Personal Interview conducted by the college."),
        ("How can I contact the admission office?",
         "You can reach Nandha Arts and Science College at info@nandhaarts.org or call 04294-222788 / +91 73737 24422. The campus is located at Koorapalayam Pirivu, Perundurai Main Road, Pitchandampalayam Post, Erode - 638052, Tamil Nadu."),
    ]
    cur.executemany("INSERT INTO faqs (question, answer) VALUES (?,?)", faqs)

    conn.commit()
    conn.close()
    print(f"Database created and seeded successfully at: {DB_PATH}")


if __name__ == "__main__":
    create_and_seed()
