# AI Lesson Summary and Reflection Coach

This assignment project lets learners paste lesson notes and receive a structured eLearning study output with a short summary, key concepts, misunderstandings, reflection questions, a mini practice activity, and a final takeaway.

## Features

- HTML frontend
- JavaScript `async/await` API call
- Python FastAPI backend
- OpenAI SDK call from the backend
- API key kept only in the backend `.env`
- Loading state and error handling
- Creative eLearning coach prompt
- Structured eLearning-specific output format

## Project Files

- `index.html` - learner-facing frontend
- `styles.css` - page styling
- `script.js` - frontend async request and output rendering
- `main.py` - FastAPI backend with OpenAI SDK
- `requirements.txt` - Python dependencies
- `.env.example` - safe environment variable template

## Setup

1. Create and activate a virtual environment.

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies.

```bash
pip install -r requirements.txt
```

3. Create a `.env` file.

```bash
copy .env.example .env
```

4. Add your OpenAI API key to `.env`.

```env
OPENAI_API_KEY=your_real_key_here
```

5. Start the backend.

```bash
uvicorn main:app --reload
```

6. Open `index.html` in your browser.

## API Endpoint

`POST /lesson-summary`

Example request:

```json
{
  "lesson_title": "Data Privacy in Generative AI Applications",
  "raw_notes": "Generative AI apps may collect prompts, files, and chat history. Teams should avoid sharing sensitive data...",
  "output_style": "workplace application"
}
```

The backend returns structured JSON that the frontend renders into a learner-friendly study output.
