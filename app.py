import io
import os
from flask import Flask, render_template,request
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv() #loads all env vars defined in '.env' into 'os.environ'
client= OpenAI(api_key = os.environ['OPENAI_API_KEY'])

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template("index.html")
    
    @app.route("/transcribe", methods=["POST"])
    def transcribe():
        file =request.files["audio"]

        #convert file into a format that OpenAI can read
        buffer = io.BytesIO(file.read())
        buffer.name = "audio.webm"

        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=buffer
        )

        return {"output":transcript.text}
    
    return app
