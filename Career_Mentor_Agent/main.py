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
    model="deepseek/deepseek-r1-0528-qwen3-8b:fgree",
    openai_client=external_client
)

# Configuration for the Runner
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

#  MULTIPLE AGENTS
CareerAgent = Agent(
    name="Career Advisor",
    instructions="You suggest possible career fields based on user's interests and strengths. Keep answers short, clear, and relevant (max 3 sentences).",
    model=model
)

SkillAgent = Agent(
    name="Skill Builder",
    instructions="You provide skill-building plans, resources, and step-by-step learning paths. Keep the answer short and to the point (max 5 bullet points).",
    model=model
)

JobAgent = Agent(
    name="Job Guide",
    instructions="You share real-world job roles, responsibilities, and industry demand insights. Give only 3 main roles with 1-line descriptions.",
    model=model
)


# RUN PROMPTS
# Step 1: Ask CareerAgent
career_result = Runner.run_sync(
    CareerAgent,
    input="I am interested in technology and problem solving. Suggest me a career field.",
    run_config=config
)
print("\n[CareerAgent]")
print(career_result.final_output)

# Step 2: Ask SkillAgent
skill_result = Runner.run_sync(
    SkillAgent,
    input="Suggest skill-building steps for becoming a software engineer.",
    run_config=config
)
print("\n[SkillAgent]")
print(skill_result.final_output)

# Step 3: Ask JobAgent
job_result = Runner.run_sync(
    JobAgent,
    input="What job roles are available for a software engineer and their responsibilities?",
    run_config=config
)
print("\n[JobAgent]")
print(job_result.final_output)


print("\nDesigned by Afroz Khan.")