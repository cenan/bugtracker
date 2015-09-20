import web

from config import db
from models import users
from models import categories


def get_projects():
    return db.select('project')


def get_issues(project_id, milestone_list=None, category_list=None, status=-1, offset=0, limit=1000):
    where = 'project_id=$project_id'
    if milestone_list is not None:
        where += ' and milestone_id in (%s)' % milestone_list
    if category_list is not None:
        where += ' and category_id in (%s)' % category_list
    if status != -1:
        where += ' and status = %d' % int(status)
    count = db.select('issue_view', where=where, vars=locals(), what='COUNT(*) AS count')[0].count
    issues = db.select('issue_view', where=where, vars=locals(), order='status, priority, milestone_id, id DESC', offset=offset, limit=limit).list()
    return issues, count

def get_issue(id):
    try:
        issue = db.select('issue_view', where='id=$id', vars=locals())[0]
        issue.opener = users.get_user(issue.opener_id)
        issue.assignee = users.get_user(issue.assignee_id)
        issue.attachments = get_issue_attachments(id)
        issue.category = categories.get_category(issue.category_id)
        return issue
    except IndexError:
        return None

def insert_issue(project_id, title, content, opener=0, category=0, assignee=0, priority=3, milestone=1):
    return db.insert('issue',
            status=0,
            project_id=project_id,
            title=title,
            content=content,
            opener_id=opener,
            category_id=category,
            assignee_id=assignee,
            priority=priority,
            milestone_id=milestone)

def delete_issue(id):
    db.delete('issue', where='id=$id', vars=locals())


def insert_issue_attachment(issue_id, filename):
    db.insert('issue_attachments', issue_id=issue_id, filename=filename)

def get_issue_attachments(issue_id):
    return db.select('issue_attachments', where='issue_id=$issue_id', vars=locals())

def get_issue_updates(issue_id):
    try:
        return db.select('issue_update_view', where='issue_id=$issue_id', vars=locals())
    except IndexError:
        return None

def update_issue(issue_id, content, status, priority, milestone_id, user_id, category, assignee):
    issue = db.select('issue', where='id=$issue_id', vars=locals())[0]
    db.update(
            'issue',
            where='id=$issue_id',
            vars=locals(),
            status=status,
            priority=priority,
            milestone_id=milestone_id,
            category_id=category,
            assignee_id=assignee)
    return db.insert(
            'issue_update',
            issue_id=issue_id,
            content=content,
            user_id=user_id,
            old_category=issue.category_id,
            new_category=category,
            old_assignee=issue.assignee_id,
            new_assignee=assignee,
            old_status=issue.status,
            new_status=status,
            old_priority=issue.priority,
            new_priority=priority,
            old_milestone=issue.milestone_id,
            new_milestone=milestone_id)

def edit_issue(issue_id, title, content):
	db.update('issue', where='id=$issue_id', vars=locals(), title=title, content=content)

