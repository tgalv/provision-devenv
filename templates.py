import os
from tempfile import NamedTemporaryFile
 

from jinja2 import Template 
  
   
SUPERVISOR_TEMPLATE = "supervisor.ini.j2"
    

def render_supervisor(fname, program, command, settings):
    dirname = os.path.dirname(os.path.abspath(__file__))
    fqname = os.path.join(dirname, SUPERVISOR_TEMPLATE)
    template = open(fqname).read()
    t = Template(template)
    ini_file = os.path.join(dirname, fname)
    f = open(ini_file, 'w')
    text = t.render(PROGRAM=program, COMMAND=command, ENVIRONMENT=settings) 
    f.write(text) 
    return ini_file
