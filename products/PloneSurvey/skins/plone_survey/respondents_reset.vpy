form = context.REQUEST.form
_ = context.translate

users = form['users']

if  not users:
    pass
elif not isinstance(users, str):
    for user in users:
        context.resetForUser(user)
else:
    context.resetForUser(users)

users = ', '.join(users)

if state.getErrors():
    return state.set(status='failure', portal_status_message=_(msgid='text_survey_reset_error', default='Survey did not reset correctly', domain='plonesurvey'))
else:
    return state.set(status='success', portal_status_message=_(msgid='text_survey_users_reset_error', default='${users} have been reset', mapping={'users':users}, domain='plonesurvey'))
return state
