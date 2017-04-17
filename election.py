from collections import defaultdict

import numpy as np

from model import DirichletModel, all_possible_second_rounds
import exdata

def keep_latest_per_institute(polls):
    latest = {}
    for poll in polls:
        if poll.institute not in latest:
            latest[poll.institute] = poll
        else:
            if poll.date > latest[poll.institute].date:
                latest[poll.institute] = poll
    return list(latest.values())

def build_model(candidates, poll_objects, election_date, number_of_samples, settings):

    # Keep only latest
    if settings["keep_only_latest"]:
        kept_polls = keep_latest_per_institute(poll_objects)
    else:
        kept_polls = poll_objects

    # Dirichlet prior concentration parameters
    # Uniform prior with large uncertainty
    concentration_parameters = np.ones(len(candidates))

    nk = len(kept_polls)

    # Compute aposteriori concentration parameters given the polls' multinomial observations
    # i.e. add all polls multinomial counts (because dirichlet is conjugate prior to multinomial)
    for poll in kept_polls:
        # Checks
        assert (poll.candidates == candidates)
        #assert (abs(np.sum(poll.values) - 100) < 1e-10)
        if not (abs(np.sum(poll.values) - 100) < 1e-10):
            print("WARNING: Poll does not sum to 100.")

        if settings["election_cycle_duration"] is not None:
            time_coeff = poll.time_coeff(election_date, settings["election_cycle_duration"])
        else:
            time_coeff = 1
        assert (time_coeff > 0 and time_coeff <= 1)

        # Non independent polls, use constant precision
        D = settings["constant_precision"]

        # Bayesian updating
        concentration_parameters += (time_coeff * D/nk) * (poll.values / 100.0)

    # Model built with parameters = candidates in alphabetical order
    model = DirichletModel(candidates, concentration_parameters, number_of_samples)
    return model

class ElectionModel(object):
    """
    Statistical model for a two-round majority voting election
    """
    def __init__(self, election, poll_collection, limit_date, number_of_samples, settings):
        self.election = election
        self.poll_collection = poll_collection
        self.candidates = poll_collection.candidates

        # Build first round model
        self.model_first_round = build_model(poll_collection.candidates,
                                             poll_collection.get_first_rounds(limit_date),
                                             election["date_first_round"],
                                             number_of_samples,
                                             settings)

        # Build second round models
        self.models_second_rounds = {}
        for duo in all_possible_second_rounds(poll_collection.candidates):
            candidates = sorted(duo, key=exdata.candidates_alphabetical_index.get)
            self.models_second_rounds[duo] = build_model(candidates,
                                                         poll_collection.get_second_rounds(duo, limit_date),
                                                         election["date_second_round"],
                                                         number_of_samples,
                                                         settings)

    def total_win_probability(self):
        "Total winning chances after both rounds"
        totals =  defaultdict(np.float64)
        # TODO also add win prob at first round

        prob_duos = self.model_first_round.probability_duos()

        # For each candidate, the total win probability is:
        #     sum( P( win | second round ) * P( second round ) )
        # So, compute this sum for each candidate by adding each possible second
        # round's contribution to both participating candidates total probabilities
        for duo in self.models_second_rounds.keys():
            c1, c2 = duo

            # The order between c1 and c2 is unknown here, so get it with .index()
            index_c1 = self.models_second_rounds[duo].candidates.index(c1)
            index_c2 = self.models_second_rounds[duo].candidates.index(c2)

            # Add contribution of this possible second round to each candidate's total probability
            win_prob = self.models_second_rounds[duo].probability_win()
            totals[c1] += win_prob[index_c1] * prob_duos[duo]
            totals[c2] += win_prob[index_c2] * prob_duos[duo]
        return totals


class TimeElectionModel(object):
    "ElectionModel function of time"
    def __init__(self, election, poll_collection, settings, quick=False):
        # Get list of fake_todays from first round file
        self.poll_dates = poll_collection.fake_today_poll_dates()

        self.candidates = poll_collection.candidates
        self.election_models = []

        for date in self.poll_dates:

            if date == self.poll_dates[-1]:
                number_of_samples = settings["number_of_samples_base"]
            else:
                number_of_samples = settings["number_of_samples_time_plot"]

            if quick:
                number_of_samples = 2000

            election_model = ElectionModel(election, poll_collection, date, number_of_samples, settings)
            self.election_models.append(election_model)
