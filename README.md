📌 Project Overview

This project showcases how to:
Generate structured output from an LLM
Enforce schema validation using Pydantic
Validate nested objects and field constraints
Apply cross-field validation logic
Integrate environment-based API key management
The system ensures that LLM responses strictly follow a predefined schema before being used in downstream applications.

🏗️ Architecture
```
User Prompt
⬇
OpenAI LLM
⬇
Structured JSON Response
⬇
Pydantic Validation
⬇
Validated Output (Safe for Production Use)
```

🧠 Key Features
```
✅ Structured JSON output parsing
✅ Pydantic BaseModel validation
✅ Field constraints (min/max length, numeric bounds)
✅ Enum validation using Literal
✅ Nested models
✅ Cross-field validation using @model_validator
✅ Environment variable management via .env
```

📂 Project Structure
```bash
Movie-Recommendation-Output-Validator/
│
├── movieRecommendation.py
├── .env
├── venv/
└── README.md

🧾 Pydantic Schema Design
```
Movie Model
Each recommendation must include:
title (string, 1–100 characters)
year (1900–2025)
genre (restricted set)
rating (0–10)
summary (20–500 characters)
```

RecommendationResponse Model
user_query
mood
recommendations (1–5 movies)
total_recommendations
Optional note
Includes cross-field validation to ensure:

```
total_recommendations == len(recommendations)
```

🚀 How to Run
1️⃣ Create Virtual Environment


```
python -m venv venv
venv\Scripts\activate
```

2️⃣ Install Dependencies
```
pip install openai pydantic python-dotenv
```
3️⃣ Create .env File
```
OPENAI_API_KEY=your_api_key_here
```

4️⃣ Run the Script
```
python movieRecommendation.py
```
🛡️ Why This Matters
In production LLM systems:
Raw text output is unreliable
JSON formatting via prompting alone is fragile
Schema enforcement ensures reliability
Using Pydantic makes LLM integrations:
Predictable
Validated
Safer for downstream systems
Production-ready

📚 Concepts Demonstrated
Structured Output in LLM Workflows
Data Type Coercion
Custom Field Validation
Schema Enforcement
Tool-Ready Output Validation

```
🧑‍💻 Author

Reza Paramarta
Software Test Engineer | NLP & LLM Enthusiast
```

