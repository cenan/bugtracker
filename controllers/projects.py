import web

from models import projects
from helpers.render import render
from helpers.session import login_required

class list:
    @login_required
    def GET(self):
        project_list = projects.get_projects()
        return render.projects(projects=project_list)

class create:
    @login_required
    def GET(self):
        return render.new_project()

    @login_required
    def POST(self):
        f = web.input()
        new_project_id = projects.create_project(project_name=f.project_name)
        raise web.seeother('/project/%d/issues' % new_project_id)

