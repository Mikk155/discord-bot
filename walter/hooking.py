import importlib.util

from __main__ import modulos, abs, os

def init():

    modulos_path = os.path.join( abs, "modulos" );

    for file in os.listdir( modulos_path ):

        if file.endswith( ".py" ):

            try:

                modulo:str = file[ : len(file) - 3 ];

                spec = importlib.util.spec_from_file_location( modulo, os.path.join( modulos_path, file ) );

                obj = importlib.util.module_from_spec( spec );

                spec.loader.exec_module( obj );

                if obj is not None:

                    print( f"Imported module {file}" );

                    modulos[ modulo ] =  obj;

                else:

                    raise Exception( 'Invalid object' );

            except Exception as e:

                print( f"Error importing module {file}: {e}" );
