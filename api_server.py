from flask_app import app
import os 
from OpenSSL import SSL
import ssl

def runserver():
    context = SSL.Context(SSL.SSLv23_METHOD)
    context.use_privatekey_file('karma_farm.key')
    context.use_certificate_file('karma_farm.crt')
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, ssl_context=('server.crt', 'server.key'))

if __name__ == '__main__':
    runserver()
