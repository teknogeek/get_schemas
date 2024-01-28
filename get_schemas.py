#!/usr/bin/env python3

import argparse
from bs4 import BeautifulSoup
import itertools
import re

is_scheme_data_tag = lambda tag: tag.name == 'data' and \
    any(f'android:{x}' in tag.attrs for x in \
        ('scheme', 'host', 'port', 'path', 'pathPrefix', 'pathPattern') \
    )

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--manifest',
                        required=False,
                        default='AndroidManifest.xml',
                        type=argparse.FileType('r'),
                        help='Path to AndroidManifest.xml (default: ./AndroidManifest.xml)')
    parser.add_argument('-s', '--strings',
                        required=False,
                        default='res/values/strings.xml',
                        type=argparse.FileType('r'),
                        help='Path to strings.xml (default: ./res/values/strings.xml)')
    args = parser.parse_args()

    strings_xml = BeautifulSoup(args.strings, 'xml')
    strings = {d['name']: d.text for d in strings_xml.find_all('string', {'name': True})}

    raw_manifest = args.manifest.read()
    raw_manifest = re.sub('"@string\/(?P<string_name>[^"]+)"', lambda g: '"{}"'.format(strings.get(g.group('string_name'), 'UNKNOWN_STRING')), raw_manifest)
    manifest_xml = BeautifulSoup(raw_manifest, 'xml')

    for e in manifest_xml.findAll(True, {'android:exported': 'true'}):
        print(f'Exported <{e.name}>: {e["android:name"]}')

    print(f'\n{"-"*50}\n')
    activity_handlers = {}
    for intent_filter in manifest_xml.find_all('intent-filter'):
        scheme_items = intent_filter.findAll(is_scheme_data_tag)
        if len(scheme_items) > 0:
            activity_name = None
            activity_exported = False

            target_activity = intent_filter.find_parent(['activity', 'activity-alias', 'service', 'receiver'])
            if not target_activity:
                continue

            if target_activity.name == 'activity-alias':
                target_activity_name = target_activity['android:targetActivity']
                target_activity = manifest_xml.find('activity', {'android:name': target_activity_name})

            if target_activity:
                activity_name = target_activity.get('android:name', None)
                activity_exported = bool(target_activity.get('android:exported', False))

            if activity_name is not None:
                schemes, hosts, ports, paths = [], [], [], []
                for item in scheme_items:
                    schemes.append(item.get('android:scheme'))
                    hosts.append(item.get('android:host'))
                    ports.append(item.get('android:port'))

                    for k in ('path', 'pathPrefix', 'pathPattern'):
                        paths.append(item.get(f'android:{k}'))

                schemes, hosts, ports, paths = map(list, map(set, map(lambda x: filter(None, x), [schemes, hosts, ports, paths])))
                no_port_path = (len(ports) == 0 and len(paths) == 0)
                if len(ports) == 0: ports.append('')
                if len(paths) == 0: paths.append('')
                if len(hosts) == 0: hosts.append('') # for filters with only <schema>://
                for scheme, host, port, path in list(itertools.product(schemes, hosts, ports, paths)):
                    if scheme:
                        uri = f'{scheme}://'
                        if host:
                            uri += host
                            if not no_port_path:
                                if port: uri += f':{port}'
                                if path: uri += f'{"/" if not path.startswith("/") else ""}{path}'

                        activity_key = (activity_name, activity_exported)
                        activity_handlers[activity_key] = activity_handlers.get(activity_key, []) + [uri]

    for (activity, exported), handlers in activity_handlers.items():
        print(f'{activity} (exported={exported})')
        print('\n'.join(f'  {h}' for h in sorted(set(handlers))))


if __name__ == '__main__':
    main()
