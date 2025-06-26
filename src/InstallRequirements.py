from src.main import g_Logger
from sys import executable;
from subprocess import check_call;

def InstallRequirements( requirements: str ) -> None:

    g_Logger.info( "Installing requirements <g>{}<>", requirements );

    check_call( [ executable, "-m", "pip", "install", "-r", requirements ] );
