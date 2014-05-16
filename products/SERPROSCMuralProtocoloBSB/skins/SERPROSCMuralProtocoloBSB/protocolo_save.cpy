from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from ZODB.POSException import ConflictError

#pega os paramentros no request
REQUEST = context.REQUEST


protocoloTool = getToolByName(context, 'portal_serproscmuralprotocolobsbtool')
usuario_atual = protocoloTool.setarPermissaoSuperUsuario()

dicProtocolo = {}

dicProtocolo['nomeInstituicao']              = str(REQUEST['nomeInstituicao'])
dicProtocolo['declaracao']     = str(REQUEST['declaracao'])
dicProtocolo['anexo']             = REQUEST['anexo']

strReturn = protocoloTool.criaObjetoProtocolo(dicProtocolo)

if(strReturn != 'no'):
    portal = getToolByName(context,'portal_url')
    pastaProtocolo = getattr(portal,'protocolo-brasilia')
    protocolo = getattr(pastaProtocolo,strReturn)
    assunto='Software Livre - Novo protocolo recebido'
    mensagem='Foi criado um protocolo no Portal Software Livre no governo do Brasil.\n Nome da instituição: '+str(protocolo.getTitle())
    email_to=portal.email_contato
    email_from='portalsoftwarelivre@serpro.gov.br'
    try:
       mMsg = "To: " + email_to + "\n"
       mMsg = mMsg + "From: " + email_from + "\n"
       mMsg = mMsg + "Mime-Version: 1.0\n"
       mMsg = mMsg + "Content-Type: text/plain; charset=UTF-8\n"
       mMsg = mMsg + mensagem + "  \n"
       context.MailHost.send(mMsg, subject=assunto)
       context.plone_utils.addPortalMessage((u'Protocolo criado e enviado com sucesso.'))
       protocoloTool.setarPermissaoUsuarioComum(usuario_atual)
       return state.set(status='success')
    except:
       portal = getToolByName(context,'portal_url').getPortalObject()
       pastaProtocolo = getattr(portal,'protocolo-brasilia')
       pastaProtocolo.manage_delObjects(strReturn)
       context.plone_utils.addPortalMessage((u'Problema no envio do Protocolo.'))
       protocoloTool.setarPermissaoUsuarioComum(usuario_atual)
       return state.set(status='failure')

else:
    context.plone_utils.addPortalMessage((u'Problema na criação do Protocolo.'))
    protocoloTool.setarPermissaoUsuarioComum(usuario_atual)
    return state.set(status='failure')

