from config import db

def get_milestones(project_id):
    return db.select('milestone', where='project_id=$project_id', vars=locals()).list()

def get_milestone(id):
    try:
        return db.select('milestone', where='id=$id', vars=locals())[0]
    except IndexError:
        return None

def insert_milestone(project_id, milestone_name):
    return db.insert('milestone', project_id=project_id, milestone_name=milestone_name)

def update_milestone(id, milestone_name, milestone_status):
    db.update('milestone', where='id=$id', vars=locals(), milestone_name=milestone_name, milestone_status=milestone_status)

def delete_milestone(id):
    db.delete('milestone', where='id=$id', vars=locals())

