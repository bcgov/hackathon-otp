import requests
import json

from config import Config


class EmailService():
    
    @classmethod
    def get_auth_token(self):

        url = Config.AUTH_HOST
        data = {'grant_type': 'client_credentials'}
        auth = (Config.CHES_CLIENT_ID, Config.CHES_CLIENT_SECRET)
        resp = requests.post(url, data, auth=auth)
        try:
            resp_data = resp.json()
        except ValueError:
            resp_data = None

        if resp.status_code != requests.codes.ok:
            message = f'Auth request returned {resp.status_code}.'
            if resp_data:
                message += f'\nError: {resp_data.get("error")}\nDescription: {resp_data.get("error_description")}'
            return

        auth_token = resp_data.get('access_token')
        if not auth_token:
            message = 'Auth request did not return an access token!'
            print(resp_data)
            print(message)
            return

        return auth_token


    # NOTE: See here for details: https://ches.nrs.gov.bc.ca/api/v1/docs#tag/Email
    @classmethod
    def send_email(self,
                   recipient,
                   otp
                   ):
        '''Sends an email.'''

        # get auth token
        auth_token = EmailService.get_auth_token()

        headers = {'Authorization': f'Bearer {auth_token}', 'Content-Type': 'application/json'}

        body = '<h1>Here is your one-time code:</h1><div><h1>' + otp + '</h1></div>'

        data = {
            'subject': 'Verify Your Email',
            'from': Config.SENDER_EMAIL,
            'to': [recipient],
            'body': body,
            'bodyType': 'html',
            'attachments': [],
            'encoding':'utf-8' ,
            'priority': 'normal',
        }

        url = f'{Config.CHES_HOST}/email'
        # call CHES api
        resp = requests.post(url, json.dumps(data), headers=headers)
        try:
            resp_data = resp.json()
        except ValueError:
            resp_data = None

        if resp.status_code != requests.codes.created:
            message = f'Email request returned {resp.status_code}.'
            if resp_data:
                message += f'\nError: {resp_data.get("title")}\nDescription: {resp_data.get("detail")}'
                print(resp_data)
            print(message)
            return

        print(
            f'Email request successful.'
        )
