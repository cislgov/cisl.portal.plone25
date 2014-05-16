__author__ = """Wesley Barroso Lopes <wesleybl@gmail.com>"""
#__author2__ = """Rafael Ferreira Silva <rafael@rafaelsilva.net>"""
__docformat__ = 'plaintext'


from zope.interface import implements

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import utils

from Products.SERPROSCCaptchaField.browser.interfaces import ICaptcha
from Products.SERPROSCCaptchaField.config import PACKAGE_HOME

import PIL.Image, ImageDraw, ImageFont
import PIL.ImageFilter as ImageFilter
import cStringIO, random, os


class Captcha(utils.BrowserView):
    implements(ICaptcha)



    def geraImagem(self):
        """Gera a Imagem do Captcha"""
        
        # carregando a fonte Arial(tamanho 24) de um arquivo. O arquivo deve 
        #estar no File System
        fonts_path = PACKAGE_HOME+'/fonts'
        fonts = [x for x in os.listdir(fonts_path) if x.endswith('.ttf')]
        font = random.choice(fonts)
        font_path = fonts_path+'/'+font
        font = ImageFont.truetype(font_path, 24)
        
        #carregando o arquivo captcha.jpg do filesystem. Esse arquivo  o 
        #fundo da imagem.
        path = PACKAGE_HOME + '/captcha.jpg'
        f = open(path,'rb')
        file = f.read()
        f.close()
        
        oriFile = cStringIO.StringIO(file)

        image = PIL.Image.open(oriFile)
        image_type = image.format
        draw = ImageDraw.Draw(image)

        #pegando pontos aleat√≥rios para escrever o texto
        x = random.randint(5, 25)
        y = random.randint(5, 20)

        txt = ''
        #caracteres dispon√≠veis para serem escritos na imagem
        tmp = 'ABCDEFGHIJKLMNOPQRSTUVYXWZabcdefghijklmnopqrstuvyxwz1234567890'

        #gerando o texto de 5 caracteres para imagem
        cont = 0
        while cont < 5:
            txt += random.choice(tmp)
            cont += 1


        #escrevendo na imagem, o texto no ponto aleat√≥rio
        draw.text((x, y), txt, font=font, fill = 'Black')

        #gerando a imagem
        Imagemcaptcha = cStringIO.StringIO()
        image  = image.filter(ImageFilter.SMOOTH_MORE)
        image.save(Imagemcaptcha, image_type)
        Imagemcaptcha.seek(0)
        
        #gerando o texto de 5 digitos para o som
        som = '%.5d' % random.randint(0,99999)
        
        request = self.request 
        
        #gravando dados na sessao
        sessao = request.SESSION
        sessao['captcha'] = txt
        sessao['som'] = som
        
        #Retirando imagem do cache
        request['RESPONSE'].setHeader('Cache-Control', 'no-cache')
        
        #retornando imagem
        return Imagemcaptcha.getvalue()
    
        
    
    def geraSom(self):
        request = self.request
        request.RESPONSE.setHeader('Content-Type','audio/mpeg')
        try:
            ssom = request.SESSION['som']
        except:
           return request.RESPONSE.redirect(request['URL1'])

        #concatena arquivos de som
        ret = ''
        pathBip = PACKAGE_HOME + '/Sons/bip.mp3'
        f = open( pathBip, 'rb' )
        s = f.read()
        ret = ret+s
        f.close()
        for num in ssom:
            numPath = PACKAGE_HOME + '/Sons/' + num + '.mp3'
            f = open( numPath, 'rb' )
            s = f.read()
            ret = ret+s
            f.close()
        f = open( pathBip, 'rb' )
        s = f.read()
        ret = ret+s
        f.close()
        return ret

            
    def validaCaptcha(self, state):
        
        # pega o request e a sessao
        request = self.request
        sessao = request.SESSION
        
        #pega o valor do captcha informado pelo usuario e o valor da sessao
        captcha = request['captcha']
        try:
            scaptcha = sessao['captcha']
        except:
            state.setError\
                ('erro_captcha', u'Os caracteres s„o diferentes da imagem!')
            state.setStatus('failure')
            getToolByName(self,'plone_utils').addPortalMessage\
               (u'Favor corrigir os erros indicados.')
            return state
        
        #testa se o valor do captcha informado pelo usuario È o mesmo que est·
        #na sessao representando a imagem
        if captcha == scaptcha:
            del sessao['captcha']
            del sessao['som']
            return state
        else:
            try:
                som = sessao['som']
            except:
                state.setError\
                    ('erro_captcha', u'Os caracteres s„o diferentes da imagem!')
                state.setStatus('failure')
                getToolByName(self,'plone_utils').addPortalMessage\
                   (u'Favor corrigir os erros indicados.')
                return state
            #testa se o valor do captcha informado pelo usuario È o mesmo que 
            #est· na sessao representando o som
            if som == captcha:
                del sessao['captcha']
                del sessao['som']
                return state

        state.setError\
            ('erro_captcha', u'Os caracteres s„o diferentes da imagem!')
        state.setStatus('failure')
        getToolByName(self,'plone_utils').addPortalMessage\
           (u'Favor corrigir os erros indicados.')
        return state

                
            

        
        
