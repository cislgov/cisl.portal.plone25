# -*- coding: utf-8 -*-
#
# File: password_tool.py
#
# Copyright (c) 2007 by SERPRO
# Generator: ArchGenXML 
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

__author__ = """Clayton Caetano de Sousa <claytonc.sousa@gmail.com>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.SERPROSenha.config import *

# additional imports from tagged value 'import'
from Products.SERPROSenha.Widgets import BloqueiaCampos
from Products.CMFCore.utils import getToolByName
import datetime
import re


from Products.CMFCore.utils import UniqueObject

    
##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    IntegerField(
        name='lim_password',
        default=5,
        widget=IntegerField._properties['widget'](
            label="MÃ­nimo de caracteres",
            description="Informe o limite mÃ­nimo de caracetres para senha.",
            label_msgid='SERPROSenha_label_lim_password',
            description_msgid='SERPROSenha_help_lim_password',
            i18n_domain='SERPROSenha',
        ),
        required=True
    ),

    IntegerField(
        name='lim_max_password',
        default="0",
        widget=IntegerField._properties['widget'](
            label="mÃ¡ximo de caracteres",
            description="Informe o limite mÃ¡ximo de caracteres para a senha. Para habilitar coloque um nÃºmero maior ou igual que o mÃ­nimo de caracteres.",
            label_msgid='SERPROSenha_label_lim_max_password',
            description_msgid='SERPROSenha_help_lim_max_password',
            i18n_domain='SERPROSenha',
        ),
        required=1
    ),

    StringField(
        name='enb_lock_login',
        widget=BloqueiaCampos(
            label="Habilita bloqueio de login ou Captcha",
            format="radio",
            label_msgid='SERPROSenha_label_enb_lock_login',
            i18n_domain='SERPROSenha',
            attributes='nchange string:onchange=listaSubValores()',
        ),
        vocabulary=['Bloqueio','Captcha']
    ),

    IntegerField(
        name='qtd_tentativas',
        default="3",
        widget=IntegerField._properties['widget'](
            label="NÃºmero de Tentativas",
            description="Informe a quantidade de tentativas.",
            label_msgid='SERPROSenha_label_qtd_tentativas',
            description_msgid='SERPROSenha_help_qtd_tentativas',
            i18n_domain='SERPROSenha',
        ),
        required=True
    ),

    IntegerField(
        name='mnt_lock',
        default="30",
        widget=IntegerField._properties['widget'](
            label="Minutos Bloqueado",
            description="Informe a quantidade de minutos que o login do usuario ficara bloqueado.",
            label_msgid='SERPROSenha_label_mnt_lock',
            description_msgid='SERPROSenha_help_mnt_lock',
            i18n_domain='SERPROSenha',
        ),
        required=True
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

password_tool_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
password_tool_schema['title'].required = 0
password_tool_schema['title'].widget.visible = {'view':'invisible', 'edit':'invisible'}
##/code-section after-schema

class password_tool(UniqueObject, BaseContent):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(UniqueObject,'__implements__',()),) + (getattr(BaseContent,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'password_tool'

    meta_type = 'password_tool'
    portal_type = 'password_tool'
    allowed_content_types = []
    filter_content_types = 0
    global_allow = 0
    #content_icon = 'password_tool.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "password_tool"
    typeDescMsgId = 'description_edit_password_tool'
    #toolicon = 'password_tool.gif'


    actions =  (


       {'action': "string:${object_url}/edit",
        'category': "object",
        'id': 'edit',
        'name': 'Edit',
        'permissions': ("ManagePortal",),
        'condition': 'python:1'
       },


       {'action': "string:$portal_url/portal_password/useslock_form",
        'category': "object",
        'id': 'users_lock',
        'name': 'UsuÃ¡rios Bloqueados',
        'permissions': ("ManagePortal",),
        'condition': 'python:1'
       },


    )

    _at_rename_after_creation = True

    schema = password_tool_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header


    # tool-constructors have no id argument, the id is fixed
    def __init__(self, id=None):
        BaseContent.__init__(self,'portal_password')
        self.setTitle('password_tool')
        
        ##code-section constructor-footer #fill in your manual code here
        ##/code-section constructor-footer


    # tool should not appear in portal_catalog
    def at_post_edit_script(self):
        self.unindexObject()
        
        ##code-section post-edit-method-footer #fill in your manual code here
        ##/code-section post-edit-method-footer


    # Methods

    security.declarePublic('testaSenha')
    def testaSenha(self,password,password_confirm,current=None,username=None):
        """
        Testa a senha do usuario como: limite minimo, senha deve ser diferente do user id etc.
        """
        if not password:
            return 'You must enter a password.'

        limpwd = self.getLim_password()
        maxpwd = self.getLim_max_password()
        
        #verifica se o maximo de caracteres esta ativado 
        if maxpwd >= limpwd:
            if len(password) > maxpwd:
                return ('Informe sua nova senha. Maximo de %s caracteres.'%maxpwd)
            
        #verificar se o usuario informou o minimo de caracteres
        if len(password) < limpwd:
            return ('Informe sua nova senha. Minimo de %s caracteres.'%limpwd)
     
        if password_confirm is not None and password_confirm != password:
            return ('Informe novamente a senha.'
                   + 'Certifique-se que as senhas informadas sao identicas.')
         
        #imposibilita que o usuario informe a senha antiga na alteração de senha 
        if current:
            if current == password:
                return ('Favor informar a nova senha diferente da atual. ')
        if username:
            user= str(username)
            password = str(password)
            if (user == password):
                return ('Favor informar uma senha diferente do id do usuario')
        
        #verifica se o usuario informou uma senha forte
        ok, message =  self.senhaForte( password )
        if not ok:
            return message

    security.declarePublic('senhaForte')
    def senhaForte(self,password):
        """
        Verifica se a senha contem uma combinacao de caracteres maiusculos, minusculos, especiais e numericos.
        """
        limpwd = self.getLim_password()
        maxpwd = self.getLim_max_password()

        if maxpwd >= limpwd:
            quant = '{'+str(limpwd)+','+str(maxpwd)+'}'
        else:
            quant = '{'+str(limpwd)+',}'

        _TESTS =[re.compile("(?!^[0-9]*$)(?!^[\W]*$)(?!^[a-zA-Z]*$)^([a-zA-Z0-9\W]"+str(quant)+")$")]

        message = 'Informe uma senha que contenha uma combinacao de caracteres: - maiusculos ou minusculos e numericos, Ou  \n - maiusculos, minusculos e especiais, Ou \n - numericos e especiais.'

        for pattern  in _TESTS:
            matched = pattern.search(str(password)) is not None
            if matched != True:
                return False, message
            return True , ''

    security.declarePublic('validaSenha')
    def validaSenha(self,userid):
        """
        Verifica a quantidade de erros de login e apos x tentativa o login e bloqueado por um determindo x tempo.
        """
        membro = getToolByName(self, 'portal_membership').getMemberById(str(userid))

        #verificar se e um usuário valido
        if membro:
            properties={}
            data_atual = datetime.datetime.now()
            teste = membro.getProperty('date_lock',None)
            erros = membro.getProperty('error_count',None)
            erros = int(erros)

            if erros >= self.getQtd_tentativas():
                    date = data_atual
                    if date > teste:
                        properties['error_count']=str(0)
                        putils = getToolByName(self, 'plone_utils').setMemberProperties(membro, **properties)
                    else:
                        tempo = teste - date
                        return (u'Login bloqueado, sera liberado em %s minutos.'%str(tempo))
            else:
                if erros <= self.getQtd_tentativas():
                    tentativas = erros
                    tentativas = int(tentativas) + 1
                    properties['error_count']=str(tentativas)
                    putils = getToolByName(self, 'plone_utils').setMemberProperties(membro, **properties)
                    if tentativas >= self.getQtd_tentativas():
                        self.envia_notificacao(usuario=membro)
                        data_futura =  data_atual + datetime.timedelta(minutes=self.getMnt_lock())
                        properties['date_lock']=data_futura
                        properties['error_count']=str(self.getQtd_tentativas())
                        putils = getToolByName(self, 'plone_utils').setMemberProperties(membro, **properties)
                    return (u'Senha incorreta, apos 3 tentativas o login no portal sera bloqueado por %s minutos.'%self.getMnt_lock())

        else:
            return ('Login failed')

    security.declarePublic('getUsersLock')
    def getUsersLock(self):
        """
        Busca os usuarios que estao com o login bloqueados.
        """
        users = users = getToolByName(self,'portal_membership').listMemberIds()
        qtd = self.getQtd_tentativas()
        users_lock = []

        for user in users:
            usuario = getToolByName(self, 'portal_membership').getMemberById(str(user))
            data_atual = datetime.datetime.now()
            date_lock = usuario.getProperty('date_lock',None)
            erros = usuario.getProperty('error_count',None)
            if int(erros) >= self.getQtd_tentativas():
                if data_atual < date_lock:
                    users_lock.append(user)
        return  users_lock

    security.declarePublic('debloqueiaUser')
    def debloqueiaUser(self,userid):
        """
        Desbloqueia o login dos usuarios.
        """
        member = getToolByName(self, 'portal_membership').getMemberById(str(userid))
        properties={}
        properties['error_count']=str(0)
        putils = getToolByName(self, 'plone_utils').setMemberProperties(member,**properties)

        return True

    security.declarePublic('envia_notificacao')
    def envia_notificacao(self,usuario):
        """
        Envia e-mail para os usuarios bloqueados
        """
        user=usuario
        mhost = getToolByName(self,'MailHost')
        urltool = getToolByName(self, 'portal_url')
        portal = urltool.getPortalObject()
        envelope_from = portal.getProperty('email_from_address')
        remetente = envelope_from
        assunto = 'Login bloqueado'
        mensagem="""
        <html>
        <body>
        Prezado usuário,<br /><br />
        Essa é uma notificação para informar-lo que de sua senha foi Bloqueada no Portal.
        Para se autênticar no portal aguarde por <b> %s minutos </b> ou entre em contato com o <b>Administrador do portal.</b>
        <br /><br/>
        seu login é: <b>%s</b><br /><br />
        Caso tenha esquecido sua senha, acesse a página de login e clique no link <b>"Se você perdeu sua senha, clique aqui para recebê-la."</b>, digite seu login e clique no botão <b>Envie minha senha</b>.<br />
        Ela será enviada para sua conta de email.<br /><br />

        Atenciosamente,<br />
        Administrador do Portal 
        </body>
        </html>
        """

        destinatario = usuario.getProperty('email',None) 
        texto = mensagem %(self.getMnt_lock(), user)
        mhost.secureSend(message=texto, mto=destinatario, mfrom=remetente, subject=assunto, subtype='html', charset='utf-8')
        return 1

def modify_fti(fti):
    # Hide unnecessary tabs (usability enhancement)
    for a in fti['actions']:
        if a['id'] in ['view', 'metadata', 'sharing']:
            a['visible'] = 0
    return fti

registerType(password_tool, PROJECTNAME)
# end of class password_tool

##code-section module-footer #fill in your manual code here
##/code-section module-footer



