from zope.interface import implements

from Products.CMFPlone import utils
from Products.SERPROSCWorkflow.browser.interfaces import IGerenciaUsers
from Products.CMFCore.utils import getToolByName


class GerenciaUsers(utils.BrowserView):
    
    implements(IGerenciaUsers)
    
    def listaUsuarios(self,name=None, todos=False):
        """ 
            Busca pelo id ou nome completo
            Caso name nao seja passado retorna todos os usuarios listed e nao Managers
        """
        usuarios = []
        membership = getToolByName(self,'portal_membership')
        ids_geral = membership.listMemberIds()
        for id in ids_geral:
            member = membership.getMemberById(id)
            if member is not None:
                if member.getProperty('listed',False) and not member.has_role(('Manager',)):
                    if name and not todos:
                        if name == id:
                            usuarios.append(member)
                        else:
                            fullname = member.getProperty('fullname','').strip().lower()
                            if fullname.find(name.strip().lower()) != -1:
                                usuarios.append(member)
                    else:
                        usuarios.append(member)
        return usuarios
