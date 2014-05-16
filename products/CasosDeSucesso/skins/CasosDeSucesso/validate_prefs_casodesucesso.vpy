## Script (Python) "validate_prefs_casodesucesso"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##title=
##
from Products.CMFCore.utils import getToolByName
addPortalMessage = getToolByName(context, 'plone_utils').addPortalMessage
request = context.REQUEST
utils = context.restrictedTraverse('@@casodesucesso_utils_view')

email = request.get('email','')

if not email or not utils.validaEmail(email):
    state.setError('email', 'E-mail não informado ou inválido. Por favor, corrija.')

if state.getErrors():
    state.setStatus('failure')
    addPortalMessage('Favor corrigir os erros indicados.')
else:
    state.setStatus('success')
    
return state
