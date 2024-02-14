import PySimpleGUI as sg
import mysql.connector

# Establish connection to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="codsoft@2024",
    database="to_do"  # Specify the database name
)
cursor = db.cursor()

# Create the table if it doesn't exist
#cursor.execute("CREATE TABLE IF NOT EXISTS data (id INT AUTO_INCREMENT PRIMARY KEY, date DATE, task VARCHAR(100))")

layout = [
    [sg.CalendarButton("Set Date", size=(10, 1)), sg.T("-- -- --", key="--DATE--")],
    [sg.T("Write Task", size=(10, 1)), sg.I(key="-TASK-", font=("None 15"), size=(32, 1))],
    [sg.Table(values=[], headings=["Number", "Date", "Task"], key="-TABLE-", enable_events=True, display_row_numbers=False, auto_size_columns=False,
              col_widths=[7, 9, 30], vertical_scroll_only=False, justification="left", font="None 15")],
    [sg.Button("ADD", key="-Add-", size=(10, 1), button_color="green"), sg.Button("DELETE", key="-DEL-", button_color="red"), sg.Button("SHOW TASKS"), sg.Button("EXIT")]
]

window = sg.Window("To-Do-App", layout, finalize=True)

tasks = []

# Function to insert task into the MySQL database
def insert_task(date, task):
    query = "INSERT INTO data (date, task) VALUES (%s, %s)"
    cursor.execute(query, (date, task))
    db.commit()

# Function to fetch tasks from MySQL database
def fetch_tasks():
    cursor.execute("SELECT * FROM data")
    return cursor.fetchall()

# Populate tasks list with existing tasks from the database
tasks = fetch_tasks()

counter = len(tasks) + 1

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == "EXIT":
        break
    elif event == "-Add-":
        date = window["--DATE--"].get().split()[0]
        task = values["-TASK-"]
        tasks.append([counter, date, task])
        insert_task(date, task)  # Insert task into the database
        window["-TABLE-"].update(values=tasks)
        window["-TASK-"].update("")
        counter += 1
    elif event == "-DEL-":
        if values["-TABLE-"]:
            index = values["-TABLE-"][0]
            task_id = tasks[index][0]  # Get the task ID from the selected row
            del tasks[index]
            window["-TABLE-"].update(values=tasks)
            # Delete the task from the database
            cursor.execute("DELETE FROM data WHERE id = %s", (task_id,))
            db.commit()
    elif event == "SHOW TASKS":
        tasks = fetch_tasks()  # Fetch tasks from the database
        window["-TABLE-"].update(values=tasks)

window.close()
