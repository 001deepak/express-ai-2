import os
import asyncio
from dotenv import load_dotenv

from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineTask, PipelineParams
from pipecat.services.sarvam import SarvamSTTService
from pipecat.services.openai import OpenAILLMService
from pipecat.services.cartesia import CartesiaTTSService

load_dotenv()

async def main():
    # 1. The Brain (OpenAI LLM)
    llm = OpenAILLMService(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4o-mini"
    )

    # 2. Speech-to-Text (Sarvam AI for Indian languages/accents)
    stt = SarvamSTTService(
        api_key=os.getenv("SARVAM_API_KEY")
    )

    # 3. Text-to-Speech (Cartesia for ultra-low latency voice)
    tts = CartesiaTTSService(
        api_key=os.getenv("CARTESIA_API_KEY"),
        voice_id="79a125e8-cd45-4c13-8a67-188112f4dd22" # Default natural voice ID
    )

    # 4. Pipeline execution loop
    pipeline = Pipeline([stt, llm, tts])
    task = PipelineTask(pipeline, PipelineParams(allow_interruptions=True))
    runner = PipelineRunner()
    await runner.run(task)

if _name_ == "_main_":
    asyncio.run(main())
