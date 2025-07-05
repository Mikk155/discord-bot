def UpdateRepoSubmodules( MyWorkspace: str ) -> None:

    from git import Repo;

    Repository = Repo( MyWorkspace );

    Repository.git.submodule( "init" );
    Repository.git.submodule( "sync" );

    for submodule in Repository.submodules:

        SubPath = submodule.abspath;
        SubRepository = Repo( SubPath );

        SubRepository.git.reset( '--hard' );
        SubRepository.git.clean( '-fdx' );

        SubRepository.remote().fetch();

        SubRepository.git.checkout( 'main' ); # Maybe "auto" and force a branch by an argument?
        SubRepository.git.reset( '--hard', 'origin/main' );
