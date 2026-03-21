import sqlite3
import json
import os

DB_NAME = 'database.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS resumes (
            id TEXT PRIMARY KEY,
            name TEXT,
            email TEXT,
            phone TEXT,
            address TEXT,
            education TEXT,
            experience TEXT,
            skills TEXT,
            projects TEXT,
            template TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_resume(resume_id, data):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    education = json.dumps(data.get('education', []))
    experience = json.dumps(data.get('experience', []))
    skills = json.dumps(data.get('skills', []))
    projects = json.dumps(data.get('projects', []))
    
    c.execute('''
        INSERT OR REPLACE INTO resumes 
        (id, name, email, phone, address, education, experience, skills, projects, template)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        resume_id,
        data.get('name', ''),
        data.get('email', ''),
        data.get('phone', ''),
        data.get('address', ''),
        education,
        experience,
        skills,
        projects,
        data.get('template', 'simple')
    ))
    conn.commit()
    conn.close()

def get_resume(resume_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM resumes WHERE id = ?', (resume_id,))
    row = c.fetchone()
    conn.close()
    
    if row:
        return {
            'id': row[0],
            'name': row[1],
            'email': row[2],
            'phone': row[3],
            'address': row[4],
            'education': json.loads(row[5]),
            'experience': json.loads(row[6]),
            'skills': json.loads(row[7]),
            'projects': json.loads(row[8]),
            'template': row[9]
        }
    return None

def update_resume_template(resume_id, template_name):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('UPDATE resumes SET template = ? WHERE id = ?', (template_name, resume_id))
    conn.commit()
    conn.close()
