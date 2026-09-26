from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI(title="Smart Bug Tracker API")


class Bug(BaseModel):
    title: str
    description: str
    severity: str
    category: str
    status: str


def get_connection():
    return sqlite3.connect("bugs.db")


@app.get("/")
def home():
    return {"message": "Smart Bug Tracker API is running"}


@app.get("/bugs")
def get_bugs():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM bugs")
    bugs = cursor.fetchall()

    conn.close()

    return [
        {
            "id": bug[0],
            "title": bug[1],
            "description": bug[2],
            "severity": bug[3],
            "category": bug[4],
            "status": bug[5]
        }
        for bug in bugs
    ]


@app.get("/bugs/{bug_id}")
def get_bug(bug_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM bugs WHERE id = ?",
        (bug_id,)
    )

    bug = cursor.fetchone()
    conn.close()

    if bug is None:
        return {"message": "Bug not found"}

    return {
        "id": bug[0],
        "title": bug[1],
        "description": bug[2],
        "severity": bug[3],
        "category": bug[4],
        "status": bug[5]
    }


@app.post("/bugs")
def create_bug(bug: Bug):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO bugs
        (title, description, severity, category, status)
        VALUES (?, ?, ?, ?, ?)
    """, (
        bug.title,
        bug.description,
        bug.severity,
        bug.category,
        bug.status
    ))

    conn.commit()

    bug_id = cursor.lastrowid

    conn.close()

    return {
        "message": "Bug created successfully",
        "id": bug_id
    }


@app.put("/bugs/{bug_id}")
def update_bug(bug_id: int, bug: Bug):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE bugs
        SET title = ?,
            description = ?,
            severity = ?,
            category = ?,
            status = ?
        WHERE id = ?
    """, (
        bug.title,
        bug.description,
        bug.severity,
        bug.category,
        bug.status,
        bug_id
    ))

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return {"message": "Bug not found"}

    conn.close()

    return {"message": "Bug updated successfully"}


@app.delete("/bugs/{bug_id}")
def delete_bug(bug_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM bugs WHERE id = ?",
        (bug_id,)
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return {"message": "Bug not found"}

    conn.close()

    return {"message": "Bug deleted successfully"}
