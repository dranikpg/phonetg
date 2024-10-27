from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from telethon import TelegramClient
from pydantic import BaseModel
from dataclasses import dataclass
import asyncio

api_id = 27979506
api_hash = '2666f30330c0333d93c5eae2c67d67b3'

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
async def on_startup():
   global client
   client = TelegramClient('nokiabot0925', api_id, api_hash)
   await client.start()


@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    dialogs = await client.get_dialogs()
    return templates.TemplateResponse(
        name="main.html", context={"dialogs": dialogs, "request": request}
    )

@app.get("/chat/{chat_id}", response_class=HTMLResponse)
async def chat(request: Request, chat_id, max_id: int=None):
    dialog = await client.get_input_entity(int(chat_id))

    params = {"limit": 20}
    if max_id is not None:
        params["max_id"] = max_id
    messages = await client.get_messages(dialog, **params)

    min_id = 0
    if len(messages) > 1:
        min_id = min(*(m.id for m in messages)) - 1

    return templates.TemplateResponse(
        name="chat.html", context={
            "chat_id": chat_id,
            "messages": messages, 
            "request": request,
            "min_id": min_id
        }
    )

@dataclass
class MessageData:
    text: str = Form("text")

@app.post("/chat/{chat_id}")
async def send_message(request: Request, chat_id, message: MessageData = Depends()):
    dialog = await client.get_input_entity(int(chat_id))
    await client.send_message(dialog, message=message.text)
    
    return RedirectResponse(f"/chat/{chat_id}", status_code=303)