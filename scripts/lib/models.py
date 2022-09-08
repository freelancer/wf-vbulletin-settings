from app import db
import phpserialize
from flask.ext.sqlalchemy import BaseQuery
from sqlalchemy.ext.declarative import declared_attr
import re
from coaster.sqlalchemy import IdMixin


class DataStore(db.Model):
    __tablename__ = 'wfdatastore'
    __bind_key__ = 'vb'

    title = db.Column(db.Text, primary_key=True)
    data = db.Column(db.Text)
    unserialize = db.Column(db.Boolean)

    def to_hash(self):
        if self.unserialize:
            return phpserialize.loads(self.data)
        else:
            return self.data


class Product(db.Model):
    __tablename__ = 'wfproduct'
    __bind_key__ = 'vb'

    productid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    url = db.Column(db.String)
    version = db.Column(db.String)
    active = db.Column(db.Boolean)
    versioncheckurl = db.Column(db.String)


class Forum(db.Model):
    __tablename__ = 'wfforum'
    __bind_key__ = 'vb'

    forumid = db.Column(db.Integer, primary_key=True)
    seo_description_un = db.Column(db.Text)
    title = db.Column(db.String)


class ThreadQuery(BaseQuery):
    def order_by_forum(self, forumid):
        return self\
            .filter_by(forumid=forumid)\
            .filter_by(visible=True)\
            .filter_by(sticky=False)\
            .order_by(Thread.priorityorder.desc())


class WSOModelMixin(IdMixin):
    @declared_attr
    def __tablename__(cls):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', cls.__name__)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


class Thread(db.Model):
    query_class = ThreadQuery
    __tablename__ = 'wfthread'
    __bind_key__ = 'vb'

    threadid = db.Column(db.Integer, primary_key=True)
    priorityorder = db.Column(db.Integer)
    forumid = db.Column(db.Integer)
    sticky = db.Column(db.Boolean)
    visible = db.Column(db.Boolean)
    title = db.Column(db.String)


class Style(db.Model):
    __tablename__ = 'wfstyle'
    __bind_key__ = 'vb'

    styleid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    templatelist = db.Column(db.Text)
    csscolors = db.Column(db.Text)
    css = db.Column(db.Text)
    stylevars = db.Column(db.Text)
    editorstyles = db.Column(db.Text)


class ThreadPaymentAction(db.Model):
    query_class = ThreadQuery
    __tablename__ = 'wfthreadpaymentaction'
    __bind_key__ = 'vb'
    id = db.Column(db.Integer, primary_key=True)
    dateline = db.Column(db.DateTime)
    threadid = db.Column(db.Integer, db.ForeignKey('wfthread.threadid'))
    thread = db.relationship("Thread")
    action = db.Column(db.String)


class ThreadAutoBump(db.Model, WSOModelMixin):
    thread_id = db.Column(db.Integer)


class Plugin(db.Model):
    __tablename__ = 'wfplugin'
    __bind_key__ = 'vb'

    pluginid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    hookname = db.Column(db.String)
    phpcode = db.Column(db.Text)
    product = db.Column(db.String)

    def filename(self):
        clean_title = re.sub('[\(\)\/]', '_', self.title)
        return '%s#%s#%s' % (self.product, self.hookname, clean_title)


class Phrase(db.Model):
    __tablename__ = 'wfphrase'
    __bind_key__ = 'vb'

    phraseid = db.Column(db.Integer, primary_key=True)
    languageid = db.Column(db.Integer)
    varname = db.Column(db.String)
    fieldname = db.Column(db.String)
    text = db.Column(db.Text)
    product = db.Column(db.String)

    def filename(self):
        return '%s#%s#%s#%s' % (self.product, self.varname, self.fieldname, self.languageid)


class Template(db.Model):
    __tablename__ = 'wftemplate'
    __bind_key__ = 'vb'

    templateid = db.Column(db.Integer, primary_key=True)
    styleid = db.Column(db.Integer)
    title = db.Column(db.String)
    template = db.Column(db.Text)
    template_un = db.Column(db.Text)
    templatetype = db.Column(db.String)
    product = db.Column(db.String)

    def filename(self):
        return '%s#%s#%s' % (self.product, self.title, self.styleid)


class BBCode(db.Model):
    __tablename__ = 'wfbbcode'
    __bind_key__ = 'vb'

    bbcodeid = db.Column(db.Integer, primary_key=True)
    bbcodetag = db.Column(db.String)
    bbcodereplacement = db.Column(db.String)
    bbcodeexample = db.Column(db.String)
    twoparams = db.Column(db.Integer)
    title = db.Column(db.String)
    buttonimage = db.Column(db.String)
    options = db.Column(db.Integer)

    def filename(self):
        return '%s#%s#%s' % (self.bbcodetag, self.title,self.bbcodeid)
