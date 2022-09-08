import os
import json
import phpserialize
from app import get_and_setup_dir, template_filename
from lib.models import *

def json_loadf_to_phpserialize(filename):
    with open(filename) as f:
        return phpserialize.dumps(json.load(f))

def read_file(filename):
    with open(filename) as f:
        return f.read()

class StyleUpdater(object):
    def update(self, name):
        style = Style.query\
            .filter_by(title=name)\
            .one()

        styles_dir = get_and_setup_dir('styles')
        os.chdir(styles_dir)

        # name

        # style.csscolors = json_loadf_to_phpserialize(name + '.csscolors.json')
        # style.editorstyles = json_loadf_to_phpserialize(name + '.editorstyles.json')
        # style.editorstyles = json_loadf_to_phpserialize(name + '.editorstyles.json')

        # print style.csscolors

        templates_dir = get_and_setup_dir('templates')
        os.chdir(templates_dir)

        templates = Template.query\
            .filter_by(styleid=9, templatetype="css")\
            .all()

        for template in templates:
            if template.template_un:
                raise "template.template_un not empty for %s" % template.templateid

            filename = template_filename(template)
            new_template = read_file(filename)
            if template.template != new_template:
                print filename
                template.template = new_template

        db.session.commit()



        # db.session.add(style)
        # db.session.commit()