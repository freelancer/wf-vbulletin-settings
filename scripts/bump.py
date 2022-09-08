from lib.models import *
from lib.dump import dump_templates, dump_datastores, dump_forums
import sys, getopt
from datetime import datetime

# 1059695
# thread = Thread.query.get(1059695)
# print thread.threadid
# print thread.forumid
# print thread.title

def pretty_ago(delta=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    second_diff = delta.seconds
    day_diff = delta.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(second_diff / 60) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(second_diff / 3600) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff / 7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff / 30) + " months ago"
    return str(day_diff / 365) + " years ago"

# 17 32 67
threads = Thread.query.order_by_forum(17).limit(60).all()
i = 1
for thread in threads:
    autobump = ThreadAutoBump.query.filter_by(thread_id=thread.threadid).first()

    action = ThreadPaymentAction.query\
        .filter_by(threadid=thread.threadid)\
        .filter(ThreadPaymentAction.action.in_(['new', 'bump']))\
        .order_by(ThreadPaymentAction.dateline.desc())\
        .first()

    autobumpstr = " "
    elapsedstr = "     "
    if autobump:
        autobumpstr = "*"

    if action:
        # delta = action.dateline - datetime.now()
        elapsed = datetime.utcnow() - action.dateline
        elapsedstr = "%4sm" % (int(elapsed.total_seconds() / 60))
        # print action.dateline
        # print datetime.utcnow()
    print("%2s%s, %s, %7s, %s" % (i, autobumpstr, elapsedstr, thread.threadid, thread.title))
    i += 1

# forum = Forum.query.get()

# autobumps = ThreadAutoBump.query.all()
# auto_bump_threadids = [autobump.thread_id for autobump in autobumps]

# threads = Thread.query\
#     .filter(Thread.threadid.in_(auto_bump_threadids))

# for autobump in autobumps:
#     thread = Thread.query.get(autobump.thread_id)
#     print thread.threadid, thread.forumid, thread.title

# for autobumps in ThreadAutoBump.query.all():
    # print thread_auto_bump.thread_id

# print ThreadAutoBump.query\
#     .filter(ThreadAutoBump.threadid.in_(threadids))
#     .all()