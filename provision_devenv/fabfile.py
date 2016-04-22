import os
import sys
from time import sleep


from fabric.api import env, local, run, sudo, put, local, cd, lcd, task, execute, shell_env
from fabric.contrib.files import exists

import templates

REPO_ROOT = os.getenv("REPO_ROOT")

if not REPO_ROOT:
    sys.exit("Please set the REPO_ROOT environment variable. e.g. `export REPO_ROOT=git@github.com:pythonista`")
    

PYTHON3 = "python3"


@task
def vagrant():
    # change from the default user to 'vagrant'
    env.user = 'vagrant'
    # connect to the port-forwarded ssh
    env.hosts = ['127.0.0.1:2222']
    # use vagrant ssh key
    result = local('vagrant ssh-config | grep IdentityFile', capture=True)
    #env.key_filename = result.split()[1]
    env.key_filename = ".vagrant//machines//dev//virtualbox//private_key"


@task
def install_sftp():
    sudo("yum install -y vsftpd")
    sudo("yum install -y openssh-clients")
    sudo("sudo sed -i 's|/usr/lib/openssh/sftp-server|internal-sftp|' /etc/ssh/sshd_config")
    sudo("service sshd restart")
    sleep(5)


@task
def uname():
    run('uname -a')


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
    sudo("pip install {0}".format(fname,))


@task
def install_supervisor():
    sudo("pip install supervisor")


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
def supervisord_config(project, program, command, environment):
    fname = "{0}.ini".format(project,)
    ini_file = templates.render_supervisor(fname, program, command, environment)
    execute(put_supervisor_ini, ini_file)


@task
def supervisorctl_reload():
    #sudo("supervisord")
    sudo("supervisorctl reload")
    sudo("supervisorctl status")


@task
def provision(project, branch, port, config):
    execute(vagrant)
    execute(install_sftp)
    execute(clone_repo, project)
    execute(build, project, branch)
    execute(deploy, project)
    execute(install_supervisor)
    py_name = "{0}".format(project.replace("-", "_"),)
    cmd = "{0} -p {1}".format(py_name, port)
    conf = '{0}.config.{1}'.format(py_name, config)
    execute(init_supervisord_config)
    execute(supervisord_config, project, py_name, cmd, conf)
    execute(supervisorctl_reload)


