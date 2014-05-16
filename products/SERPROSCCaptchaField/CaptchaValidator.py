from Products.validation.interfaces import ivalidator

class captchaValidator:
    __implements__ = (ivalidator,)
    def __init__(self, name):
        self.name = name
    def __call__(self, value, *args, **kwargs):
        context = kwargs["instance"]
        session = context.REQUEST.SESSION
        if session['captcha'] != value:
           return 'Diferença entra a Imagem e o Texto abaixo!'
        else:
            return 1