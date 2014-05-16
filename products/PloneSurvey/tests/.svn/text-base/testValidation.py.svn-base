#
# Test PloneSurvey validation
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))
#from AccessControl import Unauthorized
from Testing.makerequest import makerequest
from Products.CMFFormController.ControllerState import ControllerState
from Products.CMFCore.utils import getToolByName

from Products.PloneSurvey.tests import pstc

class TestValidation(pstc.PloneSurveyTestCase):
    """Ensure survey validation"""

    def afterSetUp(self):
        self.folder.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.folder, 's1')
        self.s1.setAllowAnonymous(True)
        self.s1.invokeFactory('Survey Text Question', 'stq1')
        stq1 = getattr(self.s1, 'stq1')
        stq1.setRequired(True)
        stq1.setValidation('None')

    def testQuestionValidates(self):
        s1 = getattr(self, 's1')
        app = makerequest(self.app)
        # add your form variables
        app.REQUEST.form['stq1'] = 'Text Answer'
        # set up a dummy state object
        dummy_controller_state = ControllerState(
                                    id='survey_view',
                                    context=s1,
                                    button='submit',
                                    status='success',
                                    errors={},
                                    next_action=None,)
        # get the form controller
        controller = self.portal.portal_form_controller
        # send the validate script to the form controller with the dummy state object
        controller_state = controller.validate(dummy_controller_state, app.REQUEST, ['validate_survey',])
        # Do any relevant tests
        assert controller_state.getErrors() == {}, "Validation error raised"
        userid = s1.getSurveyId()
        assert userid == "test_user_1_", "Not default test user"
        questions = s1.getQuestions()
        for question in questions:
            if question.portal_type == 'Survey Text Question':
                question.addAnswer('Text answer')
                assert question.getAnswerFor(userid) == 'Text answer', "Answer not saved correctly"

    def testValidateLength(self):
        s1 = getattr(self, 's1')
        stq1 = getattr(self.s1, 'stq1')
        stq1.setMaxLength(5)
        app = makerequest(self.app)
        # add your form variables
        app.REQUEST.form['stq1'] = 'Text Answer'
        # set up a dummy state object
        dummy_controller_state = ControllerState(
                                    id='survey_view',
                                    context=s1,
                                    button='submit',
                                    status='success',
                                    errors={},
                                    next_action=None,)
        # get the form controller
        controller = self.portal.portal_form_controller
        # send the validate script to the form controller with the dummy state object
        controller_state = controller.validate(dummy_controller_state, app.REQUEST, ['validate_survey',])
        # Do any relevant tests
        assert controller_state.getErrors() != {}, "Validation error not raised"

if  __name__ == '__main__':
    framework()

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestValidation))
    return suite
