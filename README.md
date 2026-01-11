# Google Tasks to Google Sheet Synchronizer

This project contains a Python script that synchronizes tasks from your Google Tasks account to a specified Google Sheet. It is designed to be run periodically to keep the sheet updated with new tasks.

The script fetches all tasks from all your task lists, identifies which tasks are not already in the spreadsheet, and appends them. It also maintains a log of all additions in a separate "History" tab, which includes a timestamp, the names of the tasks added, and an AI-generated summary of the changes.

## Features

*   **Fetches All Tasks**: Retrieves tasks from every task list in your Google Tasks.
*   **Avoids Duplicates**: Checks for existing task IDs in the sheet to prevent adding the same task more than once.
*   **History Tracking**: Appends a record of each script run that adds new tasks to a "History" tab.
*   **AI Summaries**: Uses the Gemini API to generate a concise summary of the tasks that were added in each run.
*   **Easy Authentication**: Uses OAuth 2.0 for secure authentication with Google APIs and stores credentials for future runs.

## Prerequisites

*   Python 3.7+
*   A Google Cloud Platform project with the following APIs enabled:
    *   Google Tasks API
    *   Google Sheets API
    *   Gemini API (or any other generative language model API you prefer)
*   OAuth 2.0 `credentials.json` file from your Google Cloud project.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Install dependencies:**
    It is recommended to use a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3.  **Configure Google APIs:**
    *   Follow the instructions in the [Google Cloud documentation](https://developers.google.com/workspace/guides/create-project) to create a project and enable the Google Tasks and Google Sheets APIs.
    *   Create OAuth 2.0 credentials for a "Desktop app" and download the `credentials.json` file. Place this file in the root directory of the project.

4.  **Set up Google Sheet:**
    *   Create a new Google Sheet.
    *   Create two tabs: one for the tasks (e.g., "Tasks") and another named "History".
    *   The main tasks tab should have columns for: `List ID`, `List Title`, `Task ID`, `Task Title`.
    *   The "History" tab should have columns for: `Timestamp`, `Added Tasks`, `AI Summary`.

5.  **Create `.env` file:**
    Create a `.env` file in the root directory and add the ID of your Google Sheet:
    ```
    SHEET_ID="your_google_sheet_id_here"
    ```

## Running the Script

1.  **First Run (Authentication):**
    The first time you run the script, it will open a new tab in your web browser for you to authorize access to your Google account.
    ```bash
    python main.py
    ```
    After you grant permission, a `token.json` file will be created in the project directory. This file stores your authorization tokens so you won't have to log in every time.

2.  **Subsequent Runs:**
    For all subsequent executions, the script will use the `token.json` file to authenticate automatically.
    ```bash
    python main.py
    ```
    The script will print the number of new tasks added or a message indicating that there were no new tasks.

## How it Works

1.  **Authentication**: The script authenticates with Google APIs using `credentials.json` and `token.json`.
2.  **Fetch Existing Tasks**: It reads the "Task ID" column from your Google Sheet to get a list of tasks already present.
3.  **Fetch Google Tasks**: It connects to the Google Tasks API and retrieves all tasks from all your lists.
4.  **Compare and Append**: It compares the fetched tasks with the existing ones and appends only the new tasks to your sheet.
5.  **Log History**: If new tasks were added, it creates a history entry with the current time, the names of the new tasks, and an AI-generated summary, and appends this to the "History" tab.