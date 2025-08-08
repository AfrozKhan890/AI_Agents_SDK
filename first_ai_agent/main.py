import os
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Gemini API Key from .env
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
if not openrouter_api_key:
    raise ValueError("OPENROUTER_API_KEY is not set in the environment variables.")

# Initialize OpenAI Client with Gemini endpoint
external_client = AsyncOpenAI(
    api_key=openrouter_api_key,
    base_url="https://openrouter.ai/api/v1",   
)

# Setup Model
model = OpenAIChatCompletionsModel(
    model="deepseek/deepseek-r1-0528-qwen3-8b:free",
    openai_client=external_client
)

# Configuration for the Runner
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# Create Agent
agent = Agent(
    name="Website developer",
    instructions="You are a helpful developer assistant.you also provide code according to the situation.",
    model=model
)

# Run prompt 
result = Runner.run_sync(
    agent,
    input="I want to build a portfolio website using HTML,CSS and JS.",
    run_config=config
)

# Print output
print("Calling")
print(result.final_output)





