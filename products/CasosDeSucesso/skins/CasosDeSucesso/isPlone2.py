from Products.CMFCore.utils import getToolByName
migrationTool = getToolByName(context, 'portal_migration')
return migrationTool.getInstanceVersionTuple()[0] == 2
