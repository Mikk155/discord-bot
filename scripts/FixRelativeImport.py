def SetWorkspace( File: str ) -> str:
    '''
        Fix relative library importing by appending the directory of *File* in the sys path.
    '''
    from __main__ import __file__ as File;

    from os.path import abspath, dirname, exists, join;
    MyWorkspace: str = abspath( dirname( File ) );

    import sys
    sys.path.append( MyWorkspace );

    return MyWorkspace;
