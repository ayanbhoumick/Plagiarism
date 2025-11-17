📘 Plagiarism Checker (Python)

A lightweight and beginner-friendly text-comparison tool built using pure Python.
It analyzes multiple text files, detects overlapping sentences, and calculates plagiarism-style similarity scores — all without any external NLP libraries or APIs.

⸻

🚀 Features
	•	📄 Compare multiple text files (A.txt, B.txt, C.txt…)
	•	📊 Sentence-level similarity scoring
	•	🔍 Detect and highlight common/matching sentences
	•	⚙️ Clean & modular Python code
	•	💻 Works offline — no internet or API calls
	•	🧪 Simple, transparent logic (easy to learn & extend)

⸻

🧠 How It Works
	1.	Reads all .txt files inside the project folder
	2.	Splits each file into sentences
	3.	Compares every file with every other file
	4.	Detects exact or near-exact sentence matches
	5.	Outputs:
	•	Percentage similarity
	•	List of common/matching lines

The algorithm uses basic Python string operations, making it ideal for learning how plagiarism/similarity tools work under the hood.
📂 Project Structure
plagiarism/
│
├── A.txt
├── B.txt
├── C.txt
├── plagiarism.py
└── README.md

