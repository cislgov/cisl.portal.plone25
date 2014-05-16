from Products.CMFCore import CMFCorePermissions
from Products.Archetypes.public import DisplayList
from Products.validation import validation

ADD_CONTENT_PERMISSION = CMFCorePermissions.AddPortalContent
PROJECTNAME = "PloneSurvey"
SKINS_DIR = 'skins'

GLOBALS = globals()

# this imports the SurveyQuestion, will be deprecated
ADD_SURVEY_QUESTION = 0

# this imports the SurveyLikertQuestion, will be deprecated
ADD_LIKERT_QUESTION = 0

# use btree for answers
USE_BTREE = 1

SURVEY_STATUS = DisplayList((
    ('open', 'Open', 'label_survey_open'),
    ('closed', 'Closed', 'label_survey_closed'),
    ))

NOTIFICATION_METHOD = DisplayList((
    ('', 'No emails', 'label_no_emails'),
    ('each_submission', 'Email on each submission', 'label_all_emails'),
    ))

TEXT_INPUT_TYPE = DisplayList((
    ('text', 'Text Field', 'label_text_field'),
    ('area', 'Text Area', 'label_text_area'),
    ))

SELECT_INPUT_TYPE = DisplayList((
    ('radio', 'Radio Buttons', 'label_radio_buttons'),
    ('selectionBox', 'Selection Box', 'label_selection_box'),
    ('multipleSelect', 'Multiple Selection Box', 'label_multiple_selection_box'),
    ('checkbox', 'Check Boxes', 'label_check_boxes'),
    ))

INPUT_TYPE = DisplayList((
    ('radio', 'Radio Buttons', 'label_radio_buttons'),
    ('selectionBox', 'Selection Box', 'label_selection_box'),
    ('text', 'Text Field', 'label_text_field'),
    ('area', 'Text Area', 'label_text_area'),
    ('multipleSelect', 'Multiple Selection Box', 'label_multiple_selection_box'),
    ('checkbox', 'Check Boxes', 'label_check_boxes'),
    ))

COMMENT_TYPE = DisplayList((
    ('', 'None', 'label_no_comment_field'),
    ('text', 'Text Field', 'label_text_field'),
    ('area', 'Text Area', 'label_text_area'),
    ))

##LIKERT_OPTIONS = DisplayList((
##    ('1', 'Agree Strongly'),
##    ('2', 'Agree'),
##    ('3', 'Neutral'),
##    ('4', 'Disagree'),
##    ('5', 'Disagree Strongly'),
##    ))

LIKERT_OPTIONS = [
    'Agree Strongly',
    'Agree',
    'Neutral',
    'Disagree',
    'Disagree Strongly',
    ]

BARCHART_COLORS = ['green','red','yellow','blue','pink','grey','orange','silver','purple']

VALIDATORS = validation.keys()

# remove non useful validators
if 'isEmpty' in VALIDATORS:
    VALIDATORS.remove('isEmpty')
if 'isValidId' in VALIDATORS:
    VALIDATORS.remove('isValidId')
if 'checkImageMaxSize' in VALIDATORS:
    VALIDATORS.remove('checkImageMaxSize')
if 'checkNewsImageMaxSize' in VALIDATORS:
    VALIDATORS.remove('checkNewsImageMaxSize')
if 'isMaxSize' in VALIDATORS:
    VALIDATORS.remove('isMaxSize')
if 'isTAL' in VALIDATORS:
    VALIDATORS.remove('isTAL')
if 'checkFileMaxSize' in VALIDATORS:
    VALIDATORS.remove('checkFileMaxSize')
if 'isNonEmptyFile' in VALIDATORS:
    VALIDATORS.remove('isNonEmptyFile')
if 'isEmptyNoError' in VALIDATORS:
    VALIDATORS.remove('isEmptyNoError')
if 'isTidyHtml' in VALIDATORS:
    VALIDATORS.remove('isTidyHtml')
if 'isUnixLikeName' in VALIDATORS:
    VALIDATORS.remove('isUnixLikeName')
if 'isTidyHtmlWithCleanup' in VALIDATORS:
    VALIDATORS.remove('isTidyHtmlWithCleanup')
if 'inNumericRange' in VALIDATORS:
    VALIDATORS.remove('inNumericRange')
if 'isPrintable' in VALIDATORS:
    VALIDATORS.remove('isPrintable')

TEXT_VALIDATORS = VALIDATORS