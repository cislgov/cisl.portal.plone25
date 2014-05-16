from StringIO import StringIO

from Products.CMFCore.utils import getToolByName
from Products.Archetypes.public import listTypes
from Products.Archetypes.Extensions.utils import installTypes, install_subskin

from Products.PloneSurvey.config import PROJECTNAME, GLOBALS
from Products.PloneSurvey import permissions as perms

def grantResetOwnResponsesToMember(portal, out=None):
    """Give Member the 'PloneSurvey: Reset Own Responses' permission.
    """
    role_name = 'Member'
    # Get hold of the existing roles for our permission
    roles = portal.rolesOfPermission(perms.ResetOwnResponses)
    # roles looks like this:
    # [{'selected': 'SELECTED', 'name': 'Anonymous'},
    #  {'selected': '', 'name': 'Authenticated'},]
    roles_list = []
    role_added = False
    for role in roles:
        if role['name'] == role_name:
            if role['selected']:
                if out is not None:
                    msg = "'%s' already has the '%s' permission at the portal root so no action taken."
                    print >> out, msg % (role_name, perms.ResetOwnResponses)
                return
            else:
                # Add the role to the roles list
                roles_list.append(role_name)
                role_added = True
        if role['selected']:
            roles_list.append(role['name'])
    if role_added:
        # Update with the new roles list
        portal.manage_permission(perms.ResetOwnResponses,
                                 roles=roles_list,
                                 acquire=1)
        if out is not None:
            msg = "Granted '%s' the '%s' permission at the portal root."
            print >> out, msg % (role_name, perms.ResetOwnResponses)


def install(self):
    out = StringIO()
    
    installTypes(self, out,
                 listTypes(PROJECTNAME),
                 PROJECTNAME)

    install_subskin(self, out, GLOBALS)

    # add stylesheet to 
    portal_css = getToolByName(self, 'portal_css')
    portal_css.manage_addStylesheet(id = 'survey_results.css',
                                    expression = 'python:object.template.getId() == "survey_view_results"',
                                    media = 'all',
                                    title = 'Plone Survey Results',
                                    enabled = True)

    ntp = getToolByName(self, 'portal_properties').navtree_properties
    bl = list(ntp.getProperty('metaTypesNotToList', ()))
    ntp_change = 0
    if 'Survey Question' not in bl:
        bl.append('Survey Question')
        ntp_change = 1
    if 'Survey Likert Question' not in bl:
        bl.append('Survey Likert Question')
        ntp_change = 1
    if 'Survey Matrix' not in bl:
        bl.append('Survey Matrix')
        ntp_change = 1
    if 'Survey Matrix Question' not in bl:
        bl.append('Survey Matrix Question')
        ntp_change = 1
    if 'Survey Select Question' not in bl:
        bl.append('Survey Select Question')
        ntp_change = 1
    if 'Survey Text Question' not in bl:
        bl.append('Survey Text Question')
        ntp_change = 1
    if 'Sub Survey' not in bl:
        bl.append('Sub Survey')
        ntp_change = 1
    if ntp_change:
        ntp._p_changed = 1
        ntp.metaTypesNotToList = bl

    # Enable portal_factory
    factory = getToolByName(self, 'portal_factory')
    types = factory.getFactoryTypes().keys()
    if 'Survey' not in types:
        types.append('Survey')
    if 'Sub Survey' not in types:
        types.append('Sub Survey')
    if 'Survey Question' not in types:
        types.append('Survey Question')
    if 'Survey Likert Question' not in types:
        types.append('Survey Likert Question')
    if 'Survey Matrix' not in types:
        types.append('Survey Matrix')
    if 'Survey Matrix Question' not in types:
        types.append('Survey Matrix Question')
    if 'Survey Select Question' not in types:
        types.append('Survey Select Question')
    if 'Survey Text Question' not in types:
        types.append('Survey Text Question')
    factory.manage_setPortalFactoryTypes(listOfTypeIds = types)

    grantResetOwnResponsesToMember(self, out)

    print >> out, "Successfully installed %s." % PROJECTNAME
    return out.getvalue()
