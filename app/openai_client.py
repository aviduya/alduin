import logging
import os
from dotenv import load_dotenv
from openai import OpenAI

# Configure the basic logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)
logger = logging.getLogger(__name__)  # Use a named logger

# Load environment variables
load_dotenv()
logger.info("Environment variables loaded.")

# Initialize OpenAI client
OPEN_AI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPEN_AI_API_KEY:
    logger.error("OPENAI_API_KEY not found in environment variables.")
    raise EnvironmentError("OPENAI_API_KEY is missing. Please check your .env file.")

client = OpenAI(api_key=f"{OPEN_AI_API_KEY}")
logger.info("OpenAI client initialized successfully.")

def get_task_label(task_content, project_ids):
    logger.debug("get_task_label called with task_content: %s and project_ids: %s", task_content, project_ids)
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a task categorization assistant."},
                {
                    "role": "user",
                    "content": f"Classify the following task into one of these categories. DO NOT ADD MORE CONTEXT OR WORDS OTHER THAN THESE CATEGORIES: {project_ids}, .\nTask: {task_content}\nCategory:"
                }
            ]
        )
        label = completion.choices[0].message.content
        logger.info("Task classified successfully. Task: '%s' -> Label: '%s'", task_content, label)
        return label
    except Exception as e:
        logger.error(f"Error occurred while classifying task with OpenAI API: {e}", exc_info=True)
        raise
