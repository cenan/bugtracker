import os
import web
import urlparse
import math

import config

from models import issues
from models import milestones
from models import users
from models import categories

from helpers.render import render
from helpers.session import login_required

class list:
    @login_required
    def GET(self, project_id):
        p = '1'
        filt_qs = ''
        qs = ''
        mil = None
        selected_milestones = []
        selected_categories = []

        milestone_list = milestones.get_milestones(project_id)
        category_list = categories.get_categories(project_id)

        query_string = dict(urlparse.parse_qsl(web.ctx.env['QUERY_STRING']))

        if "p" in query_string:
            p = query_string.get('p', '1')

        if "filter" in query_string:
            filt_qs = query_string.get("filter")
            query_string = dict(urlparse.parse_qsl(users.get_filter(filt_qs).filter))

        if "mil" in query_string:
            mil = query_string.get('mil', '')
            qs += "&mil="+mil
            selected_milestones = mil.split(",")
        else:
            mil = ",".join([str(m.id) for m in milestone_list if m.milestone_status == 0])
            selected_milestones = [str(m.id) for m in milestone_list if m.milestone_status == 0]

        if "cat" in query_string:
            cat = query_string.get('cat', '')
            cat = "0," + cat
            qs += "&cat="+cat
            selected_categories = cat.split(",")
        else:
            cat = ",".join([str(c.id) for c in category_list])
            cat = "0," + cat
            selected_categories = [str(c.id) for c in category_list]

        if "status" in query_string:
            status = query_string.get('status', '')
            qs += "&status="+status
        else:
            status = -1

        issue_list, issue_count = issues.get_issues(
                project_id=project_id,
                milestone_list=mil,
                category_list=cat,
                status=status,
                offset=(int(p)-1)*10,limit=10)
        page_count = int(math.ceil(issue_count / 10.0))
        if filt_qs != '':
            qs = filt_qs
        return render.issue.list(
                project_id=project_id,
                issue_count=issue_count,
                page_count=page_count,
                current_page=p,
                issues=issue_list,
                categories=category_list,
                selected_categories=selected_categories,
                milestones=milestone_list,
                selected_milestones=selected_milestones,
                status=status,
                qs=qs)

class create:
    @login_required
    def GET(self, project_id):
        milestone_list = milestones.get_milestones(project_id)
        user_list = users.get_users()
        category_list = categories.get_categories(project_id)
        return render.issue.create(project_id=project_id, milestones=milestone_list, users=user_list, categories=category_list)

    @login_required
    def POST(self, project_id):
        f = web.input(userfile={})
        id = issues.insert_issue(
                project_id=project_id,
                title=f.title,
                content=f.content,
                opener=web.ctx.session.user_id,
                category=f.category,
                assignee=f.assignee,
                priority=f.priority,
                milestone=f.milestone)
        if 'userfile' in f and f.userfile.filename != '':
            filepath = f.userfile.filename.replace('\\', '/')
            filename = filepath.split('/')[-1]
            fout = open(os.path.join(config.upload_dir,filename), 'w')
            fout.write(f.userfile.file.read())
            fout.close()
            issues.insert_issue_attachment(id, filename)
        raise web.seeother('/project/%s/issue/%d' % (project_id, id, ))

class show:
    @login_required
    def GET(self, project_id, id):
        issue = issues.get_issue(id)
        updates = issues.get_issue_updates(id)
        milestone_list = milestones.get_milestones(project_id)
        user_list = users.get_users()
        category_list = categories.get_categories(project_id)
        return render.issue.show(project_id=project_id, issue=issue, updates=updates, milestones=milestone_list, users=user_list, categories=category_list)

class delete:
    @login_required
    def GET(self, project_id, id):
        issues.delete_issue(id)
        raise web.seeother('/project/%s/issues' % project_id)

class update:
    @login_required
    def POST(self, project_id):
        f = web.input()
        issues.update_issue(
                issue_id=f.issue_id,
                content=f.content,
                status=f.status,
                priority=f.priority,
                milestone_id=f.milestone,
                user_id=web.ctx.session.user_id,
                category=f.category,
                assignee=f.assignee)
        raise web.seeother('/project/%s/issue/%s' % (project_id, f.issue_id, ))

class edit:
    @login_required
    def POST(self, project_id):
        f = web.input()
        issues.edit_issue(issue_id=f.issue_id, title=f.title, content=f.content)
        return "ok"

class search:
    @login_required
    def GET(self, project_id):
        p = '1'
        qs = ''
        mil = None
        selected_milestones = []
        milestone_list = milestones.get_milestones(project_id)
        query_string = dict(urlparse.parse_qsl(web.ctx.env['QUERY_STRING']))
        q = query_string.get("q", ".")
        if q[0] == '#':
            raise web.seeother('/project/%s/issue/%s' % (project_id, q[1:], ))
        if web.ctx.query.find("mil") != -1:
            mil = query_string.get('mil', '')
            qs = "&mil="+mil
            selected_milestones = mil.split(",")
        else:
            mil = ",".join([str(m.id) for m in milestone_list if m.milestone_status==0])
            selected_milestones = [str(m.id) for m in milestone_list if m.milestone_status==0 ]
        issue_list, issue_count = issues.get_issues(project_id=project_id, milestone_list=mil)
        page_count = int(math.ceil(issue_count / 10.0))
        category_list = categories.get_categories(project_id)
        return render.issue.list(project_id=project_id, issue_count=issue_count, page_count=page_count, current_page=p, issues=issue_list, categories=category_list, milestones=milestone_list, selected_milestones=selected_milestones, qs=qs)

