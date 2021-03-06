from optparse import OptionParser
import subprocess
import os
parser = OptionParser()
parser.add_option("-l", "--lists", action="append", type="string", help="Listas negadas en pass")
parser.add_option("-w", "--whitelists", action="append", type="string", help="Listas pass")
parser.add_option("-d", "--dir", dest="directory", action="store", type="string",
                  help="Directorio de blacklists")
parser.add_option("-f", "--file", dest="filename", action="store", type="string",
                  help="Archivo de salida", metavar="FILE")
parser.add_option("-a", "--activity", dest="activity", action="store", type="string",
                  help="Log de actividad")

(options, args) = parser.parse_args()

directory = options.directory or "/var/lib/squidguard/db"
filename = options.filename or "/etc/squidguard/squidGuard.conf"
lists = options.lists or []
whitelists = options.whitelists or []
activity = options.activity or "activity.log"

available_lists = [db_name for db_name in os.listdir(directory) if ("domains" in os.listdir("/".join([directory,db_name])) or "urls" in os.listdir("/".join([directory,db_name])))]

lists = filter(lambda x: x in available_lists, lists)
whitelists = filter(lambda x: x in available_lists, whitelists)

with open(filename, 'w') as f:
    f.write("dbhome "+directory+"\n")
    f.write("logdir /var/log/squidguard\n")
    f.write("\n")
    for lista in lists+whitelists:
        f.write("dest "+lista+" {\n")
        f.write("  domainlist "+lista+"/domains\n")
        f.write("  urllist "+lista+"/urls\n")
        f.write("  log verbose "+activity+"\n")
        f.write("}\n")
        f.write("\n")
    f.write("\n")
    f.write("acl {\n")
    f.write("  default {\n")
    f.write("    pass "+" ".join(whitelists)+" !".join([""]+lists)+" all\n")
    f.write("    redirect http://static-content.buffer.cl/blocks.html\n")
    f.write("  }\n")
    f.write("}\n")
