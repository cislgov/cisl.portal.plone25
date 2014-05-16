
------------------------------------------------------------------------------------
SERPROSCCaptchaField - Zope product 
------------------------------------------------------------------------------------ 
 
 Authors:
    Wesley Barroso Lopes <wesleybl@gmail.com>
    Rafael Ferreira Silva <rafael@rafaelsilva.net>


O Produto se destina ao uso de CAPTCHA em formulários para o Plone. 
Atualmente ele conta com um widget e um validator que pode ser usado com Archetypes, 
além de possuir uma ferramenta(tool) que gera captcha(tanto sonoro quanto visual) 
pra ser usado em qualquer formulário(através de uma macro em template).

Instalação:

Para instalar o produto coloque-o na pasta Products da instância do Zope e 
instale o CaptchaFild no PloneSite em que irá ser usado.

Requerido:

   PIL >= 1.1.4

Utilização em formulário:

- No código do login_form customizado, acrescentar a linha abaixo:

<div metal:use-macro="here/campo_captcha_sonoro/macros/captcha_sonoro"/>

- No Validation do login_form acrescentar o validador valida_captcha

- Este produto utiliza fontes dinâmicas. Você deve adicionar as fontes na pasta
fonts do produto. Elas devem ter o formato TrueType.
 
Utilização em Archetypes(gerando com ArchGenXML):

- Crie um campo, dando um nome como captcha do tipo Captcha
- Como TaggedValues utilize:
  widget: CaptchaWidget
  validators: validaCaptcha
  widget:label e widget:description com o texto desejado
  required: 1

