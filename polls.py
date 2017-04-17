from os.path import join
import os

import numpy as np
import pandas as pd
import datetime

from model import argsort, sortby, all_possible_second_rounds
import exdata
import os.path

class Poll(object):
    "A single election poll"
    def __init__(self, obj):
        self.institute = obj["sondeur"]
        self.sample_size = obj["échantillon"]

        candidates = list(obj.index[5:])
        values = list(obj.iloc[5:])

        indexes = argsort(candidates, key=exdata.candidates_alphabetical_index.get)
        self.candidates = sortby(candidates, indexes)
        self.values = np.array(sortby(values, indexes))

        self.date = datetime.datetime.strptime(obj["date fin"], "%Y-%m-%d")

    def time_coeff(self, election_date, cycle_duration):
        "Time coefficient of the poll"
        cycle_begin = election_date - datetime.timedelta(days=cycle_duration)
        return (self.date - cycle_begin).days / cycle_duration

def poll_list(data_frame):
    "Parse a poll file into a list of polls, with optional fake_today"
    return [Poll(p) for i, p in data_frame.iterrows()]

def second_round_poll_file(prefix, duo):
    candidates = list(duo)
    indexes = argsort(candidates, key=exdata.candidates_alphabetical_index.get)
    candidates = sortby(candidates, indexes)
    c1, c2 = candidates
    return join(prefix, "second-tour-{}-{}.csv".format(exdata.candidates_shortnames[c1], exdata.candidates_shortnames[c2]))

class PollCollection(object):
    "All polls (both rounds) related to a given election and first round hypothesis"
    def __init__(self, election, first_round_filename):
        # First round, get list of candidates and parse polls
        first_round_data = pd.read_csv(first_round_filename)
        self.candidates = sorted(first_round_data.columns[5:], key=exdata.candidates_alphabetical_index.get)
        self.polls_first_round = poll_list(first_round_data)

        # Second round
        self.polls_second_round = {}
        for duo in all_possible_second_rounds(self.candidates):
            # See if a poll file exists and contains valid polls
            poll_file = second_round_poll_file(election["second_round_prefix"], duo)
            if os.path.isfile(poll_file):
                second_round_data = pd.read_csv(poll_file)
                self.polls_second_round[duo] = poll_list(second_round_data)
            else:
                self.polls_second_round[duo] = []

    def fake_today_poll_dates(self):
        """
        Sorted list of unique dates where new polls are available
        starting on the first available first round poll
        """
        poll_dates = [poll.date for poll in self.polls_first_round]
        first = min(poll_dates)
        for sr in self.polls_second_round.values():
            poll_dates.extend([poll.date for poll in sr])

        # Don't consider a date if no first round poll available
        poll_dates = [date for date in poll_dates if date >= first]
        return pd.DatetimeIndex(sorted(list(set(poll_dates))))

    def get_first_rounds(self, limit_date):
        return [p for p in self.polls_first_round if p.date <= limit_date]

    def get_second_rounds(self, duo, limit_date):
        return [p for p in self.polls_second_round[duo] if p.date <= limit_date]

    def number_of_first_round_polls(self):
        "Total number of valid first round polls in the collection"
        return len(self.polls_first_round)

    def number_of_second_round_polls(self):
        "Total number of valid second round polls in the collection"
        return sum([len(poll_list) for poll_list in self.polls_second_round.values()])
