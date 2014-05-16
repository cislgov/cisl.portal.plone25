from zope.interface import Interface, Attribute


class IGerenciaUsers(Interface):
    
    def listaUsuarios(self,name=None, todos=False):
        """ Lista usuarios.
        """ 