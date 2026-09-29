# Nandha Arts and Science College — Admission Chatbot

An AI-based web application that automates the college admission enquiry
process for **Nandha Arts and Science College (NASC), Erode** — a
Bharathiar University-affiliated, NAAC B+ accredited institution under the
Sri Nandha Educational Trust. It uses NLP-based intent classification to
instantly answer questions about courses, eligibility, fees, scholarships,
admission process, important dates, required documents, hostel facilities,
and placements — available 24×7.

> The course catalog, fee ranges, and contact details are modeled on
> NASC's publicly listed information (Arts, Science, Commerce, Computer
> Applications & Management programs). Verify current figures with the
> college before using this as an official deployment.

## Tech Stack

| Layer      | Technology                                  |
|------------|----------------------------------------------|
| Backend    | Python 3, Flask                              |
| Frontend   | HTML, CSS, JavaScript (vanilla)              |
| Database   | SQLite                                       |
| NLP        | scikit-learn (TF-IDF + cosine similarity)    |

> The abstract mentions NLTK/spaCy as candidate NLP libraries. This build
> uses **TF-IDF vectorization + cosine similarity** (via scikit-learn) for
> intent classification instead — it needs no external corpus downloads,
> is lightweight to deploy, and is easy to retrain by editing
> `chatbot/intents.json`. Swapping in spaCy/NLTK for tokenization or
> lemmatization is a natural future enhancement (see below).

## Project Structure

```
college_admission_chatbot/
├── app.py                     # Flask app: routes + API endpoints
├── requirements.txt
├── chatbot/
│   ├── nlp_engine.py           # Intent classifier + dynamic response generator
│   └── intents.json            # Training patterns per intent
├── database/
│   ├── db_setup.py             # Creates & seeds admission.db
│   └── admission.db            # SQLite database (generated)
├── templates/
│   └── index.html              # Chat UI
└── static/
    ├── css/style.css           # "Admission Enquiry Desk" visual theme
    └── js/script.js            # Chat logic (fetch API calls, DOM rendering)
```

## How It Works

1. **User asks a question** in the chat widget (or taps a quick-topic tab).
2. **`/api/chat`** (Flask) receives the message and passes it to `ChatBot.get_response()`.
3. **Intent classification**: the message is normalized (lowercased, punctuation
   stripped) and compared against a TF-IDF vector space built from labeled
   sample patterns in `intents.json`. The closest intent (by cosine similarity)
   is selected; if the best score is below a confidence threshold, it falls
   back to a "didn't understand" response.
4. **Dynamic response generation**: for data-driven intents (courses, fees,
   eligibility, scholarships, dates, documents, FAQs), the engine queries
   **SQLite live** — so updating the database instantly updates chatbot
   answers, no retraining needed. It also does simple entity extraction
   (e.g. detecting "BCA" or "MBA" in the message) to give course-specific
   answers such as "What is the fee for BCA?".
5. Every conversation turn is logged to the `chat_logs` table (session id,
   message, detected intent, confidence, response, timestamp) for analytics.

## Setup & Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Build the database (only needed once, or whenever you edit seed data)
python3 database/db_setup.py

# 3. Run the app
python3 app.py
```

Then open **http://127.0.0.1:5000** in your browser.

## API Endpoints

| Method | Route               | Description                                   |
|--------|----------------------|------------------------------------------------|
| GET    | `/`                  | Serves the chat UI                              |
| POST   | `/api/chat`          | `{ "message": "..." }` → intent + reply         |
| GET    | `/api/quick-topics`  | Suggested quick-reply chips                     |
| GET    | `/api/stats`         | Total queries + top intents (basic analytics)   |

## Customizing the Knowledge Base

- **Courses, fees, eligibility, scholarships, dates, documents, FAQs**:
  edit the seed lists in `database/db_setup.py` and re-run it (or, in a real
  deployment, add an admin panel / direct SQL edits to `admission.db`).
- **Adding a new intent**: add a new entry to `chatbot/intents.json` with
  a list of sample `patterns` a user might type, then add a matching
  branch in `ResponseGenerator.generate()` in `chatbot/nlp_engine.py` if it
  needs dynamic (database-driven) data — static intents just need a
  `responses` list.

## Future Enhancements (as noted in the project abstract)

- Multilingual support (e.g. via `googletrans` or a translation API layer)
- Voice-based interaction (Web Speech API on the frontend)
- Integration with a live admission portal / application-status tracking
- Intelligent course recommendation based on the student's marks/interests
- Swap the TF-IDF classifier for a spaCy/NLTK pipeline or a small
  transformer model for improved intent accuracy on paraphrased queries
- Admin dashboard for editing courses/FAQs without touching code
