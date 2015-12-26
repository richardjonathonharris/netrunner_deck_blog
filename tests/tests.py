import unittest
from utilities.netrunnerdb import NetrunnerCardScraper, NetrunnerDeckScraper
from utilities.orm import Cards, Decks, Base, Decklists
from sqlalchemy.orm import sessionmaker, mapper
from sqlalchemy import MetaData, Table, Column, Integer, String, create_engine


class TestBasicCardScraper(unittest.TestCase):
p
    def setUp(self):
        self.test_class = NetrunnerCardScraper()

    def test_basic_parameters_init(self):
        self.assertEqual(self.test_class.base_url,
                         'http://netrunnerdb.com',
                         'Base URL should be netrunnerdb.com')
        self.assertEqual(self.test_class.endpoint,
                         '/api/cards/',
                         'Endpoint should be api/cards')

    def test_class_gets_netrunner_json(self):
        card_info = self.test_class._get_card_info()
        self.assertNotEqual(len(card_info),
                            0,
                            '_get_card_info() should \
                            return some non-zero data')

    def test_class_netrunner_json_is_correct(self):
        card_info = self.test_class._get_card_info()
        self.assertEqual(card_info[0]['type'],
                         'Identity',
                         'first entry of card info should \
                         be an identity card.')

    def test_extract_keys_successfully(self):
        self.maxDiff = None
        card_info = self.test_class._get_card_info()[0]
        parsed_info = self.test_class._parse_card_info(card_info)
        card_text = 'Draft format only.\r\n' + \
            'You can use agendas from all factions in this deck.'
        expected_entry = {
            'type': 'Identity',
            'text': card_text,
            'minimumdecksize': 30,
            'uniqueness': False,
            'subtype_code': 'megacorp',
            'cyclenumber': 0,
            'number': 5,
            'limited': 3,
            'faction_letter': '-',
            'title': 'The Shadow: Pulling the Strings',
            'code': '00005',
            'set_code': 'draft',
            'side': 'Corp',
            'faction': 'Neutral',
            'quantity': 1,
            'cost': None,
            'factioncost': None,
            'memoryunits': None,
            'strength': None
        }
        self.assertDictEqual(parsed_info,
                             expected_entry,
                             'Expected parsed data does not equal generated.')

    def test_database_mapping(self):
        cards = Cards()
        self.assertEqual(cards.__tablename__,
                        'cards',
                        'Table should return expected tablename')

    def test_database_adds_test_info(self):
        Base()
        Cards()
        engine = self.test_class._connect_to_db('sqlite:///:memory:')
        Base.metadata.create_all(engine)
        test_card = Cards(title='Title',
                          text='Text',
                          faction='Faction',
                          card_type='Card')
        self.assertEqual(test_card.id,
                         None)
        Session = sessionmaker(bind=engine)
        session = Session()
        session.add(test_card)
        query = session.query(Cards)
        self.assertEqual(query.filter_by(text='Text').first().text,
                         'Text')
        self.assertEqual(query.filter_by(text='Text').first().id,
                         1)

    def test_scraper_adds_card_info_correctly(self):
        Base()
        Cards()
        engine = self.test_class._connect_to_db('sqlite:///:memory:')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        card_info = self.test_class._get_card_info()[0]
        parsed_info = self.test_class._parse_card_info(card_info)
        self.test_class.add_card_info_to_db(parsed_info, session)
        test_query = session.query(Cards).filter_by(faction='Neutral').first()
        self.assertEqual(test_query.faction,
                         'Neutral')


class TestBasicDecksScraper(unittest.TestCase):

    def setUp(self):
        self.in_memory_db = 'sqlite:///:memory:'
        self.deckscraper = NetrunnerDeckScraper()

    def tearDown(self):
        pass

    def test_basic_deck_scraper_has_main_method(self):
        self.assertEqual(self.deckscraper.main(),
                         'main function',
                         'Main function currently should return said text')

    def test_basic_parameters_init(self):
        self.assertEqual(self.deckscraper.base_url,
                         'http://netrunnerdb.com',
                         'Base URL should be netrunnerdb.com')
        self.assertEqual(self.deckscraper.endpoint,
                         '/api/decklists/by_date/',
                         'Endpoint should be api/decklists/by_date')

    def test_class_gets_netrunner_json(self):
        decks = self.deckscraper._get_one_days_decks('2013-12-31')
        self.assertNotEqual(len(decks),
                            0,
                            'Should receive many decks for api call')

    def test_class_returns_parsed_dictionary(self):
        decks = self.deckscraper._get_one_days_decks('2013-12-31')
        parsed_deck = self.deckscraper._parse_deck_info(decks[0])
        [self.assertIn(column,
                       list(parsed_deck.keys()),
                       '%s should be in parsed deck dict' % column)
         for column in ['name', 'username', 'id',
                        'description', 'created_at']]

    def test_class_returns_parsed_decklist_dictionary(self):
        decks = self.deckscraper._get_one_days_decks('2013-12-31')
        parsed_decklist = self.deckscraper._parse_decklist_info(decks[0])
        self.assertIsInstance(parsed_decklist,
                              list,
                              'Should return dictionary')

    def test_database_mapping_decks_db(self):
        decks = Decks()
        self.assertEqual(decks.__tablename__,
                         'decks',
                         'Table should return expected tablename')

    def test_database_adds_test_info(self):
        Base()
        Cards()
        Decks()
        Decklists()
        engine = self.deckscraper._connect_to_db(self.in_memory_db)
        Base.metadata.create_all(engine)
        test_deck = Decks(
            deck_id = '88867',
            name = 'test deck',
            username = 'test user',
            description = 'test description',
            created_at = 'test created_at'
        )
        test_decklist = Decklists(
            deck_id = '1117',
            card_id = '00045',
            quantity = 0
        )
        self.assertEqual(test_deck.id,
                         None)
        self.assertEqual(test_decklist.id,
                         None)
        Session = sessionmaker(bind=engine)
        session = Session()
        session.add(test_deck)
        session.add(test_decklist)
        query = session.query(Decks)
        self.assertEqual(query.filter_by(name='test deck').first().name,
                         'test deck',
                         'Query to newly added data should be test deck')
        query = session.query(Decklists)
        self.assertEqual(query.filter_by(deck_id='1117').first().quantity,
                         0,
                         'Quantity for newly added data should be 0')

    def test_scraper_adds_deck_info_correctly(self):
        Base()
        Decks()
        engine = self.deckscraper._connect_to_db(self.in_memory_db)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        decks = self.deckscraper._get_one_days_decks('2013-12-31')
        parsed_deck = self.deckscraper._parse_deck_info(decks[0])
        self.deckscraper.add_deck_info_to_db(parsed_deck, session)
        test_query = session.query(Decks).first()
        self.assertEqual(test_query.deck_id,
                         '1171')

    def test_scraper_adds_decklist_info_correctly(self):
        Base()
        Decklists()
        engine = self.deckscraper._connect_to_db(self.in_memory_db)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        decks = self.deckscraper._get_one_days_decks('2013-12-31')
        parsed_decklist = self.deckscraper._parse_decklist_info(decks[0])
        self.deckscraper.add_decklist_info_to_db(parsed_decklist, session)
        test_query = session.query(Decklists).first()
        self.assertEqual(test_query.deck_id,
                          '1171',
                         test_query)


if __name__ == '__main__':
    print('Use nosetest you silly boy')
