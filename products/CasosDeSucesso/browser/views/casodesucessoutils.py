from zope.interface import implements
from AccessControl import getSecurityManager

from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.CasosDeSucesso.browser.interfaces import ICasoDeSucessoUtils
from DateTime import DateTime
from Products.CMFPlone import PloneMessageFactory as _
import types
import re

class CasoDeSucessoUtils(BrowserView):
    implements(ICasoDeSucessoUtils)

    def __init__(self, context, request, *args, **kw):
        self.context = [context]
        self.request = request
                
    def enviarEmail(self, de='', para='', assunto='', mensagem=''):
        """ envia email
        """
        mailHost = getToolByName(self, 'MailHost')
        result = mailHost.secureSend(message = mensagem, 
                                     mto = para, 
                                     mfrom = de, 
                                     subject = assunto, 
                                     subtype =  'plain', 
                                     charset = 'utf-8', 
                                     debug = False, )
        
        
    def validaEmail(self, valor):
        """ valida email
        """
        if valor:
            EMAIL_RE = "([0-9a-zA-Z_&.+-]+!)*[0-9a-zA-Z_&.+-]+@(([0-9a-zA-Z]([0-9a-zA-Z-]*[0-9a-z-A-Z])?\.)+[a-zA-Z]{2,6}|([0-9]{1,3}\.){3}[0-9]{1,3})$"
            comp = re.compile(EMAIL_RE)
            m = comp.match(valor)
            if not m:
                return False
        return True
    
    
    def getLogoCasoDeSucesso(self, url):
        """ retorna o logo do caso de sucesso
        """
        import urllib
        
        try:
            path_logo = '%s/logo_mini' % url
            logo = urllib.urlopen(path_logo)
            if ('image' in logo.headers.type) or ('index_html' in logo.url):
                return path_logo
        except:
            return None
        
        return None    
    
    
    def obter_casosdesucesso(self, texto=None, categoria=None, path=None, sort_on='created', sort_order='reverse', limit=None, findAll=None):
        """ retorna os casos de sucessos de acordo com os parametros passados
        """
        filter = {
              'portal_type':'CasoDeSucesso',
             }

        if not findAll:
            if texto:
                filter['SearchableText'] = texto
    
            if categoria:
                filter['getRawCategoria_casodesucesso'] = categoria
        
            if limit:
                filter['limit'] = limit

        if path:
            filter['path'] = path

        if sort_on:
            filter['sort_on'] = sort_on

        if sort_order:
            filter['sort_order'] = sort_order
        
        try:
            portal_catalog = getToolByName(self, 'portal_catalog')
            return portal_catalog(filter)
        except:
            return []
    
    def lista_categorias(self,path):  
        
        filter = {
              'portal_type':'CategoriaCasoDeSucesso',
              'path':path,
              'review_state':'published',
             }
        
        try:
            portal_catalog = getToolByName(self, 'portal_catalog')
            results = portal_catalog(filter)
            
            # transforma em List para ordenar
            plone_utils = getToolByName(self, 'plone_utils')
            normalizeString = plone_utils.normalizeString
            
            lista = [r for r in results]
            lista.sort(lambda x,y : cmp(normalizeString(x.Title),normalizeString(y.Title)))
            
            return lista
        except:
            return []
        
        
