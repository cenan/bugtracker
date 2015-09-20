import web
import socket

host = socket.gethostname()

if host in ['minic', 'tokyo', 'okinawa', 'mumbai']:
    db = web.database(dbn='sqlite', db='db/sqlite/test.db')
    upload_dir = '/home/cenan/projects/bugtrack/static/upload/'
elif host == 'bugtrack':
    db = web.database(dbn='mysql', db='project', user='root', pw='root')
    upload_dir = '/home/cenan/sites/projects.cenanozen.com/static/upload/'

