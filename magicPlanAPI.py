import requests
import pandas as pd


class MagicPlanAPI:
    def login(self):
        pass

    def __init__(self, private_key='dd0c7925689fbf4f2083412497c30f9d2445', customerID='5c7ef0e0b4132',
                 user_email='matthias.herzog@bsu-projekt-service.de', user_pw='H21ySBip', ref='123456'):
        self.customerID = customerID
        self.private_key = private_key
        self.user_email = user_email
        self.user_pw = user_pw
        self.ref = ref
        self.headers = {
            'accept': 'application/json',
            'customer': customerID,
            'key': private_key
        }

    def link_account(self):
        payload = {
            'customer': self.customerID,
            'key': self.private_key,
            'email': self.user_email,
            'password': self.user_pw,
            'ref': self.ref
        }
        r = requests.post('https://cloud.sensopia.com/newuser.php', params=payload)

    def get_project_plan(self, id):
        r = requests.get("https://cloud.magic-plan.com/api/v2/plans/get/" + id, headers=self.headers)
        return r.json()['data']['plan_detail']['magicplan_format_xml']

    def get_users(self):
        return requests.get('https://cloud.magic-plan.com/api/v2/workgroups/users', headers=self.headers).json()

    def get_projects(self, as_json=False):
        payload = {
            'page': '1',
            'sort': 'Plans.name',
            'direction': 'desc'
        }
        r = requests.get('https://cloud.magic-plan.com/api/v2/workgroups/plans', params=payload,
                         headers=self.headers)
        data = r.json()
        # return data as json for later use
        if as_json:
            return data['data']['plans']

        # convert data to dict
        plans = list()
        for plan in data['data']['plans']:
            plans.append({
                'id': plan['id'],
                'name': plan['name']
            })
        return plans
