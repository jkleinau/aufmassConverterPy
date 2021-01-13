import pandas as pd

from magicPlanAPI import MagicPlanAPI


class DataCentre:
    def __init__(self):
        self.paths = {
            'plans': 'resources/data/plans.json',
            'credentials': 'resources/data/credentials.json',
            'users': 'resources/data/users.json'
        }
        self.data = dict()
        self.load_data()
        self.magic_api = self.connect_to_api()

    def get_search_plans(self, search=None):
        if search is not None:
            # searching plans for search term with case sensitivity
            mask = self.data['plans']['name'].str.contains(search)
            filtered_plans = self.data['plans'][self.data['plans']['name'].str.contains(search)]
            plans = dict()
            if len(filtered_plans) == 0:
                return dict()
            for index, plan in filtered_plans.iterrows():
                plans[plan['id']] = plan['name']
            return plans
        else:
            return self.get_plans()

    def load_data(self):
        for datasource in self.paths:
            try:
                self.data[datasource] = pd.read_json(self.paths[datasource])
            except FileNotFoundError:
                print("Die Datei konnte nicht geöffnet werden.")

    def get_plans(self):
        plans = dict()
        for index, plan in self.data['plans'].iterrows():
            plans[plan['id']] = plan['name']
        return plans

    def reload_plans(self):
        self.data['plans'] = pd.DataFrame(self.magic_api.get_projects(as_json=True))
        return self.get_plans()

    def save_data(self):
        for datasource in self.paths:
            with open(self.paths[datasource], 'w') as f:
                f.write(self.data[datasource].to_json(indent=2))
                print("{}\t -> \t{}".format(datasource, self.paths[datasource]))

    def connect_to_api(self):
        try:
            customer_id = self.data['credenitals']['customerID'][0]
            private_key = self.data['credenitals']['private_key'][0]
            user_email = self.data['credenitals']['user_email'][0]
            return MagicPlanAPI(customerID=customer_id, private_key=private_key, user_email=user_email)
        except:
            return MagicPlanAPI()
