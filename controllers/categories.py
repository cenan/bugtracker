import web

from models import categories
from models import users

from helpers.render import render
from helpers.session import login_required


class create:
    @login_required
    def GET(self, project_id):
        user_list = users.get_users()
        return render.new_category(project_id=project_id, users=user_list)

    @login_required
    def POST(self, project_id):
        f = web.input()
        categories.insert_category(project_id=project_id,
                                   category_name=f.category_name,
                                   default_assignee_id=f.default_assignee)
        raise web.seeother('/project/%s/issues' % project_id)


class update:
    @login_required
    def GET(self, project_id, id):
        category = categories.get_category(id)
        user_list = users.get_users()
        return render.category(project_id=project_id,
                               category=category,
                               users=user_list)

    @login_required
    def POST(self, project_id, id):
        f = web.input()
        categories.update_category(id=id,
                                   category_name=f.category_name,
                                   default_assignee_id=f.default_assignee)
        raise web.seeother('/project/%s/issues' % project_id)


class delete:
    @login_required
    def POST(self, project_id, id):
        categories.delete_category(id=id)
        raise web.seeother('/project/%s/issues' % project_id)
