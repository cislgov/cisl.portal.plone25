import string
from DateTime import DateTime
from ZODB.POSException import ConflictError

from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import *
from Products.CMFCore import CMFCorePermissions
# needed for getAnonymousID
from Products.CMFCore.utils import getToolByName

from Products.PloneSurvey import permissions as perms
from Products.PloneSurvey.config import SURVEY_STATUS, NOTIFICATION_METHOD, BARCHART_COLORS

HeaderSchema = BaseSchema.copy()

schema = HeaderSchema + Schema((

    StringField('abstract',
        searchable=1,
        required=0,
        accessor="getAbstract",
        edit_accessor="getAbstract",
        mutator="setAbstract",
        widget=TextAreaWidget(
            label="Survey description",
            label_msgid="label_description",
            description="Add a short description of the survey here.",
            description_msgid="help_description",
            rows=5,
            i18n_domain="plonesurvey",
           ),
        ),

    TextField('body',
        searchable = 1,
        required=0,
        schemata="Introduction",
        default_content_type    = 'text/html',
        default_output_type     = 'text/html',
        allowable_content_types=('text/plain',
                                 'text/structured',
                                 'text/html',
                                ),
        widget = RichWidget(description = "Enter an introduction for the survey.",
                            label = "Introduction",
                            label_msgid = 'label_introduction',
                            description_msgid = 'help_introduction',
                            rows = 5,
                            i18n_domain="plonesurvey",
                           ),
        ),

    TextField('thankYouMessage',
        required=0,
        searchable=0,
        default_method="translateThankYouMessage",
        widget=TextAreaWidget(
            label="'Thank you' message text",
            label_msgid="label_thank",
            description="""This is the message that will be displayed to the
                           user when they complete the survey.""",
            description_msgid="help_thankyou",
            i18n_domain="plonesurvey",
           ),
        ),

    TextField('savedMessage',
        required=0,
        searchable=0,
        default_method="translateSavedMessage",
        widget=TextAreaWidget(
            label="'Saved' message test",
            label_msgid="label_saved_text",
            description="""This is the message that will be displayed to the user
                           when they save the survey, but don't submit it.""",
            description_msgid="help_saved_text",
            i18n_domain="plonesurvey",
           ),
        ),

    StringField('exitUrl',
        required=0,
        searchable=0,
        widget=StringWidget(
            label="Exit URL",
            label_msgid="label_exit_url",
            description="""This is the URL that the user will be directed to on completion of the survey.
                           Use "http://site.to.go.to/page" or "route/to/page" for this portal""",
            description_msgid="help_exit_url",
            i18n_domain="plonesurvey",
          ),
        ),

    BooleanField('allowAnonymous',
        searchable=0,
        required=0,
        widget=BooleanWidget(
            label="Allow Anonymous",
            label_msgid="label_allow_anonymous",
            i18n_domain="plonesurvey",
          ),
        ),

    BooleanField('allowSave',
        searchable=0,
        required=0,
        widget=BooleanWidget(
            label="Allow Save Functionality",
            label_msgid="label_allow_save",
            description="Allow logged in users to save survey for finishing later.",
            description_msgid="help_allow_save",
            i18n_domain="plonesurvey",
          ),
        ),

    StringField('surveyNotificationEmail',
        required=0,
        searchable=0,
        widget=StringWidget(
            label="Survey Notification Email Address",
            label_msgid="label_survey_notification_email",
            description="Enter an email address to receive notifications of survey completions.",
            description_msgid="help_survey_notification_email",
            i18n_domain="plonesurvey",
          ),
        ),

    StringField('surveyNotificationMethod',
        required=0,
        searchable=0,
        vocabulary=NOTIFICATION_METHOD,
        widget=SelectionWidget(
            label="Survey Notification Method",
            label_msgid="label_survey_notification_method",
            description="Select a method to receive notification emails.",
            description_msgid="help_survey_notification_method",
            i18n_domain="plonesurvey",
           ),
        ),

    StringField('completedFor',
        searchable=0,
        required=0,
        default=[],
        widget=StringWidget(visible=0,),
        ),

    ))

Actions = (
    {
    'id' : 'view',
    'name' : 'View',
    'action' : 'string:${object_url}/survey_view',
    'permissions' : (CMFCorePermissions.View, )
    },
    {
    'id' : 'results',
    'name' : 'Results',
    'action' : 'string:${object_url}/survey_view_results',
    'permissions' : (CMFCorePermissions.ModifyPortalContent, )
    },
    {
    'id' : 'reset',
    'name' : 'Reset',
    'action' : 'string:${object_url}/survey_reset_form',
    'permissions' : (CMFCorePermissions.ModifyPortalContent, )
    },
    {
    'id' : 'overview',
    'name' : 'Overview',
    'action' : 'string:${object_url}/survey_overview',
    'permissions' : (CMFCorePermissions.ModifyPortalContent, )
    },
    {
    'id' : 'sharing',
    'name' : 'Sharing',
    'action' : 'string:${object_url}/folder_localrole_form',
    'permissions' : (CMFCorePermissions.ManageProperties, )
    },
)

class Survey(OrderedBaseFolder):
    """You can add questions to surveys"""
    schema = schema
    actions = Actions
    immediate_view = "base_edit"
    global_allow = 1
    filter_content_types = 1
    allowed_content_types = (['Survey Question',
                              'Survey Likert Question',
                              'Survey Matrix',
                              'Survey Select Question',
                              'Survey Text Question',
                              'Sub Survey'])
    archetypes_name = portal_type = "Survey"
    meta_type = "Survey"
    content_icon = "icon_plonesurvey_small.gif"
    include_default_actions = 1
    _at_rename_after_creation = True

    security = ClassSecurityInfo()

    security.declareProtected(CMFCorePermissions.View, 'getAbstract')
    def getAbstract(self, **kw):
        return self.Description()

    security.declareProtected(CMFCorePermissions.ModifyPortalContent, 'setAbstract')
    def setAbstract(self, val, **kw):
        self.setDescription(val)

    security.declareProtected(CMFCorePermissions.View, 'isMultipage')
    def isMultipage(self):
        """Return true if there is more than one page in the survey"""
        if self.getFolderContents(contentFilter={'portal_type':'Sub Survey',}):
            return True

    security.declareProtected(CMFCorePermissions.View, 'getQuestions')
    def getQuestions(self):
        """Return the questions for this part of the survey"""
        questions = self.getFolderContents(
            contentFilter={'portal_type':[
                'Survey Question',
                'Survey Likert Question',
                'Survey Matrix',
                'Survey Select Question',
                'Survey Text Question',
                ]},
            full_objects=True)
        return questions

    security.declareProtected(CMFCorePermissions.View, 'getAllQuestions')
    def getAllQuestions(self):
        """Return all the questions in the survey"""
        portal_catalog = getToolByName(self, 'portal_catalog')
        questions = []
        path = string.join(self.getPhysicalPath(), '/')
        results = portal_catalog.searchResults(portal_type = ['Survey Question',
                                                              'Survey Likert Question',
                                                              'Survey Matrix Question',
                                                              'Survey Select Question',
                                                              'Survey Text Question',],
                                               path = path,
                                               order = 'getObjPositionInParent')
        for result in results:
            questions.append(result.getObject())
        return questions

    security.declareProtected(CMFCorePermissions.View, 'getAllQuestionsInOrder')
    def getAllQuestionsInOrder(self, include_sub_survey=False):
        """Return all the questions in the survey"""
        questions = []
        objects = self.getFolderContents(
            contentFilter={'portal_type':[
                'Sub Survey',
                'Survey Question',
                'Survey Likert Question',
                'Survey Matrix',
                'Survey Select Question',
                'Survey Text Question',
                ]},
            full_objects=True)
        for object in objects:
            if object.portal_type == 'Sub Survey':
                if include_sub_survey:
                    questions.append(object)
                sub_survey_objects = object.getFolderContents(
                    contentFilter={'portal_type':[
                        'Survey Question',
                        'Survey Likert Question',
                        'Survey Matrix',
                        'Survey Select Question',
                        'Survey Text Question',
                        ]},
                    full_objects=True)
                for sub_survey_object in sub_survey_objects:
                    questions.append(sub_survey_object)
                    if sub_survey_object.portal_type == 'Survey Matrix':
                        survey_matrix_objects = sub_survey_object.getFolderContents(
                            contentFilter={'portal_type' : 'Survey Matrix Question'},
                            full_objects=True)
                        for survey_matrix_object in survey_matrix_objects:
                            questions.append(survey_matrix_object)
            elif object.portal_type == 'Survey Matrix':
                questions.append(object)
                survey_matrix_objects = object.getFolderContents(
                    contentFilter={'portal_type' : 'Survey Matrix Question'},
                    full_objects=True)
                for survey_matrix_object in survey_matrix_objects:
                    questions.append(survey_matrix_object)
                # XXX should check if comment is present
            else:
                questions.append(object)
        return questions

    security.declareProtected(CMFCorePermissions.View, 'getNextPage')
    def getNextPage(self):
        """Return the next page of the survey"""
        pages = self.getFolderContents(contentFilter={'portal_type':'Sub Survey',}, full_objects=True)
        current_page = -1
        userid = self.getSurveyId()
        while 1==1:
            try:
                next_page = pages[current_page+1]
            except IndexError:
                # no next page, so survey finished
                self.setCompletedForUser()
                return self.exitSurvey()
            if next_page.getRequiredQuestion():
                question = next_page[next_page.getRequiredQuestion()]
                if next_page.getRequiredAnswerYesNo():
                    if question.getAnswerFor(userid) == next_page.getRequiredAnswer():
                        return next_page()
                else:
                    if question.getAnswerFor(userid) != next_page.getRequiredAnswer():
                        return next_page()
            else:
                return next_page()
            current_page += 1

    security.declareProtected(CMFCorePermissions.View, 'getNextPage')
    def exitSurvey(self):
        """Return the defined exit url"""
        exit_url = self.getExitUrl()
        if exit_url[:7] != 'http://':
            exit_url = self.portal_url() + '/' + exit_url + '?portal_status_message=' + self.getThankYouMessage()
        return self.REQUEST.RESPONSE.redirect(exit_url)

    security.declareProtected(CMFCorePermissions.View, 'saveSurvey')
    def saveSurvey(self):
        """Return the defined exit url"""
        exit_url = self.getExitUrl()
        if exit_url[:7] != 'http://':
            exit_url = self.portal_url() + '/' + exit_url + '?portal_status_message=' + self.getSavedMessage()
        return self.REQUEST.RESPONSE.redirect(exit_url)

    security.declareProtected(CMFCorePermissions.View, 'getNextPage')
    def setCompletedForUser(self):
        """Set completed for a user"""
        userid = self.getSurveyId()
        completed = self.getCompletedFor()
        completed.append(userid)
        self.setCompletedFor(completed)
        if self.getSurveyNotificationMethod() == 'each_submission':
            self.send_email(userid)

    security.declareProtected(CMFCorePermissions.View, 'checkCompletedFor')
    def checkCompletedFor(self, user_id):
        """Check whether a user has completed the survey"""
        completed = self.getCompletedFor()
        if user_id in completed:
            return True
        return False

    security.declareProtected(CMFCorePermissions.View, 'getSurveyId')
    def getSurveyId(self):
        """Return the userid for the survey"""
        portal_membership = getToolByName(self, 'portal_membership')
        if not portal_membership.isAnonymousUser():
            return portal_membership.getAuthenticatedMember().getId()
        request = self.REQUEST
        response = request.RESPONSE
        survey_cookie = self.getId()
        if self.getAllowAnonymous() and request.has_key(survey_cookie):
            return request.get(survey_cookie, "Anonymous")
        survey_id = self.getAnonymousId()
        #expires = (DateTime() + 365).toZone('GMT').rfc822() # cookie expires in 1 year (365 days)
        response.setCookie(survey_cookie, survey_id, path='/')
        return survey_id

    security.declareProtected(CMFCorePermissions.View, 'getAnonymousId')
    def getAnonymousId(self):
    # returns the id to use for an anonymous user
        portal_membership = getToolByName(self, 'portal_membership')
        if portal_membership.isAnonymousUser() and self.getAllowAnonymous():
            if not hasattr(self, 'survey_id_no'):
                self.survey_id_no = 0
            self.survey_id_no += 1
            return 'anonymous' + str(self.survey_id_no)
        elif portal_membership.isAnonymousUser():
            return self.REQUEST.RESPONSE.redirect(self.portal_url()+'/login_form?came_from='+self.absolute_url())
        return portal_membership.getAuthenticatedMember().getId()

    security.declareProtected(CMFCorePermissions.ModifyPortalContent, 'getRespondents')
    def getRespondents(self):
        """Return a list of respondents"""
        questions = self.getAllQuestionsInOrder()
        users = {}
        for question in questions:
            for user in question.answers.keys():
                users[user] = 1
        return users.keys()

    security.declareProtected(CMFCorePermissions.ModifyPortalContent, 'getRespondents')
    def getAnswersByUser(self, userid):
        """Return a set of answers by user id"""
        questions = self.getAllQuestionsInOrder()
        answers = {}
        for question in questions:
            answer = question.getAnswerFor(userid)
            answers[question.getId()] = answer
        return answers

    security.declareProtected(CMFCorePermissions.View, 'getQuestionsCount')
    def getQuestionsCount(self):
        """Return a count of questions asked"""
        return len(self.questions)

    security.declareProtected(CMFCorePermissions.View, 'getSurveyColors')
    def getSurveyColors(self, num_options):
        """Return the colors for the barchart"""
        colors = BARCHART_COLORS
        num_colors = len(colors)
        while num_colors < num_options:
            colors = colors + colors
            num_colors = len(colors)
        return colors

    security.declareProtected(CMFCorePermissions.View, 'buildSpreadsheetUrl')
    def buildSpreadsheetUrl(self):
        """Create a filename for the spreadsheets"""
        date = DateTime().strftime("%Y-%m-%d")
        id = self.title.replace(" ", "")
        id = "%s-%s" % (date, id)
        url = "inval-%s.csv" % id
        return url

    security.declareProtected(perms.ResetOwnResponses,
                              'resetForAuthenticatedUser')
    def resetForAuthenticatedUser(self):
        mtool = getToolByName(self, 'portal_membership')
        member = mtool.getAuthenticatedMember()
        user_id = member.getMemberId()
        return self.resetForUser(user_id)

    security.declareProtected(CMFCorePermissions.ModifyPortalContent,
                              'resetForUser')
    def resetForUser(self, userid):
        """Remove answer for a single user"""
        completed = self.getCompletedFor()
        if userid in completed:
            completed.remove(userid)
        self.setCompletedFor(completed)
        questions = self.getAllQuestionsInOrder()
        for question in questions:
            question.resetForUser(userid)

    security.declareProtected(CMFCorePermissions.View, 'send_email')
    def send_email(self, userid):
        """ Send email to nominated address """
        properties = self.portal_properties.site_properties
        mTo = self.getSurveyNotificationEmail()
        mFrom = properties.email_from_address
        mSubj = '[%s] New survey submitted' % self.Title()
        message = []
        message.append('Survey %s.' % self.Title())
        message.append('has been completed by user: %s.' % userid)
        message.append(self.absolute_url() + '/survey_view_results')
        mMsg = '\n\n'.join(message)
        try:
            self.MailHost.send(mMsg, mTo, mFrom, mSubj)
        except ConflictError:
            raise
        except:
            # XXX too many things can go wrong
            pass

    security.declarePublic('translateThankYouMessage')
    def translateThankYouMessage(self):
        """ """
        return self.translate(msgid="text_default_thank_you",
                              default="Thank you for completing the survey.",
                              domain="plonesurvey")

    security.declarePublic('translateSavedMessage')
    def translateSavedMessage(self):
        """ """
        return self.translate(msgid="text_default_saved_message",
                              default="You have saved the survey.\nDon't forget to come back and finish it.",
                              domain="plonesurvey")

registerType(Survey)
