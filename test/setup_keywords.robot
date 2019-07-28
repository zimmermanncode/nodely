*** Settings ***

Library   OperatingSystem
Library   Process

Variables   ./variables.py


*** Test Cases ***

Require Node Modules
   ${python} =   Evaluate   sys.executable   modules=sys
   ${node package dir} =   Evaluate
   ...   nodely.NODE_MODULES_DIR / '${NODE_PACKAGE}'
   ...   modules=nodely

   Evaluate
   ...   nodely.uninstall('${NODE_PACKAGE}')
   ...   modules=nodely
   Directory Should Not Exist   ${node package dir}

   Run Process
   ...   ${python}   setup.py   develop
   ...   cwd=${CURDIR}
   Directory Should Exist   ${node package dir}
