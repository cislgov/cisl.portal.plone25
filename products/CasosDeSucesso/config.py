# -*- coding: utf-8 -*-
#
# File: CasosDeSucesso.py
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


# Product configuration.
#
# The contents of this module will be imported into __init__.py, the
# workflow configuration and every content type module.
#
# If you wish to perform custom configuration, you may put a file
# AppConfig.py in your product's root directory. This will be included
# in this file if found.

try: # New CMF
    from Products.CMFCore.permissions import setDefaultRoles 
except ImportError: # Old CMF
    from Products.CMFCore.CMFCorePermissions import setDefaultRoles


##code-section config-head #fill in your manual code here
##/code-section config-head


PROJECTNAME = "CasosDeSucesso"

# Check for Plone 2.1
try:
    from Products.CMFPlone.migrations import v2_1
except ImportError:
    HAS_PLONE21 = False
else:
    HAS_PLONE21 = True

# Permissions
DEFAULT_ADD_CONTENT_PERMISSION = "Add portal content"
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner'))

ADD_CASODESUCESSO_PERMISSION = "CasoDeSucesso: Adicionar Caso de Sucesso"
ADD_FOLDERCASODESUCESSO_PERMISSION = "CasoDeSucesso: Adicionar Folder Caso de Sucesso"
ADD_CATEGORIACASODESUCESSO_PERMISSION = "CasoDeSucesso: Adicionar Categoria para Caso de Sucesso"
ADD_FOLDERCATEGORIACASODESUCESSO_PERMISSION = "CasoDeSucesso: Adicionar Folder Categoria"

ADD_CONTENT_PERMISSIONS = {'CasoDeSucesso':ADD_CASODESUCESSO_PERMISSION,
                           'PastaCasoDeSucesso':ADD_FOLDERCASODESUCESSO_PERMISSION,
                           'CategoriaCasoDeSucesso':ADD_CATEGORIACASODESUCESSO_PERMISSION,
                           'PastaCategoriaCasoDeSucesso':ADD_FOLDERCATEGORIACASODESUCESSO_PERMISSION,}

setDefaultRoles(ADD_CASODESUCESSO_PERMISSION, ('Manager','Owner'))
setDefaultRoles(ADD_FOLDERCASODESUCESSO_PERMISSION, ('Manager','Owner'))
setDefaultRoles(ADD_CATEGORIACASODESUCESSO_PERMISSION, ('Manager','Owner'))
setDefaultRoles(ADD_FOLDERCATEGORIACASODESUCESSO_PERMISSION, ('Manager','Owner'))

product_globals = globals()

# Dependencies of Products to be installed by quick-installer
# override in custom configuration
DEPENDENCIES = ['SERPROSCCaptchaField']

# Dependend products - not quick-installed - used in testcase
# override in custom configuration
PRODUCT_DEPENDENCIES = []

# You can overwrite these two in an AppConfig.py:
# STYLESHEETS = [{'id': 'my_global_stylesheet.css'},
#                {'id': 'my_contenttype.css',
#                 'expression': 'python:object.getTypeInfo().getId() == "MyType"'}]
# You can do the same with JAVASCRIPTS.
STYLESHEETS = []
JAVASCRIPTS = []

##code-section config-bottom #fill in your manual code here
##/code-section config-bottom


# Load custom configuration not managed by ArchGenXML
try:
    from Products.CasosDeSucesso.AppConfig import *
except ImportError:
    pass
