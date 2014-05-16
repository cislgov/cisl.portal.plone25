# File: CaptchaWidget.py
#
# Copyright (c) 2006 by ['Rafael Ferreira Silva']
# Generator: ArchGenXML Version 1.4.1
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

__author__ = """Wesley Barroso Lopes <wesleybl@gmail.com>"""
__author2__ = """Rafael Ferreira Silva <rafael@rafaelsilva.net>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Acquisition import aq_base

from Products.CMFCore.utils import getToolByName

from Products.Archetypes.Registry import registerWidget
from Products.Archetypes.utils import DisplayList
from Products.Archetypes import config as atconfig
from Products.Archetypes.Widget import *
from Products.Archetypes.Widget import TypesWidget
from Products.generator import i18n

from Products.SERPROSCCaptchaField import config

##code-section module-header #fill in your manual code here
##/code-section module-header



class CaptchaWidget(TypesWidget):
    ''' '''

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    __implements__ = (getattr(TypesWidget,'__implements__',()),)

    _properties = TypesWidget._properties.copy()
    _properties.update({
        'macro' : 'CaptchaWidget',
        'size' : '30',
        'maxlength' : '255',
        ##code-section widget-properties #fill in your manual code here
        ##/code-section widget-properties

        })

    security = ClassSecurityInfo()



registerWidget(CaptchaWidget,
               title='CaptchaWidget',
               description=('Widget para mostrar o captcha'),
               used_for=('Products.Archetypes.Field.CaptchaField',)
               )
##code-section module-footer #fill in your manual code here
##/code-section module-footer



