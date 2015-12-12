import unittest
from utilities.netrunnerdb import NetrunnerCardScraper, Cards, Base
from sqlalchemy.orm import sessionmaker

class TestBasicCardScraper(unittest.TestCase):

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
                            '_get_card_info() should return some non-zero data')

    def test_class_netrunner_json_is_correct(self):
        card_info = self.test_class._get_card_info()
        self.assertEqual(card_info[0]['type'],
                         'Identity',
                         'first entry of card info should be an identity card.')

    def test_extract_keys_successfully(self):
        card_info = self.test_class._get_card_info()[0]
        parsed_info = self.test_class._parse_card_info(card_info)
        expected_entry = {
            'type': 'Identity',
            'text': 'Draft format only.\r\nYou can use agendas from all factions in this deck.',
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

    def test_connect_to_in_memory_db(self):
        self.test_class._connect_to_db('sqlite:///:memory:')
        # We need to figure out what to actually *test* here

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
        self.assertEqual(session.query(Cards).filter_by(text='Text').first().text,
                         'Text')
        self.assertEqual(session.query(Cards).filter_by(text='Text').first().id,
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



if __name__ == '__main__':
    print('Use nosetest you silly boy')
