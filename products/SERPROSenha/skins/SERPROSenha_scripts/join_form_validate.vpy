## Controller Validator "join_form_validate"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=username='',email='',password='',password_confirm=''
##title=validates the Registration of a User
##
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFCore.utils import getToolByName


ptool = getToolByName(context, 'portal_password')
limpwd = int(ptool.getLim_password())
maxpwd = int(ptool.getLim_max_password())

reg_tool=context.portal_registration
def missing(field):
    state.setError(field, _(u'This field is required, please provide some information.'), 'input_required')
def nomatch(field):
    state.setError(field, _(u'Passwords do not match.'), 'nomatch_password')
def minlimit(field):
    state.setError(field, _(u'Minimo %s caracteres.'%limpwd), 'min_password')
def maxlimit(field):
    state.setError(field, _(u'Maximo %s caracteres.'%maxpwd), 'max_limit')
def notallowed(field):
    state.setError(field, _(u'This username is reserved. Please choose a different name.'), 'not_allowed')
def invalidpassword(field):
    state.setError(field, _(u'Favor informar uma senha diferente do id do usuario.'), 'not_allowed')
def senhaforte(field):
    state.setError(field, _(u'Favor informar uma senha que contenha uma combina��o de caracteres:    mai�sculos ou min�sculos e num�ricos; ou mai�sculos ou min�sculos e especiais; ou num�ricos e especiais.'), 'senhaforte_password')

if not username:
    missing('username')
if not email:
    missing('email')
if username and username == context.portal_url.getPortalObject().getId():
    notallowed('username')

properties = context.portal_properties.site_properties
if not properties.validate_email:
     if password!=password_confirm:
         nomatch('password')
         nomatch('password_confirm')

     if not password:
         missing('password')
     if not password_confirm:
         missing('password_confirm')

     if not state.getError('password') and len(password) < limpwd:
         minlimit('password')
         minlimit('password_confirm')
     
     #verifica se o m�ximo de caracteres foi habilitado
     if maxpwd >= limpwd: 
         if not state.getError('password') and len(password) > maxpwd:
             maxlimit('password')
             maxlimit('password_confirm')

     #imposibilita que usu�rio informe uma senha identica ao id do usu�rio utilizado para se autenticar
     if not (state.getError('password')) and (password == username):
         invalidpassword ('password')
         invalidpassword ('password_confirm')

     #verificar se a senha cont�m numeros ou caracteres especiais
     ok, message =  ptool.senhaForte( password ) 
     if not ok:
         senhaforte('password')
         senhaforte('password_confirm')

if not state.getError('username') and not reg_tool.isMemberIdAllowed(username):
    state.setError('username',
                   _(u'The login name you selected is already in use or is not valid. Please choose another.'),
                   'username_invalid' )

if state.getErrors():
    context.plone_utils.addPortalMessage(_(u'Please correct the indicated errors.'))
    return state.set(status='failure')
else:
    context.plone_utils.addPortalMessage(_(u'You have been registered.'))
    return state

