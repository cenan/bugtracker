#!/usr/bin/env python

import os, sys

# http://stackoverflow.com/questions/72852/how-to-do-relative-imports-in-python/1083169#1083169
def import_path(fullpath):
    """
    Import a file with full path specification. Allows one to
    import from anywhere, something __import__ does not do.
    """
    path, filename = os.path.split(fullpath)
    filename, ext = os.path.splitext(filename)
    sys.path.append(path)
    module = __import__(filename)
    reload(module) # Might be out of date
    del sys.path[-1]
    return module

config = import_path('/home/cenan/projects/bugtrack/config.py')

db = config.db

def field_str(field):
    if field is None:
        return 'NULL'
    if type(field) is int:
        return str(field).replace("'","\\")
    else:
        return "'"+str(field).replace("'","\\")+"'"

def export_table(table_name):
    rows = db.select(table_name).list()
    fields = rows[0].keys()
    print "insert into %s (%s) values" % (table_name, ",".join(["%s" % field for field in fields]), )
    lines = []
    for row in rows:
        lines.append("(%s)" % ",".join([field_str(row[field]) for field in fields]))
    print ",".join(lines)
    print ";"

if __name__=="__main__":
    export_table("category")
    export_table("issue")
    export_table("issue_attachments")
    export_table("issue_update")
    export_table("milestone")
    export_table("project")
    export_table("sessions")
    export_table("user")
    export_table("user_filter")

