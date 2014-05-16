#
# Test PloneSurvey Branching
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.PloneSurvey.tests import pstc

class TestBranching(pstc.PloneSurveyTestCase):
    """Test Survey Branching"""

    def afterSetUp(self):
        self.folder.invokeFactory('Survey', 's1')
        s1 = getattr(self.folder, 's1')
        s1.invokeFactory('Survey Select Question', 'ssq1')
        s1.invokeFactory('Sub Survey', 'ss1')
        s1.invokeFactory('Sub Survey', 'ss2')

    def testEditSubSurveyBranch(self):
        s1 = getattr(self.folder, 's1')
        ssq1 = getattr(s1, 'ssq1')
        ss1 = getattr(s1, 'ss1')
        ss2 = getattr(s1, 'ss2')

        ss1.setRequiredQuestion('ssq1')
        ss1.setRequiredAnswer(1)

        self.assertEqual(ss1.getRequiredQuestion(), 'ssq1')
        self.assertEqual(ss1.getRequiredAnswer(), 1)

if  __name__ == '__main__':
    framework()

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestBranching))
    return suite
