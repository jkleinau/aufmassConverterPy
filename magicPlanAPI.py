import requests
from magicXMLImport import get_file_urls


def write_file_from_url(url: str, path: str) -> None:
    """
    Writes the whole content of a get request into a specified file
    :param url: URL for get request
    :param path: Path file location
    """
    r = requests.get(url)
    with open(f'{path}', 'wb')as f:
        f.write(r.content)


class MagicPlanAPI:

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

    def get_files_by_plan(self, plan_id, filetype=None, since=None):
        """
        Get the corresponding files for a plan by id and filter with filetype and since
        :param plan_id: Plan ID
        :param filetype: type as 'pdf'
        :param since: timestamp
        :return: dict ['name':'url']
        """
        payload = dict()
        payload['content-type'] = 'application/x-www-form-urlencoded'
        payload['planid'] = plan_id
        payload['customer'] = self.headers['customer']
        payload['key'] = self.headers['key']

        if filetype:
            payload['filetype'] = filetype
        if since:
            payload['since'] = since

        r = requests.post('https://cloud.sensopia.com/listfiles.php', payload)
        return get_file_urls(r.text, filetype=filetype)

    def get_project_plan(self, plan_id: str) -> str:
        """
        performs get requests and returns response as dict
        :param plan_id: Plan Id
        :return: xml as string
        """
        r = requests.get("https://cloud.magic-plan.com/api/v2/plans/get/" + plan_id, headers=self.headers)
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
