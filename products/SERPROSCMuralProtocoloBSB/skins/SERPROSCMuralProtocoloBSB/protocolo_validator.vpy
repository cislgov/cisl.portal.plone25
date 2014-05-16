## Controller Validator "protocolo_validator"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=nomeInstituicao,declaracao,anexo 
##title=
##

from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFCore.utils import getToolByName

portal = getToolByName(context,'portal_url').getPortalObject()
protocoloTool = portal.portal_serproscmuralprotocolobsbtool

if anexo:
    anexo.seek(0, 2) 
    size = anexo.tell() 
    anexo.seek(0) 
    if size > 5000000: 
        state.setError('anexo', 'O arquivo ultrapassou o tamanho máximo de 5MB.') 

anexo = protocoloTool.verificaExtensaoArquivo(anexo)
if (anexo == 'no'):
    state.setError('anexo', 'Tipo de arquivo não permitido!','anexo_required')

if not nomeInstituicao:
   state.setError('nomeInstituicao', 'Nome da instituição é obrigatório!','nomeInstituicao_required')

if not declaracao:
   state.setError('declaracao', 'Declaração é obrigatória!','declaracao_required')

if state.getErrors():
    context.plone_utils.addPortalMessage((u'Please correct the indicated errors.'))
    return state.set(status='failure')
else:
    return state
