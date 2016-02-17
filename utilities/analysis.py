import pandas as pd
import operator
from math import ceil


def create_average_deck(dataframe, decksize, clustering_column=None):
    # Takes in a dataframe of non-normalized card counts
    # if None, creates a deck for all
    # Decksize is an int that says how big said deck should be
    data_copy = dataframe.copy()
    return_list = []
    if clustering_column:
        for column in data_copy[clustering_column].unique():
            column_copy = data_copy.copy()
            column_copy = column_copy.loc[
                (column_copy[clustering_column] == column)]
            cards = list(column_copy.columns)
            cards = [card for card in cards if card != clustering_column]
            average_card_usage = {}
            for card in cards:
                average = column_copy[card].describe()['mean']
                if average > 0.0:
                    average_card_usage[card] = average
            sorted_dict = sorted(average_card_usage.items(),
                                 key=operator.itemgetter(1),
                                 reverse=True)
            decklist = []
            card_counter = 0
            for card in sorted_dict:
                card_count = ceil(card[1])
                card_counter += card_count
                if card_counter < decksize:
                    decklist.append((card[0], card_count, card[1]))
                elif card_counter == decksize:
                    decklist.append((card[0], card_count, card[1]))
                    break
                else:
                    amount_over = card_counter - decksize
                    card_count = card_count - amount_over
                    decklist.append((card[0], card_count, card[1]))
                    break
            return_list.append(decklist)
    else:
        cards = list(data_copy.columns)
        average_card_usage = {}
        for card in cards:
            average = column_copy[card].describe()['mean']
            if average > 0.0:
                average_card_usage[card] = average
        sorted_dict = sorted(average_card_usage.items(),
                            key=operator.itemgetter(1),
                            reverse=True)
        decklist = []
        card_counter = 0
        for card in sorted_dict:
            card_count = round(card[1])
            card_counter += card_count
            if card_counter < decksize:
                decklist.append((card[0], card_count, card[1]))
            elif card_counter == decksize:
                decklist.append((card[0], card_count, card[1]))
                break
            else:
                amount_over = card_counter - decksize
                card_count = card_count - amount_over
                decklist.append((card[0], card_count, card[1]))
                break
        return_list = decklist
    return return_list
