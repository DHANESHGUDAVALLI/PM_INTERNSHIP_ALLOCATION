# 🎓 PM Internship Allocation System

> An intelligent internship-matching system that uses student skills and internship requirements to recommend the most relevant internship opportunity.

[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)](https://www.python.org/)
[![scikit--learn](https://img.shields.io/badge/scikit--learn-TF--IDF%20%7C%20Cosine%20Similarity-orange)](https://scikit-learn.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-150458?logo=pandas)](https://pandas.pydata.org/)

## 📌 Overview

The **PM Internship Allocation System** is a data-driven recommendation application designed to simplify internship allocation by matching a student's skills with internship requirements.

Instead of relying only on manual allocation, the project converts skill descriptions into TF-IDF vectors and uses **cosine similarity** to identify the strongest skill-based match.

The repository contains separate data, recommendation-engine, API, UI, and testing components, making the project easy to understand and extend. The current implementation uses `students.csv` and `internships.csv` as its core data sources.

## 🎯 Problem Statement

Internship allocation can become difficult when the number of students and available opportunities increases. Manual matching can be time-consuming and may overlook relevant skill similarities.

This project addresses that problem by:

- Structuring student and internship information.
- Comparing student skills with required internship skills.
- Producing a best-match recommendation.
- Presenting the recommendation through an application interface.

## ✨ Key Features

- 🔎 **Skill-based internship matching**
- 🧠 **TF-IDF text vectorization**
- 📐 **Cosine-similarity based recommendation**
- 👨‍🎓 Student profile and skill processing
- 🏢 Internship requirement matching
- 📍 Internship location and sector information
- 🖥️ Application UI
- 🔌 API layer for application integration
- 🧪 Testable recommendation engine
- 📊 CSV-based data workflow

## 🧠 Recommendation Logic

The core matching pipeline is:

```text
Student Skills
      ↓
Text Preprocessing / TF-IDF
      ↓
Internship Skill Vectors
      ↓
Cosine Similarity
      ↓
Similarity Scores
      ↓
Best-Matching Internship
```

The implementation loads student and internship datasets, vectorizes internship requirements using `TfidfVectorizer`, transforms the selected student's skills into the same vector space, calculates cosine similarity, and selects the highest-scoring internship.

## 🏗️ Architecture

```text
┌──────────────────────┐
│ Student / Internship │
│       CSV Data       │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Recommendation       │
│ Engine               │
│ TF-IDF + Similarity  │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ API / Application    │
│ Interface            │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Best Internship      │
│ Recommendation       │
└──────────────────────┘
```

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| Language | Python |
| Data Processing | Pandas |
| NLP / Feature Extraction | TF-IDF |
| Similarity | Cosine Similarity |
| ML Library | scikit-learn |
| Interface | Python-based UI |
| Data Storage | CSV |

## 📂 Project Structure

```text
PM_INTERNSHIP_ALLOCATION/
├── data/
│   ├── students.csv
│   └── internships.csv
├── api.py
├── engine.py
├── ui.py
├── test.py
└── .gitignore
```

## ⚙️ Installation

```bash
git clone https://github.com/DHANESHGUDAVALLI/PM_INTERNSHIP_ALLOCATION.git
cd PM_INTERNSHIP_ALLOCATION

python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

pip install pandas scikit-learn
```

Install any additional dependencies required by `api.py` or `ui.py` in your local environment.

## ▶️ Run the Recommendation Engine

```bash
python engine.py
```

The engine includes a sample recommendation call and returns the student's details together with the best matching internship, required skills, location, and sector.

## 📊 Example Output

```text
Student
  ↓
Skills: Python, Machine Learning, Data Analysis
  ↓
Similarity Analysis
  ↓
Best Match: Relevant Internship
  ↓
Location + Sector + Required Skills
```

## 🌍 Real-World Applications

The concept can be extended to:

- Government internship allocation programs
- University placement cells
- Corporate internship portals
- Skill-based recruitment systems
- Career recommendation platforms
- Workforce allocation systems

## 🚀 Future Enhancements

- Top-N internship recommendations instead of only one result
- Skill normalization and synonym handling
- Weighted scoring for skills, location, education, and preferences
- Explainable recommendations showing why an internship matched
- Database-backed student and internship management
- Authentication and role-based access
- Admin dashboard and analytics
- Fairness and bias monitoring
- Feedback-based recommendation improvement
- Cloud deployment and scalable APIs

## ⚠️ Current Limitations

The current recommendation engine is primarily skill-text based. It should therefore be treated as a **decision-support tool**, not an automated final allocation authority.

For production use, additional constraints such as eligibility, capacity, location preference, academic criteria, deadlines, and fairness rules should be incorporated.

## 🔗 Repository

[View PM Internship Allocation on GitHub](https://github.com/DHANESHGUDAVALLI/PM_INTERNSHIP_ALLOCATION)

## 👨‍💻 Author

**Dhanesh Gudavalli**

If this project is useful, consider giving the repository a ⭐.
