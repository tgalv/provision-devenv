import os
import sys
from time import sleep


from fabric.api import env, local, run, sudo, put, local, cd, lcd, task, execute, shell_env, settings
from fabric.contrib.files import exists

import templates

REPO_ROOT = os.getenv("REPO_ROOT")

if not REPO_ROOT:
    sys.exit("Please set the REPO_ROOT environment variable. e.g. `export REPO_ROOT=git@github.com:pythonista`")
    

PYTHON3 = os.getenv("PYTHON3")

if not PYTHON3:
    PYTHON3 = "python3"

VAGRANT_KEY = os.getenv("VAGRANT_KEY")

if not VAGRANT_KEY:
    VAGRANT_KEY = ".vagrant/machines/default/virtualbox/private_key"

print("Vagrant key: {0}".format(VAGRANT_KEY,))

@task
def vagrant():
    # change from the default user to 'vagrant'
    env.user = 'vagrant'
    # connect to the port-forwarded ssh
    env.hosts = ['127.0.0.1:2222']
    # use vagrant ssh key
    result = local('vagrant ssh-config | grep IdentityFile', capture=True)
    #env.key_filename = result.split()[1]
    env.key_filename = VAGRANT_KEY

@task
def uname():
    run('uname -a')


#################
# PREREQS
#################


@task
def install_sftp():
    sudo("yum install -y vsftpd")
    sudo("yum install -y openssh-clients")
    sudo("sudo sed -i 's|/usr/lib/openssh/sftp-server|internal-sftp|' /etc/ssh/sshd_config")
    sudo("service sshd restart")
    sleep(5)


@task
def install_supervisor():
    sudo("pip install supervisor")


#################
# PROVISION
#################


@task
def clone_repo(project):
    if not os.path.exists(project):
        local('git clone {0}/{1}.git'.format(REPO_ROOT, project))


@task
def build(project, branch = None):
    with lcd(project):
    	if branch is not None:
    	    local("git fetch")
            local("git checkout {0}".format(branch,))
	    local("git pull")
        local('{0} setup.py sdist'.format(PYTHON3,))


@task
def deploy(project):
    dirname = "./{0}/dist".format(project,)
    fname = sorted(os.listdir(dirname))[-1]

    put(os.path.join(dirname, fname),
      	"/home/vagrant")
    sudo("pip3 install {0}".format(fname,))


@task
def init_supervisord_config():
    sudo("echo_supervisord_conf > /etc/supervisord.conf")
    sudo("sed -i 's/;\[include\]/\[include\]/' /etc/supervisord.conf")
    sudo("echo 'files = /etc/supervisord.d/*.ini' >> /etc/supervisord.conf")
    

@task
def put_supervisor_ini(fname):
    if not exists('/etc/supervisord.d', use_sudo=True):
        sudo('mkdir /etc/supervisord.d')
    put(fname, "/etc/supervisord.d/", use_sudo=True)


@task
def supervisord_config(program, command, environment):
    fname = "{0}.ini".format(program,)
    ini_file = templates.render_supervisor(fname, program, command, environment)
    execute(put_supervisor_ini, ini_file)


@task
def supervisorctl_reload():
    sleep(10)
    with settings(warn_only=True):
        sudo("supervisord")
    sudo("supervisorctl reload")
    sudo("supervisorctl status")


@task
def flask_config(project, port, config, service_name = None):
    py_name = "{0}".format(project.replace("-", "_"),)
    cmd = "/usr/local/bin/{0} -p {1}".format(py_name, port)
    conf = '{0}.config.{1}'.format(py_name, config)
    execute(init_supervisord_config)
    if service_name is None:
        service_name=py_name
    execute(supervisord_config, service_name, cmd, conf)
    execute(supervisorctl_reload)


@task
def provision(project, branch, port, config, service_name=None):
    execute(vagrant)
    execute(clone_repo, project)
    execute(build, project, branch)
    execute(deploy, project)
    execute(flask_config, project, port, config, service_name)


@task
def curl(header, url):
    run("curl -H {0} {1}".format(header, url))
