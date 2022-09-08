from models import *
from app import ensure_dir, get_and_setup_dir
import os
import codecs
import re
import json


def phpserialize_to_pretty_json(str):
    data = phpserialize.loads(str)
    return json.dumps(data, indent=2)




def write_file(filename, text):
    print filename
    with codecs.open(filename, 'w', 'utf-8') as file:
        file.write(unicode(text))


def dump_model(model):
    for column in model.__table__.columns:
        fieldname = str(column).split('.')[-1]
        primary_keyname = model.__table__.primary_key.columns.__getstate__()['_data'].keys()[0]
        primary_key = model.__dict__[primary_keyname]
        dirname = '%s/%s' % (model.__table__.name, primary_key)

        ensure_dir(dirname)
        write_file(dirname + '/%s' % fieldname, model.__dict__[fieldname])


def _dump_datastores(datastores):
    for datastore in datastores:
        filename = datastore.title
        if not filename:
            continue

        if datastore.unserialize:
            text = json.dumps(datastore.to_hash(), indent=2)
        else:
            text = datastore.data

        write_file(filename, text)


def dump_models(models):
    for model in models:
        dump_model(model)


def dump_emails(phrases):
    for phrase in phrases:
        filename = "%s_%d" % (phrase.varname, phrase.languageid)
        print filename
        write_file(filename, phrase.text)


def _dump_plugins(plugins):
    for plugin in plugins:
        clean_title = re.sub('[\(\)\/]', '_', plugin.title)
        filename = '%s#%s#%s' % (plugin.product, plugin.hookname, clean_title)
        write_file(filename, plugin.phpcode)


def _dump_templates(templates):
    styles = Style.query.all()
    style_names_by_id = dict((style.styleid, style.title) for style in styles)

    style_names_by_id[-1] = 'vBulletin'

    for template in templates:
        print template.title
        clean_title = re.sub('[\(\)\/]', '_', template.title)

        # print template.styleid
        directory = style_names_by_id[template.styleid]
        path = '%s/%s#%s#%s#%s' % (directory, template.templatetype, template.styleid, template.product, template.title)

        try:
            os.mkdir(directory)
        except:
            pass

        if template.template_un:
            write_file(path, template.template_un)
        else:
            write_file(path, template.template)


def _dump_bbcodes(bbcodes):
    for bbcode in bbcodes:
        print bbcode.title
        clean_title = re.sub('[\(\)\/]', '_', bbcode.title)
        filename = '%s#%s#%s' % (bbcode.bbcodetag, bbcode.title, bbcode.bbcodeid)
        write_file(filename,bbcode.bbcodetag)


def _dump_phrases(phrases):
    for phrase in phrases:
        filename = '%s#%s#%s#%s' % (phrase.product, phrase.varname, phrase.fieldname, phrase.languageid)
        write_file(filename, phrase.text)


def _dump_styles(styles):
    for style in styles:
        for field in ['templatelist', 'csscolors', 'stylevars', 'editorstyles']:
            filename = '%s#%s.%s.json' % (style.title, style.styleid, field)
            write_file(filename, phpserialize_to_pretty_json(getattr(style, field)))

        field = 'css'
        filename = '%s#%s.%s' % (style.title, style.styleid, field)
        write_file(filename, getattr(style, field))


def dump_styles():
    style_dir = get_and_setup_dir('styles')
    os.chdir(style_dir)

    _dump_styles(Style.query.all())


def dump_datastores():
    datastores_dir = get_and_setup_dir('datastores')
    os.chdir(datastores_dir)

    _dump_datastores(DataStore.query.all())


def dump_plugins():
    plugins_dir = get_and_setup_dir('plugins')
    os.chdir(plugins_dir)

    _dump_plugins(Plugin.query.all())


def dump_templates():
    templates_dir = get_and_setup_dir('templates')
    os.chdir(templates_dir)

    _dump_templates(Template.query.all())


def dump_bbcodes():
    bbcodes_dir = get_and_setup_dir('bbcodes')
    os.chdir(bbcodes_dir)
    _dump_bbcodes(BBCode.query.all())


def dump_phrases():
    phrases_dir = get_and_setup_dir('phrases')
    os.chdir(phrases_dir)

    _dump_phrases(Phrase.query.all())


def generate_product_csv():
    print ','.join(['productid', 'title', 'version', 'active', 'url', 'versioncheckurl'])
    for product in Product.query.all():
        print ','.join([product.productid, product.title.strip(), str(product.version), str(product.active), product.url.strip(), product.versioncheckurl.strip()])


def group_by(items, attr):
    result = {}
    for item in items:
        key = getattr(item, attr)
        if key in result:
            plugin_list = result[key]
        else:
            plugin_list = []
            result[key] = plugin_list

        plugin_list.append(item)

    return result


def dump_products():
    header_size = 80
    plugin_by_product = group_by(Plugin.query.all(), 'product')
    phrase_by_product = group_by(Phrase.query.all(), 'product')
    template_by_product = group_by(Template.query.all(), 'product')

    products = {}
    for product in Product.query.all():
        plugins = plugin_by_product.get(product.productid, [])
        phrases = phrase_by_product.get(product.productid, [])
        templates = template_by_product.get(product.productid, [])
        products[product] = len(plugins) + len(phrases) + len(templates)

    products = sorted(products.items(), key=operator.itemgetter(1))

    for (product, count) in products:
        print product.productid + '-' * (header_size - len(product.productid))
        print

        plugins = plugin_by_product.get(product.productid, [])
        if len(plugins) > 0:
            print '    plugins (%s)' % len(plugins)
            for plugin in plugins:
                print '    plugins/' + plugin.filename()
            print

        phrases = phrase_by_product.get(product.productid, [])
        if len(phrases) > 0:
            print '    phrases (%s)' % len(phrases)
            for phrase in phrases:
                print '    phrases/' + phrase.filename()
            print

        templates = template_by_product.get(product.productid, [])
        if len(templates) > 0:
            print '    templates (%s)' % len(templates)
            for template in templates:
                print '    templates/' + template.filename()
            print

        print '-' * header_size


def _dump_forums(forums):
    for forum in forums:
        # if forum.seo_description_un:
        clean_title = re.sub('[\(\)\/]', '_', forum.title)
        filename = '%s#seo_description' % (clean_title)
        write_file(filename, forum.seo_description_un)


def dump_forums():
    path = os.path.dirname(os.path.abspath(__file__)) + '/../../forums'
    os.chdir(path)
    _dump_forums(Forum.query.all())
