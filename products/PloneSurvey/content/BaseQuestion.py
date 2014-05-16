from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from AccessControl import Unauthorized
from BTrees.OOBTree import OOBTree
# backword compatibility for zope 2.7.x
try:
    from persistent.mapping import PersistentMapping
except ImportError:
    from PersistentMapping import PersistentMapping

from Products.Archetypes.public import *
from Products.CMFCore import CMFCorePermissions
from Products.CMFCore.utils import getToolByName

from Products.PloneSurvey.config import COMMENT_TYPE
from Products.PloneSurvey.config import USE_BTREE

BaseQuestionSchema = BaseSchema + Schema((

    StringField('abstract',
        searchable=1,
        required=0,
        accessor="getAbstract",
        edit_accessor="getAbstract",
        mutator="setAbstract",
        widget=TextAreaWidget(
            label="Description",
            label_msgid="label_question_description",
            description="Add a long description of the question here, to clarify any details.",
            description_msgid="help_question_description",
            i18n_domain="plonesurvey",
            rows=5),
        ),

    BooleanField('required',
        searchable=0,
        required=0,
        default=1,
        widget=BooleanWidget(
            label="Required",
            label_msgid="label_required",
            description="Select if this question is required, meaning participant must give a response.",
            description_msgid="help_required",
            i18n_domain="plonesurvey",
           ),
        ),

    StringField('commentType',
        schemata="Comment Field",
        searchable=0,
        required=0,
        vocabulary=COMMENT_TYPE,
        widget=SelectionWidget(
            label="Comment Type",
            label_msgid="label_comment_type",
            description="Select what type of comment box you would like.",
            description_msgid="help_label_comment_type",
            format="select",
            i18n_domain="plonesurvey",
          )
        ),

    StringField('commentLabel',
        schemata="Comment Field",
        searchable=0,
        required=0,
        default="Comment - mandatory if \"no\"",
        widget=TextAreaWidget(
            label="Comment label",
            label_msgid="label_comment_label",
            description="The comment label.",
            description_msgid="help_comment_label",
            i18n_domain="plonesurvey",
          )
        ),

    ))


class BaseQuestion(BaseContent):
    """Base class for survey questions"""
    immediate_view = "base_edit"
    global_allow = 0
    filter_content_types = 1
    allowed_content_types = ()
    include_default_actions = 1
    _at_rename_after_creation = True

    def __init__(self, oid, **kwargs):
        self.reset()
        BaseContent.__init__(self, oid, **kwargs)

    security = ClassSecurityInfo()

    security.declareProtected(CMFCorePermissions.View, 'getAbstract')
    def getAbstract(self, **kw):
        return self.Description()

    security.declareProtected(CMFCorePermissions.ModifyPortalContent, 'setAbstract')
    def setAbstract(self, val, **kw):
        self.setDescription(val)

    security.declareProtected(CMFCorePermissions.ModifyPortalContent, 'reset')
    def reset(self):
        """Remove answers for all users."""
        if USE_BTREE:
            self.answers = OOBTree()
        else:
            self.answers = PersistentMapping()

    security.declareProtected(CMFCorePermissions.ModifyPortalContent, 'resetForUser')
    def resetForUser(self, userid):
        """Remove answer for a single user"""
        if self.answers.has_key(userid):
            del self.answers[userid]

    security.declareProtected(CMFCorePermissions.View, 'addAnswer')
    def addAnswer(self, value, comments=""):
        """Add an answer and optional comments for a user.
        This method protects _addAnswer from anonymous users specifying a
        userid when they vote, and thus apparently voting as another user
        of their choice.
        """
        # Get hold of the parent survey
        survey = None
        ob = self
        while survey is None:
            ob = ob.aq_parent
            if ob.meta_type == 'Survey':
                survey = ob
            elif getattr(ob, '_isPortalRoot', False):
                raise Exception("Could not find a parent Survey.")
        portal_membership = getToolByName(self, 'portal_membership')
        if portal_membership.isAnonymousUser() and not survey.getAllowAnonymous():
            raise Unauthorized, ("This survey is not available to anonymous users.")
        # Use the survey to get hold of the appropriate userid
        userid = survey.getSurveyId()
        # Call the real method for storing the answer for this user.
        return self._addAnswer(userid, value, comments)

    def _addAnswer(self, userid, value, comments=""):
        """Add an answer and optional comments for a user."""
        # We don't let users over-write answers that they've already made.
        # Their first answer must be explicitly 'reset' before another
        # answer can be supplied.
        # XXX this causes problem when survey fails validation
        # will also cause problem with save function
##        if self.answers.has_key(userid):
##            # XXX Should this get raised?  If so, a more appropriate
##            # exception is probably in order.
##            msg = "User '%s' has already answered this question. Reset the original response to supply a new answer."
##            raise Exception(msg % userid)
##        else:
        self.answers[userid] = PersistentMapping(value=value,
                                                 comments=comments)
        if not isinstance(self.answers, (PersistentMapping, OOBTree)):
            # It must be a standard dictionary from an old install, so
            # we need to inform the ZODB about the change manually.
            self.answers._p_changed = 1

    security.declareProtected(CMFCorePermissions.View, 'getAnswerFor')
    def getAnswerFor(self, userid):
        """Get a specific user's answer"""
        answer = self.answers.get(userid, {}).get('value', None)
        if self.getInputType() in ['multipleSelect', 'checkbox']:
            if type(answer) == 'NoneType':
                return []
        return answer

    security.declareProtected(CMFCorePermissions.View, 'getCommentsFor')
    def getCommentsFor(self, userid):
        """Get a specific user's comments"""
        return self.answers.get(userid, {}).get('comments', None)

    security.declareProtected(CMFCorePermissions.View, 'getComments')
    def getComments(self):
        """Return a userid, comments mapping"""
        mlist = []
        for k, v in self.answers.items():
            mapping = {}
            mapping['userid'] = k
            mapping['comments'] = v.get('comments', '')
            mlist.append(mapping)
        return mlist


InitializeClass(BaseQuestion)