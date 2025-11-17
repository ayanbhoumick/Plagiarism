📘 Plagiarism Checker (Python)

A lightweight, fast, and beginner-friendly text plagiarism detection tool built using pure Python.
This project compares multiple text files, highlights matching content, and calculates similarity scores — all without external APIs.

⸻

 Features
	•	Upload / Load Multiple Text Files (A.txt, B.txt, C.txt, etc.)
	•	Sentence-level Similarity Detection
	•	Percentage-based Plagiarism Score
	•	Common Sentence Highlighting
	•	Clean & Modular Python Code
	•	Works offline — no internet or API required

⸻

 How It Works
	1.	Reads all text files from the project directory
	2.	Splits content into sentences
	3.	Compares each file with every other file
	4.	Identifies common or highly similar sentences
	5.	Outputs:
	•	Plagiarism percentage per file
	•	List of matching sentences

The core logic uses basic Python string matching (no external NLP libraries), making it easy to understand and modify.

📂 Project Structure
plagiarism/
│
├── A.txt
├── B.txt
├── C.txt
├── plagiarism.py
└── README.md

🛠️ Running the Program

1. Clone the repository
   git clone https://github.com/<your-username>/plagiarism.git
   cd plagiarism

2. Run the script
   python3 plagiarism.py

Example Output
Comparing A.txt and B.txt...
Similarity: 42%

Common sentences:
- The quick brown fox jumps over the lazy dog.
- Machine learning is transforming the world.

📌 Future Improvements
	•	Add GUI with Tkinter or a simple Streamlit app
	•	Add visual color-coded plagiarism bar
	•	Add PDF/Docx support
	•	Improve matching using NLP (spaCy, fuzzywuzzy, cosine similarity)
