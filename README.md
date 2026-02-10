# Secret Santa Application

A robust Python application for automating Secret Santa assignments for your company or group.

## Features

-   **Constraints-Based Assignment**:
    -   **No Self-Assignment**: A participant is never assigned to themselves.
    -   **No Repeats**: (Optional) Ensures that participants are not assigned the same "Secret Child" as the previous year.
-   **CSV Support**: Reads employee data and previous year's assignments from CSV files.
-   **Validation**:
    -   Ensures input files are not empty.
    -   Requires more than 2 participants.
    -   Checks for duplicate email addresses to prevent logical errors.
-   **Robustness**: Uses a randomized retry mechanism (up to 100 attempts) to find a valid solution even in tight constraint scenarios.

## Setup

1.  **Prerequisites**: Ensure you have Python 3.x installed.
2.  **Files**: Clone or extract the project to your local machine.

## How to Run

1.  Open your terminal or command prompt.
2.  Navigate to the project directory:
    ```bash
    cd "path/to/your/secret-santa"
    ```
3.  Run the application:
    ```bash
    python main.py
    ```
4.  Follow the interactive prompts:
    -   enter the path to your **Employee List CSV**.
    -   (Optional) Enter the path to **Last Year's Assignment CSV**.
    -   Enter the desired filename for the **Output CSV** (defaults to `secret_santa_result.csv`).

## Input Formats

### 1. Employee List CSV
A CSV file containing the list of current participants.
**Required Columns:**
-   `Employee_Name`
-   `Employee_EmailID`

**Example:**
```csv
Employee_Name,Employee_EmailID
John Doe,john@example.com
Jane Smith,jane@example.com
...
```

### 2. Last Year's Assignments CSV (Optional)
A CSV file containing the historical data to prevent repeat assignments.
**Required Columns:**
-   `Employee_Name`
-   `Employee_EmailID` (The Giver)
-   `Secret_Child_Name`
-   `Secret_Child_EmailID` (The Receiver/Child)

**Example:**
```csv
Employee_Name,Employee_EmailID,Secret_Child_Name,Secret_Child_EmailID
John Doe,john@example.com,Jane Smith,jane@example.com
...
```

## Output Format

The application generates a CSV file with the new assignments.
**Columns:**
-   `Employee_Name`: The Secret Santa.
-   `Employee_EmailID`: The Secret Santa's email.
-   `Secret_Child_Name`: The assigned recipient.
-   `Secret_Child_EmailID`: The recipient's email.

## Error Handling

-   The application will alert you if input files are missing or malformed.
-   It will raise an error if duplicate emails are found in the employee list.
-   If no valid assignment exists (e.g., small groups with too many constraints), it will inform you after multiple retry attempts.
