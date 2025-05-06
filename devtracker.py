
import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = "devtracker.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS tech (
                        id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE,
                        progress INTEGER DEFAULT 0
                    )''')
        c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY,
                        tech_id INTEGER,
                        description TEXT,
                        done BOOLEAN DEFAULT 0,
                        FOREIGN KEY (tech_id) REFERENCES tech(id)
                    )''')

def add_tech(name):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        try:
            c.execute("INSERT INTO tech (name) VALUES (?)", (name,))
            conn.commit()
            print(f"✓ Технология '{name}' добавлена.")
        except sqlite3.IntegrityError:
            print("⚠️ Уже существует.")

def list_tech():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT id, name, progress FROM tech")
        rows = c.fetchall()
        for row in rows:
            print(f"[{row[0]}] {row[1]} - {row[2]}%")

def add_task(tech_id, description):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO tasks (tech_id, description) VALUES (?, ?)", (tech_id, description))
        conn.commit()
        print("✓ Задача добавлена.")

def list_tasks(tech_id):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT id, description, done FROM tasks WHERE tech_id = ?", (tech_id,))
        rows = c.fetchall()
        for row in rows:
            status = "✅" if row[2] else "❌"
            print(f"[{row[0]}] {status} {row[1]}")

def complete_task(task_id):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
        conn.commit()
        print("✓ Выполнено.")

def calculate_progress():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT id FROM tech")
        techs = c.fetchall()
        for tech in techs:
            tech_id = tech[0]
            c.execute("SELECT COUNT(*) FROM tasks WHERE tech_id = ?", (tech_id,))
            total = c.fetchone()[0]
            c.execute("SELECT COUNT(*) FROM tasks WHERE tech_id = ? AND done = 1", (tech_id,))
            done = c.fetchone()[0]
            progress = int((done / total) * 100) if total else 0
            c.execute("UPDATE tech SET progress = ? WHERE id = ?", (progress, tech_id))
        conn.commit()

def main():
    init_db()
    while True:
        print("\n=== DevTracker ===")
        print("[1] Добавить технологию")
        print("[2] Показать технологии")
        print("[3] Добавить задачу")
        print("[4] Показать задачи по технологии")
        print("[5] Отметить задачу выполненной")
        print("[6] Обновить прогресс")
        print("[0] Выход")
        cmd = input("Выбор: ")

        if cmd == "1":
            name = input("Название технологии: ")
            add_tech(name)
        elif cmd == "2":
            list_tech()
        elif cmd == "3":
            tech_id = int(input("ID технологии: "))
            desc = input("Описание задачи: ")
            add_task(tech_id, desc)
        elif cmd == "4":
            tech_id = int(input("ID технологии: "))
            list_tasks(tech_id)
        elif cmd == "5":
            task_id = int(input("ID задачи: "))
            complete_task(task_id)
        elif cmd == "6":
            calculate_progress()
            print("✓ Прогресс обновлён.")
        elif cmd == "0":
            print("👋 Пока!")
            break
        else:
            print("Неверная команда.")

if __name__ == "__main__":
    main()
