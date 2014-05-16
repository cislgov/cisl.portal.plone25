file = context.buildSpreadsheetUrl()
setHeader = context.REQUEST.RESPONSE.setHeader
setHeader('Content-Type','application/vnd.ms-excel')
setHeader('Content-disposition','attachment; filename=%s' % file)
lines = []
header = '"user",'
for question in context.getAllQuestionsInOrder():
    header += '"' + question.Title() + '",'
#    if question.getCommentType():
#        header += '"' + question.getCommentLabel() + '",'

header += '"completed"'
print header

for user in context.getRespondents():
    line = []
    line.append('"' + test(user, user, "Anonymous") + '"')
    for question in context.getAllQuestionsInOrder():
        answer = ""
        if question.getInputType() in ['text', 'area']:
            if question.getAnswerFor(user):
                answer = '"' + question.getAnswerFor(user).replace('"',"'") + '"'
            else:
                answer = "Blank"
        elif question.getInputType() in ['checkbox', 'multipleSelect']:
            options = question.getAnswerOptions()
            answerList = question.getAnswerFor(user)
            if answerList and not isinstance(answerList, str):
                for option in options:
                  if answerList.count(option) > 0:
                    answer += '1;'
                  else:
                    answer += '0;'
                answer = '"' + answer[0:len(answer)-1] + '"'
            elif answerList:
                answer = '"' + answerList + '"'
            else:
                answer = ''
        else:
            options = question.getAnswerOptions()
            answerLabel = question.getAnswerFor(user)
            answer = str(len(options))
            i = 0
            while i < len(options):
                if options[i] == answerLabel:
                    answer = str(i)
                    break
                i = i + 1
        line.append(answer)
#        if question.getCommentType():
#            line.append('"' + test(question.getCommentsFor(user), question.getCommentsFor(user).replace('"',"'"), "Blank") + '"')
    line.append('"' + test(context.checkCompletedFor(user), "Completed", "Not Completed") + '"')
    line = ','.join(line)
    lines.append(line)

for l in lines:
    print l
return printed
