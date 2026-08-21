import os
import asyncio
from dotenv import load_dotenv

from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineTask, PipelineParams
from pipecat.services.sarvam.stt import SarvamSTTService
from pipecat.services.sarvam.tts import SarvamTTSService
from pipecat.services.openai import OpenAILLMService

load_dotenv()

async def main():
    # 1. The Brain (OpenAI LLM)
    llm = OpenAILLMService(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4o-mini"
    )

    # 2. Speech-to-Text (Sarvam AI for Indian languages/accents)
    stt = SarvamSTTService(
        api_key=os.getenv("SARVAM_API_KEY"),
        language="hi-IN",
        model="saaras:v3"
    )

    # 3. Text-to-Speech (Sarvam AI Bulbul voices)
    tts = SarvamTTSService(
        api_key=os.getenv("SARVAM_API_KEY"),
        model="bulbul:v2"
    )

    # 4. Pipeline execution loop
    pipeline = Pipeline([stt, llm, tts])
    task = PipelineTask(pipeline, PipelineParams(allow_interruptions=True))
    runner = PipelineRunner()
    await runner.run(task)

if _name_ == "_main_":
    asyncio.run(main())
