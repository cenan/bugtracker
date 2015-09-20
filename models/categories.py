from config import db


def get_category(id):
    try:
        return db.select('category', where='id=$id', vars=locals())[0]
    except IndexError:
        return None

def get_categories(project_id):
    return db.select('category', where='id>0 AND project_id=$project_id', vars=locals()).list()

def insert_category(project_id, category_name, default_assignee_id):
    db.insert('category', project_id=project_id, category_name=category_name, default_assignee_id=default_assignee_id)

def update_category(id, category_name, default_assignee_id):
    db.update('category', where='id=$id', vars=locals(), category_name=category_name, default_assignee_id=default_assignee_id)

def delete_category(id):
    db.delete('category', where='id=$id', vars=locals())

