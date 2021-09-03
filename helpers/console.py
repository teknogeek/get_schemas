#!/usr/bin/env python3

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def write_to_console(str, color):
    print(color + str + bcolors.ENDC)

def print_deeplinks(deeplinks, only_applinks):
    for activity, handlers in deeplinks.items():
        write_to_console('\n' + activity + '\n', bcolors.BOLD)
        for deeplink in sorted(handlers.keys()):
            is_applink = deeplink.startswith('http')
            if not only_applinks or is_applink:
                if is_applink:
                    if handlers[deeplink]:
                        print('autoverify=true ' + bcolors.OKGREEN + deeplink + bcolors.ENDC)
                    else:
                        print(bcolors.FAIL + 'autoverify=false ' + bcolors.ENDC + bcolors.OKGREEN + deeplink + bcolors.ENDC)
                else:
                    write_to_console('\t\t' + deeplink, bcolors.OKGREEN)