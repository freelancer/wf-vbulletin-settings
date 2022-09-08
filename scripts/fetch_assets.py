import re
import json
import requests
import random
import os
import commands
import argparse
from collections import OrderedDict


def rando():
    return random.randrange(1, 2 ** 32)


def get_filename(project_path):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return script_dir + '/..' + project_path


def update_footer():
    filename = get_filename('/templates/template#7#vbulletin#footer')
    with open(filename, 'r+') as file:
        text = file.read()
        text = re.sub('/static/scripts/vendor\..+\.js', assets['scripts/vendor.js'], text)
        text = re.sub('/static/scripts/wf\..+\.js', assets['scripts/wf.js'], text)
        file.seek(0)
        file.write(text)


def update_header():
    filename = get_filename('/templates/template#7#vbulletin#header')
    with open(filename, 'r+') as file:
        text = file.read()
        text = re.sub('/static/styles/vendor\..+\.css', assets['styles/vendor.css'], text)
        text = re.sub('/static/styles/wf\..+\.css', assets['styles/wf.css'], text)
        text = re.sub('/static/styles/feed\..+\.css', assets['styles/feed.css'], text)
        file.seek(0)
        file.write(text)


def get_asset_location(name):
    if environment == 'staging':
        return '//s3.amazonaws.com/wso-staging.warriorforum.com' + assets[name]
    elif environment == 'production':
        return '//static.warriorforum.com' + assets[name]
    elif environment == 'dev':
        return 'http://payments.wf-dev.net:8080' + assets[name]
    elif environment == 'local':
        path = re.sub('\.[\da-z]{8}', '', assets[name])
        path = re.sub('^/static', '', path)
        return 'http://local.wf-dev.net:9000' + re.sub('\.[\da-z]{8}', '', path)

def replace_line(line):
    match = re.match('.*assets\[\'(.*?)\'\] = \'(.*)\';', line)
    if not match:
        return

    name = match.group(1)
    url = match.group(2)

    if re.search('local', url):
        return

    mapping = {
        'css_wf': 'styles/wf.css',
        'css_vendor_wf': 'styles/vendor_wf.css',
        'css_feed': 'styles/feed.css',
        'css_guide': 'styles/guide.css',
        'js_vendor': 'scripts/vendor.js',
        'js_wf': 'scripts/wf.js'
    }

    if name in mapping:
        print get_asset_location(mapping[name])
        return r"    $vbulletin->assets['%s'] = '%s';" % (name, get_asset_location(mapping[name]))


def update_global(root_dir, commit):
    # print root_dir
    # found_live = False
    if environment == 'local':
        filename = root_dir + '/wf-vbulletin/src/includes/assets_local.json'
    else:
        filename = root_dir + '/wf-vbulletin/src/includes/assets.json'


    # lines = []
    with open(filename, 'w') as file:
        # print assets
        items = list((key, get_asset_location(key)) for (key, value) in assets.items())
        items.append(('__environment', environment))

        if environment != 'local':
            if commit:
                items.append(('__commit', commit))

        assets_updated = OrderedDict(sorted(items, key= lambda x: x[0]))
        text = json.dumps(assets_updated, indent=4)
        file.write(text)
    #     for line in file.readlines():
    #         line = line.rstrip('\n')

    #         new_line = None
    #         if re.search('// production', line):
    #             new_line = '    // %s' % environment
    #             found_live = True

    #         elif re.search('// staging', line):
    #             new_line = '    // %s' % environment
    #             found_live = True

    #         elif found_live:
    #             new_line = replace_line(line)

    #         if new_line:
    #             lines.append(new_line)
    #         else:
    #             lines.append(line)

    #     file.seek(0)
    #     for line in lines:
    #         file.write(line + "\n")


parser = argparse.ArgumentParser(description='Update global.php.')
parser.add_argument('--user', default='paulo')
parser.add_argument('--location', default='production')

if __name__ == '__main__':
    args = parser.parse_args()
    environment = args.location
    user = args.user

    if environment not in ['dev', 'staging', 'production', 'local']:
        raise Exception('Invalid  location')

    if user == 'ben':
        root_dir = '/home/bb/Code/cc'
    elif user == 'paulo':
        root_dir = '/home/paulo'
    elif user == 'paulodeploy':
        root_dir = '/home/paulo/Deployment'
    elif user == 'neil':
        root_dir = '/home/neil/Projects'
    else:
        raise Exception('Invalid User')

    commit = None
    if environment == 'staging':
        returncode, output = commands.getstatusoutput('cd ' + root_dir + '/wsomanager && git log --pretty=format:\'%h%n%n%s\' -n 1 origin/master')
        print "Sync wsomanager:%s" % output
        commit = "wsomanager:%s" % output.split()[0]
        assets = json.loads(requests.get('https://s3.amazonaws.com/wso-staging.warriorforum.com/static/assets.json?%s' % rando()).text)

    elif environment == 'production':
        returncode, output = commands.getstatusoutput('cd ' + root_dir + '/wsomanager && git log --pretty=format:\'%h%n%n%s\' -n 1 origin/production')
        print "Sync wsomanager:%s" % output
        commit = "wsomanager:%s" % output.split()[0]
        assets = json.loads(requests.get('https://static.warriorforum.com/static/assets.json?%s' % rando()).text)

    elif environment == 'local':
        returncode, output = commands.getstatusoutput('cd ' + root_dir + '/wsomanager && git log --pretty=format:\'%h%n%n%s\' -n 1 origin/production')
        print "Sync wsomanager:%s" % output
        commit = "wsomanager:%s" % output.split()[0]
        assets = json.loads(requests.get('https://static.warriorforum.com/static/assets.json?%s' % rando()).text)

    elif environment == 'dev':
        # returncode, output = commands.getstatusoutput('cd ' + root_dir + '/wsomanager && git log --pretty=format:\'%h%n%n%s\' -n 1 origin/production')
        # print "sync wsomanager:%s" % output
        assets = json.loads(requests.get('http://payments.wf-dev.net:8080/static/assets.json?%s' % rando()).text)

    update_global(root_dir, commit)
