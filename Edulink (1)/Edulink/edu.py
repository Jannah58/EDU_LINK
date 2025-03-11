from fastapi import FastAPI
from pydantic import BaseModel
from collections import Counter
from typing import List, Dict

app = FastAPI()

class QuestionResponse(BaseModel):
    questionid: int
    answer: List[str]  # Multiple answers per question allowed

# Answer mapping for all 15 questions
answer_mapping = {
    i+1: {"A": "A", "B": "V", "C": "R", "D": "K"} for i in range(15)
}

@app.post("/vark-result/")
async def calculate_vark(answers: List[QuestionResponse]) -> Dict[str, str]:
    score = Counter({"V": 0, "A": 0, "R": 0, "K": 0})

    for response in answers:
        if response.questionid in answer_mapping:
            for ans in response.answer:
                if ans in answer_mapping[response.questionid]:
                    score[answer_mapping[response.questionid][ans]] += 1

    max_score = max(score.values())
    dominant_styles = [key for key, val in score.items() if val == max_score]

    # Convert list to a comma-separated string (if multiple learning styles are tied)
    return {"category": ", ".join(dominant_styles)}


from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all frontend origins (change if needed)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
