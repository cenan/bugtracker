import web

from models import users

from helpers.render import render
from helpers.session import login_required

class login:
    def GET(self):
        return render.login()

    def POST(self):
        f = web.input()
        user = users.try_login(username=f.username, password=f.password)
        if user is not False:
            web.ctx.session.logged_in = True
            web.ctx.session.user_id = user.id
            web.ctx.session.user_name = user.username
            raise web.seeother('/')
        else:
            raise web.seeother('/login')

class logout:
    def GET(self):
        web.ctx.session.kill()
        raise web.seeother('/login')

class user:
    def GET(self, user_id):
        user = users.get_user(user_id)
        return render.user(user=user)

class save_filter:
    @login_required
    def POST(self):
        filter = web.ctx.env['QUERY_STRING']
        users.save_filter(user_id=web.ctx.session.user_id, filter=filter)
        return "Filter saved"

