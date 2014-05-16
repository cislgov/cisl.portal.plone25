import string
from AccessControl import ClassSecurityInfo

from Products.Archetypes.public import *
from Products.CMFCore import CMFCorePermissions
from Products.CMFCore.utils import getToolByName

from Products.PloneSurvey.config import SELECT_INPUT_TYPE, BARCHART_COLORS
from Products.PloneSurvey.content.BaseQuestion import BaseQuestion, BaseQuestionSchema
from Products.PloneSurvey.config import USE_BTREE

MainSchema = BaseQuestionSchema.copy()
del MainSchema['commentType']
del MainSchema['commentLabel']
del MainSchema['abstract']

schema = MainSchema

class SurveyMatrixQuestion(BaseQuestion):
    """A question in a matrix within a survey"""
    schema = schema
    #actions = Actions
    immediate_view = "base_edit"
    global_allow = 0
    filter_content_types = 1
    allowed_content_types = ()
    archetypes_name = portal_type = "Survey Matrix Question"
    meta_type = "SurveyMatrixQuestion"
    content_icon = "icon_plonesurvey_small.gif"
    include_default_actions = 1
    _at_rename_after_creation = True

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

registerType(SurveyMatrixQuestion)