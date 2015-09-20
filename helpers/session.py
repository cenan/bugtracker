import web

def login_required(func):
    def proxy(*args):
        if not web.ctx.session.get('logged_in', False):
            return web.seeother('/login')
        return func(*args)
    return proxy


