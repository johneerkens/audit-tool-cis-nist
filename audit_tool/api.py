from __future__ import annotations
from fastapi import FastAPI
from pydantic import BaseModel
from audit_tool.core.dataset import load_controls
from audit_tool.core.scoring import summarize_assessment

app = FastAPI(title='Audit Tool API', version='0.1.0')


class AssessmentPayload(BaseModel):
    answers: dict[str, str]


@app.get('/health')
def health():
    return {'status': 'ok'}


@app.get('/controls')
def controls():
    return load_controls()


@app.post('/assess')
def assess(payload: AssessmentPayload):
    return summarize_assessment(load_controls(), {k: v.upper() for k, v in payload.answers.items()})
