from __main__ import abs

TOKEN = open( '{}\\token.txt'.format( abs ), 'r' ).readline();

if not TOKEN:
    raise Exception( 'Can not open token.txt!' )
