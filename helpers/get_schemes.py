#!/usr/bin/env python3

from typing import List
from bs4 import BeautifulSoup
import itertools
import re

AUTOVERIFY_KEY = 'has-autoverify'
INCLUDES_VIEW_ACTION_KEY = 'has-view-action'
INCLUDES_BROWSABLE_CATEGORY_KEY = 'has-browsable-category'
INCLUDES_DEFAULT_CATEGORY_KEY = 'has-default-category'


is_scheme_data_tag = lambda tag: tag.name == 'data' and \
    any(f'android:{x}' in tag.attrs for x in \
        ('scheme', 'host', 'port', 'path', 'pathPrefix', 'pathPattern') \
    )

def get_schemes(strings, manifest):
    strings_xml = BeautifulSoup(strings, 'xml')
    strings = {d['name']: d.text for d in strings_xml.find_all('string', {'name': True})}

    raw_manifest = manifest.read()
    raw_manifest = re.sub('"@string\/(?P<string_name>[^"]+)"', lambda g: '"{}"'.format(strings.get(g.group('string_name'), 'UNKNOWN_STRING')), raw_manifest)
    manifest_xml = BeautifulSoup(raw_manifest, 'xml')

    activity_handlers = {}
    for intent_filter in manifest_xml.find_all('intent-filter'):
        scheme_items = intent_filter.findAll(is_scheme_data_tag)
        if len(scheme_items) > 0:
            activity_name = None
            
            # find activity name from parent
            parent_elem = intent_filter.find_parent(['activity', 'activity-alias', 'service', 'receiver'])
            if parent_elem:
                # parent type
                p_type = parent_elem.name
                if p_type in ['activity', 'service', 'receiver']:
                    activity_name = parent_elem['android:name']
                elif p_type == 'activity-alias':
                    target_activity_name = parent_elem['android:targetActivity']
                    target_activity = manifest_xml.find('activity', {'android:name': target_activity_name})
                    if target_activity:
                        activity_name = target_activity['android:name']

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

                        if activity_name not in activity_handlers:
                            activity_handlers[activity_name] = {}
                        activity_handlers[activity_name][uri] = {
                            AUTOVERIFY_KEY: 'android:autoVerify="true"' in str(intent_filter),
                            INCLUDES_VIEW_ACTION_KEY: '<action android:name="android.intent.action.VIEW"/>' in str(intent_filter),
                            INCLUDES_BROWSABLE_CATEGORY_KEY: 'android.intent.category.BROWSABLE' in str(intent_filter),
                            INCLUDES_DEFAULT_CATEGORY_KEY: 'android.intent.category.DEFAULT' in str(intent_filter)
                        }

    return activity_handlers