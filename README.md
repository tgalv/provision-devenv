# Provision DevEnv

A tool to install a Flask Application to a Vagrant Environment.

The Flask App will run as a Service under Supervisord.


# Environment

## Windows

The Python Paths will need setting in Windows (under cygwin).

'''
$ export PATH=$PATH:/c/Python27
$ export PATH=$PATH:/c/Python27/Scripts
'''

## Python3

`python3` is assumed. Otherwise set it:

'''
$ export PYTHON3="c:\\\python34\\\python.exe"
'''

## Git 

'''
$ export REPO_ROOT=git@github.com:pythonista
'''

## Vagrant Key

'''
$ export VAGRANT_KEY=./path/to/private/key
'''

# Usage

Two usage modes are suggested:

## 1. fabfile.py

Setup [Fabric] (http://www.fabfile.org/) on your host

For Windows without admin privileges you can used [precompiled binaries] (http://www.voidspace.org.uk/python/modules.shtml#pycrypto)

'''
$ fab -f path/to/fabfile.py vagrant provision:my-flask-project,my_branch,5000
'''

## 2. API

For example with the Windows exe:

'''
$ ./provision_devenv.exe --help


Options:
  -h, --help            show this help message and exit
  -b BRANCH, --branch=BRANCH
                                Git Branch
  -p PORT, --port=PORT  Port
  -c CONFIG, --config=CONFIG
                    Flask Config
'''

'''
$ ./provision_devenv.exe my-flask-project -b master -p 5000 -c Config

$ vagrant ssh

$ sudo supervisorctl status
 deed_api_stub                    RUNNING   pid 17783, uptime 0:20:24
'''

## Building an exe

You will need the prereq as described above and pyinstaller

From the provision_devenv directory run:

$ pyinstaller.exe provision_devenv.spec
