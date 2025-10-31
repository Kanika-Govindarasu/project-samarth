Markdown

# 🇮🇳 Project Samarth: Intelligent Q&A for Government Data

This project is a submission for the "Project Samarth" challenge. It is a functional, end-to-end prototype of an intelligent Q&A system built to answer natural language questions by querying multiple, inconsistent datasets from `data.gov.in`.

The system can successfully understand a user's question, determine which dataset to query, and answer questions about both **agricultural economy** (from a `.csv` file) and **climate patterns** (from an `.xls` file).

<img width="1479" height="738" alt="image" src="https://github.com/user-attachments/assets/9f5e51b3-a324-4e80-a8fb-6bfa0136e850" />


## 🚀 Core Features

* **Intelligent Agent Brain:** A "Router Agent" (powered by the Groq API) classifies user questions into different categories (Greeting, Crop Question, Climate Question, or Other).
* **Multi-Tool Architecture:** The agent routes questions to specialized "Data Tools," each responsible for one dataset.
* **Dynamic Code Generation:** Each tool uses an AI to dynamically write and execute `pandas` code to query its data file. This allows it to answer complex questions without being pre-programmed.
* **Multi-Format Data Handling:** The system successfully pulls data from two different file formats (`.csv` and `.xls`) to prove its robustness.
* **Accuracy & Traceability:** All answers are 100% accurate to the data and cite their exact source file.
* **Conversational UI:** The agent can handle simple greetings and politely deflect off-topic questions.

---

## 🛠️ System Architecture

This prototype is built as a modular "Agent" system, which is robust and scalable.

1.  **Front-End (Streamlit):** The user types a question.
2.  **Orchestrator / "Brain" (`run_agent`):** The user's question is first sent to the Groq API to be classified into one of four categories: `CROP_YIELD`, `CLIMATE_DATA`, `GREETING`, or `OTHER`.
3.  **Tool Routing:** Based on the classification, the brain routes the question to the correct tool:
    * `CROP_YIELD` → `query_crop_yield()`
    * `CLIMATE_DATA` → `query_climate_data()`
    * `GREETING` / `OTHER` → A friendly, pre-written response is given.
4.  **Data Tools / "Hands" (`query_...`):**
    * The tool loads its specific data file (e.g., `pd.read_csv` or `pd.read_excel`).
    * It sends the column names and the user's question to the Groq API, asking it to **write Python `pandas` code**.
    * It safely **executes** this generated code to get a raw answer.
    * It sends the raw answer (e.g., `3421.0`) back to Groq for a final **"cleanup"** pass to make it user-friendly.
5.  **Response:** The final, clean answer is formatted with its source and shown to the user.

---

## ⚙️ Tech Stack

* **Python 3.10+**
* **Streamlit:** For the web app front-end.
* **Groq API:** Provides the LLM "brain" (using the `llama-3.1-8b-instant` model).
* **Pandas:** For loading and querying the data.
* **`xlrd`:** Required by pandas to read `.xls` files.

---

## 📦 Data Sources

Both datasets were sourced from `data.gov.in` and are included in the `/data` folder:

1.  **`crop_yield_2019.csv`:** An agricultural dataset showing crop yields (kg/hectare) for various crops.
2.  **`Rainfall.xls`:** A climate dataset showing normal annual rainfall (in mm) for districts across India.

---

## Local Setup & Installation

To run this project on your own machine, follow these steps.

### 1. Clone the Repository

```bash
git clone [https://github.com/your-username/project-samarth.git](https://github.com/your-username/project-samarth.git)
cd project-samarth
2. Create and Activate a Virtual Environment
Create the environment:

Bash

python -m venv .venv
Activate it (Windows):

PowerShell

.\.venv\Scripts\Activate.ps1
(On Mac/Linux, use: source .venv/bin/activate)

3. Install Dependencies
Install all the required Python libraries from the requirements.txt file.

Bash

pip install -r requirements.txt
4. Set Up Your API Key
This project requires a free API key from Groq.

Create a new folder in your project root named .streamlit.

Inside that folder, create a new file named secrets.toml.

Your folder structure should look like this:

project-samarth/
├── .streamlit/
│   └── secrets.toml   <-- YOUR SECRET KEY GOES HERE
├── data/
│   ├── crop_yield_2019.csv
│   └── Rainfall.xls
├── app.py
├── requirements.txt
└── README.md
Add your Groq API key to the secrets.toml file:

Ini, TOML

GROQ_API_KEY = "gsk_YourActualKeyGoesHere"
5. Run the App
You're all set! Run the Streamlit app from your terminal.

Bash

streamlit run app.py
