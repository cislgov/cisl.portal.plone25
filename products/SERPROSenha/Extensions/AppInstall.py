from StringIO import StringIO
from Products.CMFCore.utils import getToolByName


def install(self):
    out = StringIO()
    portal = getToolByName(self, 'portal_url').getPortalObject()

    setupMemberdata(portal)

def setupMemberdata(portal):
    portal_memberdata = getToolByName(portal, 'portal_memberdata')

    if not portal_memberdata.hasProperty('error_count'):
        portal_memberdata._setProperty('error_count', '0', 'string')
    if not portal_memberdata.hasProperty('date_lock'):
        portal_memberdata._setProperty('date_lock', "2000/01/01", 'date')



