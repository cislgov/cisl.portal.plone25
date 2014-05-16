# -*- coding: utf-8 -*-
#
# File: CasoDeSucesso.py
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

##code-section module-header #fill in your manual code here
from Products.Archetypes.references import HoldingReference
from Products.ATContentTypes.content.document import ATDocument
from Products.SERPROSCCaptchaField.CaptchaField import CaptchaField
from Products.ATContentTypes.permission import ChangeEvents
from Products.CMFCore.utils import getToolByName
##/code-section module-header

schema = Schema((
                 
    ReferenceField(
        name='categoria_casodesucesso',
        read_permission='View',
        allowed_types=('CategoriaCasoDeSucesso',),
        multiValued=1,
        required=0,        
        relationship='categoria_casodesuceso',
        vocabulary='getCategoriaCasoDeSucesso',
        index='KeywordIndex:brains',
        referenceClass=HoldingReference,
        widget=ReferenceWidget(
            label='Categoria(s)',
            description="Marque uma ou mais categorias nas quais essa adoção/migração para Software Livre se enquadra",
            checkbox_bound=0,
            macro='macro_categoria_casodesucesso',
        ),
    ),

    LinesField(
        name='categoriasugerida_casodesucesso',
        read_permission = ChangeEvents,
        widget=LinesWidget(
            label="Sugerir categoria",
            description='Se seu caso de sucesso se enquadra em alguma categoria que não está listada acima, sugira novas categorias, uma por linha',
            #visible={'view': 'invisible'},
        ),        
        searchable = True,        
    ),

    LinesField(
        name='softwares_casodesucesso',
        required=1,        
        widget=LinesWidget(
            label="Softwares Utilizados",
            description='Cada software deve estar em uma linha',
        )
    ),

    StringField(
        name='orgao_casodesucesso',
        required=1,        
        index='ZCTextIndex, lexicon_id=plone_lexicon, index_type=Okapi BM25 Rank | FieldIndex:brains',
        widget=StringWidget(
            label="Orgão / Instituição",
        ),
        validators=('isNotOnlySpace_Casosdesucesso',),        
        searchable = True,
    ),

    StringField(
        name='autor_casodesucesso',
        required=1,        
        default='',
        widget=StringWidget(
            label="Autor",
        ),
        validators=('isNotOnlySpace_Casosdesucesso',),
    ),

    StringField(
        name='email_casodesucesso',
        required=1,        
        widget=StringWidget(
            label="E-mail do autor",
            visible={'view': 'invisible'},
        ),
        validators=('isValidEmail_Casosdesucesso',), 
    ),

    StringField(
        name='saibamais_casodesucesso',
        widget=StringWidget(
            label="Saiba mais",
            description="Link para mais detalhes",
        )
    ),
    
    ImageField(
        name='logo',
        required=0,      
        widget=ImageWidget(
            label='Logo',
            description='Caso deseje, você pode adicionar uma figura com o logo do Software Livre adotado ou do órgão/instituição em que você trabalha. Extensões de arquivos permitidas: .gif, .jpg, .jpeg, .png',
            visible={'view': 'invisible'},
        ),
        storage=AttributeStorage(),
        sizes= {'large'   : (768, 768),
               'preview' : (400, 400),
               'mini'    : (200, 200),
               'thumb'   : (128, 128),
               'tile'    :  (64, 64),
               'icon'    :  (32, 32),
               'listing' :  (16, 16),
              }, 
    ),

    FileField(
        name='arquivo_casodesucesso',
        widget=FileWidget(
            label='Baixe o caso completo',
            description="Caso deseje, você pode anexar um documento que tenha mais detalhes sobre seu caso de migração/adoção de Software Livre. Arquivo em formato PDF limitado a tamanho de 2MB",
        ),
    ),    


),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

CasoDeSucesso_schema = BaseSchema.copy() + \
    getattr(ATDocument, 'schema', Schema(())).copy() + \
    schema.copy()
    
CasoDeSucesso_schema['title'].validators = ('isNotOnlySpace_Casosdesucesso',)
CasoDeSucesso_schema['title']._validationLayer()
CasoDeSucesso_schema['description'].required=1
CasoDeSucesso_schema['description'].validators = ('isNotOnlySpace_Casosdesucesso',)
CasoDeSucesso_schema['description']._validationLayer()
CasoDeSucesso_schema['text'].widget.label = 'Detalhes do caso'
CasoDeSucesso_schema['text'].widget.label_msgid = ''
CasoDeSucesso_schema['text'].validators = ('isNotOnlySpace_Casosdesucesso',)
CasoDeSucesso_schema['text']._validationLayer()
CasoDeSucesso_schema['relatedItems'].widget.visible['edit'] = 'invisible'
CasoDeSucesso_schema['relatedItems'].widget.visible['view'] = 'invisible'
CasoDeSucesso_schema.moveField('categoria_casodesucesso', after='title')
CasoDeSucesso_schema.moveField('categoriasugerida_casodesucesso', after='categoria_casodesucesso')
CasoDeSucesso_schema.moveField('softwares_casodesucesso', after='description')
CasoDeSucesso_schema.moveField('orgao_casodesucesso', after='softwares_casodesucesso')
CasoDeSucesso_schema.moveField('autor_casodesucesso', after='text')
CasoDeSucesso_schema.moveField('email_casodesucesso', after='autor_casodesucesso')
CasoDeSucesso_schema.moveField('saibamais_casodesucesso', after='email_casodesucesso')
CasoDeSucesso_schema.moveField('arquivo_casodesucesso', after='saibamais_casodesucesso')
##code-section after-schema #fill in your manual code here
##/code-section after-schema

class CasoDeSucesso(ATDocument):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(ATDocument,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Caso de sucesso'

    meta_type = 'CasoDeSucesso'
    portal_type = 'CasoDeSucesso'
    allowed_content_types = []
    filter_content_types = 0
    global_allow = 0
    #content_icon = 'CasoDeSucesso.gif'
    immediate_view = 'casodesucesso_view'
    default_view = 'casodesucesso_view'
    suppl_views = ()
    typeDescription = "caso de sucesso"
    typeDescMsgId = 'description_edit_casodesucesso'

    _at_rename_after_creation = True

    actions =  (

       {'action': "string:${object_url}/casodesucesso_edit_form",
        'category': "object",
        'id': 'edit',
        'name': 'Edit',
        'permissions': ("Modify portal content",),
       },

    )

    aliases = {
         '(Default)' : 'casodesucesso_view', 
         'edit': 'casodesucesso_edit_form',
         'base_edit': 'casodesucesso_edit_form', 
         'view': 'casodesucesso_view',
         'base_view': 'casodesucesso_view',
        }


    schema = CasoDeSucesso_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods
    def at_post_create_script(self):
        putils = getToolByName(self, 'plone_utils')
        msg = 'O seu caso será analisado pela Secretaria do CISL e estará disponível em breve.'
        putils.addPortalMessage(msg)
            
    security.declarePublic('getCategoriaCasoDeSucesso')
    
    def getCategoriaCasoDeSucesso(self):
        """ Retorna a lista das categorias
        """  
        
        listaValores = []
        
        results_catalog = self.portal_catalog(portal_type='CategoriaCasoDeSucesso', review_state='published')
        ids_validos = [item.id for item in results_catalog]
        results_uid_catalog = self.uid_catalog(portal_type='CategoriaCasoDeSucesso')
        for r in results_uid_catalog:
            if r.id in ids_validos:
                listaValores.append((r.UID,r.Title))
                
        return DisplayList(listaValores) 
    
   
    def validate_arquivo_casodesucesso(self, value):
        """valida tamanho do arquivo e extensão
        """
        import types
        if value:
            
            # pega o nome do arquivo para ter certeza que o value é um file
            try:
                nome_arquivo = value.filename
            except:
                nome_arquivo = ''
            
            if nome_arquivo:
                result = True 
                try:
                    value.seek(pow(1024,2)*2)
                    if value.read(1):
                        result = False                
                    value.seek(0) # rewind to start  
                except:
                    pass               
                
                try:
                    extensao = ''.join(nome_arquivo.split('.')[1:])
                    if extensao.lower()!='pdf':
                        return 'Arquivo deve ser do tipo PDF'    
                    elif not result:
                        return 'Arquivo enviado maior que o máximo permitido'
                except:
                    return 'Arquivo deve ser do tipo PDF'

            
    def validate_logo(self, value):
        """valida tamanho do arquivo e extensão
        """
        arquivo = value
        result=True
        if arquivo:            
            try: 
                arquivo.seek(pow(1024,2)*0.25)
                if arquivo.read(1):
                    result = False                
                arquivo.seek(0) # rewind to start        
    
                if not result:
                    return 'Arquivo enviado maior que o máximo permitido:250kb'        
                else:
                   extensao = arquivo.filename[-4:].lower()
        
                   if extensao not in ['.gif','.jpg','.png','jpeg']:
                       return 'Arquivo precisa ser do tipo Imagem'
            except: pass
        

    def emptyFieldValue(self, field):
        """ verifica se o campo está vazio
        """
        accessor = field.accessor
        value = getattr(self, accessor)()
        return not value or len(value)==0 or len(str(value))==0
        
        
    

registerType(CasoDeSucesso, PROJECTNAME)
# end of class CasoDeSucesso

##code-section module-footer #fill in your manual code here
##/code-section module-footer



