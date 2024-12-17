from todoist_api_python.api import TodoistAPI
import re
import uuid
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

TODOIST_API_KEY = os.getenv("TODOIST_API_KEY")
API = TodoistAPI(f"{TODOIST_API_KEY}")
TODOIST_SYNC_URL = "https://api.todoist.com/sync/v9/sync"
RE_EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)

def _strip_emoji(text):
    return RE_EMOJI.sub(r'', text)

def get_inbox_tasks(inbox_proj_id):
    inbox_task = []
    try:
        tasks = API.get_tasks()
        for x in tasks:
            print(f'project ID:{x.project_id}, Task: {x.content}, id: {x.id}')
            if x.project_id == str(inbox_proj_id):
                inbox_task.append(x)
        return inbox_task
    except Exception as error:
        print(error)


def get_project_ids():
    projects_ids = {}
    try:
        projects = API.get_projects()
        for project in projects:
            stripped_name =_strip_emoji(project.name)
            print(f'Project Name: {stripped_name} - {project.id}')
            projects_ids[project.id] =_strip_emoji(stripped_name)

        print(projects_ids)
        return projects_ids
    except Exception as error:
        print(error)

def update_task_label(task_id, id):
    try:
        command_uuid = str(uuid.uuid4())
        commands = [
            {
                "type": "item_move",
                "uuid": command_uuid,
                "args": {
                    "id": task_id,
                    "project_id": id
                }
            }
        ]

        response = requests.post(
            TODOIST_SYNC_URL,
            headers={
                "Authorization": f"Bearer {TODOIST_API_KEY}"
            },
            data={
                "commands": json.dumps(commands)
            }
        )

        response_data = response.json()
        print(response_data)
        sync_status = response_data.get("sync_status", {}).get(command_uuid)

        if sync_status == "ok":
            print(f"Task {task_id} successfully moved to project {id}.")
            return True
        else:
            print(f"Failed to move task. Sync status: {sync_status}")
            return False
    except Exception as error:
        print(f"Error moving task: {error}")
        return False



if __name__ == "__main__":
    get_project_ids()
