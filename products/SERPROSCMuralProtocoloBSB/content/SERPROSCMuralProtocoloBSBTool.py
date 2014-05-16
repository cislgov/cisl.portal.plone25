# -*- coding: utf-8 -*-
#
# File: SERPROSCMuralProtocoloBSBTool.py
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
from Products.CMFCore.utils import getToolByName
from AccessControl.SecurityManagement import newSecurityManager, noSecurityManager
from Products.CMFCore.utils import UniqueObject
    
##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

SERPROSCMuralProtocoloBSBTool_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class SERPROSCMuralProtocoloBSBTool(UniqueObject, BaseContent):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(UniqueObject,'__implements__',()),) + (getattr(BaseContent,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'SERPROSCMuralProtocoloBSBTool'

    meta_type = 'SERPROSCMuralProtocoloBSBTool'
    portal_type = 'SERPROSCMuralProtocoloBSBTool'
    allowed_content_types = []
    filter_content_types = 0
    global_allow = 0
    #content_icon = 'SERPROSCMuralProtocoloBSBTool.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "SERPROSCMuralProtocoloBSBTool"
    typeDescMsgId = 'description_edit_serproscmuralprotocolobsbtool'
    #toolicon = 'SERPROSCMuralProtocoloBSBTool.gif'

    _at_rename_after_creation = True

    schema = SERPROSCMuralProtocoloBSBTool_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header


    # tool-constructors have no id argument, the id is fixed
    def __init__(self, id=None):
        BaseContent.__init__(self,'portal_serproscmuralprotocolobsbtool')
        self.setTitle('SERPROSCMuralProtocoloBSBTool')
        
        ##code-section constructor-footer #fill in your manual code here
        ##/code-section constructor-footer


    # tool should not appear in portal_catalog
    def at_post_edit_script(self):
        self.unindexObject()
        
        ##code-section post-edit-method-footer #fill in your manual code here
        ##/code-section post-edit-method-footer


    # Methods
    security.declarePublic('setarPermissaoSuperUsuario')
    def setarPermissaoSuperUsuario(self):
        """
        """
        mtool = getToolByName(self, 'portal_membership')
     
        usuario_atual = mtool.getAuthenticatedMember()        
        if usuario_atual.has_role('Manager'):
           return usuario_atual
     
        super_usuario = self.getWrappedOwner()
        newSecurityManager(None, super_usuario)
     
        return usuario_atual

    security.declarePublic('setarPermissaoUsuarioComum')
    def setarPermissaoUsuarioComum(self, usuario):
        """
        """
        if not usuario.has_role('Manager'):
           newSecurityManager(None, usuario)


    security.declarePublic('verificaExtensaoArquivo')
    def verificaExtensaoArquivo(self,value):
        """valida extensão para anexar arquivo (campo anexo)"""
	extValidas=['ODT','TXT','PDF']
        if value != "":
            filename = value.filename
            if filename != "":
                extensao = filename[filename.rfind('.')+1:]
                if extensao.upper() not in extValidas:
		    return "no"
                else:
                    return "yes"
    
    def criaObjetoProtocolo(self,dic_protocolo):
        """"""

	portal = getToolByName(self,'portal_url').getPortalObject()
        strPathProtocolos = getToolByName(portal,'protocolo-brasilia')

	strID = 'protocolos.' + str(self.generateUniqueId())
        
        arquivo=dic_protocolo['anexo']
        arquivo.seek(0, 2) 
        size = arquivo.tell()  
               
        if size==0:
              strPathProtocolos.invokeFactory(id=strID,
                                              title=str(dic_protocolo['nomeInstituicao']),
                                              description=dic_protocolo['declaracao'],                                     
                                              type_name='Protocolo',
                                              excludeFromNav=True)              
        else: 
              strPathProtocolos.invokeFactory(id=strID,
                                              title=str(dic_protocolo['nomeInstituicao']),
                                              description=dic_protocolo['declaracao'],
                                                                                   
                                              file=dic_protocolo['anexo'],                                     
                                              type_name='Protocolo',
                                              excludeFromNav=True)
              
	verificaArtigo = portal.portal_catalog.searchResults(id=strID)
	strReturn = ''
	if(len(verificaArtigo) == 1):            
	    strReturn=strID
	    return strReturn
	else:
	    strReturn='no'
	    return strReturn     

registerType(SERPROSCMuralProtocoloBSBTool, PROJECTNAME)
# end of class SERPROSCMuralProtocoloBSBTool

##code-section module-footer #fill in your manual code here
##/code-section module-footer



