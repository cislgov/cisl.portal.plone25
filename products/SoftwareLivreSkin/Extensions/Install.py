from cStringIO import StringIO
from Products.CMFCore.utils import getToolByName
from Products.ExternalMethod.ExternalMethod import manage_addExternalMethod
from Products.SoftwareLivreSkin.Extensions.utils import *
from Products.SoftwareLivreSkin.config import *
import sys, os

def install(self):

	# If the this file contains a list of dependencies, try to install
    # them.  Add a list called DEPENDENCIES to your Install.py to use it.
    DEPENDENCIES = ['Archetypes', 'PloneLanguageTool',\
                    'CMFSin', 'CMFPublicator']
    portal = getToolByName(self,'portal_url').getPortalObject()
    quickinstaller = portal.portal_quickinstaller
    out = StringIO()

    for dependency in DEPENDENCIES:
        print >> out, "Installing dependency %s:" % dependency
        quickinstaller.installProduct(dependency)
        get_transaction().commit(1)
 
    setupSkins(self, out, GLOBALS, SKINSELECTIONS, SELECTSKIN, DEFAULTSKIN,
                          ALLOWSELECTION, PERSISTENTCOOKIE)
    registerResources(self, out, 'portal_css', STYLESHEETS)
    registerResources(self, out, 'portal_javascripts', JAVASCRIPTS)
    if DISPLAY_VIEWS:
        setupDisplayViews(self, out, DISPLAY_VIEWS)

    setup_tool = getToolByName(portal, 'portal_setup')
    originalContext = setup_tool.getImportContextID()
    portal.portal_setup.setImportContext(originalContext)

    setupIndex(portal)
    setupSlots(portal)
    setupLanguages(portal)
    setupProperties(portal)
    setupPublicatorInteragir(portal)
    setupPublicatorGuia(portal)
    setupPublicatorCasos(portal)
    setupPublicatorBanner(portal)
    setupPublicatorPublicacoes(portal)
    setStatesCalendar(self)

    print >> out, "Installation completed."
    return out.getvalue()

def setupIndex(portal):
    portal_types = getToolByName(portal, 'portal_types')
    front_page = getattr(portal, 'front-page', None)
    if front_page is not None: 
        portal._delObject('front-page')
        portal.manage_changeProperties(default_page='pagina_inicial')

    portal_types['Plone Site'].manage_changeProperties(view_methods = ['pagina_inicial', 'folder_listing', 'folder_summary_view', 'folder_tabular_view', 'atct_album_view'])


# Alterar "Workflow states to show in the calendar" para aceitar os estados published e publicado_todos
def setStatesCalendar(self):
    portal_calendar = getToolByName(self, 'portal_calendar')
    portal_calendar.calendar_states=['published','publicado_todos']
    portal_calendar.calendar_types=['Event','RichEvent']

	
def setupSlots(portal):
    left_slots =  ('here/portlet_navigation/macros/portlet','here/portlet_banner/macros/portlet')
    portal._setPropValue('left_slots', left_slots)
    right_slots = ('here/portlet_interagir/macros/portlet','here/portlet_guia/macros/portlet','here/portlet_publicacoes/macros/portlet')
    portal._setPropValue('right_slots', right_slots)

def setupLanguages(portal):
    languages = getToolByName(portal, 'portal_languages')
    defaultLanguage = 'pt-br'
    supportedLanguages = ['pt-br']
    languages.manage_setLanguageSettings(defaultLanguage, supportedLanguages,
                                         setCookieN=True, setRequestN=False,
                                         setPathN=True, setForcelanguageUrls=True,
                                         setAllowContentLanguageFallback=False,
                                         setUseCombinedLanguageCodes=True,
                                         startNeutral=True, displayFlags=False)

def setupProperties(portal):
    portal_properties = getToolByName(portal, 'portal_properties')
    portal_properties.site_properties.allowAnonymousViewAbout = (False)
    portal_properties.site_properties.default_language = 'pt-br'
    portal_properties.site_properties.localTimeFormat = '%d/%m/%Y'
    portal_properties.site_properties.localLongTimeFormat = '%d/%m/%Y %H:%M'
    portal_properties.site_properties.disable_folder_sections = (True)
    portal_properties.navtree_properties.includeTop = (False)

def setupPublicatorInteragir(portal):
    portal_publicator = getToolByName(portal, 'portal_publicator')
    portal_publicator.addPublicationBox(id='interagir',
						   icon_url='interagir_ico.png', 
                           name='Interagir',
                           content_type=['Link'],
                           n_items=1,
                           search_states=['publicado_todos','published'],
						   image_states=['publicado_todos','visible'])

def setupPublicatorGuia(portal):
    portal_publicator = getToolByName(portal, 'portal_publicator')
    portal_publicator.addPublicationBox(id='guia',
						   icon_url='guia_ico.png',
                           name='Tire suas dúvidas',
                           content_type=['Document'],
                           n_items=3,
                           search_states=['publicado_todos','published'],
						   image_states=['publicado_todos','visible'])


def setupPublicatorCasos(portal):
    portal_url = getToolByName(portal, 'portal_url')
    portal_publicator = getToolByName(portal, 'portal_publicator')
    portal_publicator.addPublicationBox(id='casos',
                           name='Casos de Sucesso',
                           content_type=['Document'],
                           n_items=1,
                           search_states=['publicado_todos','published'],
						   image_states=['publicado_todos','visible'])

def setupPublicatorBanner(portal):
    portal_url = getToolByName(portal, 'portal_url')
    portal_publicator = getToolByName(portal, 'portal_publicator')    
    portal_publicator.addPublicationBox(id='banner',
                           name='Banner',
                           content_type=['Link'],
                           n_items=6,
                           search_states=['publicado_todos','published'],
                           with_image=True,
						   image_states=['publicado_todos','visible'])

def setupPublicatorPublicacoes(portal):
    portal_publicator = getToolByName(portal, 'portal_publicator')
    portal_publicator.deletePublicationBoxes(['publicacoes'])
    portal_publicator.addPublicationBox(id='publicacoes',
			               icon_url='publicacoes_ico.png', 
                           name='Publicações',
                           content_type=['Document'],
                           n_items=3,
                           search_states=['publicado_todos','published'],
						   image_states=['publicado_todos','visible'])

def uninstall(self):
    out = StringIO()

    removeSkins(self, out, SKINSELECTIONS, DEFAULTSKIN, RESETSKINTOOL)
    resetResources(self, out, 'portal_css', STYLESHEETS)
    resetResources(self, out, 'portal_javascripts', JAVASCRIPTS)
    if DISPLAY_VIEWS:
        removeDisplayViews(self, out, DISPLAY_VIEWS)

    portal_publicator = getToolByName(self, 'portal_publicator')
    portal_publicator.deletePublicationBoxes(['interagir', 'guia', 'casos', 'banner', 'publicacoes'])

    left_slots = ('here/portlet_navigation/macros/portlet', 'here/portlet_login/macros/portlet', 'here/portlet_recent/macros/portlet', 'here/portlet_related/macros/portlet')
    self._setPropValue('left_slots', left_slots)
    right_slots = ('here/portlet_review/macros/portlet', 'here/portlet_news/macros/portlet', 'here/portlet_events/macros/portlet', 'here/portlet_calendar/macros/portlet')
    self._setPropValue('right_slots', right_slots)

