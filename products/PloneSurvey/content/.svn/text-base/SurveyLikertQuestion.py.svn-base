from AccessControl import ClassSecurityInfo

from Products.Archetypes.public import *
from Products.CMFCore import CMFCorePermissions

from Products.PloneSurvey.config import SELECT_INPUT_TYPE, LIKERT_OPTIONS
from Products.PloneSurvey.content.BaseQuestion import BaseQuestion, BaseQuestionSchema
from Products.PloneSurvey.config import USE_BTREE

schema = BaseQuestionSchema + Schema((

    LinesField('answerOptions',
        searchable=0,
        required=0,
        default=LIKERT_OPTIONS,
        widget=LinesWidget(visible=0,),
        ),

    StringField('inputType',
        searchable=0,
        required=0,
        vocabulary=SELECT_INPUT_TYPE,
        widget=SelectionWidget(
            label="Input Type",
            label_msgid="label_input_type",
            description="Please select what type of input you would like to use for this question.",
            description_msgid="help_input_type",
            i18n_domain="plonesurvey",
           ),
        ),

    ))

class SurveyLikertQuestion(BaseQuestion):
    """A question with select vocab within a survey"""
    schema = schema
    #actions = Actions
    archetypes_name = portal_type = "Survey Likert Question"
    meta_type = "SurveyLikertQuestion"
    content_icon = "icon_plonesurvey_small.gif"

    security = ClassSecurityInfo()

    security.declareProtected(CMFCorePermissions.View, 'getAggregateAnswers')
    def getAggregateAnswers(self):
        """Return a mapping of aggregrate answer values,
        suitable for a histogram"""
        if self.getInputType() in ['area', 'text']:
            return {}
        aggregate_answers = {}
        options = self.getAnswerOptions()
        for option in options:
            aggregate_answers[option] = 0
        for k, answer in self.answers.items():
            if answer['value']:
                if isinstance(answer['value'], str):
                    try:
                        aggregate_answers[answer['value']] += 1
                    except KeyError:
                        aggregate_answers[answer['value']] = 1
                else:
                    for value in answer['value']:
                        try:
                            aggregate_answers[value] += 1
                        except KeyError:
                            aggregate_answers[value] = 1
        return aggregate_answers

    security.declareProtected(CMFCorePermissions.View, 'getPercentageAnswers')
    def getPercentageAnswers(self):
        """Return a mapping of aggregrate answer values,
        suitable for a barchart"""
        max = 0
        aggregate_answers = self.getAggregateAnswers()
        for k,v in aggregate_answers.items():
            if v > max:
                max = v
        pct_aggregate_answers = {}
        for k,v in aggregate_answers.items():
            if v == 0:
                value = 0
            else:
                value = v/float(max)
            pct_aggregate_answers[k] = int(value * 100)
        return pct_aggregate_answers

registerType(SurveyLikertQuestion)