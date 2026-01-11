"""
This script retrieves tasks from Google Tasks and appends them to a Google Sheet.

It authenticates with the Google API, fetches all task lists and their tasks,
formats the data, and then appends it to the specified spreadsheet.
"""

import sys
import os.path
from datetime import datetime
from dotenv import load_dotenv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google import genai
from google.genai.types import HttpOptions

load_dotenv()

# Define the scopes required for Google Tasks and Google Sheets APIs.
SCOPES = [
    'https://www.googleapis.com/auth/tasks',
    'https://www.googleapis.com/auth/tasks.readonly',
    'https://www.googleapis.com/auth/spreadsheets'
]


def get_existing_task_ids(creds, sheet_id):
    """
    Reads the existing task IDs from the spreadsheet.

    Args:
        creds: Google API credentials.
        sheet_id: The ID of the Google Sheet.

    Returns:
        A set of existing task IDs.
    """
    sheets_service = build("sheets", "v4", credentials=creds)
    # Read the C column (task IDs)
    result = sheets_service.spreadsheets().values().get(
        spreadsheetId=sheet_id,
        range="C:C"
    ).execute()
    values = result.get('values', [])
    return set(v[0] for v in values if v)


def add_to_history(creds, sheet_id, changed_tasks):
    """
    Appends the change history to the "History" tab in the Google Sheet.

    Args:
        creds: Google API credentials.
        sheet_id: The ID of the Google Sheet.
        changed_tasks: A list of tasks that have been changed.
    """
    sheets_service = build("sheets", "v4", credentials=creds)
    gemini_client = genai.Client(http_options=HttpOptions(api_version="v1"))

    # Generate AI summary
    prompt = f"Summarize the following changes in a single sentence: {changed_tasks}"
    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
        )
    ai_summary = response.text

    # Prepare row for History tab
    history_row = [
        str(datetime.now()),
        ", ".join([task[3] for task in changed_tasks]),
        ai_summary
    ]

    body = {"values": [history_row]}
    result = (
        sheets_service.spreadsheets()
        .values()
        .append(
            spreadsheetId=sheet_id,
            range="History!A2",
            valueInputOption="RAW",
            body=body,
        )
        .execute()
    )
    print(f"{result.get('updates').get('updatedCells')} cells appended to History.")
    return result


def main():
    """
    Main function to fetch tasks and append them to a Google Sheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    tasks_service = build("tasks", "v1", credentials=creds)

    # Get all task lists
    lists = tasks_service.tasklists().list().execute()['items']

    # Get all tasks for each task list
    task_lists = [
        {
            'id': list['id'],
            'title': list['title'],
            'items': tasks_service.tasks().list(tasklist=list['id']).execute()
        }
        for list in lists
    ]

    sheets_service = build("sheets", "v4", credentials=creds)
    sheet_id = os.getenv("SHEET_ID")
    
    existing_task_ids = get_existing_task_ids(creds, sheet_id)

    # Prepare rows for the spreadsheet
    new_tasks = []
    for task_list in task_lists:
        if 'items' in task_list['items'] and task_list['items']['items']:
            for task in task_list['items']['items']:
                if task['id'] not in existing_task_ids:
                    new_tasks.append([task_list['id'], task_list['title'], task['id'], task['title']])

    # Append rows to the spreadsheet if there are new tasks
    if new_tasks:
        body = {"values": new_tasks}
        result = (
            sheets_service.spreadsheets()
            .values()
            .append(
                spreadsheetId=sheet_id,
                range="A2",
                valueInputOption="RAW",
                body=body,
            )
            .execute()
        )
        print(f"{result.get('updates').get('updatedCells')} cells appended.")
        
        add_to_history(creds, sheet_id, new_tasks)
        
        return result
    else:
        print("No new tasks to add.")
        return 0



if __name__ == '__main__':
    sys.exit(main())