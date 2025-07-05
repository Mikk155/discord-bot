def InstallRequirements( requirements: str ) -> None:

    from sys import executable;
    from subprocess import check_call;

    if isinstance( requirements, str ):

        check_call( [ executable, "-m", "pip", "install", "-r", requirements ] );

    else:

        for requirement in requirements:

            check_call( [ executable, "pip", "install", requirement ] );
