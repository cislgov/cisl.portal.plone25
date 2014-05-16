#
# Skeleton PloneSureyTestCase
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase
from Products.PloneSurvey.tests import pstc

# A test class defines a set of tests
class TestSomething(pstc.PloneSurveyTestCase):

    # The afterSetUp method can be used to define test class variables
    # and perform initialisation before tests are run. The beforeTearDown() 
    # method can also be used to clean up anything set up in afterSetUp(),
    # though it is less commonly used since test always run in a sandbox
    # that is cleared after the test is run.
    def afterSetUp(self):
        pass

    # All methods starting with 'tests' will be run when the unit test is
    # run.
    def testSomething(self):
        self.assertEqual(1+1, 2)

# This boilerplate method sets up the test suite
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    # Add our test class here - you can add more test classes if you wish,
    # and they will be run together.
    suite.addTest(makeSuite(TestSomething))
    return suite

if __name__ == '__main__':
    framework()
