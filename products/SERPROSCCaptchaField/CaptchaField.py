# File: CaptchaField.py
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

#CaptchaField

from AccessControl import ClassSecurityInfo
from Acquisition import aq_base

from Products.CMFCore.utils import getToolByName

from Products.Archetypes.Field import ObjectField,encode,decode
from Products.Archetypes.Registry import registerField
from Products.Archetypes.utils import DisplayList
from Products.Archetypes import config as atconfig
from Products.Archetypes.Widget import *
from Products.Archetypes.Field  import *
from Products.Archetypes.Schema import Schema
from Products.generator import i18n

from Products.SERPROSCCaptchaField import config

##code-section module-header #fill in your manual code here
import PIL.Image, ImageDraw, ImageFont
import cStringIO, random
##/code-section module-header

from Products.SERPROSCCaptchaField.CaptchaWidget import CaptchaWidget




class CaptchaField(ObjectField):
    ''' '''

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    __implements__ = (getattr(ObjectField,'__implements__',()),)


    _properties = ObjectField._properties.copy()
    _properties.update({
        'type': 'captchafield',
        'widget':CaptchaWidget,
        ##code-section field-properties #fill in your manual code here
        ##/code-section field-properties

        })

    security  = ClassSecurityInfo()


    security.declarePrivate('set')
    security.declarePrivate('get')


    def getRaw(self, instance, **kwargs):
        return ObjectField.getRaw(self,instance,**kwargs)

    def set(self, instance, value, **kwargs):
        return ObjectField.set(self,instance,value,**kwargs)

    def get(self, instance, **kwargs):
        return ObjectField.get(self,instance,**kwargs)


registerField(CaptchaField,
              title='CaptchaField',
              description='')

##code-section module-footer #fill in your manual code here
##/code-section module-footer



