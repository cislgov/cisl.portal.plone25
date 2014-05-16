##Controller Python Script "unlock_users"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=obj_paths=[]
##title=
##
usuarios = obj_paths

if usuarios:
    for userid in usuarios:
        context.portal_password.debloqueiaUser(userid)

return state

