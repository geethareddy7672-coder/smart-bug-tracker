import streamlit as st
import sqlite3
import pandas as pd
# Sidebar
st.sidebar.title("🐞 Smart Bug Tracker")

st.sidebar.write(
    "A software bug tracking and analysis system "
    "built using Python, Streamlit, SQLite and FastAPI."
)

st.sidebar.divider()

st.sidebar.subheader("🛠️ Technology Stack")

st.sidebar.write("🐍 Python")
st.sidebar.write("🎨 Streamlit")
st.sidebar.write("🗄️ SQLite")
st.sidebar.write("⚡ FastAPI")
st.sidebar.write("📊 Pandas")

def analyze_bug(description):

    text = description.lower()

    # Category detection
    if any(word in text for word in [
        "login", "password", "authentication",
        "sign in", "logout", "account"
    ]):
        category = "Authentication"

    elif any(word in text for word in [
        "database", "sql", "query",
        "record", "data", "table"
    ]):
        category = "Database"

    elif any(word in text for word in [
        "slow", "lag", "performance",
        "loading", "response time", "timeout"
    ]):
        category = "Performance"

    elif any(word in text for word in [
        "security", "hack", "vulnerability",
        "attack", "unauthorized"
    ]):
        category = "Security"

    elif any(word in text for word in [
        "button", "screen", "display",
        "layout", "color", "font", "page"
    ]):
        category = "UI"

    else:
        category = "Other"

    # Severity detection
    if any(word in text for word in [
        "crash", "critical", "data loss",
        "system down", "cannot login"
    ]):
        severity = "Critical"

    elif any(word in text for word in [
        "error", "failure", "not working",
        "broken", "unable to"
    ]):
        severity = "High"

    elif any(word in text for word in [
        "slow", "delay", "sometimes",
        "minor performance"
    ]):
        severity = "Medium"

    else:
        severity = "Low"

    return category, severity
# Create database connection
conn = sqlite3.connect("bugs.db")
cursor = conn.cursor()

# Create bugs table
cursor.execute("""
CREATE TABLE IF NOT EXISTS bugs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    severity TEXT NOT NULL,
    category TEXT NOT NULL,
    status TEXT NOT NULL
)
""")

conn.commit()

# Page settings
st.set_page_config(
    page_title="Smart Bug Tracker",
    page_icon="🐞",
    layout="wide"
)

st.title("🐞 Smart Bug Tracker & Analyzer")

st.write("Report, track and analyze software bugs in one place.")

st.subheader("Create New Bug")

# Bug title
title = st.text_input("Bug Title")

# Bug description
description = st.text_area(
    "Bug Description",
    height=150
)

# Smart bug analysis
if description:
    suggested_category, suggested_severity = analyze_bug(description)

    st.info(
        f"🤖 Suggested Category: {suggested_category} | "
        f"Suggested Severity: {suggested_severity}"
    )

    category = suggested_category
    severity = suggested_severity

else:
    category = "Other"
    severity = "Low"
# Status
status = st.selectbox(
    "Status",
    ["Open", "In Progress", "Resolved"]
)

# Submit button
if st.button("Submit Bug"):

    if title and description:

        cursor.execute("""
        INSERT INTO bugs
        (title, description, severity, category, status)
        VALUES (?, ?, ?, ?, ?)
        """, (title, description, severity, category, status))

        conn.commit()

        st.success("Bug submitted successfully! 🐞")

    else:
        st.warning("Please enter the bug title and description.")

# Show stored bugs
st.subheader("Reported Bugs")

cursor.execute("SELECT * FROM bugs")
bugs = cursor.fetchall()

if bugs:
    for bug in bugs:
        st.write(
            f"**#{bug[0]} — {bug[1]}** | "
            f"Severity: {bug[3]} | "
            f"Category: {bug[4]} | "
            f"Status: {bug[5]}"
        )
else:
    st.info("No bugs reported yet.")
st.subheader("Search & Filter Bugs")

search = st.text_input("Search bugs")

filter_status = st.selectbox(
    "Filter by Status",
    ["All", "Open", "In Progress", "Resolved"]
)

cursor.execute("SELECT * FROM bugs")
all_bugs = cursor.fetchall()

filtered_bugs = []

for bug in all_bugs:

    matches_search = (
        search.lower() in bug[1].lower()
        or search.lower() in bug[2].lower()
    )

    matches_status = (
        filter_status == "All"
        or bug[5] == filter_status
    )

    if matches_search and matches_status:
        filtered_bugs.append(bug)

st.subheader("Filtered Results")

if filtered_bugs:

    for bug in filtered_bugs:
        st.write(
            f"**#{bug[0]} — {bug[1]}**  \n"
            f"Description: {bug[2]}  \n"
            f"Severity: {bug[3]} | "
            f"Category: {bug[4]} | "
            f"Status: {bug[5]}"
        )
        st.divider()

else:
    st.info("No matching bugs found.")

    st.subheader("📊 Bug Dashboard")

# Get total bugs
cursor.execute("SELECT COUNT(*) FROM bugs")
total_bugs = cursor.fetchone()[0]

# Count bugs by status
cursor.execute("SELECT COUNT(*) FROM bugs WHERE status = 'Open'")
open_bugs = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM bugs WHERE status = 'In Progress'")
in_progress = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM bugs WHERE status = 'Resolved'")
resolved_bugs = cursor.fetchone()[0]

# Display statistics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Bugs", total_bugs)

with col2:
    st.metric("Open", open_bugs)

with col3:
    st.metric("In Progress", in_progress)

with col4:
    st.metric("Resolved", resolved_bugs)

# Bug status chart
status_data = {
    "Status": ["Open", "In Progress", "Resolved"],
    "Count": [open_bugs, in_progress, resolved_bugs]
}

status_df = pd.DataFrame(status_data)

st.subheader("📈 Bugs by Status")

st.bar_chart(
    status_df.set_index("Status")
)
# Bug category chart
cursor.execute("""
SELECT category, COUNT(*)
FROM bugs
GROUP BY category
""")

category_data = cursor.fetchall()

category_df = pd.DataFrame(
    category_data,
    columns=["Category", "Count"]
)

st.subheader("📊 Bugs by Category")

st.bar_chart(
    category_df.set_index("Category")
)
# Bug severity chart
cursor.execute("""
SELECT severity, COUNT(*)
FROM bugs
GROUP BY severity
""")

severity_data = cursor.fetchall()

severity_df = pd.DataFrame(
    severity_data,
    columns=["Severity", "Count"]
)

st.subheader("🚨 Bugs by Severity")

st.bar_chart(
    severity_df.set_index("Severity")
)
st.subheader("🚨 Bugs by Severity")

st.bar_chart(
    severity_df.set_index("Severity")
)


# Manage Bugs
st.subheader("⚙️ Manage Bugs")

cursor.execute("SELECT * FROM bugs")
manage_bugs = cursor.fetchall()

if manage_bugs:

    for bug in manage_bugs:

        st.write(f"### Bug #{bug[0]} - {bug[1]}")

        st.write(f"Current Status: **{bug[5]}**")

        new_status = st.selectbox(
            "Change Status",
            ["Open", "In Progress", "Resolved"],
            index=["Open", "In Progress", "Resolved"].index(bug[5]),
            key=f"status_{bug[0]}"
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button(
                "✏️ Update Status",
                key=f"update_{bug[0]}"
            ):
                cursor.execute(
                    "UPDATE bugs SET status = ? WHERE id = ?",
                    (new_status, bug[0])
                )
                conn.commit()

                st.success("Status updated successfully! ✅")
                st.rerun()

        with col2:
            if st.button(
                "🗑️ Delete",
                key=f"delete_{bug[0]}"
            ):
                cursor.execute(
                    "DELETE FROM bugs WHERE id = ?",
                    (bug[0],)
                )
                conn.commit()

                st.success("Bug deleted successfully! 🗑️")
                st.rerun()

        st.divider()

else:
    st.info("No bugs available to manage.")
