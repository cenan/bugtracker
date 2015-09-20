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

class mail:
    def POST(self, project_id):
        f = web.input()
        user = users.get_user_with_email(f.sender)
        if user is not None:
            user_id = user.id
        else:
            user_id = 0
        issues.insert_issue(
                project_id=project_id,
                title=f.subject,
                content=f.get("body-plain"),
                opener=user_id
                )

