## Script (Python) "content_edit_impl_casodesucesso"
##title=Edit content
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=state, id=''
##

from Products.CMFCore.utils import getToolByName

REQUEST = context.REQUEST
old_id = context.getId()

try:
    new_context = context.portal_factory.doCreate(context, id)
except AttributeError:
    # Fallback for AT + plain CMF where we don't have a portal_factory
    new_context = context
    
new_context.processForm()

# Get the current language and put it in request/LANGUAGE
form = REQUEST.form
if form.has_key('current_lang'):
    form['language'] = form.get('current_lang')

portal_status_message = context.translate(
    msgid='message_content_changes_saved',
    default='Content changes saved.')

portal_status_message = REQUEST.get('portal_status_message',
                                    portal_status_message)

# handle navigation for multi-page edit forms
next = not REQUEST.get('form_next', None) is None
previous = not REQUEST.get('form_previous', None) is None
fieldset = REQUEST.get('fieldset', None)
schemata = new_context.Schemata()

if next or previous:
    s_names = [s for s in schemata.keys() if s != 'metadata']

    if previous:
        s_names.reverse()

    next_schemata = None
    try:
        index = s_names.index(fieldset)
    except ValueError:
        raise 'Non-existing fieldset: %s' % fieldset
    else:
        index += 1
        if index < len(s_names):
            next_schemata = s_names[index]
            return state.set(status='next_schemata',
                             context=new_context,
                             fieldset=next_schemata,
                             portal_status_message=portal_status_message)

    if next_schemata != None:
        return state.set(status='next_schemata', \
                 context=new_context, \
                 fieldset=next_schemata, \
                 portal_status_message=portal_status_message)
    else:
        raise 'Unable to find next field set after %s' % fieldset

env = state.kwargs
reference_source_url = env.get('reference_source_url')
if reference_source_url is not None:
    reference_source_url = env['reference_source_url'].pop()
    reference_source_field = env['reference_source_field'].pop()
    reference_source_fieldset = env['reference_source_fieldset'].pop()
    portal = context.portal_url.getPortalObject()
    reference_obj = portal.restrictedTraverse(reference_source_url)
    portal_status_message = context.translate(
        msgid='message_reference_added',
        default='Reference Added.')

    edited_reference_message = context.translate(
        msgid='message_reference_edited',
        default='Reference Edited.')

    # Avoid implicitly creating a session if one doesn't exists
    session = None
    sdm = getToolByName(context, 'session_data_manager', None)
    if sdm is not None:
        session = sdm.getSessionData(create=0)

    # update session saved data, if session exists.
    uid = new_context.UID()
    if session is not None:
        saved_dic = session.get(reference_obj.getId(), None)
        if saved_dic:
            saved_value = saved_dic.get(reference_source_field, None)
            if same_type(saved_value, []):
                # reference_source_field is a multiValued field, right!?
                if uid in saved_value:
                    portal_status_message = edited_reference_message
                else:
                    saved_value.append(uid)
            else:
                if uid == saved_value:
                    portal_status_message = edited_reference_message
                else:
                    saved_value = uid
            saved_dic[reference_source_field] = saved_value
            session.set(reference_obj.getId(), saved_dic)

    # XXX disabled mark creation flag
    ## context.remove_creation_mark(old_id)

    kwargs = {
        'status':'success_add_reference',
        'context':reference_obj,
        'portal_status_message':portal_status_message,
        'fieldset':reference_source_fieldset,
        'field':reference_source_field,
        'reference_focus':reference_source_field,
        }
    return state.set(**kwargs)

if state.errors:
    errors = state.errors
    s_items = [(s, schemata[s].keys()) for s in schemata.keys()]
    fields = []
    for s, f_names in s_items:
        for f_name in f_names:
            fields.append((s, f_name))
    for s_name, f_name in fields:
        if errors.has_key(f_name):
            REQUEST.set('fieldset', s_name)
            return state.set(
                status='failure',
                context=new_context,
                portal_status_message=portal_status_message)

# XXX disabled mark creation flag
## context.remove_creation_mark(old_id)

if not state.errors:
    from Products.Archetypes import transaction_note
    transaction_note('Edited %s %s at %s' % (new_context.meta_type,
                                             new_context.title_or_id(),
                                             new_context.absolute_url()))

try:
    new_context.portal_workflow.doActionFor(new_context, 'submit')
except:
    pass
 
member = new_context.portal_membership.getAuthenticatedMember()
isManager = member.has_role('Manager')

if isManager:
    return state.set(status='success',
                     context=new_context,
                     portal_status_message=portal_status_message)

else:
    utils = context.restrictedTraverse('@@casodesucesso_utils_view')
    portal = context.portal_url.getPortalObject()
    try:
        nome_portal = portal.title
        de = portal.email_from_address
        para = context.portal_properties.serpro_casodesucesso_properties.email_administrator
        assunto = 'Novo Caso de Sucesso cadastrado'
        mensagem = """
    O portal %s recebeu um novo caso de sucesso:
                
    %s 
    """ % (nome_portal, new_context.absolute_url())
                    
        utils.enviarEmail(de=de, para=para, assunto=assunto, mensagem=mensagem)
    except:
        pass
    return state.set(status='success',
                     context=new_context.aq_parent,
                     portal_status_message=portal_status_message)
