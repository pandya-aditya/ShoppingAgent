import uuid
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agent import root_agent
import pandas as pd

df = pd.read_json('data.json')

DATASET = df.to_dict(orient='records')
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   
    allow_methods=["*"],
    allow_headers=["*"],
)

APP_NAME = "CategorizationQueryingApp"
USER_ID = "test_user"


session_service = InMemorySessionService()

SESSION_ID = str(uuid.uuid4())

initial_state = {"data": DATASET}

session_service.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
    state=initial_state,
)

runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service,
)


class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
async def chat_endpoint(payload: ChatRequest):
    user_text = payload.message

    new_message = types.Content(
        role="user",
        parts=[types.Part(text=user_text)]
    )

    for event in runner.run(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=new_message,
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_text = event.content.parts[0].text
    return final_text
