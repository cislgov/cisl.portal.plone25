# -*- coding: utf-8 -*-
#
# File: Install.py
#
# Copyright (c) 2010 by []
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
from Products.CasosDeSucesso.config import PROJECTNAME
from Products.CasosDeSucesso.config import product_globals as GLOBALS


def setup_casodesucesso_propertysheet(self):
    """
    """
    portal = getToolByName(self, 'portal_url').getPortalObject()
    if not hasattr(portal.portal_properties, 'serpro_casodesucesso_properties'):
        portal.portal_properties.addPropertySheet('serpro_casodesucesso_properties', 
                                                'Caso de Sucesso')
        
    portal_properties = portal.portal_properties
    casodesucesso_properties = portal_properties.serpro_casodesucesso_properties
    
    if not hasattr(casodesucesso_properties, 'email_administrator'):
        casodesucesso_properties.manage_addProperty('email_administrator', '', 'string')


def install(self, reinstall=False):
    """ External Method to install CasosDeSucesso """
    out = StringIO()
    print >> out, "Installation log of %s:" % PROJECTNAME

    # If the config contains a list of dependencies, try to install
    # them.  Add a list called DEPENDENCIES to your custom
    # AppConfig.py (imported by config.py) to use it.
    try:
        from Products.CasosDeSucesso.config import DEPENDENCIES
    except:
        DEPENDENCIES = []
    portal = getToolByName(self,'portal_url').getPortalObject()
    quickinstaller = portal.portal_quickinstaller
    for dependency in DEPENDENCIES:
        print >> out, "Installing dependency %s:" % dependency
        quickinstaller.installProduct(dependency)
        try:
            get_transaction().commit(1)
        except:
            import transaction
            transaction.commit(1)

    classes = listTypes(PROJECTNAME)
    installTypes(self, out,
                 classes,
                 PROJECTNAME)
    install_subskin(self, out, GLOBALS)


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
        "CasoDeSucesso",
        "CategoriaCasoDeSucesso",
        "PastaCasoDeSucesso",
        "PastaCategoriaCasoDeSucesso",
        ] + factory_tool.getFactoryTypes().keys()
    factory_tool.manage_setPortalFactoryTypes(listOfTypeIds=factory_types)

    from Products.CasosDeSucesso.config import STYLESHEETS
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
    from Products.CasosDeSucesso.config import JAVASCRIPTS
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
        
    
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.setImportContext('profile-CasosDeSucesso:casosdesucesso')
    setup_tool.runAllImportSteps()
    """
    comentei a linha abaixo pois estava dando o erro abaixo (Plone 3.3.5):
    KeyError: 'CMFPlone:plone'
    """
    #setup_tool.setImportContext('profile-CMFPlone:plone')
    
    print >>out,"Ran all import steps."
    
    
       
    setup_casodesucesso_propertysheet(self)
    
    return out.getvalue()

def uninstall(self, reinstall=False):
    out = StringIO()



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

    # remove the configlets from the portal control panel
    if not reinstall:
        configTool = getToolByName(self, 'portal_controlpanel', None)
        if configTool:
            for conf in configlets:
                configTool.unregisterConfiglet(conf['id'])
                out.write('Removed configlet %s\n' % conf['id'])
    
        print >> out, "Successfully uninstalled %s." % PROJECTNAME

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
