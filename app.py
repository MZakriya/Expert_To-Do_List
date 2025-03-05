import streamlit as st
import pandas as pd
from datetime import datetime
import random

# Set the page configuration
st.set_page_config(page_title="Expert To-Do List App", layout="centered", initial_sidebar_state="collapsed")

# Custom CSS for the app
st.markdown("""
    <style>
    .stButton button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        padding: 10px 24px;
        margin: 5px;
    }
    .stTextInput input {
        padding: 10px;
        border: 2px solid #ccc;
        font-size: 16px;
    }
    .css-12w0qpk {
        font-family: Arial, sans-serif;
        font-size: 20px;
        color: #333333;
    }
    .dark-mode {
        background-color: #1E1E1E;
        color: white;
    }
    .dark-mode .stTextInput input {
        background-color: #333333;
        color: white;
        border-color: #555555;
    }
    .dark-mode .stButton button {
        background-color: #555555;
        color: white;
    }
    .dark-mode .css-12w0qpk {
        color: white;
    }
    .toggle-dark-mode {
        position: fixed;
        top: 10px;
        right: 10px;
        z-index: 1000;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state for dark mode
if "dark_mode" not in st.session_state:
    st.session_state["dark_mode"] = False

# Function to toggle dark mode
def toggle_dark_mode():
    st.session_state["dark_mode"] = not st.session_state["dark_mode"]
    st.rerun()  # Force the app to rerender immediately

# Dark Mode Toggle Button (Top Right)
with st.container():
    col1, col2 = st.columns([10, 1])  # Create a column layout
    with col2:
        if st.button("🌞" if not st.session_state["dark_mode"] else "🌙", key="dark_mode_toggle"):
            toggle_dark_mode()

# Apply dark mode styles dynamically
if st.session_state["dark_mode"]:
    st.markdown(
        """
        <style>
        body {
            background-color: #1E1E1E;
            color: white;
        }
        .stTextInput input {
            background-color: #333333;
            color: white;
            border-color: #555555;
        }
        .stButton button {
            background-color: #555555;
            color: white;
        }
        .css-12w0qpk {
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Sidebar - About Section
with st.sidebar:
    st.title("About Expert To-Do List App 📝")
    st.write("""
    **Welcome to the Expert To-Do List App!**  
    This app is designed to help you organize your tasks efficiently and stay productive.  
    Here's what you can do:
    - Add new tasks with a description, category, priority, and due date.
    - Mark tasks as completed or delete them.
    - Edit tasks to update their details.
    - Filter tasks by status, category, or priority.
    - Track overdue and upcoming tasks with notifications.
    - Export your tasks to a CSV file.
    - Earn points for completing tasks and unlock milestones.
    - Get motivated with daily quotes and tips!

    **Why Use This App?**
    - Stay organized and focused on your goals.
    - Develop a growth mindset by tracking your progress.
    - Gamify your productivity and make task management fun!

    **Pro Tip:**  
    Use the dark mode toggle (🌞/🌙) at the top right for a comfortable viewing experience.
             
    Made with ❤️ by Muhammad Zakriya.  
    Feel free to reach out for feedback or suggestions!
    """)

# Title and intro text
st.title("📝 Expert To-Do List App")
st.write("Organize your tasks like a pro! Manage your daily to-do's with ease and style.")

# Initialize session state for storing tasks and history
if "tasks" not in st.session_state:
    st.session_state["tasks"] = []
if "task_history" not in st.session_state:
    st.session_state["task_history"] = []
if "points" not in st.session_state:
    st.session_state["points"] = 0
if "last_milestone" not in st.session_state:
    st.session_state["last_milestone"] = 0  # Track the last milestone reached

# Function to add task to the list
def add_task():
    task_description = st.session_state["new_task"]
    if task_description:
        task = {
            "task": task_description,
            "status": "Pending",
            "timestamp": datetime.now(),
            "category": st.session_state["task_category"],
            "priority": st.session_state["task_priority"],
            "due_date": st.session_state["task_due_date"]
        }
        st.session_state["tasks"].append(task)
        # Clear the input field after adding the task
        st.session_state["new_task"] = ""

# Function to mark a task as completed
def complete_task(index):
    task = st.session_state["tasks"][index]
    task["status"] = "Completed"
    st.session_state["task_history"].append(task)  # Add to task history
    st.session_state["points"] += 10  # Add points for completing a task
    st.session_state["tasks"].pop(index)

# Function to delete a task
def delete_task(index):
    task = st.session_state["tasks"][index]
    st.session_state["task_history"].append(task)  # Add to task history
    st.session_state["tasks"].pop(index)

# Function to delete a task from history
def delete_task_history(index):
    st.session_state["task_history"].pop(index)

# Function to edit a task
def edit_task(index, new_task, new_category, new_priority, new_due_date):
    st.session_state["tasks"][index]["task"] = new_task
    st.session_state["tasks"][index]["category"] = new_category
    st.session_state["tasks"][index]["priority"] = new_priority
    st.session_state["tasks"][index]["due_date"] = new_due_date

# Input for new tasks
st.text_input("Enter a new task:", key="new_task")
st.selectbox("Select Category", ["Work", "Personal", "Shopping", "Other"], key="task_category")
st.selectbox("Select Priority", ["High", "Medium", "Low"], key="task_priority")
st.date_input("Due Date", key="task_due_date")
st.button("Add Task", on_click=add_task)

# Display the to-do list in a DataFrame-style table
if st.session_state["tasks"]:
    df = pd.DataFrame(st.session_state["tasks"])
    df["Time Added"] = df["timestamp"].apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S"))
    df.drop("timestamp", axis=1, inplace=True)
    st.write("### Your To-Do List:")

    # Task filtering
    filter_status = st.selectbox("Filter by Status", ["All", "Pending", "Completed"])
    filter_category = st.selectbox("Filter by Category", ["All", "Work", "Personal", "Shopping", "Other"])
    filter_priority = st.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"])

    filtered_tasks = df.copy()
    if filter_status != "All":
        filtered_tasks = filtered_tasks[filtered_tasks["status"] == filter_status]
    if filter_category != "All":
        filtered_tasks = filtered_tasks[filtered_tasks["category"] == filter_category]
    if filter_priority != "All":
        filtered_tasks = filtered_tasks[filtered_tasks["priority"] == filter_priority]

    st.dataframe(filtered_tasks[["task", "status", "category", "priority", "due_date", "Time Added"]])

    # Buttons to mark tasks as completed, delete, or edit
    for index, task in enumerate(st.session_state["tasks"]):
        if task["status"] == "Pending":
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                if st.button(f"Mark as completed - {task['task']}", key=f"complete_{index}"):
                    complete_task(index)
                    st.rerun()  # Refresh the app to reflect changes
            with col2:
                if st.button(f"Delete - {task['task']}", key=f"delete_{index}"):
                    delete_task(index)
                    st.rerun()  # Refresh the app to reflect changes
            with col3:
                if st.button(f"Edit - {task['task']}", key=f"edit_{index}"):
                    st.session_state["edit_index"] = index  # Store the index of the task being edited

    # Edit Task Form
    if "edit_index" in st.session_state:
        index = st.session_state["edit_index"]
        task = st.session_state["tasks"][index]
        with st.form(key="edit_form"):
            st.write("### Edit Task")
            new_task = st.text_input("Task Description", value=task["task"])
            new_category = st.selectbox("Category", ["Work", "Personal", "Shopping", "Other"], index=["Work", "Personal", "Shopping", "Other"].index(task["category"]))
            new_priority = st.selectbox("Priority", ["High", "Medium", "Low"], index=["High", "Medium", "Low"].index(task["priority"]))
            new_due_date = st.date_input("Due Date", value=task["due_date"])
            if st.form_submit_button("Save Changes"):
                edit_task(index, new_task, new_category, new_priority, new_due_date)
                del st.session_state["edit_index"]  # Clear the edit index
                st.rerun()  # Refresh the app to reflect changes

# Task Notifications (Overdue and Upcoming Tasks)
st.write("### Notifications:")
today = datetime.now().date()
overdue_tasks = [task for task in st.session_state["tasks"] if task["due_date"] and task["due_date"] < today and task["status"] == "Pending"]
upcoming_tasks = [task for task in st.session_state["tasks"] if task["due_date"] and task["due_date"] >= today and task["status"] == "Pending"]

if overdue_tasks:
    st.warning("🚨 You have overdue tasks!")
    for task in overdue_tasks:
        st.write(f"- {task['task']} (Due: {task['due_date']})")
        st.toast(f"🚨 Overdue Task: {task['task']} (Due: {task['due_date']})", icon="⚠️")
else:
    st.success("🎉 No overdue tasks!")

if upcoming_tasks:
    st.info("📅 Upcoming tasks:")
    for task in upcoming_tasks:
        st.write(f"- {task['task']} (Due: {task['due_date']})")
        st.toast(f"📅 Upcoming Task: {task['task']} (Due: {task['due_date']})", icon="📅")

# Export Tasks to CSV
if st.button("Export Tasks to CSV"):
    df = pd.DataFrame(st.session_state["tasks"])
    df["Time Added"] = df["timestamp"].apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S"))  # Format timestamp
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="tasks.csv",
        mime="text/csv"
    )


# Task History
st.write("## Task History:")
if st.session_state["task_history"]:
    history_df = pd.DataFrame(st.session_state["task_history"])
    history_df["Time Added"] = history_df["timestamp"].apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S"))
    history_df.drop("timestamp", axis=1, inplace=True)

    # Display task history with delete buttons
    for index, task in enumerate(st.session_state["task_history"]):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"- **Task:** {task['task']} | **Status:** {task['status']} | **Category:** {task['category']} | **Priority:** {task['priority']} | **Due Date:** {task['due_date']}")
        with col2:
            if st.button(f"Delete", key=f"delete_history_{index}"):
                delete_task_history(index)
                st.rerun()  # Refresh the app to reflect changes
else:
    st.write("No tasks in history yet.")

# Gamification (Points System)
st.write("## Gamification:")
st.write(f"### Total Points: {st.session_state['points']}")

# Check for milestones and trigger animations
if st.session_state["points"] >= st.session_state["last_milestone"] + 100:
    st.session_state["last_milestone"] = st.session_state["points"]  # Update the last milestone
    st.balloons()  # Trigger animation
    st.success(f"🎉 Congratulations! You've earned {st.session_state['points']} points!")

# Motivational Quotes
st.write("## Motivational Quotes:")
quotes = [
    "The secret of getting ahead is getting started.",
    "You don't have to be great to start, but you have to start to be great.",
    "Do something today that your future self will thank you for."
]
st.write(f"**💡 Quote of the Day:** *{random.choice(quotes)}*")

# Summary Section
st.write("## Task Summary:")
pending_tasks = len([task for task in st.session_state["tasks"] if task["status"] == "Pending"])
completed_tasks = len([task for task in st.session_state["task_history"] if task["status"] == "Completed"])
st.write(f"### Total Tasks: {len(st.session_state['tasks']) + len(st.session_state['task_history'])}")
st.write(f"### Pending Tasks: {pending_tasks}")
st.write(f"### Completed Tasks: {completed_tasks}")

# Add a motivational quote at the bottom
st.write("---")
st.write("**💡 Pro Tip:** *Stay focused and complete your tasks one step at a time. You got this!**")

