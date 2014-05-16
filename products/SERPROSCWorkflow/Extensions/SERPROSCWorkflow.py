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
from Products.CMFCore.WorkflowTool import addWorkflowFactory
from Products.DCWorkflow.DCWorkflow import DCWorkflowDefinition
from Products.ExternalMethod.ExternalMethod import ExternalMethod
from Products.SERPROSCWorkflow.config import *


productname = 'SERPROSCWorkflow'

def setupSERPROSCWorkflow(self, workflow):
    """Define the SERPROSCWorkflow workflow.
    """
    # Add additional roles to portal
    portal = getToolByName(self,'portal_url').getPortalObject()
    data = list(portal.__ac_roles__)
    for role in ['Conteudista', 'Visitante_Restrito','Administrador_Usuario']:
        if not role in data:
            data.append(role)
        #Adiciona roles no acl_users.portal_role_manager
        # first try to fetch it. if its not there, we probaly have no PAS 
        # or another way to deal with roles was configured.
        try:
            prm = portal.acl_users.get('portal_role_manager', None)
            if prm is not None:
                try:
                    prm.addRole(role, role, "Added by product SERPROSCWorkflow")
                except KeyError: # role already exists
                    pass
        except AttributeError:
            pass

    #Adiciona roles na aba securiy
    portal.__ac_roles__ = tuple(data)

    workflow.setProperties(title='SERPROSCWorkflow')


    for s in ['publicado_todos', 'rascunho', 'aguardando_revisao', 'publicado_restrito']:
        workflow.states.addState(s)

    for t in ['submeter', 'publicar', 'rejeitar', 'retirar', 'restringir']:
        workflow.transitions.addTransition(t)

    for v in ['review_history', 'comments', 'time', 'actor', 'action']:
        workflow.variables.addVariable(v)

    for p in ['Access contents information', 'Add portal content', \
              'ATContentTypes: Add Document', 'ATContentTypes: Add Event',\
              'ATContentTypes: Add Favorite', 'ATContentTypes: Add File', \
              'ATContentTypes: Add Folder', 'ATContentTypes: Add Image', \
              'ATContentTypes: Add Large Plone Folder', \
              'ATContentTypes: Add Link', 'ATContentTypes: Add News Item', \
              'Add portal topics', 'Change portal events',  'Delete objects', \
              'List folder contents', 'Manage portal', 'Manage users', \
              'Modify portal content', 'Modify constrain types', 'View', \
              'Manage properties', 'Copy or Move', 'Review portal content', \
              'View management screens','Modify view template','View Groups',\
              'Delete Groups','Add Groups','Manage Groups','Add portal member']:
        
        workflow.addManagedPermission(p)

    for l in ['pendentes']:
        if not l in workflow.worklists.objectValues():
            workflow.worklists.addWorklist(l)

    ## Initial State
    workflow.states.setInitialState('rascunho')
    ## States initialization

    stateDef = workflow.states['rascunho']
    stateDef.setProperties(title="""Rascunho""",
                           transitions=['submeter'])

    stateDef.setPermission('View management screens',
                           0,
                           ['Owner', 'Manager'])

    stateDef.setPermission('Review portal content',
                           0,
                           ['Manager', 'Reviewer'])

    stateDef.setPermission('Manage properties',
                           0,
                           ['Manager'])
				
    stateDef.setPermission('Manage users',
                           0,
                           ['Manager','Administrador_Usuario'])
	
    stateDef.setPermission('Copy or Move',
                           0,
                           ['Owner', 'Manager', 'Conteudista'])

    stateDef.setPermission('Add portal content',
                           0,
                           ['Manager', 'Conteudista'])

    stateDef.setPermission('Access contents information',
                           0,
                           ['Owner', 'Manager', 'Reviewer', 'Conteudista'])

    stateDef.setPermission('Add portal topics',
                           0,
                           ['Manager'])

    stateDef.setPermission('Change portal events',
                           0,
                           ['Owner', 'Manager'])

    stateDef.setPermission('Delete objects',
                           0,
                           ['Owner', 'Manager', 'Conteudista'])

    stateDef.setPermission('List folder contents',
                           0,
                           ['Owner', 'Manager', 'Reviewer', 'Conteudista'])

    stateDef.setPermission('Manage portal',
                           0,
                           ['Owner', 'Manager', 'Conteudista','Administrador_Usuario'])

    stateDef.setPermission('Modify portal content',
                           0,
                           ['Owner', 'Manager', 'Conteudista'])

    stateDef.setPermission('Modify constrain types',
                           0,
                           ['Manager'])

    stateDef.setPermission('Modify view template',
                           0,
                           ['Owner', 'Manager', 'Reviewer'])

    stateDef.setPermission('View',
                           0,
                           ['Owner', 'Manager', 'Conteudista', 'Reviewer'])

    stateDef.setPermission('ATContentTypes: Add Document',
                           0,
                           ['Manager', 'Conteudista'])

    stateDef.setPermission('ATContentTypes: Add Event',
                           0,
                           ['Manager', 'Conteudista'])

    stateDef.setPermission('ATContentTypes: Add Favorite',
                           0,
                           ['Manager', 'Conteudista'])

    stateDef.setPermission('ATContentTypes: Add File',
                           0,
                           ['Manager', 'Conteudista'])

    stateDef.setPermission('ATContentTypes: Add Folder',
                           0,
                           ['Manager', 'Conteudista'])

    stateDef.setPermission('ATContentTypes: Add Image',
                           0,
                           ['Manager', 'Conteudista'])

    stateDef.setPermission('ATContentTypes: Add Large Plone Folder',
                           0,
                           ['Manager', 'Conteudista'])

    stateDef.setPermission('ATContentTypes: Add Link',
                           0,
                           ['Manager', 'Conteudista'])

    stateDef.setPermission('ATContentTypes: Add News Item',
                           0,
                           ['Manager', 'Conteudista'])


    stateDef = workflow.states['publicado_todos']
    stateDef.setProperties(title="""Publicado Para Todos""",
                           transitions=['retirar', 'restringir'])

    stateDef.setPermission('Add portal member',
                           1,
                           ['Manager','Administrador_Usuario'])

    stateDef.setPermission('Manage Groups',
                           0,
                           ['Manager','Administrador_Usuario'])

    stateDef.setPermission('Delete Groups',
                           0,
                           ['Manager','Administrador_Usuario'])

    stateDef.setPermission('Add Groups',
                           0,
                           ['Manager','Administrador_Usuario'])
    
    stateDef.setPermission('View Groups',
                           0,
                           ['Manager','Administrador_Usuario'])
    
    stateDef.setPermission('View management screens',
                           0,
                           ['Manager'])

    stateDef.setPermission('Review portal content',
                           0,
                           ['Manager', 'Reviewer'])

    stateDef.setPermission('Manage properties',
                           0,
                           ['Manager'])
				
    stateDef.setPermission('Manage users',
                           0,
                           ['Manager','Administrador_Usuario'])
    
    stateDef.setPermission('Copy or Move',
                           0,
                           ['Manager', 'Conteudista'])

    stateDef.setPermission('Add portal content',
                           0,
                           ['Conteudista', 'Manager'])

    stateDef.setPermission('Access contents information',
                           0,
                           ['Anonymous', 'Authenticated', 'Conteudista', 'Manager', 'Owner', 'Reviewer'])

    stateDef.setPermission('Add portal topics',
                           0,
                           ['Manager'])

    stateDef.setPermission('Change portal events',
                           0,
                           ['Manager'])

    stateDef.setPermission('Delete objects',
                           0,
                           ['Manager'])

    stateDef.setPermission('List folder contents',
                           0,
                           ['Authenticated', 'Conteudista', 'Manager', 'Owner', 'Reviewer'])

    stateDef.setPermission('Manage portal',
                           0,
                           ['Reviewer', 'Manager','Administrador_Usuario'])

    stateDef.setPermission('Modify portal content',
                           0,
                           ['Manager'])

    stateDef.setPermission('Modify constrain types',
                           0,
                           ['Manager'])

    stateDef.setPermission('Modify view template',
                           0,
                           ['Manager', 'Reviewer'])

    stateDef.setPermission('View',
                           1,
                           ['Anonymous', 'Authenticated', 'Conteudista', 'Manager', 'Owner', 'Reviewer'])


    stateDef.setPermission('ATContentTypes: Add Document',
                           0,
                           ['Manager', 'Conteudista'])

    stateDef.setPermission('ATContentTypes: Add Event',
                           0,
                           ['Manager', 'Conteudista'])

    stateDef.setPermission('ATContentTypes: Add Favorite',
                           0,
                           ['Manager', 'Conteudista'])

    stateDef.setPermission('ATContentTypes: Add File',
                           0,
                           ['Manager', 'Conteudista'])

    stateDef.setPermission('ATContentTypes: Add Folder',
                           0,
                           ['Manager', 'Conteudista'])

    stateDef.setPermission('ATContentTypes: Add Image',
                           0,
                           ['Manager', 'Conteudista'])

    stateDef.setPermission('ATContentTypes: Add Large Plone Folder',
                           0,
                           ['Manager', 'Conteudista'])

    stateDef.setPermission('ATContentTypes: Add Link',
                           0,
                           ['Manager', 'Conteudista'])

    stateDef.setPermission('ATContentTypes: Add News Item',
                           0,
                           ['Manager', 'Conteudista'])



    stateDef = workflow.states['aguardando_revisao']
    stateDef.setProperties(title="""Aguardando Revisão""",
                           transitions=['publicar', 'rejeitar', 'restringir'])

    stateDef.setPermission('View management screens',
                           0,
                           ['Manager', 'Reviewer'])

    stateDef.setPermission('Review portal content',
                           0,
                           ['Manager', 'Reviewer'])

    stateDef.setPermission('Manage properties',
                           0,
                           ['Manager'])

    stateDef.setPermission('Manage users',
                           0,
                           ['Manager','Administrador_Usuario'])
    
    stateDef.setPermission('Copy or Move',
                           0,
                           ['Reviewer', 'Manager', 'Conteudista'])

    stateDef.setPermission('Add portal content',
                           0,
                           ['Manager', 'Conteudista'])

    stateDef.setPermission('Access contents information',
                           0,
                           ['Manager', 'Owner', 'Reviewer', 'Conteudista'])

    stateDef.setPermission('Add portal topics',
                           0,
                           ['Manager'])

    stateDef.setPermission('Change portal events',
                           0,
                           ['Manager', 'Reviewer'])

    stateDef.setPermission('Delete objects',
                           0,
                           ['Manager'])

    stateDef.setPermission('List folder contents',
                           0,
                           ['Manager', 'Owner', 'Reviewer', 'Conteudista'])

    stateDef.setPermission('Manage portal',
                           0,
                           ['Reviewer', 'Manager','Administrador_Usuario'])

    stateDef.setPermission('Modify portal content',
                           0,
                           ['Manager','Reviewer'])

    stateDef.setPermission('Modify constrain types',
                           0,
                           ['Manager'])

    stateDef.setPermission('Modify view template',
                           0,
                           ['Reviewer', 'Manager'])

    stateDef.setPermission('View',
                           0,
                           ['Manager', 'Owner', 'Reviewer', 'Conteudista'])


    stateDef.setPermission('ATContentTypes: Add Document',
                           0,
                           ['Manager', 'Conteudista'])

    stateDef.setPermission('ATContentTypes: Add Event',
                           0,
                           ['Manager', 'Conteudista'])

    stateDef.setPermission('ATContentTypes: Add Favorite',
                           0,
                           ['Manager', 'Conteudista'])

    stateDef.setPermission('ATContentTypes: Add File',
                           0,
                           ['Manager', 'Conteudista'])

    stateDef.setPermission('ATContentTypes: Add Folder',
                           0,
                           ['Manager', 'Conteudista'])

    stateDef.setPermission('ATContentTypes: Add Image',
                           0,
                           ['Manager', 'Conteudista'])

    stateDef.setPermission('ATContentTypes: Add Large Plone Folder',
                           0,
                           ['Manager', 'Conteudista'])

    stateDef.setPermission('ATContentTypes: Add Link',
                           0,
                           ['Manager', 'Conteudista'])

    stateDef.setPermission('ATContentTypes: Add News Item',
                           0,
                           ['Manager', 'Conteudista'])


    stateDef = workflow.states['publicado_restrito']
    stateDef.setProperties(title="""Publicado Restrito""",
                           transitions=['retirar', 'publicar'])

    stateDef.setPermission('View management screens',
                           0,
                           ['Manager', 'Reviewer', 'Owner'])

    stateDef.setPermission('Review portal content',
                           0,
                           ['Manager', 'Reviewer'])

    stateDef.setPermission('Manage properties',
                           0,
                           ['Manager'])

    stateDef.setPermission('Copy or Move',
                           0,
                           ['Manager', 'Conteudista'])
				
    stateDef.setPermission('Manage users',
                           0,
                           ['Manager','Administrador_Usuario'])
    
    stateDef.setPermission('Add portal content',
                           0,
                           ['Manager', 'Conteudista'])

    stateDef.setPermission('Access contents information',
                           0,
                           ['Manager', 'Reviewer','Visitante_Restrito', 'Conteudista'])

    stateDef.setPermission('Add portal topics',
                           0,
                           ['Manager'])

    stateDef.setPermission('Change portal events',
                           0,
                           ['Manager'])

    stateDef.setPermission('Delete objects',
                           0,
                           ['Manager'])

    stateDef.setPermission('List folder contents',
                           0,
                           ['Manager', 'Reviewer','Visitante_Restrito', 'Conteudista'])

    stateDef.setPermission('Manage portal',
                           0,
                           ['Reviewer', 'Manager','Administrador_Usuario'])

    stateDef.setPermission('Modify portal content',
                           0,
                           ['Manager'])

    stateDef.setPermission('Modify constrain types',
                           0,
                           ['Manager'])

    stateDef.setPermission('Modify view template',
                           0,
                           ['Manager', 'Reviewer'])

    stateDef.setPermission('View',
                           0,
                           ['Manager', 'Reviewer', 'Visitante_Restrito', 'Conteudista'])


    stateDef.setPermission('ATContentTypes: Add Document',
                           0,
                           ['Manager', 'Conteudista'])

    stateDef.setPermission('ATContentTypes: Add Event',
                           0,
                           ['Manager', 'Conteudista'])

    stateDef.setPermission('ATContentTypes: Add Favorite',
                           0,
                           ['Manager', 'Conteudista'])

    stateDef.setPermission('ATContentTypes: Add File',
                           0,
                           ['Manager', 'Conteudista'])

    stateDef.setPermission('ATContentTypes: Add Folder',
                           0,
                           ['Manager', 'Conteudista'])

    stateDef.setPermission('ATContentTypes: Add Image',
                           0,
                           ['Manager', 'Conteudista'])

    stateDef.setPermission('ATContentTypes: Add Large Plone Folder',
                           0,
                           ['Manager', 'Conteudista'])

    stateDef.setPermission('ATContentTypes: Add Link',
                           0,
                           ['Manager', 'Conteudista'])

    stateDef.setPermission('ATContentTypes: Add News Item',
                           0,
                           ['Manager', 'Conteudista'])


						   
						   ## Transitions initialization

    transitionDef = workflow.transitions['submeter']
    transitionDef.setProperties(title="""Aguardando Revisão""",
                                new_state_id="""aguardando_revisao""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""""",
                                actbox_name="""Aguardando Revisão""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={'guard_roles': 'Manager; Owner; Conteudista'},
                                )

    transitionDef = workflow.transitions['publicar']
    transitionDef.setProperties(title="""Publicado Para Todos""",
                                new_state_id="""publicado_todos""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""""",
                                actbox_name="""Publicado Para Todos""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={'guard_roles': 'Manager; Reviewer'},
                                )

    transitionDef = workflow.transitions['rejeitar']
    transitionDef.setProperties(title="""Rascunho""",
                                new_state_id="""rascunho""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""""",
                                actbox_name="""Rascunho""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={'guard_roles': 'Manager; Reviewer; Conteudista'},
                                )

    transitionDef = workflow.transitions['retirar']
    transitionDef.setProperties(title="""Aguardando Revisão""",
                                new_state_id="""aguardando_revisao""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""""",
                                actbox_name="""Aguardando Revisão""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={'guard_roles': 'Manager; Reviewer'},
                                )

    transitionDef = workflow.transitions['restringir']
    transitionDef.setProperties(title="""Publicado Restrito""",
                                new_state_id="""publicado_restrito""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""""",
                                actbox_name="""Publicado Restrito""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={'guard_roles': 'Manager; Reviewer'},
                                )

    ## State Variable
    workflow.variables.setStateVar('review_state')

    ## Variables initialization
    variableDef = workflow.variables['review_history']
    variableDef.setProperties(description="""Provides access to workflow history""",
                              default_value="""""",
                              default_expr="""state_change/getHistory""",
                              for_catalog=0,
                              for_status=0,
                              update_always=0,
                              props={'guard_permissions': 'Request review; Review portal content'})

    variableDef = workflow.variables['comments']
    variableDef.setProperties(description="""Comments about the last transition""",
                              default_value="""""",
                              default_expr="""python:state_change.kwargs.get('comment', '')""",
                              for_catalog=0,
                              for_status=1,
                              update_always=1,
                              props=None)

    variableDef = workflow.variables['time']
    variableDef.setProperties(description="""Time of the last transition""",
                              default_value="""""",
                              default_expr="""state_change/getDateTime""",
                              for_catalog=0,
                              for_status=1,
                              update_always=1,
                              props=None)

    variableDef = workflow.variables['actor']
    variableDef.setProperties(description="""The ID of the user who performed the last transition""",
                              default_value="""""",
                              default_expr="""user/getId""",
                              for_catalog=0,
                              for_status=1,
                              update_always=1,
                              props=None)

    variableDef = workflow.variables['action']
    variableDef.setProperties(description="""The last transition""",
                              default_value="""""",
                              default_expr="""transition/getId|nothing""",
                              for_catalog=0,
                              for_status=1,
                              update_always=1,
                              props=None)

    ## Worklists Initialization

    worklistDef = workflow.worklists['pendentes']
    worklistStates = ['aguardando_revisao']
    actbox_url = "%(portal_url)s/search?review_state=" + "&review_state=".join(worklistStates)
    worklistDef.setProperties(description="Reviewer tasks",
                              actbox_name="Pending (%(count)d)",
                              actbox_url=actbox_url,
                              actbox_category="global",
                              props={'guard_permissions': 'Review portal content',
                                     'guard_roles': 'Manager; Reviewer',
                                     'var_match_review_state': ';'.join(worklistStates)})

    # WARNING: below protected section is deprecated.
    # Add a tagged value 'worklist' with the worklist name to your state(s) instead.


def createSERPROSCWorkflow(self, id):
    """Create the workflow for SERPROSCWorkflow.
    """

    ob = DCWorkflowDefinition(id)
    setupSERPROSCWorkflow(self, ob)
    return ob

addWorkflowFactory(createSERPROSCWorkflow,
                   id='SERPROSCWorkflow',
                   title='SERPROSCWorkflow')

