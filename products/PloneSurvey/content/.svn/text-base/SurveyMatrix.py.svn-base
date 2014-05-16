import string
from AccessControl import ClassSecurityInfo

from Products.Archetypes.public import *
from Products.CMFCore import CMFCorePermissions
from Products.CMFCore.utils import getToolByName

from Products.PloneSurvey.config import SELECT_INPUT_TYPE
from Products.PloneSurvey.content.BaseQuestion import BaseQuestion, BaseQuestionSchema

MainSchema = BaseQuestionSchema.copy()
del MainSchema['required']

schema = MainSchema + Schema((

    LinesField('answerOptions',
        searchable=0,
        required=1,
        default=("Yes", "No"),
        widget=LinesWidget(
            label="Answer options",
            label_msgid="label_answer_options",
            description="""Enter the options you want to be available to the user here.
                           Press enter to seperate the options.""",
            description_msgid="help_answer_options",
            i18n_domain="plonesurvey",
           ),
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

class SurveyMatrix(OrderedBaseFolder, BaseQuestion):
    """A matrix of questions within a survey"""
    schema = schema
    #actions = Actions
    immediate_view = "base_edit"
    global_allow = 0
    filter_content_types = 1
    allowed_content_types = (['Survey Matrix Question',])
    archetypes_name = portal_type = "Survey Matrix"
    meta_type = "SurveyMatrix"
    content_icon = "icon_plonesurvey_small.gif"
    include_default_actions = 1
    _at_rename_after_creation = True

    security = ClassSecurityInfo()

    # A matrix doesn't have answers of its own, but it needs to have an
    # 'answers' attribute so that it plays properly with getAnswerFor etc.
    answers = {}

    security.declareProtected(CMFCorePermissions.View, 'getAbstract')
    def getAbstract(self, **kw):
        return self.Description()

    security.declareProtected(CMFCorePermissions.ModifyPortalContent, 'setAbstract')
    def setAbstract(self, val, **kw):
        self.setDescription(val)

    security.declareProtected(CMFCorePermissions.View, 'getRequired')
    def getRequired(self):
        """Return nothing to sidestep validation"""
        return 0

    security.declareProtected(CMFCorePermissions.View, 'getQuestions')
    def getQuestions(self):
        """Return the questions for this part of the survey"""
        questions = self.getFolderContents(
            contentFilter={'portal_type':[
                'Survey Matrix Question',
                ]},
            full_objects=True)
        return questions

registerType(SurveyMatrix)