#
# Test PloneSurvey add answer
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))
from AccessControl import Unauthorized

from Products.PloneSurvey.tests import pstc

class TestAddAnswer(pstc.PloneSurveyTestCase):
    """Ensure survey question can be answered"""

    def afterSetUp(self):
        self.folder.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.folder, 's1')
        self.s1.setAllowAnonymous(True)
        self.s1.invokeFactory('Survey Text Question', 'stq1')
        stq1 = getattr(self.s1, 'stq1')
        stq1.setRequired(True)

    def testAddAnswer(self):
        s1 = getattr(self, 's1')
        userid = s1.getSurveyId()
        assert userid == "test_user_1_", "Not default test user"
        questions = s1.getQuestions()
        for question in questions:
            if question.portal_type == 'Survey Text Question':
                question.addAnswer('Text answer')
                assert question.getAnswerFor(userid) == 'Text answer', "Answer not saved correctly"
        answers = self.s1.getAnswersByUser(userid)
        self.assertEqual(len(answers), 1)

    def testAnonymousAddAnswer(self):
        s1 = getattr(self, 's1')
        self.logout()
        questions = s1.getQuestions()
        for question in questions:
            if question.portal_type == 'Survey Text Question':
                question.addAnswer('Anonymous Text answer')
                # need to login as original user, as anonymous cannot getAnswer
                self.login("test_user_1_")
                assert question.getAnswerFor('anonymous1') == 'Anonymous Text answer', "Answer not saved correctly"

    def testAnonymousCantAddAnswer(self):
        s1 = getattr(self, 's1')
        stq1 = getattr(self.s1, 'stq1')
        s1.setAllowAnonymous(False)
        self.logout()
        questions = s1.getQuestions()
        for question in questions:
            if question.portal_type == 'Survey Text Question':
                self.assertRaises(Unauthorized,
                    question.addAnswer,
                    'Anonymous Text answer')

    def testAnonymousIdGeneration(self):
        s1 = getattr(self, 's1')
        self.logout()
        userid = s1.getSurveyId()
        assert userid == "anonymous1", "Anonymous id generation not working"

# XXX add more tests

if  __name__ == '__main__':
    framework()

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestAddAnswer))
    return suite
