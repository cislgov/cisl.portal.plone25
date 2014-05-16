# -*- coding: utf-8 -*-
#
# File: Protocolo.py
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
from Products.ATContentTypes.content.file import ATFile

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    StringField(
        name='title',
        widget=StringWidget(
            label="Nome da Instituição",
            label_msgid='SERPROSCMuralProtocoloBSB_label_title',
            i18n_domain='SERPROSCMuralProtocoloBSB',
        )
    ),

    TextField(
        name='description',
        widget=TextAreaWidget(
            label="Declaração",
            label_msgid='SERPROSCMuralProtocoloBSB_label_description',
            i18n_domain='SERPROSCMuralProtocoloBSB',
        )
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Protocolo_schema = BaseSchema.copy() + \
    getattr(ATFile, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
#Inscrito_schema['title'].widget.visible = {'view':'invisible', 'edit':'invisible'}
#Inscrito_schema['title'].required = 0
ATFileSchema = getattr(ATFile, 'schema', Schema(()))
Protocolo_schema['file'].required = 0
Protocolo_schema['file'].widget.label = "Plano de Migração"
Protocolo_schema['file'].widget.label_msgid = "Plano de Migração"
print ATFileSchema.keys()
print Protocolo_schema.keys()
#Protocolo_schema.delField("relatedItems")
Protocolo_schema['relatedItems'].widget.visible = {'view':'invisible', 'edit':'invisible'}


##/code-section after-schema

class Protocolo(BaseContent, ATFile):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseContent,'__implements__',()),) + (getattr(ATFile,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Protocolo'

    meta_type = 'Protocolo'
    portal_type = 'Protocolo'
    allowed_content_types = [] + list(getattr(ATFile, 'allowed_content_types', []))
    filter_content_types = 0
    global_allow = 0
    #content_icon = 'Protocolo.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'    
    suppl_views = ()
    typeDescription = "Protocolo"
    typeDescMsgId = 'description_edit_protocolo'

    _at_rename_after_creation = True

    schema = Protocolo_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods
    def at_post_create_script(self):
         self.setExcludeFromNav(True)

registerType(Protocolo, PROJECTNAME)
# end of class Protocolo

##code-section module-footer #fill in your manual code here
##/code-section module-footer



