#!/bin/sh
# Generate ILCertificador code
# Run this script from the same level of directory ./ILCertificador

echo "==>> Generating code..."
./python ArchGenXML/ArchGenXML.py -c SERPROSenha/model/generate.conf SERPROSenha/model/modelo.zargo
./SERPROSenha/model/cleanup.sh

