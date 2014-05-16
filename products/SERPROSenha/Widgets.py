from AccessControl import ClassSecurityInfo
from Products.Archetypes.Registry import registerWidget
from Products.Archetypes.public import StringWidget


class BloqueiaCampos(StringWidget):
    security = ClassSecurityInfo()

    _properties = StringWidget._properties.copy()
    _properties.update({
        'macro' : 'bloqueiowidget',
        'helper_js': ('bloqueiacampos.js',),
        })

registerWidget(BloqueiaCampos,
               title='Seleciona Bloqueio',
               description="Widget para seleção de bloqueio ou captcha",
               used_for=('Products.Archetypes.public.StringField',)
               ) 
