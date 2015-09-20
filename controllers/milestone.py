import web

from models import milestones

from helpers.render import render
from helpers.session import login_required

class create:
    @login_required
    def GET(self, project_id):
        return render.new_milestone(project_id=project_id)

    @login_required
    def POST(self, project_id):
        f = web.input()
        id = milestones.insert_milestone(project_id=project_id, milestone_name=f.milestone_name)
        raise web.seeother('/project/%s/milestones' % project_id)

class list:
    @login_required
    def GET(self, project_id):
        milestone_list = milestones.get_milestones(project_id)
        return render.milestones(project_id=project_id, milestones=milestone_list)

class show:
    @login_required
    def GET(self, project_id, id):
        milestone = milestones.get_milestone(id)
        return render.milestone(project_id=project_id, milestone=milestone)

class update:
    @login_required
    def GET(self, project_id, id):
        milestone = milestones.get_milestone(id)
        return render.milestone(project_id=project_id, milestone=milestone)

    @login_required
    def POST(self, project_id, id):
        f = web.input()
        milestones.update_milestone(id, milestone_name=f.milestone_name, milestone_status=f.milestone_status)
        raise web.seeother('/project/%s/issues' % project_id)

class delete:
    @login_required
    def GET(self, project_id, id):
        milestones.delete_milestone(id)
        raise web.seeother('/project/%s/milestones' % project_id)

