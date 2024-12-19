import logging
from .todoist_client import get_inbox_tasks, update_task_label, get_project_ids
from .openai_client import get_task_label

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Helper function to convert a project label to its ID
def convert_proj_id(label, data):
    logger.debug("convert_proj_id called with label: '%s'", label)
    for key, value in data.items():
        if value.strip() == label.strip():
            logger.info("Found project ID '%s' for label '%s'.", key, label)
            return key
    logger.warning("Value '%s' not found in project dictionary.", label)
    return None

# Main function to process tasks
def process_tasks():
    logger.info("Starting task processing...")

    # Fetch project IDs
    projects = get_project_ids()
    if not projects:
        logger.error("No projects found. Exiting task processing.")
        return

    # Get inbox project ID
    inbox_id = convert_proj_id('Inbox', projects)
    if not inbox_id:
        logger.error("Inbox project ID not found. Exiting task processing.")
        return

    # Fetch tasks in the inbox
    tasks = get_inbox_tasks(inbox_id)
    if not tasks:
        logger.info("No tasks found in the inbox.")
        return

    # Process each task
    for task in tasks:
        task_content = task.content
        task_id = task.id

        if not task_content or not task_id:
            logger.warning("Task content or ID is missing. Skipping task.")
            continue

        logger.debug("Processing task ID: '%s', Content: '%s'", task_id, task_content)

        # Get task label
        label = get_task_label(task_content, project_ids=list(projects.values()))
        if not label:
            logger.warning("No label found for task '%s'. Skipping task.", task_content)
            continue

        # Find project ID for the label
        project_id = convert_proj_id(label, projects)
        if not project_id:
            logger.warning(
                "Cannot update task '%s' as project ID could not be found for label '%s'.",
                task_id, label
            )
            continue

        # Update task label (move task to the corresponding project)
        is_updated = update_task_label(task_id, project_id=project_id)
        if is_updated:
            logger.info("Successfully updated task '%s' to project ID '%s'.", task_id, project_id)
        else:
            logger.error("Failed to update task '%s' to project ID '%s'.", task_id, project_id)

if __name__ == "__main__":
    logger.info("Starting the script...")
    try:
        process_tasks()
    except Exception as e:
        logger.critical("An unexpected error occurred: %s", e, exc_info=True)
