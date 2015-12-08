import unittest
from utilities.netrunnerdb import NetrunnerCardScraper


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

if __name__ == '__main__':
    print('Use nosetest you silly boy')
