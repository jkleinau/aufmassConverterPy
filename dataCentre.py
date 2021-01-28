import pandas as pd

from magicPlanAPI import MagicPlanAPI


class DataCentre:
    def __init__(self):
        """
        Instance to simulate a Cache by storing values in files and reading at the start of the program into variables
        """
        self.paths = {
            'plans': 'resources/data/plans.json',
            'credentials': 'resources/data/credentials.json',
            'users': 'resources/data/users.json'
        }
        self.data = dict()
        self.load_data()
        self.magic_api = self.connect_to_api()

    def get_search_plans(self, search: str = None) -> dict[str, str]:
        """
        Returns all plans which match the search term
        If no search term is provided all the plans get returned
        :param search: search term
        :return: Dict of plans with dict['ID','name']
        """
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
        """
        Loads all the files into class variables
        """
        for datasource in self.paths:
            try:
                self.data[datasource] = pd.read_json(self.paths[datasource])
            except FileNotFoundError:
                print("Die Datei konnte nicht geöffnet werden.")

    def get_plans(self):
        """
        Returns all plans
        :return: Dict of plans with dict['ID','name']
        """
        plans = dict()
        for index, plan in self.data['plans'].iterrows():
            plans[plan['id']] = plan['name']
        return plans

    def reload_plans(self):
        """
        Reloads plans by pulling them from the magicplan API
        :return: Dict of plans with dict['ID','name']
        """
        self.data['plans'] = pd.DataFrame(self.magic_api.get_projects(as_json=True))
        return self.get_plans()

    def save_data(self):
        """
        Stores the data in class variables into files to save them
        """
        for datasource in self.paths:
            with open(self.paths[datasource], 'w') as f:
                f.write(self.data[datasource].to_json(indent=2))
                print("{}\t -> \t{}".format(datasource, self.paths[datasource]))

    def connect_to_api(self):
        """
        Initiates magicplanAPI instance with credentials if defined
        :return: MagicPlanAPI instance
        """
        try:
            customer_id = self.data['credenitals']['customerID'][0]
            private_key = self.data['credenitals']['private_key'][0]
            user_email = self.data['credenitals']['user_email'][0]
            return MagicPlanAPI(customerID=customer_id, private_key=private_key, user_email=user_email)
        except:
            return MagicPlanAPI()
