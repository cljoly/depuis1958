import numpy as np
import scipy.stats
from collections import defaultdict
import warnings
import itertools

class DirichletModel(object):
    def __init__(self, candidates, concentration_parameters, number_of_samples):
        self.candidates = candidates
        self.weights = concentration_parameters
        self.size = len(self.weights)
        self.number_of_samples = number_of_samples

    def get_samples(self):
        """Generate samples from the distribution"""
        return scipy.stats.dirichlet.rvs(self.weights, size=self.number_of_samples)

    def sum(self):
        "Sum of the concentration parameters"
        return np.sum(self.weights)

    def mode(self):
        "Mode of the distribution"
        if np.any(self.weights <= 1):
            warnings.warn("Dirichlet mode is undefined with concentration parameter <= 1.")
        return (self.weights - 1) / (np.sum(self.weights) - self.size)

    def mean(self):
        "Mean of the distribution"
        return self.weights / np.sum(self.weights)

    def marginal_parameters(self):
        "Parameters of the marginal beta distributions"
        return self.weights, np.sum(self.weights) - self.weights

    def marginal_modes(self):
        "Modes of the marginal beta distributions"
        a, b = self.marginal_parameters()
        return (a - 1) / (a + b - 2)

    def marginal_means(self):
        a, b = self.marginal_parameters()
        return a / (a + b)

    def probability_win(self):
        "Probability vector of individual score > 0.5"
        alphas, betas = self.marginal_parameters()
        return np.array([1 - scipy.stats.beta.cdf(0.5, a, b) for a, b in zip(alphas, betas)])

    def samples_ranks(self):
        "argsort in reverse order (highest score first), then argsort again to get ranks"
        samples = self.get_samples()
        sort_indices = np.fliplr(np.argsort(samples, axis=1))
        return np.argsort(sort_indices)

    def probability_rank(self, rank):
        """
        Probability of being {rank}
        rank is a 0-based index
        """
        ranks = self.samples_ranks()

        return np.sum(ranks[:, :] == rank, axis=0) / self.number_of_samples

    def probability_second_round(self):
        "Probability vector of individually passing to second round"

        ranks = self.samples_ranks()

        # Probability of being first or second
        first = np.sum(ranks[:, :] == 0, axis=0) / self.number_of_samples
        second = np.sum(ranks[:, :] == 1, axis=0) / self.number_of_samples
        return first + second

    def probability_better_than(self, R):
        "Individual probabilities of being greater than a reference"
        samples = self.get_samples()
        return np.sum(samples > R, axis=0) / self.number_of_samples

    def probability_duos(self):
        "Probability of second round duos"
        # Indexes of the two winners
        samples = self.get_samples()
        winners = np.fliplr(np.argsort(samples, axis=1))[:, :2]

        # Frequency count of rows of 'winners'
        # crazy snippet from http://stackoverflow.com/a/16973510/565840
        b = np.ascontiguousarray(winners).view(np.dtype((np.void, winners.dtype.itemsize * winners.shape[1])))
        _, idx, pcounts = np.unique(b, return_index=True, return_counts=True)

        # First round results are unordered pairs, so sum equivalent ones using a frozenset dict key
        counts = defaultdict(int)
        for pair, pc in zip(winners[idx], pcounts):
            key = frozenset({self.candidates[pair[0]], self.candidates[pair[1]]})
            counts[key] += pc

        # Divide by number of samples to get probability, zero if unseen
        probs = {
            duo: counts[duo] / self.number_of_samples
            for duo in all_possible_second_rounds(self.candidates)
        }

        # TODO this does not take into account that the second round might not
        # happen if one candidate does > 50% at the first
        return probs

    def covariance_matrix(self):
        "Covariance matrix"
        cov = np.zeros((self.size, self.size))

        a0 = np.sum(self.weights)
        D = a0*a0*(a0+1)

        # Diagonal
        for k in range(self.size):
            ak = self.weights[k]
            cov[k, k] = (ak*(a0-ak))/D

        # Off diagonal
        for i in range(self.size):
            for j in range(self.size):
                if i != j:
                    ai = self.weights[i]
                    aj = self.weights[j]
                    cov[i, j] = (-ai*aj)/D

        return cov

def all_possible_second_rounds(candidates):
    s = frozenset({frozenset({i, j}) for i, j in itertools.product(candidates, candidates) if i != j})
    N = len(candidates)
    assert(len(s) == (N*N - N)/2)
    return s

def argsort(seq, key=None):
    if key is None:
        return sorted(range(len(seq)), key=lambda x: seq[x])
    else:
        return sorted(range(len(seq)), key=lambda x: key(seq[x]))

def sortbyx(seqs, indexes):
    return [[seq[i] for i in indexes] for seq in seqs]

def sortby(seq, indexes):
    return [seq[i] for i in indexes]

