from utilities.netrunnerdb import NetrunnerCardScraper, NetrunnerDeckScraper

if __name__ == '__main__':
    netrunner_cards = NetrunnerCardScraper()
    netrunner_decklists = NetrunnerDeckScraper(update=True)
    netrunner_cards.main()
    netrunner_decklists.main()
