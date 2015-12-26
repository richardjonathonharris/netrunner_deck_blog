from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

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


class Decks(Base):
    __tablename__ = 'decks'

    id = Column(Integer, primary_key=True)
    deck_id = Column(String)
    name = Column(String)
    username = Column(String)
    description = Column(String)
    created_at = Column(String)


class Decklists(Base):
   __tablename__ = 'decklist'
   id = Column(Integer, primary_key=True)
   deck_id = Column(String)
   card_id = Column(String)
   quantity = Column(Integer)
