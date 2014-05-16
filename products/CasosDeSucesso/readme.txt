Por padrão, os editores de texto (Kupu e FCKEditor) não permitem 
que usuários anônimos utilizem o editor. Para "forçar" a utilização
de um editor, acrescente as linhas abaixo no arquivo __init__.py
do produto principal de seu projeto.

#####

def getProperty(self, name, default=''): 
	""" método para forçar o uso do editor de texto
	""" 
    if name == 'wysiwyg_editor': 
        return 'kupu' 
    return False 

(nobody.__class__).getProperty = getProperty 

nobody.wysiwyg_editor = 'kupu'      

#####

No exemplo acima, está configurado para o Kupu, caso o editor 
seja o FCKEditor, basta substituir a palavra 'kupu' por 'fckeditor'. 