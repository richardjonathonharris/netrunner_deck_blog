import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utilities.orm import Cards, Decks, Decklists, Base
from datetime import datetime, timedelta
import time

class NetrunnerCardScraper:

    def __init__(self):
        self.base_url = 'http://netrunnerdb.com'
        self.endpoint = '/api/cards/'
        self.database = 'sqlite:///netrunnerdb.db'

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

    def main(self):
        engine = self._connect_to_db(self.database)
        Session = sessionmaker(bind=engine)
        session = Session()
        session.execute('DROP TABLE IF EXISTS cards;')
        Base.metadata.create_all(engine)
        card_info = self._get_card_info()
        for card in card_info:
            card_dict = self._parse_card_info(card)
            self.add_card_info_to_db(card_dict, session)
        session.commit()


class NetrunnerDeckScraper:
    def __init__(self, start_date=None, update=False):
        self.base_url = 'http://netrunnerdb.com'
        self.endpoint = '/api/decklists/by_date/'
        self.database = 'sqlite:///netrunnerdb.db'
        self.start_date = start_date
        self.update = update

    def _connect_to_db(self, database):
        return create_engine(database, echo=True)

    def _get_one_days_decks(self, str_date):
        try:
            deck_info = requests.get(self.base_url+self.endpoint+str_date)
            return deck_info.json()
        except:
            return None

    def _parse_deck_info(self, deck_info):
        parsed_dict = {
            'id': deck_info.get('id', None),
            'name': deck_info.get('name', None),
            'username': deck_info.get('username', None),
            'description': deck_info.get('description', None),
            'created_at': deck_info.get('creation', None)
        }
        return parsed_dict

    def _parse_decklist_info(self, deck_info):
        return_list = []
        deck_id = deck_info.get('id', None)
        for card, quantity in deck_info['cards'].items():
            return_list.append({
                'deck_id': deck_id,
                'card_id': card,
                'quantity': quantity
            })
        return return_list

    def add_deck_info_to_db(self, deck_dict, engine):
        deck = Decks(deck_id=deck_dict.get('id', None),
                     name=deck_dict.get('name', None),
                     username=deck_dict.get('username', None),
                     description=deck_dict.get('description', None),
                     created_at=deck_dict.get('created_at', None)
                     )
        engine.add(deck)

    def add_decklist_info_to_db(self, decklist, engine):
        for item in decklist:
            decklist = Decklists(**item)
            engine.add(decklist)

    def _string_to_datetime(self, string):
        return datetime.strptime(string, '%Y-%m-%d')

    def main(self):
        engine = self._connect_to_db(self.database)
        Session = sessionmaker(bind=engine)
        session = Session()
        if not self.update:
            session.execute('DROP TABLE IF EXISTS decks;')
            session.execute('DROP TABLE IF EXISTS decklists;')
        Base.metadata.create_all(engine)
        if not self.start_date:
            if not self.update:
                start_date = '2013-12-01'
            else:
                start_date = session.query(func.max(Dates.created_at)).first()
        else:
            start_date = self.start_date
        datetime_start = self._string_to_datetime(start_date)
        today = datetime.today()
        delta = today - datetime_start
        print('End date is today %s' % today)
        print('Starting at %s' % datetime_start)
        counter = 0
        for i in range(delta.days + 1):
            current_date = datetime_start + timedelta(days=i)
            print('Current date is %s' % current_date)
            deck_info = self._get_one_days_decks(
                current_date.strftime('%Y-%m-%d'))
            print('Received deck information for %s' % current_date)
            if not deck_info:
                print('No decks available for %s' % current_date)
                pass
            for entry in deck_info:
                deck_dictionary = self._parse_deck_info(entry)
                decklist_dictionary = self._parse_decklist_info(entry)
                self.add_deck_info_to_db(deck_dictionary, session)
                self.add_decklist_info_to_db(decklist_dictionary, session)
            print('Sleeping for 2 seconds for API Limiting')
            time.sleep(2)
            counter += 1
            if counter == 10:
                session.commit()
                counter = 0
        session.commit()

if __name__ == '__main__':
    exit()
