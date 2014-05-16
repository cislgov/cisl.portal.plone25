import re
from Products.validation.interfaces import ivalidator
from Products.validation.validators.RegexValidator import RegexValidator
from Products.Archetypes.public import ImageField
from Products.CasosDeSucesso.config import *
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _

class isNumberValidator:
    __implements__ = (ivalidator,)
    def __init__(self,name):
        self.name = name
    def __call__(self,value,*args,**kwargs):
        
        if not value.isdigit():
            return 'Este campo só deve conter números inteiros.'
        
        return True


class isSpaceValidator:
    __implements__ = (ivalidator,)
    def __init__(self,name):
        self.name = name
    def __call__(self,value,*args,**kwargs):
        
        if not value.strip():
            return 'Este campo não deve conter apenas espaços.'
        
        return True    
    

class isEmailValidator:
    __implements__ = (ivalidator,)
    def __init__(self,name):
        self.name = name
    def __call__(self,value,*args,**kwargs):

        if value:
            msg_email_invalido = 'E-mail inválido, favor corrigir.'
            EMAIL_RE = "([0-9a-zA-Z_&.+-]+!)*[0-9a-zA-Z_&.+-]+@(([0-9a-zA-Z]([0-9a-zA-Z-]*[0-9a-z-A-Z])?\.)+[a-zA-Z]{2,6}|([0-9]{1,3}\.){3}[0-9]{1,3})$"
            
            comp = re.compile(EMAIL_RE)
            m = comp.match(value)
            
            if not m:
                    return msg_email_invalido
        
        return True