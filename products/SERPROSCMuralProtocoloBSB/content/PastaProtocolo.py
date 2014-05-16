# -*- coding: utf-8 -*-
#
# File: PastaProtocolo.py
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

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.SERPROSCMuralProtocoloBSB.config import *

# additional imports from tagged value 'import'
from Products.ATContentTypes.content.folder import ATFolder

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((
	TextField('bodyBefore',
              required = False,
              searchable = True,
              allowable_content_types = ('text/html',),
              default_output_type = 'text/x-html-safe',
              widget=RichWidget(description='Explanatory text, before applet.',
                                description_msgid ='desc_description_before',
                                label='Text',
                                label_msgid ='label_description',                                
                                i18n_domain = 'Freemind',
                                rows=15,),

             ),
),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

PastaProtocolo_schema = BaseFolderSchema.copy() + \
    getattr(ATFolder, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class PastaProtocolo(BaseFolder, ATFolder):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseFolder,'__implements__',()),) + (getattr(ATFolder,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Pasta de Protocolos'

    meta_type = 'PastaProtocolo'
    portal_type = 'PastaProtocolo'
    allowed_content_types = ['Protocolo','Document','File']
    filter_content_types = 1
    global_allow = 1
    #content_icon = 'PastaProtocolo.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "Pasta de Protocolos"
    typeDescMsgId = 'description_edit_pastaprotocolo'

    _at_rename_after_creation = True

    schema = PastaProtocolo_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

registerType(PastaProtocolo, PROJECTNAME)
# end of class PastaProtocolo

##code-section module-footer #fill in your manual code here
##/code-section module-footer



