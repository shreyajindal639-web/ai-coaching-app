import os
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from openai import AsyncOpenAI

load_dotenv()

app = FastAPI(
    title="AI Lesson Summary and Reflection Coach API",
    description="Transforms raw lesson notes into structured eLearning study material.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LessonRequest(BaseModel):
    lesson_title: str = Field(
        ...,
        min_length=3,
        example="Data Privacy in Generative AI Applications",
    )
    raw_notes: str = Field(
        ...,
        min_length=20,
        example="Generative AI apps may collect user prompts, uploaded files, and chat history...",
    )
    output_style: str = Field(
        default="summary",
        example="workplace application",
    )


class ConceptItem(BaseModel):
    concept: str
    explanation: str


class LessonCoachResponse(BaseModel):
    short_summary: str
    key_concepts: List[ConceptItem]
    common_misunderstandings: List[str]
    reflection_questions: List[str]
    mini_practice_activity: str
    final_takeaway: str


def build_lesson_prompt(request: LessonRequest) -> str:
    return f"""
You are an eLearning content coach.

Your task is not to merely summarize notes. Convert the raw lesson notes into a useful learning experience that helps a learner revise, reflect, and apply the lesson.

Lesson title:
{request.lesson_title}

Preferred output style:
{request.output_style}

Raw lesson notes:
{request.raw_notes}

Create a structured learning output with:
1. A short summary in plain language.
2. Key concepts with brief explanations.
3. Common misunderstandings or mistakes learners may have.
4. Reflection questions that make the learner connect the topic to decisions, behavior, or real situations.
5. A mini practice activity the learner can complete in 5-10 minutes.
6. A final takeaway that is memorable and practical.

Style rules:
- Write for a learner, not for an expert.
- Keep it practical and eLearning-friendly.
- If the preferred style is "exam revision", emphasize recall and test preparation.
- If the preferred style is "workplace application", emphasize real job scenarios.
- If the preferred style is "reflection-based learning", emphasize personal insight and deeper thinking.
- If the preferred style is "summary", keep the output balanced and concise.
- Do not invent facts that contradict the notes.
"""


async def generate_lesson_summary(request: LessonRequest) -> LessonCoachResponse:
    client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = await client.responses.parse(
        model="gpt-4o-mini",
        input=[
            {
                "role": "system",
                "content": "You are a helpful eLearning content coach who creates structured study material.",
            },
            {
                "role": "user",
                "content": build_lesson_prompt(request),
            },
        ],
        text_format=LessonCoachResponse,
    )

    return response.output_parsed


@app.get("/")
async def root():
    return {"message": "AI Lesson Summary and Reflection Coach backend is running"}


@app.post("/lesson-summary", response_model=LessonCoachResponse)
async def lesson_summary(request: LessonRequest):
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(
            status_code=500,
            detail="OPENAI_API_KEY is missing. Add it to your .env file on the backend.",
        )

    try:
        return await generate_lesson_summary(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
