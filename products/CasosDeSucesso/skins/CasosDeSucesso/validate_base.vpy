## Script (Python) "validate_base"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##
from Products.CMFPlone import PloneMessageFactory as _

errors = {}
errors = context.validate(REQUEST=context.REQUEST, errors=errors, data=1, metadata=0)

erro = container.restrictedTraverse('@@captcha_view').valida(context.REQUEST.get('captcha',''))
if erro:
    errors['erro_captcha'] =  _(erro)

if errors:
    return state.set(status='failure', errors=errors, portal_status_message='Please correct the indicated errors.')
else:
    return state.set(portal_status_message='Changes saved.')
