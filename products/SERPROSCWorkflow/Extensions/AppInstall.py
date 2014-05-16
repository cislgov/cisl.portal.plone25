from Products.CMFCore.utils import getToolByName
from StringIO import StringIO
from zExceptions import BadRequest


def setConfigInicial(self, portal):

    wftool = getToolByName(self, 'portal_workflow')
    if wftool.getInfoFor(portal, 'review_state', '') == "rascunho":
        wftool.doActionFor(portal, 'submeter')
    if wftool.getInfoFor(portal, 'review_state', '') in ["aguardando_revisao","publicado_restrito"]:
        wftool.doActionFor(portal, 'publicar')

    wftool.updateRoleMappings()

def setPermissions(self, portal):

    #Setando Kupu: Query libraries para a role Authenticated na raiz do portal
    portal.manage_permission('Kupu: Query libraries',roles=['Authenticated','Manager'],acquire=1)


def setPortalProperties(self, portal):

    #left_slots
    itens_esquerda = ['here/menu_adm_scw/macros/menu_adm_scw',]
    if portal.hasProperty('left_slots'):
        slotEsquerdoT = portal.getProperty(id='left_slots')
        lista = list(slotEsquerdoT) + itens_esquerda
        portal.manage_changeProperties({'left_slots': tuple(lista)})


    portal_properties = getToolByName(self, 'portal_properties')
    workflow_properties = getattr(portal_properties, 'workflow_properties', None)

    if workflow_properties is None:
        portal_properties.addPropertySheet('workflow_properties',
                                           'Workflow Properties')
    workflow_properties = getattr(portal_properties, 'workflow_properties')

    if not workflow_properties.hasProperty('groups_hidden'):
        workflow_properties.manage_addProperty(id='groups_hidden',value=('Administrators'),type='lines')

    if not workflow_properties.hasProperty('roles_hidden'):
        workflow_properties.manage_addProperty(id='roles_hidden',value=('Manager'),type='lines')



def install(self):

    out = StringIO()
    portal = getToolByName(self,'portal_url').getPortalObject()
    print >> out, "Inicio AppInstal"

    setPermissions(self, portal)
    setConfigInicial(self,portal)
    setPortalProperties(self, portal)

    print >> out, "Fim AppInstal"


def uninstall(self):

    portal = getToolByName(self, 'portal_url').getPortalObject()
    itens_esquerda = ('here/menu_adm_scw/macros/menu_adm_scw',)
    if portal.hasProperty('left_slots'):
        slotEsquerdoT = portal.getProperty(id='left_slots')
        slotEsquerdoL = list(slotEsquerdoT)
        if 'here/menu_adm_scw/macros/menu_adm_scw' in slotEsquerdoL:
            slotEsquerdoL.remove('here/menu_adm_scw/macros/menu_adm_scw')
        slotEsquerdoT = tuple(slotEsquerdoL)
        portal.manage_changeProperties({'left_slots':slotEsquerdoT})