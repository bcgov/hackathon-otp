import os
class Config(object):
  
    CHES_CLIENT_ID = os.environ.get('CHES_CLIENT_ID')
    CHES_CLIENT_SECRET = os.environ.get('CHES_CLIENT_SECRET')
    AUTH_HOST = 'https://dev.loginproxy.gov.bc.ca/auth/realms/comsvcauth/protocol/openid-connect/token'
    CHES_HOST = 'https://ches-dev.api.gov.bc.ca/api/v1/'
    SENDER_EMAIL = 'noreply-hackathon@gov.bc.ca'  
