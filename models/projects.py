from config import db


def get_projects():
    return db.select('project')

def get_project(project_id):
    try:
        return db.select('project', where='id=$project_id', vars=locals())[0]
    except IndexError:
        return None

def create_project(project_name):
    return db.insert('project', project_name=project_name)

