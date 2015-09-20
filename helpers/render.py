import datetime
import re
import os

import web

from jinja2 import Environment,FileSystemLoader

def plrl(s1, s2, f):
    if f > 1:
        return s2
    else:
        return s1

def timesince(d, now=None):
    chunks = (
            (60 * 60 * 24 * 365, lambda n: plrl('year', 'years', n)),
            (60 * 60 * 24 * 30, lambda n: plrl('month', 'months', n)),
            (60 * 60 * 24 * 7, lambda n : plrl('week', 'weeks', n)),
            (60 * 60 * 24, lambda n : plrl('day', 'days', n)),
            (60 * 60, lambda n: plrl('hour', 'hours', n)),
            (60, lambda n: plrl('minute', 'minutes', n))
            )
    # Convert datetime.date to datetime.datetime for comparison.
    if not isinstance(d, datetime.datetime):
        if not isinstance(d, datetime.date):
            d = datetime.datetime.strptime(d, "%Y-%m-%d %H:%M:%S")
        else:
            d = datetime.datetime(d.year, d.month, d.day)
    if now and not isinstance(now, datetime.datetime):
        now = datetime.datetime(now.year, now.month, now.day)

    if not now:
        now = datetime.datetime.now()

    # ignore microsecond part of 'd' since we removed it from 'now'
    delta = now - (d - datetime.timedelta(0, 0, d.microsecond))
    since = delta.days * 24 * 60 * 60 + delta.seconds
    if since <= 0:
        # d is in the future compared to now, stop processing.
        return u'0 ' + 'minutes'
    for i, (seconds, name) in enumerate(chunks):
        count = since // seconds
        if count != 0:
            break
    s = '%(number)d %(type)s' % {'number': count, 'type': name(count)}
    if i + 1 < len(chunks):
        # Now get the second item
        seconds2, name2 = chunks[i + 1]
        count2 = (since - (seconds * count)) // seconds2
        if count2 != 0:
            s += ', %(number)d %(type)s' % {'number': count2, 'type': name2(count2)}
    return s

def markdown(text):
    import markdown2

    link_patterns = [
            (re.compile("#(\d+)"), r"/issue/\1"),
            (re.compile(r"\B@(\w+)"), r"/user/\1"),
            (re.compile("rev:(\w{6})"), r"/source/browse/?rev=\1"),
            ]
    return markdown2.markdown(text, extras=["cuddled-lists", "link-patterns"], link_patterns=link_patterns)

def priority_string(p):
    if (p == 1):
        return "Critical"
    elif (p == 2):
        return "High"
    elif (p == 3):
        return "Medium"
    elif (p == 4):
        return "Low"
    return "-"

def status_string(s):
    if (s == 0):
        return "Open"
    elif (s == 1):
        return "Closed"
    return "-"

def avatar(user):
    return "/static/upload/avatars/%s.png" % user.id

class render_jinja:

    def __init__(self, *a, **kwargs):
        extensions = kwargs.pop('extensions', [])
        globals = kwargs.pop('globals', {})

        self._templ_sub_dir = ''

        self._lookup = Environment(loader=FileSystemLoader(*a, **kwargs), extensions=extensions)
        self._lookup.filters['timesince'] = timesince
        self._lookup.filters['markdown'] = markdown
        self._lookup.filters['priority_string'] = priority_string
        self._lookup.filters['status_string'] = status_string
        self._lookup.filters['avatar'] = avatar
        self._lookup.globals.update(globals)

    def __getattr__(self, name):
        if self._templ_sub_dir != '':
            name = self._templ_sub_dir + "/" + name
        if os.path.exists('./templates/%s/' % name):
            self._templ_sub_dir = name
            return self
        else:
            self._templ_sub_dir = ''
        path = name + '.html'
        t = self._lookup.get_template(path)
        return t.render

render = render_jinja('templates', encoding='utf-8', globals=web.template.Template.globals, )


