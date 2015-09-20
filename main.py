#!/usr/bin/env python

import web

import config
import controllers

urls = (
    '/',                                           'index',

    '/projects',                                   'controllers.projects.list',
    '/new-project',                                'controllers.projects.create',

    '/login',                                      'controllers.auth.login',
    '/logout',                                     'controllers.auth.logout',
    '/user/([0-9]*)',                              'controllers.auth.user',
    '/user/save-filter/',                          'controllers.auth.save_filter',

    '/project/([0-9]*)/search/',                   'controllers.issue.search',

    '/project/([0-9]*)/issues',                    'controllers.issue.list',
    '/project/([0-9]*)/new-issue',                 'controllers.issue.create',
    '/project/([0-9]*)/issue/([0-9]*)',            'controllers.issue.show',
    '/project/([0-9]*)/delete-issue/([0-9]*)',     'controllers.issue.delete',
    '/project/([0-9]*)/update-issue',              'controllers.issue.update',
    '/project/([0-9]*)/edit-issue',                'controllers.issue.edit',

    '/project/([0-9]*)/milestones',                'controllers.milestone.list',
    '/project/([0-9]*)/edit-milestone/([0-9]*)',   'controllers.milestone.update',
    '/project/([0-9]*)/new-milestone',             'controllers.milestone.create',
    '/project/([0-9]*)/delete-milestone/([0-9]*)', 'controllers.milestone.delete',
    '/project/([0-9]*)/milestone/([0-9]*)',        'controllers.milestone.show',

    '/project/([0-9]*)/new-category',              'controllers.categories.create',
    '/project/([0-9]*)/edit-category/([0-9]*)',    'controllers.categories.update',
    '/project/([0-9]*)/delete-category/([0-9]*)',  'controllers.categories.delete',

    '/project/([0-9]*)/source/',                   'controllers.source.repo',
    '/project/([0-9]*)/source/browse/(.*)',        'controllers.source.browse',

    "/api/mail/project/([0-9]*)",                  "controllers.api.mail",
)

web.config.debug = False
store = web.session.DBStore(config.db, 'sessions')
app = web.application(urls, globals())
_session = web.session.Session(app, store)

def session_hook():
    web.ctx.session = _session
    web.template.Template.globals['session'] = _session

app.add_processor(web.loadhook(session_hook))

class index:
    def GET(self):
        raise web.seeother('/projects')

if __name__ == "__main__":
    app.run()

