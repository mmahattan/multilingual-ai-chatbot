from fastapi import FastAPI, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from agent.agent_core import KTBClientZeroAgent
from dotenv import load_dotenv
import tempfile
import os
import whisper

load_dotenv()

app   = FastAPI(title="KTB Client Zero Agent")
agent = KTBClientZeroAgent()

# Preload Whisper model once at startup
print("Loading Whisper model...")
whisper_model = whisper.load_model("medium")
print("Whisper model loaded and ready!")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/agent/text")
async def text_input(text: str = Form(...), language: str = Form("en")):
    return agent.run(text=text, language=language)

@app.post("/agent/voice")
async def voice_input(file: UploadFile = File(...), language: str = Form("en")):
    tmp_path = None
    try:
        audio_data = await file.read()
        tmp_fd, tmp_path = tempfile.mkstemp(suffix=".wav")
        os.close(tmp_fd)
        with open(tmp_path, "wb") as f:
            f.write(audio_data)

        # Use preloaded model — no reload needed
        detect_result = whisper_model.transcribe(tmp_path, task="transcribe")
        detected_lang = detect_result["language"]
        original_text = detect_result["text"].strip()

        if detected_lang == "th":
            translate_result = whisper_model.transcribe(tmp_path, task="translate")
            english_text = translate_result["text"].strip()
        else:
            english_text = original_text

        result = agent.run(text=english_text, language=detected_lang)
        result["original_text"] = original_text
        result["english_query"] = english_text

        return result

    except Exception as e:
        return {"error": "Transcription failed: " + str(e)}

    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)

@app.get("/agent/history")
async def get_history():
    return {"history": [vars(e) for e in agent.memory.history]}

@app.post("/agent/reset")
async def reset():
    agent.memory.clear()
    return {"status": "Memory cleared"}