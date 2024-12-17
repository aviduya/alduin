from .todoist_client import get_inbox_tasks, update_task_label, get_project_ids
from .openai_client import get_task_label

def convert_proj_id(label, data):
    for key, value in data.items():
        if value.strip() == label.strip():
            return key
    print(f"Value '{label}' not found in dictionary.")
    return None

def process_tasks():
    projects = get_project_ids()
    inbox_id = convert_proj_id('Inbox', projects)
    tasks = get_inbox_tasks(inbox_id)

    for task in tasks:
        task_content = task.content
        task_id = task.id

        if not task_content or not task_id:
            continue

        label = get_task_label(task_content, project_ids=list(projects.values()))
        if not label:
            print(f"No label found for task '{task_content}'.")
            continue

        project_id = convert_proj_id(label, projects)
        if not project_id:
            print(f"Cannot update task '{task_id}' as project ID could not be found for label '{label}'.")
            continue

        is_updated = update_task_label(task_id, id=project_id)
        if is_updated:
            print(f"Updated task '{task_id}' with project ID '{project_id}'.")
        else:
            print("Something went wrong")


if __name__ == "__main__":
    process_tasks()
