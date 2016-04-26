===============
DEMO 2016-04-26
===============

Demonstration of hot swapping of collaborating microservices.

1. Provision
------------

deploy boiler_plate to the dev-env as three services: boiler_plate, bp_server_5001, bp_server_5002

::

    fab -f /path/to/provision-devenv/provision_devenv/fabfile.py vagrant provision:boiler_plate,endpoint-demo,5000,DevelopmentConfig
    fab -f /path/to/projects/provision-devenv/provision_devenv/fabfile.py vagrant provision:boiler_plate,endpoint-demo,5001,DevelopmentConfig,service_name=bp_server_5001
    fab -f /path/to/tomgalvin/projects/provision-devenv/provision_devenv/fabfile.py vagrant provision:boiler_plate,endpoint-demo,5002,DevelopmentConfig,service_name=bp_server_5002

2. Curl
-------

boiler_plate is running on Port 5000 in server mode. Run a health check::

    fab -f /Users/tomgalvin/projects/provision-devenv/provision_devenv/fabfile.py vagrant curl:accept:application/json,http://127.0.0.1:5000/helloworld/
    [localhost] local: vagrant ssh-config | grep IdentityFile
    [127.0.0.1:2222] Executing task 'curl'
    [127.0.0.1:2222] run: curl -H accept:application/json http://127.0.0.1:5000/helloworld/
    [127.0.0.1:2222] out: {
    [127.0.0.1:2222] out:   "from": "127.0.0.1:5000",
    [127.0.0.1:2222] out:   "message": "Hello World!"
    [127.0.0.1:2222] out: }

3. Client Mode
--------------

Put boiler_plate in "Client Mode"::

    fab -f /Users/tomgalvin/projects/provision-devenv/provision_devenv/fabfile.py vagrant flask_config:boiler_plate,5000,DemoClientEndpoint5001

Curl again, we can see that boiler_plate is now hitting bp_server_5001::

    $ fab -f /Users/tomgalvin/projects/provision-devenv/provision_devenv/fabfile.py vagrant curl:accept:application/json,http://127.0.0.1:5000/helloworld/
    [localhost] local: vagrant ssh-config | grep IdentityFile
    [127.0.0.1:2222] Executing task 'curl'
    [127.0.0.1:2222] run: curl -H accept:application/json http://127.0.0.1:5000/helloworld/
    [127.0.0.1:2222] out: {"from": "0.0.0.0:5001", "message": "Hello World!"}

4. Change the endpoint
----------------------

This models how a service maybe swapped out for a stub::

    fab -f /Users/tomgalvin/projects/provision-devenv/provision_devenv/fabfile.py vagrant flask_config:boiler_plate,5000,DemoClientEndpoint5002

We can see that boiler_plate is now hitting bp_server_5002::

    fab -f /Users/tomgalvin/projects/provision-devenv/provision_devenv/fabfile.py vagrant curl:accept:application/json,http://127.0.0.1:5000/helloworld/
    [localhost] local: vagrant ssh-config | grep IdentityFile
    [127.0.0.1:2222] Executing task 'curl'
    [127.0.0.1:2222] run: curl -H accept:application/json http://127.0.0.1:5000/helloworld/
    [127.0.0.1:2222] out: {"from": "0.0.0.0:5002", "message": "Hello World!"}