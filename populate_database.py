from utilities.netrunnerdb import NetrunnerCardScraper, NetrunnerDeckScraper

if __name__ == '__main__':
    netrunner_cards = NetrunnerCardScraper()
    netrunner_decklists = NetrunnerDeckScraper()
    netrunner_cards.main()
    netrunner_decklists.main()
