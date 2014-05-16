# -*- coding: utf-8 -*-
from AccessControl.SecurityManagement import newSecurityManager
from collective.jsonify import get_item

import simplejson as json
import os


def get_children(path):
    children = ct.searchResults(path={'query': path,
                                      'depth': 1},
                                sort_on='getObjPositionInParent')
    if children:
        data = [{'id': b.getId,
                 'title': b.Title,
                 'portal_type': b.portal_type}
                for b in children]
        arq = open('dados%s/children.json' % path, 'wb')
        arq.write(json.dumps(data))
        arq.close()

newSecurityManager(None, app.acl_users.getUserById('admin'))  # noqa

site = app.clientes.softwarelivre.softwarelivre  # noqa
path = '/clientes/softwarelivre/softwarelivre'

ct = site.portal_catalog
uid_catalog = site.uid_catalog

all_uids = uid_catalog()
p_to_uid = dict([('%s/%s' % (path, b.getPath()), b.UID) for b in all_uids])


get_children(path)
results = ct.searchResults(path=path)

for brain in results:
    obj = brain.getObject()
    data = get_item(obj)
    path = brain.getPath()
    if not os.path.exists('dados%s' % path):
        os.makedirs('dados%s' % path)
    arq = open('dados%s/data.json' % path, 'wb')
    arq.write(data)
    arq.close()
    get_children(path)
    uid = p_to_uid[path]
    print uid, path, len(data)
