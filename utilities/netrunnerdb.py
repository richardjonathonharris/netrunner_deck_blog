import requests
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


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

    def _connect_to_db(self, database):
        return create_engine(database, echo=True)

    def identify_table(self, table):
        self.table = table

    def add_card_info_to_db(self, card_dict, engine):
        card = Cards(title=card_dict['title'],
                     card_type=card_dict['type'],
                     faction=card_dict['faction'],
                     text=card_dict['text'],
                     code=card_dict['code'],
                     uniqueness=card_dict['uniqueness'],
                     cyclenumber=card_dict['cyclenumber'],
                     faction_letter=card_dict['faction_letter'],
                     limited=card_dict['limited'],
                     decksize=card_dict['minimumdecksize'],
                     number=card_dict['number'],
                     set_code=card_dict['set_code'],
                     side=card_dict['side'],
                     quantity=card_dict['quantity'],
                     cost=card_dict['cost'],
                     factioncost=card_dict['factioncost'],
                     strength=card_dict['strength'],
                     memory=card_dict['memoryunits'])
        engine.add(card)

Base = declarative_base()

class Cards(Base):
    __tablename__ = 'cards'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    card_type = Column(String)
    faction = Column(String)
    text = Column(String)
    code = Column(String)
    uniqueness = Column(String)
    cyclenumber = Column(String)
    faction_letter = Column(String)
    limited = Column(String)
    limited = Column(String)
    decksize = Column(String)
    number = Column(String)
    set_code = Column(String)
    side = Column(String)
    quantity = Column(String)
    cost = Column(String)
    factioncost = Column(String)
    strength = Column(String)
    memory = Column(String)


if __name__ == '__main__':
    get_cards = NetrunnerCardScraper()
    get_cards._print_card_info()
