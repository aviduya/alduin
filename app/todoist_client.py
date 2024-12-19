import logging
import re
import uuid
import requests
import json
import os
from dotenv import load_dotenv
from todoist_api_python.api import TodoistAPI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
logger.info("Environment variables loaded.")

# Initialize API
TODOIST_API_KEY = os.getenv("TODOIST_API_KEY")
if not TODOIST_API_KEY:
    logger.critical("TODOIST_API_KEY not found in environment variables. Exiting.")
    raise EnvironmentError("TODOIST_API_KEY is missing. Check your .env file.")
API = TodoistAPI(f"{TODOIST_API_KEY}")
TODOIST_SYNC_URL = "https://api.todoist.com/sync/v9/sync"
RE_EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)

# Helper function to strip emojis
def _strip_emoji(text):
    return RE_EMOJI.sub(r'', text)

# Function to get tasks in the inbox
def get_inbox_tasks(inbox_proj_id):
    logger.debug("get_inbox_tasks called with inbox_proj_id: %s", inbox_proj_id)
    inbox_tasks = []
    try:
        tasks = API.get_tasks()
        for x in tasks:
            if x.project_id == str(inbox_proj_id):
                inbox_tasks.append(x)
        logger.info("Retrieved %d tasks for inbox project ID %s", len(inbox_tasks), inbox_proj_id)
        return inbox_tasks
    except Exception as error:
        logger.error("Failed to retrieve inbox tasks: %s", error, exc_info=True)
        return []

# Function to retrieve project IDs
def get_project_ids():
    logger.info("get_project_ids called to fetch Todoist project IDs.")
    project_ids = {}
    try:
        projects = API.get_projects()
        for project in projects:
            stripped_name = _strip_emoji(project.name)
            project_ids[project.id] = stripped_name
        logger.info("Successfully retrieved %d projects.", len(project_ids))
        return project_ids
    except Exception as error:
        logger.error("Failed to retrieve project IDs: %s", error, exc_info=True)
        return {}

# Function to update task label by moving it to another project
def update_task_label(task_id, project_id):
    logger.info("update_task_label called with task_id: %s and project_id: %s", task_id, project_id)
    try:
        command_uuid = str(uuid.uuid4())
        commands = [
            {
                "type": "item_move",
                "uuid": command_uuid,
                "args": {
                    "id": task_id,
                    "project_id": project_id
                }
            }
        ]

        response = requests.post(
            TODOIST_SYNC_URL,
            headers={"Authorization": f"Bearer {TODOIST_API_KEY}"},
            data={"commands": json.dumps(commands)}
        )

        response_data = response.json()
        sync_status = response_data.get("sync_status", {}).get(command_uuid)

        if sync_status == "ok":
            logger.info("Task %s successfully moved to project %s.", task_id, project_id)
            return True
        else:
            logger.warning("Failed to move task %s. Sync status: %s", task_id, sync_status)
            return False
    except Exception as error:
        logger.error("Error moving task %s: %s", task_id, error, exc_info=True)
        return False

if __name__ == "__main__":
    logger.info("Starting the script...")
    try:
        project_ids = get_project_ids()
        logger.debug("Project IDs: %s", project_ids)
    except Exception as e:
        logger.critical("An unexpected error occurred during script execution: %s", e, exc_info=True)
