form = context.REQUEST.form
_ = context.translate
questions = context.getQuestions()

if form.get('form.button.save', ''):
    # skip validation
    for q in questions:
        value = form.get(q.getId(), '')
        comments = form.get("%s_comments" % q.getId(), '')
        if q.portal_type != 'Survey Matrix':
            q.addAnswer(value, comments)
        if q.portal_type == 'Survey Matrix':
            matrix_questions = q.getQuestions()
            for matrix_q in matrix_questions:
                value = form.get(matrix_q.getId(), '')
                matrix_q.addAnswer(value)
    return state.set(status='success')

for q in questions:
    value = form.get(q.getId(), '')
    if q.getRequired() and not value:
        error_msg = context.translate(
            default='Please provide an answer for this question',
            msgid='please_provide_answer',
            domain='plonesurvey')
        state.setError(q.getId(), error_msg)
    if value and hasattr(q, 'getValidation') and q.getValidation() != 'None':
        validation_output = q.validateQuestion(value)
        if validation_output != 1:
            state.setError(q.getId(), validation_output)
    comments = form.get("%s_comments" % q.getId(), '')
    if q.portal_type == 'Survey Text Question':
        if len(value) > q.getMaxLength():
            state.setError(q.getId(), "Answer too long, must be less than %s characters" % q.getMaxLength())
        else:
            q.addAnswer(value, comments)
    elif q.portal_type != 'Survey Matrix':
        q.addAnswer(value, comments)
    elif q.portal_type == 'Survey Matrix':
        matrix_questions = q.getQuestions()
        qnum = ''
        for matrix_q in matrix_questions:
            value = form.get(matrix_q.getId(), '')
            if matrix_q.getRequired() and not value:
               qnum = qnum + ' ' + str(matrix_q.getId()) + ','
            matrix_q.addAnswer(value)
        if qnum != '':
            qnum = qnum[:-1]
            error_msg = context.translate(
                default='Please provide an answer for the question',
                msgid='please_provide_answer_for',
                domain='plonesurvey')
            state.setError(q.getId(), "%s %s" % (error_msg, qnum))

if state.getErrors():
    return state.set(status='failure', portal_status_message=_(msgid='text_correct_errors', domain='plonesurvey', default='Please correct the errors shown'))
else:
    return state.set(status='success')
return state
