Cygwin='CYGWIN';

uname=`uname`

if [[ $uname == $Cygwin* ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi
