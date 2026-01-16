"""
Database module for video generation tasks
"""
import sqlite3
import json
from datetime import datetime, timezone, timedelta
from typing import Optional
from config import DB_PATH

# UTC+8 timezone (东八区)
UTC_PLUS_8 = timezone(timedelta(hours=8))


def get_now_utc8() -> str:
    """Get current time in UTC+8 as ISO format string"""
    return datetime.now(UTC_PLUS_8).strftime("%Y-%m-%d %H:%M:%S")


def get_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database tables"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_key TEXT NOT NULL,
            model_name TEXT NOT NULL,
            prompt TEXT,
            image_path TEXT,
            params TEXT,
            status TEXT DEFAULT 'pending',
            task_id TEXT,
            result_urls TEXT,
            local_paths TEXT,
            error_msg TEXT,
            api_token TEXT,
            site TEXT DEFAULT 'mulerun',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create index for faster queries
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_status ON tasks(status)
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_created_at ON tasks(created_at DESC)
    """)

    # Migration: Add site column if it doesn't exist (for existing databases)
    try:
        cursor.execute("ALTER TABLE tasks ADD COLUMN site TEXT DEFAULT 'mulerun'")
        conn.commit()
    except sqlite3.OperationalError:
        # Column already exists
        pass

    # Create site index after ensuring column exists
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_site ON tasks(site)
    """)

    # Migration: Add local_paths column if it doesn't exist (for existing databases)
    try:
        cursor.execute("ALTER TABLE tasks ADD COLUMN local_paths TEXT")
        conn.commit()
    except sqlite3.OperationalError:
        # Column already exists
        pass

    conn.commit()
    conn.close()


def create_task(
    model_key: str,
    model_name: str,
    prompt: str,
    params: dict,
    image_path: Optional[str] = None,
    api_token: Optional[str] = None,
    site: str = "mulerun"
) -> int:
    """Create a new task record"""
    conn = get_connection()
    cursor = conn.cursor()
    now = get_now_utc8()

    cursor.execute("""
        INSERT INTO tasks (model_key, model_name, prompt, image_path, params, api_token, site, status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'pending', ?, ?)
    """, (model_key, model_name, prompt, image_path, json.dumps(params, ensure_ascii=False), api_token, site, now, now))

    task_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return task_id


def update_task_api_id(local_id: int, api_task_id: str):
    """Update task with API task ID after POST request"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tasks
        SET task_id = ?, status = 'processing', updated_at = ?
        WHERE id = ?
    """, (api_task_id, get_now_utc8(), local_id))

    conn.commit()
    conn.close()


def update_task_status(local_id: int, status: str, error_msg: Optional[str] = None):
    """Update task status"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tasks
        SET status = ?, error_msg = ?, updated_at = ?
        WHERE id = ?
    """, (status, error_msg, get_now_utc8(), local_id))

    conn.commit()
    conn.close()


def update_task_result(local_id: int, result_urls: list, local_paths: list = None):
    """Update task with result URLs and optional local paths"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tasks
        SET status = 'completed', result_urls = ?, local_paths = ?, updated_at = ?
        WHERE id = ?
    """, (json.dumps(result_urls), json.dumps(local_paths) if local_paths else None, get_now_utc8(), local_id))

    conn.commit()
    conn.close()


def update_task_local_paths(local_id: int, local_paths: list):
    """Update task with local file paths (for re-downloading)"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tasks
        SET local_paths = ?, updated_at = ?
        WHERE id = ?
    """, (json.dumps(local_paths), get_now_utc8(), local_id))

    conn.commit()
    conn.close()


def get_pending_tasks() -> list:
    """Get all tasks that need polling (processing status)"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM tasks
        WHERE status = 'processing' AND task_id IS NOT NULL
        ORDER BY created_at ASC
    """)

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_all_tasks(limit: int = 100, site: Optional[str] = None) -> list:
    """Get all tasks for display, optionally filtered by site"""
    conn = get_connection()
    cursor = conn.cursor()

    if site:
        cursor.execute("""
            SELECT * FROM tasks
            WHERE site = ?
            ORDER BY created_at DESC
            LIMIT ?
        """, (site, limit))
    else:
        cursor.execute("""
            SELECT * FROM tasks
            ORDER BY created_at DESC
            LIMIT ?
        """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_task_by_id(local_id: int) -> Optional[dict]:
    """Get a single task by ID"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks WHERE id = ?", (local_id,))
    row = cursor.fetchone()
    conn.close()

    return dict(row) if row else None


def get_task_by_uuid(task_uuid: str) -> Optional[dict]:
    """Get a single task by API task UUID"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks WHERE task_id = ?", (task_uuid,))
    row = cursor.fetchone()
    conn.close()

    return dict(row) if row else None


def delete_task(local_id: int):
    """Delete a task"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id = ?", (local_id,))

    conn.commit()
    conn.close()


def get_task_stats(site: Optional[str] = None) -> dict:
    """Get statistics about tasks, optionally filtered by site"""
    conn = get_connection()
    cursor = conn.cursor()

    if site:
        cursor.execute("""
            SELECT
                status,
                COUNT(*) as count
            FROM tasks
            WHERE site = ?
            GROUP BY status
        """, (site,))
    else:
        cursor.execute("""
            SELECT
                status,
                COUNT(*) as count
            FROM tasks
            GROUP BY status
        """)

    rows = cursor.fetchall()
    conn.close()

    stats = {
        "pending": 0,
        "processing": 0,
        "completed": 0,
        "failed": 0
    }

    for row in rows:
        stats[row["status"]] = row["count"]

    return stats


# Initialize database on module import
init_db()
