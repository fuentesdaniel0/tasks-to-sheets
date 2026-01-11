# Google Tasks to Google Sheet Synchronizer

This script synchronizes tasks from Google Tasks to a Google Sheet. It identifies and appends only new tasks to prevent duplicates. For each run that adds tasks, it records a timestamp, a list of added tasks, and an AI-generated summary to a "History" tab in the same sheet.

## Features

*   **Avoids Duplicates**: Checks for existing task IDs in the sheet to prevent adding the same task more than once.
*   **History Tracking**: Appends a record of each script run that adds new tasks to a "History" tab.
*   **AI Summaries**: Uses the Gemini API to generate a concise summary of the tasks that were added in each run.
*   **Easy Authentication**: Uses OAuth 2.0 for secure authentication with Google APIs and stores credentials for future runs.

## Prerequisites

*   Python 3.7+
*   A Google Cloud Platform project with the following APIs enabled:
    *   Google Tasks API
    *   Google Sheets API
    *   Generative Language API (for Gemini)
*   OAuth 2.0 `credentials.json` file from your Google Cloud project.

## Setup and Usage

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```
2.  **Install dependencies** (virtual environment recommended):
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure Environment:**
    *   Follow the Google Cloud documentation to enable the APIs listed in the prerequisites.
    *   Create OAuth 2.0 credentials for a "Desktop app" and save the downloaded file as `credentials.json` in the project root.
    *   Create a Google Sheet with two tabs: `Tasks` (columns: `List ID`, `List Title`, `Task ID`, `Task Title`) and `History` (columns: `Timestamp`, `Added Tasks`, `AI Summary`).
    *   Create a `.env` file in the root directory and add your Google Sheet ID:
    ```
    SHEET_ID="your_google_sheet_id_here"
    ```
4.  **Run the script:**
    ```bash
    python main.py
    ```
    *   On the first run, you will be prompted to authorize the application in your browser. This creates a `token.json` file to automate authentication for subsequent runs.
    *   The script will print the number of new tasks added or a message if there are no new tasks.