from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

OPEN_AI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=f"{OPEN_AI_API_KEY}")

def get_task_label(task_content, project_ids):
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
        print(f"Task: '{task_content}' -> Label: '{label}'")
        return label
    except Exception as e:
        print(f"Error with OpenAI API: {e}")


if __name__ == "__main__":
    project = {'2345107997': 'Inbox', '2345108005': 'My work ', '2345108006': 'Home ', '2345116827': 'Personal ', '2345122373': "Philippines & Japan Trip 25' ", '2345150791': 'Finances', '2345150947': 'Shopping & Groceries'}
    get_task_label("Clean and cook in the backyard", project_ids=project)
