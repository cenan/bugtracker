import web

from models import projects

from helpers import git
from helpers.render import render

from helpers.session import login_required

class repo:
    def GET(self, project_id):
        web.seeother('/project/%s/source/browse/' % project_id)

class browse:
    @login_required
    def GET(self, project_id, path=''):
        p = projects.get_project(project_id)
        git.path = p.git_repo_path
        if path[:-1] != '/':
            path += '/'
        if web.ctx.query.find("rev") != -1:
            rev = web.ctx.query.split('=')[1]
            commit_obj = git.read_object(rev)
            commit_tree = commit_obj.split()[1].strip()
            files = git.read_object(commit_tree)
        else:
            rev = ''
            files = git.read_head()
        breadcrumb = []
        history = git.read_history()

        fullpath = ''
        for p in path.split('/'):
            fullpath += '/' + p
            for f in files:
                if f.get('path', '0') == '0':
                    f['path'] = fullpath + f['filename']
                if f['filename'] == p:
                    breadcrumb.append({'name': f['filename'],'path': fullpath,'hash': f['hash']})
                    if f['access_code'] == '40000':
                        files = git.read_object(f['hash'])
                    else:
                        blob = git.read_blob(f['hash'])
                        return render.git.show_file(project_id=project_id, file_contents=unicode(blob, "utf-8"), breadcrumb=breadcrumb, history=history, rev=rev)
                    break
        return render.git.index(project_id=project_id, files=files, breadcrumb=breadcrumb, history=history, rev=rev)

