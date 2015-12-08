import requests


class NetrunnerCardScraper:
    def __init__(self):
        self.base_url = 'http://netrunnerdb.com'
        self.endpoint = '/api/cards/'

    def _get_card_info(self):
        card_info = requests.get(self.base_url+self.endpoint)
        return card_info.json()

    def _print_card_info(self):
        card_info = requests.get(self.base_url+self.endpoint)
        for entry in card_info.json()[16:25]:
            print('\n', entry, '\n')

    def _parse_card_info(self, card_info):
        return_dict = {
            'type': card_info.get('type', None),
            'uniqueness': card_info.get('uniqueness', None),
            'subtype_code': card_info.get('subtype_code', None),
            'code': str(card_info.get('code', None)),
            'cyclenumber': card_info.get('cyclenumber', None),
            'faction': card_info.get('faction', None),
            'faction_letter': card_info.get('faction_letter', None),
            'text': card_info.get('text', None),
            'title': card_info.get('title', None),
            'limited': card_info.get('limited', None),
            'minimumdecksize': card_info.get('minimumdecksize', None),
            'number': card_info.get('number', None),
            'set_code': card_info.get('set_code', None),
            'side': card_info.get('side', None),
            'quantity': card_info.get('quantity', None),
            'cost': card_info.get('cost', None),
            'factioncost': card_info.get('factioncost', None),
            'strength': card_info.get('strength', None),
            'memoryunits': card_info.get('memoryunits', None)
        }
        return return_dict

if __name__ == '__main__':
    get_cards = NetrunnerCardScraper()
    get_cards._print_card_info()
