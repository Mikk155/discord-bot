from __main__ import abs
from hlunity import jsonc

config = jsonc( '{}\\config.json'.format( abs ) );

if not config:
    raise Exception( 'Can not open config.json!' )
