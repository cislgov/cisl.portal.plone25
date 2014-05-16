# -*- coding: utf-8 -*-
#
# File: SERPROSCWorkflow.py
#
# Copyright (c) 2006 by ['SERPRO/SUPSC']
# Generator: ArchGenXML Version 1.5.0
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

__author__ = """SERPRO/SUPSC/SCWEB-BHE"""
__docformat__ = 'plaintext'


from Products.CMFCore.utils import getToolByName
from Products.ExternalMethod.ExternalMethod import ExternalMethod

##code-section module-header #fill in your manual code here
##/code-section module-header

def installWorkflows(self, package, out):
    """Install the custom workflows for this product."""

    productname = 'SERPROSCWorkflow'
    workflowTool = getToolByName(self, 'portal_workflow')

    ourProductWorkflow = ExternalMethod('temp', 'temp',
                                        productname+'.'+'SERPROSCWorkflow',
                                        'createSERPROSCWorkflow')
    workflow = ourProductWorkflow(self, 'SERPROSCWorkflow')
    if 'SERPROSCWorkflow' in workflowTool.listWorkflows():
        print >> out, 'SERPROSCWorkflow already in workflows.'
    else:
        workflowTool._setObject('SERPROSCWorkflow', workflow)

    #setar o workflow como Default
    workflowTool.setDefaultChain(workflow.getId())

    #setar o workflow em outros Portal types
    #workflowTool.setChainForPortalTypes(['Plone Site'], workflow.getId())
    # A linha acima foi comentada para nao permitir a despublicacao do plone site
    workflowTool.setChainForPortalTypes(['Folder'], workflow.getId())
    workflowTool.setChainForPortalTypes(['Large Plone Folder'], workflow.getId())
    workflowTool.setChainForPortalTypes(['Topic'], workflow.getId())


    return workflowTool


def uninstallWorkflows(self, package, out):
    """Deinstall the workflows.

    This code doesn't really do anything, but you can place custom
    code here in the protected section.
    """

    ##code-section workflow-uninstall #fill in your manual code here
    ##/code-section workflow-uninstall

    pass
