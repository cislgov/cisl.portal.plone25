Versão original do CMFPublicator: 1.2.2

Alterações realizadas na versão 1.2.2.serpro:

- Incluída condição para que os objetos criados na instalação (tool portal_publicator) 
  não fossem excluídos na reinstalação ou desistalação do produto.
  Todas as configurações e registro de itens selecionados nas boxes encontra-se na tool.
  A reinstalação/desistalação excluía a tool e a criava novamente.Tal comportamento fazia
  com que novas boxes e itens selecionados fossem perdidos.

- Alterada macro edit-box para que o item atualmente selecionado não desapareça da
  lista de opções caso este item não esteja mais entre os N objetos mais novos.
  Antes da alteração, não era possível manter a seleção de um item e alterar os demais,
  caso este item não estivesse mais entre os N mais novos listados nas opções da lista
  de seleção.
 
 - Alterada macro edit-box para que inclua na lista de seleção de imagens, objetos dos tipos
   Imagem e Arquivo, além dos tipos padrão Image e File.