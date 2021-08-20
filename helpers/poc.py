#!/usr/bin/env python3

def write_deeplinks_to_file(activity_handlers, poc_filename):
    html = "<!DOCTYPE html>\n<html>\n<body>\n<div>\n"
    for activity, handlers in activity_handlers.items():
        html += '<h3>' + activity + '</h3>\n'
        for deeplink in sorted(handlers):
            if "http" in deeplink:
                html += '<a href="' + deeplink + '">' + deeplink + '</a></br>'
    html += "</div>\n</body>\n</html>"
    html_file = open(poc_filename, 'w')
    html_file.write(html)
    html_file.close()