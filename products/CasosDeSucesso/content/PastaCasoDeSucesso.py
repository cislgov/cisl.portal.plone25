# -*- coding: utf-8 -*-
#
# File: PastaCasoDeSucesso.py
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

PastaCasoDeSucesso_schema = getattr(ATFolder, 'schema', Schema(())).copy() + \
    getattr(ATDocument, 'schema', Schema(())).copy() + \
    schema.copy()
    
PastaCasoDeSucesso_schema['description'].widget.visible['edit'] = 'invisible'
PastaCasoDeSucesso_schema['description'].widget.visible['view'] = 'invisible'
PastaCasoDeSucesso_schema['relatedItems'].widget.visible['edit'] = 'invisible'
PastaCasoDeSucesso_schema['relatedItems'].widget.visible['view'] = 'invisible'
PastaCasoDeSucesso_schema['text'].required=1


##code-section after-schema #fill in your manual code here
##/code-section after-schema

class PastaCasoDeSucesso(ATFolder, ATDocument):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(ATFolder,'__implements__',()),) + (getattr(ATDocument,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Pasta de casos de sucesso'

    meta_type = 'PastaCasoDeSucesso'
    portal_type = 'PastaCasoDeSucesso'
    allowed_content_types = ['CasoDeSucesso']
    filter_content_types = 1
    global_allow = 1
    #content_icon = 'PastaCasoDeSucesso.gif'
    immediate_view = 'lista_casosdesucesso'
    default_view = 'lista_casosdesucesso'
    suppl_views = ()
    typeDescription = "Pasta de casos de sucesso"
    typeDescMsgId = 'description_edit_pastacasodesucesso'

    _at_rename_after_creation = True

    schema = PastaCasoDeSucesso_schema

    aliases = {
        '(Default)'  : 'lista_casosdesucesso',
        'view'       : 'lista_casosdesucesso',
        'base_view'  : 'lista_casosdesucesso',
        'edit'       : 'atct_edit',
        }

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods
    
    security.declarePublic('at_post_create_script')
    def at_post_create_script(self):
        self.portal_types['PastaCasoDeSucesso'].allowed_content_types = ['CasoDeSucesso','PastaCategoriaCasoDeSucesso']
        self.invokeFactory(type_name='PastaCategoriaCasoDeSucesso', id='categorias', title='Categorias')
        self.portal_workflow.doActionFor(self, 'publish')
        self.portal_types['PastaCasoDeSucesso'].allowed_content_types = ['CasoDeSucesso']
    
    security.declarePublic('obter_dicionario_categorias')
    def obter_dicionario_categorias(self):
        dicionario = {}
        lista = self.uid_catalog(portal_type='CategoriaCasoDeSucesso')
        for item in lista:
            dicionario[item.UID] = item.Title 
    
    security.declarePublic('obter_casosdesucesso')
    def obter_casosdesucesso(self, texto=None, categoria=None, limit=None, findAll=None):
        utils = self.restrictedTraverse('@@casodesucesso_utils_view')
        return utils.obter_casosdesucesso(texto=texto, categoria=categoria, path='/'.join(self.getPhysicalPath()), sort_on='created', sort_order='reverse', limit=limit, findAll=findAll)


registerType(PastaCasoDeSucesso, PROJECTNAME)
# end of class PastaCasoDeSucesso

##code-section module-footer #fill in your manual code here
##/code-section module-footer



