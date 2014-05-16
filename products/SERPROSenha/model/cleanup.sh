# General cleanup of product SERPROSenha

echo "==>> Cleaning product..."
find ./SERPROSenha/ -name "*.pyc" -exec rm {} \;
find ./SERPROSenha/ -name "*.pyo" -exec rm {} \;
find ./SERPROSenha/ -name "*~" -exec rm {} \;
find ./SERPROSenha/ -name "*.zuml.bak.*" -exec rm {} \;
rm -rf ./SERPROSenha/skins/SERPROSenha/readme.txt

