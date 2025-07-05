# Format all sources

import sys
from os.path import abspath, dirname, exists, join;
MyWorkspace: str = abspath( dirname( dirname( __file__ ) ) );

sys.path.append( MyWorkspace );

from utils.fmt import fmt;
from utils.Path import Path;

# Set licence headers
LICENCE: str = Path.enter( "LICENCE.txt" );

fmt.FormatSourcesWithLicence( LICENCE, sources_folder=Path.enter( "src" ) );
fmt.FormatSourcesWithLicence( LICENCE, sources_folder=Path.enter( "utils" ) );

from os import walk;
from os.path import exists, join;

for root, _, DirectoryFiles in walk( MyWorkspace ):

    ValidFiles: list[str] = [ join( root, file ) for file in DirectoryFiles if file.endswith( ".py" ) ];

    files += ValidFiles;

for file in files:

    if exists( file ):

        fileIO: list[str] = open( file, 'r' ).readlines();

        HasAny = False;

        for i, l in range( fileIO.copy() ):

            l = l.strip( " " );

            if len(l) == 0:
                fileIO[i] = l;
                HasAny = True;

        if HasAny:
            open( file, 'w' ).writelines( fileIO );
            