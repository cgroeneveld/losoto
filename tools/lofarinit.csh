#!/bin/csh
# optimized for cep3
if ! $?PYTHONPATH then
    setenv PYTHONPATH "" 
endif
setenv PYTHONPATH "/home/fdg/scripts/:/home/fdg/opt/lib/python:/home/fdg/opt/lib/python2.6/site-packages:/usr/lib/python2.6/site-packages:/home/fdg/opt/lib/python2.7/site-packages:/usr/lib/python2.7/site-packages:/home/fdg/.local/lib/python2.7/site-packages:/home/fdg/losoto:/home/fdg/scripts/:/home/fdg/opt/lib/python:/home/fdg/opt/lib/python2.6/site-packages:/usr/lib/python2.6/site-packages:/home/fdg/opt/lib/python2.7/site-packages:/usr/lib/python2.7/site-packages:/home/fdg/.local/lib/python2.7/site-packages:/opt/cep/tools/scripts//scripts-master:/opt/cep/LofIm/daily/Thu/lofar_build/install/gnu_opt/lib/python2.7/site-packages:/opt/cep/pyrap/current/lib/python2.7/site-packages:/opt/cep/lofar/external/lib/python/site-packages:/opt/cep/tools/cookbook:/opt/cep/tools/drawMS:/opt/cep/tools/uvplot:/opt/cep/tools/simulation:/opt/cep/tools/lib/python2.7/site-packages:${PYTHONPATH}"
setenv PATH ${PATH}:/home/fdg/losoto/bin
