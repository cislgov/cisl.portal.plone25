# -*- coding: utf-8 -*-
#
# File: CategoriaCasoDeSucesso.py
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

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.CasosDeSucesso.config import *
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.schemata import ATContentTypeSchema

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

CategoriaCasoDeSucesso_schema = ATContentTypeSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
#CategoriaCasoDeSucesso_schema['description'].widget.visible['view'] = 'visible'
#CategoriaCasoDeSucesso_schema['description'].isMetadata = 0

CategoriaCasoDeSucesso_schema['relatedItems'].widget.visible['edit'] = 'invisible'
CategoriaCasoDeSucesso_schema['relatedItems'].widget.visible['view'] = 'invisible'
##/code-section after-schema

class CategoriaCasoDeSucesso(ATCTContent):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(ATCTContent,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Categoria'

    meta_type = 'CategoriaCasoDeSucesso'
    portal_type = 'CategoriaCasoDeSucesso'
    allowed_content_types = []
    filter_content_types = 0
    global_allow = 1
    #content_icon = 'CategoriaCasoDeSucesso.gif'
    immediate_view = 'categoriacasodesucesso_view'
    default_view = 'categoriacasodesucesso_view'
    suppl_views = ()
    typeDescription = "Categoria"
    typeDescMsgId = 'description_edit_categoria'

    _at_rename_after_creation = True

    aliases = {
        '(Default)'  : 'categoriacasodesucesso_view',
        'view'       : 'categoriacasodesucesso_view',
        'base_view'  : 'categoriacasodesucesso_view',
        'edit'       : 'atct_edit',
        }

    schema = CategoriaCasoDeSucesso_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods
    security.declarePublic('obter_casosdesucesso')
    def obter_casosdesucesso(self):
        utils = self.restrictedTraverse('@@casodesucesso_utils_view')
        return utils.obter_casosdesucesso(categoria=self.UID(), sort_on='sortable_title', sort_order='asc')


registerType(CategoriaCasoDeSucesso, PROJECTNAME)
# end of class CategoriaCasoDeSucesso

##code-section module-footer #fill in your manual code here
##/code-section module-footer



