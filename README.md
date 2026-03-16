# 🤖 AI Job Intelligence Platform

An **AI-powered job market intelligence dashboard** that analyzes real AI and tech job listings, extracts skill demand using NLP, and allows users to explore job opportunities and AI career insights using intelligent assistants.

The system combines **web scraping, PostgreSQL, NLP pipelines, LLM agents, and an interactive Streamlit dashboard** to create a real-world AI data product.

Users can:

- Discover **latest AI job opportunities**
- Filter jobs by **skills and regions**
- Analyze **top hiring locations**
- Ask an **AI career assistant** about AI roles and learning paths
- Use a **tech assistant** to ask general technology questions

---

# 🛠 Tech Stack

## Backend
- Python
- PostgreSQL
- SQLAlchemy
- psycopg2

## Data Engineering
- Web Scraping
- REST APIs
- Requests
- JSON Parsing
- Pandas Data Processing

## Natural Language Processing
- spaCy
- Named Entity Recognition (Skill Extraction)

## AI / LLM
- OpenAI API
- GPT Models
- Prompt Engineering
- LLM-based Query Agents

## Web Search Integration
- Tavily API
- Web Search Agent

## Frontend
- Streamlit

## Development Tools
- Git
- GitHub
- dotenv
- Virtual Environments

---

# 🚀 Features

## 📊 AI Job Dashboard

The main dashboard provides insights into the AI job market.

Features include:

- Latest AI job opportunities
- Region-based filtering
- Skill-based job discovery
- Top hiring locations visualization
- Direct job application links

---

## 🔎 Skill-Based Job Discovery

Users can filter job listings using a **skill dropdown**.

Example filters:

- Machine Learning
- Python
- AWS
- NLP
- Data Engineering

The system queries the PostgreSQL database to return **relevant job listings matching the selected skill.**

---

## 🌍 Top Hiring Locations

The dashboard analyzes job data and visualizes **top AI hiring regions globally.**

This provides insight into where AI jobs are most concentrated.

Example output:

```
USA
UK
India
Germany
```

Displayed using **interactive charts in Streamlit**.

---

## 💬 AI Career Assistant

Users can ask questions about AI careers such as:

- How do I become a Machine Learning Engineer?
- What skills are required for AI roles?
- What tools should I learn for data science?

The assistant performs **web search + LLM reasoning** to generate structured responses.

---

## 🤖 AI Tech Assistant

A second assistant designed for general technology questions.

Example queries:

```
What is LangChain?
How does Kubernetes work?
What tools should a data engineer learn?
```

The assistant retrieves web context and generates an answer using GPT.

---

# 🏗 System Architecture

```
Job Sources
(RemoteOK, Greenhouse, Remotive)
        │
        ▼
Web Scrapers (Python)
        │
        ▼
PostgreSQL Database
        │
        ▼
NLP Skill Extraction
(spaCy)
        │
        ▼
AI Query Agents
(OpenAI + Web Search)
        │
        ▼
Interactive Dashboard
(Streamlit)
```

---

# ⚙️ Installation

## Clone Repository

```
git clone https://github.com/karanexc/ai-job-market-intelligence.git
cd ai-job-market-intelligence
```

---

## Create Virtual Environment

```
python -m venv venv
```

Activate environment

Mac / Linux

```
source venv/bin/activate
```

Windows

```
venv\Scripts\activate
```

---

## Install Dependencies

```
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file in the project root.

```
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key

DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database
DB_USER=your_user
DB_PASSWORD=your_password
```

---

# ▶️ Run the Application

Start the dashboard:

```
streamlit run dashboard/chat_app.py
```

The **AI Job Intelligence Dashboard** will launch locally.

---

# 📌 Example Usage

### Skill-Based Job Discovery

```
Skill: Machine Learning
Region: Europe
```

Output:

- Machine Learning Engineer
- AI Engineer
- Data Scientist
- Solutions Architect

---

### AI Career Assistant Example

```
How do I become a Machine Learning Engineer?
```

AI generates:

- Required programming languages
- ML frameworks
- Cloud tools
- Learning roadmap

---

### AI Tech Assistant Example

```
What tools should a data engineer learn?
```

The assistant returns curated insights using web search + GPT.

---

# 📈 Future Improvements

Planned enhancements include:

- AI job salary prediction
- Skill gap analysis for users
- AI job demand forecasting
- Time-series analysis of skill trends
- Cloud deployment (AWS / GCP / Azure)

---

# 👨‍💻 Author

**Karan Mhaswadkar**

MSc Computer Science (Artificial Intelligence)  
University of Kent

GitHub  
https://github.com/karanexc

---

# 📄 License

MIT License
