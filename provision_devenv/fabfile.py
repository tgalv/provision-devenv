import os

from fabric.api import env, local, run, sudo, put, local, cd, lcd, task, execute, shell_env

import templates

REPO_ROOT = "git@github.com:tgalv"
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
    if os.path.exists("/etc/supervisord.d"):
        sudo("mv /etc/supervisord.d /etc/supervisord.d.bak")
    #sudo("mkdir /etc/supervisord.d")


@task
def put_supervisor_ini(fname):
    put(fname, "/etc/supervisord.d/", use_sudo=True)


@task
def supervisord_config(project, program, command, environment):
    fname = "{0}.ini".format(project,)
    ini_file = templates.render_supervisor(fname, program, command, environment)
    execute(put_supervisor_ini, ini_file)


@task
def supervisorctl_reload():
    sudo("supervisorctl reload")
    sudo("supervisorctl status")


@task
def provision(project, branch, port, config):
    execute(vagrant)
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


