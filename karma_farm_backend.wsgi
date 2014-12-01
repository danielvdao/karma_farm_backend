activate_this = '/root/karma_farm_backend/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys 
sys.path.insert(0,'/root/karma_farm_backend'

from flask_app import app as application



