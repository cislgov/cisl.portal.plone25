from AccessControl import ClassSecurityInfo

from Products.Archetypes.public import *
from Products.CMFCore import CMFCorePermissions
from Products.validation import validation

from Products.PloneSurvey.config import INPUT_TYPE, COMMENT_TYPE, TEXT_VALIDATORS
from Products.PloneSurvey.content.BaseQuestion import BaseQuestion, BaseQuestionSchema
from Products.PloneSurvey.config import USE_BTREE

schema = BaseQuestionSchema + Schema((

    LinesField('answerOptions',
        searchable=0,
        required=0,
        default=("Yes", "No"),
        widget=LinesWidget(
            label="Answer options",
            label_msgid="label_answer_options",
            description="""Enter the options you want to be available to the user here.
                           This only applies to the selection box, multiple selection box,
                           checkbox and radio button input types (selected below).
                           The text input options allow the user to type the input
                           rather than selecting from options. Press enter to seperate
                           the options.""",
            description_msgid="help_answer_options",
            i18n_domain="plonesurvey",),
        ),

    StringField('inputType',
        searchable=0,
        required=0,
        vocabulary=INPUT_TYPE,
        widget=SelectionWidget(
            label="Input Type",
            label_msgid="label_input_type",
            description="Please select what type of input you would like to use for this question.",
            description_msgid="help_input_type",
            i18n_domain="plonesurvey",
           ),
        ),

    StringField('validation',
        searchable=0,
        required=0,
        vocabulary='getValidators',
        widget=SelectionWidget(
            label="Validation",
            label_msgid="label_validation",
            description="Select a validation for this question",
            description_msgid="help_validation",
            i18n_domain="plonesurvey",
           ),
        ),

    ))

class SurveyQuestion(BaseQuestion):
    """A question within a survey"""
    schema = schema
    #actions = Actions
    archetypes_name = portal_type = "Survey Question"
    meta_type = "SurveyQuestion"
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

    security.declareProtected(CMFCorePermissions.View, 'getValidators')
    def getValidators(self):
        """Return a list of validators"""
        validator_list = ['None', ]
        validator_list.extend(TEXT_VALIDATORS)
        return validator_list

    security.declareProtected(CMFCorePermissions.View, 'getValidators')
    def validateQuestion(self, value):
        """Return a list of validators"""
        validator = self.getValidation()
        if validator:
            v = validation.validatorFor(validator)
            return v(value)
        else:
            return True

    security.declareProtected(CMFCorePermissions.View, 'getAverageAnswer')
    def getAverageAnswer(self, raise_exception="no"):
        """Return an average of numeric answers.  If *raise_exception*
        is passed, then this method will cause an error if any answers
        are not numeric"""
        raise "NotImplemented"

    security.declareProtected(CMFCorePermissions.View, 'getHistogram')
    def getHistogram(self):
        """Return an image representing answer data"""
        raise "NotImplemented"

registerType(SurveyQuestion)