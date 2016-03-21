from optparse import OptionParser

from fabric.api import run
from fabric.tasks import execute

from provision_devenv.fabfile import provision

def main():
    parser = OptionParser(usage="Usage: $path/to/devenv-root ./provision_devenv.exe name-of-project [options]")
    parser.add_option("-b", "--branch", dest="branch", default="develop", help="Git Branch")
    parser.add_option("-p", "--port", dest="port", default="5000", help="Port")
    parser.add_option("-c", "--config", dest="config", default="Config", help="Flask Config")
    options, args = parser.parse_args()
    project = args[0]
    print "Provisioning '{0}' ('{1}') on Port '{2}' with Config '{3}'".format(project,
                                                                             options.branch, 
                                                                             options.port,
									     options.config)
    execute(provision, project, options.branch, options.port, options.config, hosts='vagrant' )


if __name__ == "__main__":
    main()
