from zope.interface import Interface, Attribute

       
class ICasoDeSucessoUtils(Interface):
    """Orgao marker interface
    """        
    def enviarEmail():
        """ envia email
        """

    def validaEmail():
        """ valida email
        """    

    def getLogoCasoDeSucesso():
        """ retorna o logo do caso de sucesso
        """

    def obter_casosdesucesso():
        """ retorna os casos de sucessos de acordo com os parametros passados
        """
        
    def lista_categorias():
        """ retorna as categorias de acordo com os parametros passados
        """
        
