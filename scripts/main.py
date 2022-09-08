import os
from lib.style_updater import StyleUpdater
from lib.models import *
from lib.dump import dump_templates, dump_forums, dump_styles, dump_bbcodes
import sys, getopt
import argparse

if not 'DB_CONNECTION_VB' in os.environ:
    os.environ['DB_CONNECTION_VB'] = 'mysql://dev:test@172.17.9.101:3366/warriorf_vb'
    os.environ['DB_CONNECTION_WSO'] = 'mysql://dev:test@172.17.9.101:3366/warriorf_vb'

# if not 'DB_CONNECTION_VB' in os.environ:
    # raise "need db credentials, try > export DB_CONNECTION_VB=mysql://dev:test@172.17.9.101:3366/warriorf_vb"

def print_help():
    print 'test.py [--dump-forums] [--dump-templates]'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--update-style')
    parser.add_argument('--dump-templates', action='store_true')
    parser.add_argument('--dump-styles', action='store_true')
    parser.add_argument('--dump-forums', action='store_true')
    parser.add_argument('--dump-bbcodes', action='store_true')

    args = parser.parse_args()
    if args.update_style:
        StyleUpdater().update(args.update_style)

    if args.dump_templates:
        dump_templates()

    if args.dump_styles:
        dump_styles()

    if args.dump_bbcodes:
        dump_bbcodes()
    # try:
    #     opts, args = getopt.getopt(argv,"",["dump-forums", "dump-templates", "dump-styles"])
    # except getopt.GetoptError:
    #     print_help()
    #     sys.exit(2)

    # found = False
    # for opt, arg in opts:
    #     if opt in ("-i", "--dump-forums"):
    #         found = True
    #         dump_forums()

    #     if opt in ("--dump-styles"):
    #         found = True
    #         dump_styles()

    #     if opt in ("-t", "--dump-templates"):
    #         found = True
    #         dump_templates()

    # if not found:
    #     print_help()


if __name__ == "__main__":
    main()
