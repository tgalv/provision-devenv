import os
import sys
from tempfile import NamedTemporaryFile
 

from jinja2 import Template 
  
   
SUPERVISOR_TEMPLATE = "supervisor.ini.j2"
    

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def render_supervisor(fname, program, command, settings):
    fqname = resource_path(SUPERVISOR_TEMPLATE)
    template = open(fqname).read()
    t = Template(template)
    ini_file = resource_path(fname)
    f = open(ini_file, 'w')
    text = t.render(PROGRAM=program, COMMAND=command, ENVIRONMENT=settings) 
    f.write(text) 
    return ini_file
