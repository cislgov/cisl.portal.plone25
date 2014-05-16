file = context.buildSpreadsheetUrl()
setHeader = context.REQUEST.RESPONSE.setHeader
setHeader('Content-Type','application/vnd.ms-excel')
setHeader('Content-disposition','attachment; filename=%s' % file)
lines = []
header = '"user",'
for question in context.getAllQuestionsInOrder():
    if question.meta_type != "SurveyTextQuestion":
        header += '"' + question.Title() + '",'
    #    if question.getCommentType():
    #        header += '"' + question.getCommentLabel() + '",'

header += '"completed"'
print header

for user in context.getRespondents():
    line = []
    line.append('"' + test(user, user, "Anonymous") + '"')
    for question in context.getAllQuestionsInOrder():
        if question.meta_type != "SurveyTextQuestion":
            # handle there being no answer (e.g branched question)
            if question.getAnswerFor(user):
              answer = question.getAnswerFor(user)
              if not isinstance(answer, str):
                  answers = ''
                  for value in answer:
                      if answers != '':
                          answers = answers + ', ' + value
                      else:
                          answers = value
                  answer = answers
            try:
                answer = answer.replace('"',"'")
            except:
                answer = "Blank"
            line.append('"' + str(answer) + '"')
 #       if question.getCommentType():
 #           if question.getCommentsFor(user):
 #               line.append('"' + test(question.getCommentsFor(user), question.getCommentsFor(user).replace('"',"'"), "Blank") + '"')
    line.append('"' + test(context.checkCompletedFor(user), "Completed", "Not Completed") + '"')
    line = ','.join(line)
    lines.append(line)

for l in lines:
    print l
return printed
