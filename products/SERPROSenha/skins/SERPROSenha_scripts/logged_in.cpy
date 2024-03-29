## Controller Python Script "logged_in"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Initial post-login actions
##
from Products.CMFPlone import PloneMessageFactory as _
REQUEST=context.REQUEST

# If someone has something on their clipboard, expire it.
if REQUEST.get('__cp', None) is not None:
    REQUEST.RESPONSE.expireCookie('__cp', path='/')

membership_tool=context.portal_membership
if membership_tool.isAnonymousUser():
    REQUEST.RESPONSE.expireCookie('__ac', path='/')
    context.plone_utils.addPortalMessage(_(u'Login failed'))
    return state.set(status='failure')
    
member = membership_tool.getAuthenticatedMember()
login_time = member.getProperty('login_time', '2000/01/01')
initial_login = int(str(login_time) == '2000/01/01')
state.set(initial_login=initial_login)

must_change_password = member.getProperty('must_change_password', 0)
state.set(must_change_password=must_change_password)

if initial_login:
    state.set(status='initial_login')
elif must_change_password:
    state.set(status='change_password')

#zera o n�mero de erros de login
member.setProperties(error_count=str(0))
membership_tool.setLoginTimes()
membership_tool.createMemberArea()

return state
