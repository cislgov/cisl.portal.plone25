## Script (Python) "save_prefs_casodesucesso"
##title=Edit content
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##
from Products.CMFCore.utils import getToolByName
addPortalMessage = getToolByName(context, 'plone_utils').addPortalMessage

request = context.REQUEST
site = getToolByName(context, 'portal_url').getPortalObject()
portal_properties = site.portal_properties
casodesucesso_properties = portal_properties.serpro_casodesucesso_properties

state.setNextAction('redirect_to:string:plone_control_panel')

email = request.get('email')

try:
    casodesucesso_properties.manage_changeProperties({'email_administrator':email})
    addPortalMessage('Configuração alterada com sucesso.')
    return state.set(status='success')
                     
except Exception, e:
    addPortalMessage('Erro ao salvar as configurações do produto: '+str(e))
    return state.set(status='failure')
    