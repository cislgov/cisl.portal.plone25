# -*- coding: utf-8 -*-
#
# File: content.py
#
# Copyright (c) 2010 by []
# Generator: ArchGenXML Version 1.5.2
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

__author__ = """unknown <unknown>"""
__docformat__ = 'plaintext'


##code-section init-module-header #fill in your manual code here
##/code-section init-module-header


# Subpackages
# Additional

# Classes
import CasoDeSucesso
import CategoriaCasoDeSucesso
import PastaCasoDeSucesso
import PastaCategoriaCasoDeSucesso

##code-section init-module-footer #fill in your manual code here
from AccessControl.User import nobody 

def getProperty(self, name, default=''): 
    if name == 'wysiwyg_editor': 
        return 'FCKeditor' 
    return False 
(nobody.__class__).getProperty = getProperty 

nobody.wysiwyg_editor = 'FCKeditor'
##/code-section init-module-footer

