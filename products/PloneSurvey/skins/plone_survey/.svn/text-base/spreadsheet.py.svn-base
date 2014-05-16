file = context.buildSpreadsheetUrl()
setHeader = context.REQUEST.RESPONSE.setHeader
setHeader('Content-Type','application/vnd.ms-excel')
setHeader('Content-disposition','attachment; filename=%s' % file)
lines = []
header = '"EO", "Question", "Yes", "No", "Comments"'
print header

for question in context.getAllQuestionsInOrder():
    line = []
    #line.append('"' + question.getEnablingObjective() + '"')
    line.append('"' + question.Title() + '"')
    try:
        answers = question.getAggregateAnswers()
    except AttributeError:
        continue
    # we only cater for yes / no answers
    for option in ["Yes","No"]:
        line.append('"' + str(answers.get(option, 0)) + '"')
    # comments are joined into a single string
    comments = " ".join(["%s: %s //   " % (q['userid'], q['comments']) for q in question.getComments() if q['comments'].strip()])
    # replace double quotes and linebreaks which may confuse spreadsheet imports
    comments = comments.replace('"',"'")
    comments = comments.replace("\r", " ")
    comments = comments.replace("\n", " ")
    # join all the fields together
    line.append('"' + comments + '"')
    line = ','.join(line)
    lines.append(line)

for l in lines:
    print l
return printed