# -*- coding: utf-8 -*-
#
# File: Install.py
#
# Copyright (c) 2009 by []
# Generator: ArchGenXML Version 1.5.2
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

__author__ = """unknown <unknown>"""
__docformat__ = 'plaintext'


import os.path
import sys
from StringIO import StringIO
from sets import Set
from App.Common import package_home
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.utils import manage_addTool
from Products.ExternalMethod.ExternalMethod import ExternalMethod
from zExceptions import NotFound, BadRequest

from Products.Archetypes.Extensions.utils import installTypes
from Products.Archetypes.Extensions.utils import install_subskin
from Products.Archetypes.config import TOOL_NAME as ARCHETYPETOOLNAME
from Products.Archetypes.atapi import listTypes
from Products.SERPROSCMuralProtocoloBSB.config import PROJECTNAME
from Products.SERPROSCMuralProtocoloBSB.config import product_globals as GLOBALS

def publicaObjeto(self,obj,portal_workflow):   
   objeto = portal_workflow.listActions(self,obj)
   if(objeto[0]['id']=='submeter'):     
     portal_workflow.doActionFor(obj, 'submeter')     
     objeto = portal_workflow.listActions(self,obj)
     if(objeto[0]['id']=='publicar'):       
       portal_workflow.doActionFor(obj, 'publicar')

def adicionaProtocoloSitePropertie(self):

    portal_properties = getToolByName(self, 'portal_properties')
    site_properties = getattr(portal_properties, 'site_properties')
    if hasattr(site_properties, 'typesUseViewActionInListings'):        
       listAux = getattr(site_properties, 'typesUseViewActionInListings')
       listValues = list(listAux)
       encontrou=False
       for elemento in listValues:
           if elemento == 'Protocolo':
              encontrou=True
              break
       if not encontrou:
           listValues = list(listAux) + ['Protocolo']
       site_properties.manage_changeProperties({'typesUseViewActionInListings':tuple(listValues)})
    else:
       listValues = ['File','Image','Protocolo'] 
       site_properties.manage_addProperty('typesUseViewActionInListings',tuple(listValues),'lines')

def criaPastaProtocolo(self):

   portal = getToolByName(self,'portal_url').getPortalObject()   
   if not portal.hasProperty('email_contato'):
        portal.manage_addProperty(id='email_contato',value='cisl@serpro.gov.br',type='string') 
   portal_workflow = getToolByName(portal, 'portal_workflow')
   
   pasta=getattr(portal,'protocolo-brasilia',None)
   if(pasta==None):
     portal.invokeFactory(id='protocolo-brasilia', type_name='PastaProtocolo', title='Protocolo Brasília')   
     obj = getattr(portal,'protocolo-brasilia')   
     publicaObjeto(self,obj,portal_workflow)  

def defineVisaoPadrao(self):
   
   portal = getToolByName(self,'portal_url').getPortalObject()
   obj = getattr(portal,'protocolo-brasilia')	
   
   if obj.hasProperty('default_page'):
     obj.manage_changeProperties({'default_page':'pageProtocolo'})	
   else:
     obj.manage_addProperty('default_page', 'pageProtocolo', 'string') 

def install(self, reinstall=False):
    """ External Method to install SERPROSCMuralProtocoloBSB """
    out = StringIO()
    print >> out, "Installation log of %s:" % PROJECTNAME

    # If the config contains a list of dependencies, try to install
    # them.  Add a list called DEPENDENCIES to your custom
    # AppConfig.py (imported by config.py) to use it.
    try:
        from Products.SERPROSCMuralProtocoloBSB.config import DEPENDENCIES
    except:
        DEPENDENCIES = []
    portal = getToolByName(self,'portal_url').getPortalObject()
    quickinstaller = portal.portal_quickinstaller
    for dependency in DEPENDENCIES:
        print >> out, "Installing dependency %s:" % dependency
        quickinstaller.installProduct(dependency)
        get_transaction().commit(1)

    classes = listTypes(PROJECTNAME)
    installTypes(self, out,
                 classes,
                 PROJECTNAME)
    install_subskin(self, out, GLOBALS)

    # autoinstall tools
    portal = getToolByName(self,'portal_url').getPortalObject()
    for t in ['SERPROSCMuralProtocoloBSBTool']:
        try:
            portal.manage_addProduct[PROJECTNAME].manage_addTool(t)
        except BadRequest:
            # if an instance with the same name already exists this error will
            # be swallowed. Zope raises in an unelegant manner a 'Bad Request' error
            pass
        except:
            e = sys.exc_info()
            if e[0] != 'Bad Request':
                raise

    # hide tools in the search form
    portalProperties = getToolByName(self, 'portal_properties', None)
    if portalProperties is not None:
        siteProperties = getattr(portalProperties, 'site_properties', None)
        if siteProperties is not None and siteProperties.hasProperty('types_not_searched'):
            for tool in ['SERPROSCMuralProtocoloBSBTool']:
                current = list(siteProperties.getProperty('types_not_searched'))
                if tool not in current:
                    current.append(tool)
                    siteProperties.manage_changeProperties(**{'types_not_searched' : current})

    # remove workflow for tools
    portal_workflow = getToolByName(self, 'portal_workflow')
    for tool in ['SERPROSCMuralProtocoloBSBTool']:
        portal_workflow.setChainForPortalTypes([tool], '')

    # uncatalog tools
    for toolname in ['portal_serproscmuralprotocolobsbtool']:
        try:
            portal[toolname].unindexObject()
        except:
            pass

    # hide tools in the navigation
    portalProperties = getToolByName(self, 'portal_properties', None)
    if portalProperties is not None:
        navtreeProperties = getattr(portalProperties, 'navtree_properties', None)
        if navtreeProperties is not None and navtreeProperties.hasProperty('idsNotToList'):
            for toolname in ['portal_serproscmuralprotocolobsbtool']:
                current = list(navtreeProperties.getProperty('idsNotToList'))
                if toolname not in current:
                    current.append(toolname)
                    navtreeProperties.manage_changeProperties(**{'idsNotToList' : current})


    # try to call a workflow install method
    # in 'InstallWorkflows.py' method 'installWorkflows'
    try:
        installWorkflows = ExternalMethod('temp', 'temp',
                                          PROJECTNAME+'.InstallWorkflows',
                                          'installWorkflows').__of__(self)
    except NotFound:
        installWorkflows = None

    if installWorkflows:
        print >>out,'Workflow Install:'
        res = installWorkflows(self,out)
        print >>out,res or 'no output'
    else:
        print >>out,'no workflow install'



    # enable portal_factory for given types
    factory_tool = getToolByName(self,'portal_factory')
    factory_types=[
        "PastaProtocolo",
        "Protocolo",
        "SERPROSCMuralProtocoloBSBTool",
        ] + factory_tool.getFactoryTypes().keys()
    factory_tool.manage_setPortalFactoryTypes(listOfTypeIds=factory_types)

    from Products.SERPROSCMuralProtocoloBSB.config import STYLESHEETS
    try:
        portal_css = getToolByName(portal, 'portal_css')
        for stylesheet in STYLESHEETS:
            try:
                portal_css.unregisterResource(stylesheet['id'])
            except:
                pass
            defaults = {'id': '',
            'media': 'all',
            'enabled': True}
            defaults.update(stylesheet)
            portal_css.registerStylesheet(**defaults)
    except:
        # No portal_css registry
        pass
    from Products.SERPROSCMuralProtocoloBSB.config import JAVASCRIPTS
    try:
        portal_javascripts = getToolByName(portal, 'portal_javascripts')
        for javascript in JAVASCRIPTS:
            try:
                portal_javascripts.unregisterResource(javascript['id'])
            except:
                pass
            defaults = {'id': ''}
            defaults.update(javascript)
            portal_javascripts.registerScript(**defaults)
    except:
        # No portal_javascripts registry
        pass

    # try to call a custom install method
    # in 'AppInstall.py' method 'install'
    try:
        install = ExternalMethod('temp', 'temp',
                                 PROJECTNAME+'.AppInstall', 'install')
    except NotFound:
        install = None

    if install:
        print >>out,'Custom Install:'
        try:
            res = install(self, reinstall)
        except TypeError:
            res = install(self)
        if res:
            print >>out,res
        else:
            print >>out,'no output'
    else:
        print >>out,'no custom install'

    adicionaProtocoloSitePropertie(self)
    criaPastaProtocolo(self)
    defineVisaoPadrao(self)

    return out.getvalue()

def uninstall(self, reinstall=False):
    out = StringIO()


    # unhide tools in the search form
    portalProperties = getToolByName(self, 'portal_properties', None)
    if portalProperties is not None:
        siteProperties = getattr(portalProperties, 'site_properties', None)
        if siteProperties is not None and siteProperties.hasProperty('types_not_searched'):
            for tool in ['SERPROSCMuralProtocoloBSBTool']:
                current = list(siteProperties.getProperty('types_not_searched'))
                if tool in current:
                    current.remove(tool)
                    siteProperties.manage_changeProperties(**{'types_not_searched' : current})


    # unhide tools
    portalProperties = getToolByName(self, 'portal_properties', None)
    if portalProperties is not None:
        navtreeProperties = getattr(portalProperties, 'navtree_properties', None)
        if navtreeProperties is not None and navtreeProperties.hasProperty('idsNotToList'):
            for toolname in ['portal_serproscmuralprotocolobsbtool']:
                current = list(navtreeProperties.getProperty('idsNotToList'))
                if toolname in current:
                    current.remove(toolname)
                    navtreeProperties.manage_changeProperties(**{'idsNotToList' : current})

    # try to call a workflow uninstall method
    # in 'InstallWorkflows.py' method 'uninstallWorkflows'
    try:
        uninstallWorkflows = ExternalMethod('temp', 'temp',
                                            PROJECTNAME+'.InstallWorkflows',
                                            'uninstallWorkflows').__of__(self)
    except NotFound:
        uninstallWorkflows = None

    if uninstallWorkflows:
        print >>out, 'Workflow Uninstall:'
        res = uninstallWorkflows(self, out)
        print >>out, res or 'no output'
    else:
        print >>out,'no workflow uninstall'

    # try to call a custom uninstall method
    # in 'AppInstall.py' method 'uninstall'
    try:
        uninstall = ExternalMethod('temp', 'temp',
                                   PROJECTNAME+'.AppInstall', 'uninstall')
    except:
        uninstall = None

    if uninstall:
        print >>out,'Custom Uninstall:'
        try:
            res = uninstall(self, reinstall)
        except TypeError:
            res = uninstall(self)
        if res:
            print >>out,res
        else:
            print >>out,'no output'
    else:
        print >>out,'no custom uninstall'

    return out.getvalue()

def beforeUninstall(self, reinstall, product, cascade):
    """ try to call a custom beforeUninstall method in 'AppInstall.py'
        method 'beforeUninstall'
    """
    out = StringIO()
    try:
        beforeuninstall = ExternalMethod('temp', 'temp',
                                   PROJECTNAME+'.AppInstall', 'beforeUninstall')
    except:
        beforeuninstall = []

    if beforeuninstall:
        print >>out, 'Custom beforeUninstall:'
        res = beforeuninstall(self, reinstall=reinstall
                                  , product=product
                                  , cascade=cascade)
        if res:
            print >>out, res
        else:
            print >>out, 'no output'
    else:
        print >>out, 'no custom beforeUninstall'
    return (out,cascade)

def afterInstall(self, reinstall, product):
    """ try to call a custom afterInstall method in 'AppInstall.py' method
        'afterInstall'
    """
    out = StringIO()
    try:
        afterinstall = ExternalMethod('temp', 'temp',
                                   PROJECTNAME+'.AppInstall', 'afterInstall')
    except:
        afterinstall = None

    if afterinstall:
        print >>out, 'Custom afterInstall:'
        res = afterinstall(self, product=None
                               , reinstall=None)
        if res:
            print >>out, res
        else:
            print >>out, 'no output'
    else:
        print >>out, 'no custom afterInstall'
    return out
