## Controller Validator "login_form_validate"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Validate login
##
from Products.CMFPlone import PloneMessageFactory as _

request = context.REQUEST
session = request.SESSION
js_enabled = request.get('js_enabled',0) # is javascript enabled?
js_enabled = js_enabled=='1' or js_enabled==1
cookies_enabled = request.get('cookies_enabled',0) # are cookies enabled?
cookies_enabled = cookies_enabled=='1' or cookies_enabled==1

qtd_tentativas = context.portal_password.getQtd_tentativas()

passwd = request.get('__ac_password',0) # recupera o password

if js_enabled and not cookies_enabled:
    context.plone_utils.addPortalMessage(_(u'You must enable cookies before you can log in.'))
    state.set(status='enable_cookies')
    return state

mt=context.portal_membership
if str(context.portal_password.getEnb_lock_login()) == 'Captcha':
   captcha = context.REQUEST.get('captcha', None)
   if not captcha:
       state.setError('erro_captcha', _(u'This field is required, please provide some information.'), 'input_required')
   if captcha:
       if session['captcha'] != captcha and session['som'] != captcha:
           state.setError('erro_captcha',_(u'Os caracteres sao diferentes da imagem!'))
   if state.getErrors():        
       context.plone_utils.addPortalMessage(_(u'Captcha erro! Os caracteres sao diferentes da imagem!'))
       state.set(status='failure_page')

#verifica se o Bloqueio de Login esta ativado e se o usuário informou uma senha
if str(context.portal_password.getEnb_lock_login()) == 'Bloqueio' and passwd:
    if mt.isAnonymousUser():
        membro = mt.getMemberById(request.get('login_name', None))
        if membro:
            #verifica se o usuário esta bloqueado ou não
            failMessage=context.portal_password.validaSenha(userid=(request.get('login_name', None)))
            if failMessage:
#                context.plone_utils.addPortalMessage(failMessage)
                context.plone_utils.addPortalMessage(_(u'Falha no acesso. Apos ' +str(qtd_tentativas)+' tentativas o login sera bloqueado. Um e-mail sera enviado apos o bloqueio.'))
                state.set(status='failure')
                return state

    if not mt.isAnonymousUser():
        member=mt.getAuthenticatedMember()
        qtd = context.portal_password.getQtd_tentativas() 
        error_count = member.getProperty('error_count')
        error_count = int(error_count)
        if error_count >= qtd:
            #verifica se o usuário esta bloqueado ou não
            failMessage=context.portal_password.validaSenha(userid=member)
            if failMessage:
#                context.plone_utils.addPortalMessage(failMessage)
                context.plone_utils.addPortalMessage(_(u'Falha no acesso. Apos ' +str(qtd_tentativas)+' tentativas o login sera bloqueado. Um e-mail sera enviado apos o bloqueio.'))
                state.set(status='failure')
                return state

if mt.isAnonymousUser():
    if js_enabled: # javascript is enabled - we can diagnose the failure
        auth = getattr(context, 'cookie_authentication', None) # using cookie authentication?
        if auth:
            user_name = request.get('login_name', None)
            password_empty = request.get('pwd_empty', None)=='1'
            ac_name = auth.name_cookie
            ac_password = auth.pw_cookie

            if not user_name:
                # no user name
                state.setError(ac_name, _(u'Please enter your login name.'), 'login_name_required')
            if password_empty:
                state.setError(ac_password, _(u'Please enter your password.'), 'password_required')
            verify_login_name = context.portal_properties.site_properties.getProperty('verify_login_name', 0)
            if user_name and verify_login_name:
                # XXX mixing up username and loginname here
                if mt.getMemberById(user_name) is None:
                    state.setError(ac_name, _(u'Login name not found.'), 'login_name_not_found')
                elif not password_empty:
                    state.setError(ac_password, _(u'Password incorrect.'), 'password_incorrect')

        #verifica se o Bloqueio de Login esta ativado
        if str(context.portal_password.getEnb_lock_login()) == 'Bloqueio':
            context.plone_utils.addPortalMessage(_(u'Falha no acesso. Apos ' +str(qtd_tentativas)+' tentativas o login sera bloqueado. Um e-mail sera enviado apos o bloqueio.'))
            state.set(status='failure')
        else:
            context.plone_utils.addPortalMessage(_(u'Falha no acesso.'))
            state.set(status='failure')

    else: # no javascript - do low tech login failure
        if str(context.portal_password.getEnb_lock_login()) == 'Bloqueio':
            context.plone_utils.addPortalMessage(_(u'Falha no acesso. Apos ' +str(qtd_tentativas)+' tentativas o login sera bloqueado. Um e-mail sera enviado apos o bloqueio.'))
            state.set(status='failure')
        else: 
            context.plone_utils.addPortalMessage(_(u'Falha no acesso.'))
            state.set(status='failure_page')

return state
