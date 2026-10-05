# Datacom Kudos Portal

An internal employee portal feature built using a **Spec-Driven Development** methodology, allowing colleagues to recognize, appreciate, and moderate "Kudos" across teams.

---

## Features

1. **Public Kudos Feed & Filtering**: View recent appreciations with category badges (🌟 Great work, 🤝 Teamwork, 💡 Innovation), relative timestamps, and instant filter tabs (*All, Received by Me, Given by Me*).
2. **Interactive Kudos Submission**: Searchable colleague selection with team context, live character counter (500-char limit), and button state locking to prevent duplicate submissions.
3. **Engagement Stats Strip**: Real-time counters showing your received kudos, given kudos, and total team kudos for the week.
4. **Content Moderation & Admin Portal**: Dedicated admin panel enabling authorized administrators to toggle kudos visibility (Hide/Unhide with mandatory reason tracking) or delete inappropriate records permanently.

---

## Project Structure

```text
datacom-kudos-portal/
├── SPECIFICATION.md       # Formal requirements, database schema, and design specifications
├── README.md              # Project documentation and setup guide
├── requirements.txt       # Python dependencies list
├── app.py                 # Core Flask backend, database models, and route handlers
├── templates/             # HTML templates
│   ├── index.html         # Main dashboard, stats strip, submission form, and interactive feed
│   └── admin.html         # Content moderation panel with reason tracking
└── instance/
    └── kudos.db           # SQLite local database file


Setup & Installation Instructions
1. Prerequisites
Ensure you have Python 3.x installed on your system.

2. Clone the Repository & Navigate to Folder
git clone https://github.com/Hanibani7532/datacom-kudos-portal.git
cd datacom-kudos-portal

3. Install Dependencies
Run the following command in your terminal to install Flask and SQLAlchemy:
python -m pip install -r requirements.txt


4. Run the Application
Start the Flask development server:
python app.py

5. Access in Browser
Open your browser and navigate to:
Main Dashboard: http://127.0.0.1:5000
Admin Moderation Panel: http://127.0.0.1:5000/admin