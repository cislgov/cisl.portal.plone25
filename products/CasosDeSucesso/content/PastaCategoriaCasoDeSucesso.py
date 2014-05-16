# -*- coding: utf-8 -*-
#
# File: PastaCategoriaCasoDeSucesso.py
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
from Products.ATContentTypes.content.folder import ATFolder

##code-section module-header #fill in your manual code here
from Products.ATContentTypes.content.document import ATDocument
##/code-section module-header

schema = Schema((

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

PastaCategoriaCasoDeSucesso_schema = getattr(ATFolder, 'schema', Schema(())).copy() + \
    getattr(ATDocument, 'schema', Schema(())).copy() + \
    schema.copy()
    
PastaCategoriaCasoDeSucesso_schema['description'].widget.visible['edit'] = 'invisible'
PastaCategoriaCasoDeSucesso_schema['description'].widget.visible['view'] = 'invisible'
PastaCategoriaCasoDeSucesso_schema['relatedItems'].widget.visible['edit'] = 'invisible'
PastaCategoriaCasoDeSucesso_schema['relatedItems'].widget.visible['view'] = 'invisible'
PastaCategoriaCasoDeSucesso_schema['text'].required=1


##code-section after-schema #fill in your manual code here
##/code-section after-schema

class PastaCategoriaCasoDeSucesso(ATFolder, ATDocument):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(ATFolder,'__implements__',()),) + (getattr(ATDocument,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Pasta de categorias'

    meta_type = 'PastaCategoriaCasoDeSucesso'
    portal_type = 'PastaCategoriaCasoDeSucesso'
    allowed_content_types = ['CategoriaCasoDeSucesso']
    filter_content_types = 1
    global_allow = 0
    #content_icon = 'PastaCategoriaCasoDeSucesso.gif'
    immediate_view = 'folder_listing'
    default_view = 'folder_listing'
    suppl_views = ()
    typeDescription = "Pasta de categorias"
    typeDescMsgId = 'description_edit_PastaCategoriaCasoDeSucesso'

    _at_rename_after_creation = True

    schema = PastaCategoriaCasoDeSucesso_schema

    aliases = {
        '(Default)'  : 'folder_listing',
        'view'       : 'folder_listing',
        'base_view'  : 'folder_listing',
        'edit'       : 'atct_edit',
        }

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods
    def getFolderContents(self, contentFilter=None, batch=False, b_size=100, full_objects=False):
        """ sobrescreve o método para ordenar
        """
        cur_path = '/'.join(self.getPhysicalPath())
        path = {}
        
        if not contentFilter:
            # The form and other are what really matters
            contentFilter = dict(getattr(self.REQUEST, 'form',{}))
            contentFilter.update(dict(getattr(self.REQUEST, 'other',{})))
        else:
            contentFilter = dict(contentFilter)
        
        # altera a ordenação
        contentFilter['sort_on'] = 'sortable_title'
        
        if contentFilter.get('path', None) is None:
            path['query'] = cur_path
            path['depth'] = 1
            contentFilter['path'] = path
        
        contents = self.portal_catalog.queryCatalog(contentFilter, show_all=1,)
        
        if full_objects:
            contents = [b.getObject() for b in contents]
        
        if batch:
            from Products.CMFPlone import Batch
            b_start = self.REQUEST.get('b_start', 0)
            batch = Batch(contents, b_size, int(b_start), orphan=0)
            return batch
        
        return contents
        
    
registerType(PastaCategoriaCasoDeSucesso, PROJECTNAME)
# end of class PastaCategoriaCasoDeSucesso

##code-section module-footer #fill in your manual code here
##/code-section module-footer



