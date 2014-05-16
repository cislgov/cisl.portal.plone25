from zope.interface import Interface

class ICaptcha(Interface):
    
    def geraImagem(self):
        """Gera a imagem do Captcha"""

    def geraSom(self):
        """Gera o Som do Captcha Sonoro"""
        
    def validaCaptcha(self, state):
        """Valida o captcha"""