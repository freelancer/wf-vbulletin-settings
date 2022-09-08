import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import re

app = Flask(__name__)

def get_and_setup_dir(name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    style_dir = script_dir + '/../../' + name
    ensure_dir(style_dir)
    return style_dir

def template_filename(template):
    clean_title = re.sub('[\(\)\/]', '_', template.title)
    return '%s#%s#%s#%s' % (template.templatetype, template.styleid, template.product, template.title)

def ensure_dir(dirname):
    try:
        os.makedirs(dirname)
    except:
        pass

if 'DB_CONNECTION_VB' not in os.environ:
    raise "need db credentials, try > export DB_CONNECTION_VB=mysql://dev:test@172.17.9.1:3366/warriorf_vb"

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DB_CONNECTION_WSO']
app.config['SQLALCHEMY_BINDS'] = {'vb': os.environ['DB_CONNECTION_VB']}
db = SQLAlchemy(app)

    # plugins_dir = get_and_setup_dir('plugins')
    # os.chdir(plugins_dir)
