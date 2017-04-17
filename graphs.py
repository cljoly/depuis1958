# -*- coding: utf-8 -*-

import datetime
import locale
from collections import defaultdict

import numpy as np
import scipy
import scipy.interpolate
from matplotlib import font_manager
import matplotlib.pyplot as plt
from matplotlib.dates import drange, date2num, WeekdayLocator, DayLocator, DateFormatter, SUNDAY
from matplotlib.ticker import FuncFormatter, NullFormatter
import pandas as pd

from model import argsort, sortby, sortbyx
import exdata

def violin_vert(model, filename, title, ground_truth=None):
    plt.style.use("seaborn-white")
    fig = plt.figure(figsize=(11,6))
    ax = fig.add_subplot(1, 1, 1)

    positions = range(1, model.size + 1)

    width = 0.5
    Q = 0.001
    number_of_points = 1000

    for c in model.candidates:
        if c not in exdata.candidates_left_right_index:
            print("missing:", c)

    indexes = argsort(model.candidates, key=exdata.candidates_left_right_index.get)
    #indexes = argsort(candidates, key=exdata.candidates_alphabetical_index.get)
    candidates = sortby(model.candidates, indexes)

    # Violins
    alphas, betas = sortbyx(model.marginal_parameters(), indexes)

    lowers = scipy.stats.beta.ppf(Q, alphas, betas)
    highers = scipy.stats.beta.ppf(1-Q, alphas, betas)

    for a, b, l, h, pos, candidate in zip(alphas, betas, lowers, highers, positions, candidates):
        y = np.linspace(l, h, number_of_points)
        vals = scipy.stats.beta.pdf(y, a, b)
        # The 0.5 factor reflects the fact that we plot from v-p to v+p (mirror around x=pos)
        vals = 0.5 * width * vals / vals.max() # Warning, not the same scale for each violin, but prettier
        
        art = ax.fill_betweenx(y, pos - vals, pos + vals,
                               color=exdata.candidates_colors[candidate],
                               linewidth=1, edgecolor="k",
                               alpha=0.6)
        art.set_edgecolor("k") # workaround https://github.com/matplotlib/matplotlib/issues/5423

    # Mean and mode lines
    widths = [width] * model.size
    pmins = -0.25 * np.array(widths) + positions
    pmaxes = 0.25 * np.array(widths) + positions
    ax.hlines(sortby(model.mean(), indexes), pmins, pmaxes, colors="k", linestyle="-", linewidth=1, alpha=1)
    #ax.hlines(sortby(model.mode(), indexes), pmins, pmaxes, colors="k", linestyle="-", linewidth=1, alpha=0.5)

    if ground_truth is not None:
        gs = [ground_truth[c] / 100 for c in candidates]
        ax.hlines(gs, pmins, pmaxes, colors="r", linewidth=1, alpha=1)

    # Ticks and tick labels
    def percent(x, pos):
        return "{0:.0f} %".format(100 * x)

    majors = np.arange(0, 100, 10)
    minors = np.array([x for x in np.arange(0, 100, 2) if x not in majors])

    ax.set_yticks(majors / 100)
    ax.set_yticks(minors / 100, minor=True)
    ax.yaxis.set_major_formatter(FuncFormatter(percent))
    ax.yaxis.set_minor_formatter(FuncFormatter(percent))
    for t in ax.get_yticklabels(which="both"):
        t.set_horizontalalignment("right")

    ax.set_xticks(range(len(candidates) + 1))
    ax.set_xticklabels([""] + [exdata.candidates_tight[c] for c in candidates])

    ax.tick_params(axis="y", which="major", labelsize=12, direction="out", pad=5)
    ax.tick_params(axis="y", which="minor", labelsize=12, direction="out", pad=5)
    ax.tick_params(axis="x", which="major", labelsize=11, direction="out", pad=7)

    ticks_font = font_manager.FontProperties(family='DejaVu Sans Mono', style='normal')
    for label in ax.get_yticklabels(which="both"):
        label.set_fontproperties(ticks_font)

    # Plot limits
    if len(model.candidates) > 2:
        ax.set_ylim([0, 0.40])
    else:
        ax.set_ylim([0.30, 0.70])
    ax.set_xlim([0.5, model.size + 0.5])

    # Grid
    ax.grid(True, axis="y", which='major', linestyle="-", linewidth=1, color=(0.6, 0.6, 0.6))
    ax.grid(True, axis="y", which='minor', linestyle=":", linewidth=1, color=(0.7, 0.7, 0.7))
    ax.grid(False, axis="x", which='major')

    # Other visuals
    if title is not None:
        ax.set_title(title)
    ax.set_axis_bgcolor('white')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.yaxis.set_ticks_position('none')
    ax.xaxis.set_ticks_position('none')

    fig.savefig(filename, dpi=300, bbox_inches="tight")
    plt.close(fig)

events = {
    "2002": [
        (exdata.elections["2002"]["date_first_round"], None, "Premier tour", 0.20 + 0.025, "right"),
        (exdata.elections["2002"]["date_second_round"], None, "Second tour", 0.20 + 0.025, "right"),
    ],
    "2007": [
        (exdata.elections["2007"]["date_first_round"], None, "Premier tour", 0.20 + 0.025, "right"),
        (exdata.elections["2007"]["date_second_round"], None, "Second tour", 0.20 + 0.025, "right"),
    ],
    "2012": [
        (exdata.elections["2012"]["date_first_round"], None, "Premier tour", 0.15 + 0.025, "right"),
        (exdata.elections["2012"]["date_second_round"], None, "Second tour", 0.15 + 0.025, "right"),
    ],
    "2017": [
        (datetime.datetime(2017, 1, 25), "François Fillon", "Penelopegate", 0.65 + 0.025, "right"),
        (datetime.datetime(2017, 1, 29), "Benoît Hamon", "Primaire PS", 0.1 + 0.025, "right"),
        (datetime.datetime(2017, 3, 17), None, "Limite 500 signatures", 0.1 + 0.025, "left"),
        (datetime.datetime(2017, 2, 22), "Emmanuel Macron", "Retrait F. Bayrou", 0.75 + 0.025, "right"),
        (datetime.datetime(2017, 2, 23), "Benoît Hamon", "Retrait Y. Jadot", 0.10 + 0.025, "right"),
        (datetime.datetime(2017, 3, 20), None, "Débat TF1", 0.05 + 0.025, "left"),
        (datetime.datetime(2017, 4, 4), None, "Débat BFM", 0.05 + 0.025, "left"),
        (exdata.elections["2017"]["date_first_round"], None, "Premier tour", 0.05 + 0.025, "left"),
        (exdata.elections["2017"]["date_second_round"], None, "Second tour", 0.10 + 0.025, "right"),
    ],
}

text_black = (0, 0, 0)
background_gray = (0.55, 0.55, 0.55)
small_text = 9

def time_plot(filename, election, dated_time_election_models, winning_duo, interpolation):
    plt.style.use("seaborn-white")
    fig = plt.figure(figsize=(11,5))
    ax = fig.add_subplot(1, 1, 1)
    locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")

    # Intervals where candidate hypothesis are to be plotted
    segments_begins, time_election_models = list(zip(*dated_time_election_models))
    segments_ends = list(segments_begins[1:]) + [election["date_second_round"] + datetime.timedelta(1)]

    # Dictionnary with key: candidate, value: (poll_dates, total_win_prob)
    candidates_data = defaultdict(lambda: ([], []))

    # For each segment, keep polls they contain
    for segment_begin, segment_end, time_election_model in zip(segments_begins, segments_ends, time_election_models):
        # Take poll_dates and win_probs that are within the segment
        for poll_date, election_model in zip(time_election_model.poll_dates, time_election_model.election_models):
            if poll_date >= segment_begin and poll_date < segment_end:
                win_prob = election_model.total_win_probability()
                for candidate in election_model.candidates:
                    candidates_data[candidate][0].append(poll_date)
                    candidates_data[candidate][1].append(win_prob[candidate])

    # Build candidate order for plotting, from worse to best
    candidates_ordered = list(zip(*sorted({c: candidates_data[c][1][-1] for c in candidates_data.keys()}.items(), key=lambda x: x[1])))[0]

    # Plot first round lines
    interpolators = {} # Keep candidates interpolators for later (event lines)
    for candidate in candidates_ordered:
        # Build X axis range from poll_dates and Y
        poll_dates = pd.DatetimeIndex(candidates_data[candidate][0])
        Y = candidates_data[candidate][1]
        X = drange(poll_dates.min(), min(election["date_first_round"], poll_dates.max())+datetime.timedelta(1), datetime.timedelta(1))

        #ax.plot(poll_dates, Y[:, i], linestyle="", marker="o", color=exdata.candidates_colors[candidate])
        interpolated = scipy.interpolate.interp1d(date2num(list(poll_dates)), Y, kind=interpolation)
        interpolators[candidate] = interpolated
        ax.plot_date(X, interpolated(X),
                linestyle="-",
                marker="",
                linewidth=2.5,
                color=exdata.candidates_colors[candidate],
                label=candidate,
                )

    # Plot second round lines
    if winning_duo is not None:
        # poll dates in between rounds
        time_election_model = time_election_models[-1] # take the last hypothesis, but conditional models are the same

        poll_dates = pd.DatetimeIndex(time_election_model.poll_dates)

        # If there's anything to plot
        if poll_dates.max() > election["date_first_round"]:

            # Same as above
            candidates_data_second_round = defaultdict(lambda: ([], []))

            for poll_date, election_model in zip(time_election_model.poll_dates, time_election_model.election_models):
                model = election_model.models_second_rounds[winning_duo]
                cond_win_prob = model.probability_win()
                for c, p in zip(model.candidates, cond_win_prob):
                    candidates_data_second_round[c][0].append(poll_date)
                    candidates_data_second_round[c][1].append(p)

            # Plot
            for candidate in candidates_data_second_round.keys(): # whatever order here
                X = drange(election["date_first_round"], poll_dates.max()+datetime.timedelta(1), datetime.timedelta(1))
                Y = candidates_data_second_round[candidate][1]

                interpolated = scipy.interpolate.interp1d(date2num(candidates_data_second_round[candidate][0]), Y, kind=interpolation)

                ax.plot_date(X, interpolated(X),
                        linestyle="-",
                        marker="",
                        linewidth=2.5,
                        color=exdata.candidates_colors[candidate],
                        label=candidate,
                        )

    # Plot events
    for date, candidate, label, textypos, halign in events[str(election["date_first_round"].year)]:
        x = date2num(date)
        y = 0 if candidate is None else interpolators[candidate](x)
        ax.text(x, textypos, " " + label + " ", horizontalalignment=halign, verticalalignment="center", color=background_gray, fontsize=small_text)
        ax.plot((x, x), (y, textypos), "-", color=background_gray, linewidth=1, zorder=0)

    # Spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_position(('data', -0.02))
    ax.spines['bottom'].set_color(text_black)

    # X axis tick and labels
    # ax.xaxis.set_major_locator(WeekdayLocator(SUNDAY, interval=2))
    # WeekdayLocator works but is sometimes offbeat, we want ticks fixed on first and second rounds
    # So do it by hand :(
    def sunday_ticks():
        second_round = election["date_second_round"]
        ticks = [date2num(second_round)]
        for n in range(100):
            ticks.append(ticks[-1] - 14)
        return list(reversed(ticks))

    ax.xaxis.set_ticks(sunday_ticks())

    ax.xaxis.set_minor_locator(DayLocator())
    ax.xaxis.set_major_formatter(DateFormatter("%d %b"))

    for t in ax.get_xticklabels():
        t.set_horizontalalignment("center")
        t.set_rotation(0)

    ax.tick_params(axis="x", which="major", direction="out", bottom=True, top=False,
                   labelsize=14, pad=15, length=8, width=1,
                   labelcolor=text_black,
                   color=text_black,
                   )

    ax.tick_params(axis="x", which="minor", direction="out", bottom=True, top=False,
                   length=3, width=1,
                   color=text_black,
                   )

    # Y axis tick and labels
    def percent(x, pos):
        return "{0:.0f} %".format(100 * x)

    majors = np.array([0, 25, 50, 75, 100])
    minors = np.array([x for x in np.arange(0, 100, 5) if x not in majors])
    #minors = np.array([])

    ax.set_yticks(majors / 100)
    ax.set_yticks(minors / 100, minor=True)

    ax.yaxis.set_major_formatter(FuncFormatter(percent))
    ax.yaxis.set_minor_formatter(NullFormatter())

    for t in ax.get_yticklabels(which="both"):
        t.set_horizontalalignment("right")

    ax.tick_params(axis="y", which="major",
                   labelsize=14, direction="out", pad=5,
                   labelcolor=text_black,
                   )
    ticks_font = font_manager.FontProperties(family='DejaVu Sans Mono', style='normal')
    for label in ax.get_yticklabels(which="both"):
        label.set_fontproperties(ticks_font)

    # Limits
    start = election["timeplot_start"]
    end = election["date_second_round"]
    ax.set_xlim([date2num(start), date2num(end)])
    ax.set_ylim([-0.02, 1.02]) # small margin to fix grid line width

    # Grid
    ax.grid(True, axis="y", which='major', linestyle="-", linewidth=0.5, color=background_gray)
    ax.grid(True, axis="y", which='minor', linestyle=":", linewidth=0.5, color=background_gray)
    ax.grid(False, axis="x", which='major')

    # Other visuals
    ax.set_axis_bgcolor('white')

    #ax.text(date2num(start + datetime.timedelta(1)), 0.95 + 0.025, "depuis1958.fr", horizontalalignment="left", verticalalignment="center", size=small_text, color=background_gray)
    #ax.text(date2num(start + datetime.timedelta(1)), 0.90 + 0.025, "CC BY-NC 3.0 FR", horizontalalignment="left", verticalalignment="center", size=small_text, color=background_gray)

    fig.savefig(filename, dpi=300, bbox_inches="tight")

    plt.close(fig)

def pgm(path):
    from matplotlib import rc
    rc("font", family="serif", size=12)

    import daft

    pgm = daft.PGM([3.3, 3.1], origin=[0.4, 0.3])

    # First round
    pgm.add_node(daft.Node("alpha", r"$\alpha$", 1, 3, fixed=True))
    pgm.add_node(daft.Node("theta", r"$\theta$", 1, 2))
    pgm.add_node(daft.Node("X", r"$X$", 1, 1, observed=True))

    # Second rounds
    pgm.add_node(daft.Node("beta", r"$\beta$", 3, 3, fixed=True))
    pgm.add_node(daft.Node("pi", r"$\pi_{AB}$", 3, 2))
    pgm.add_node(daft.Node("Y", r"$Y_{AB}$", 3, 1, observed=True))

    # Middle part
    pgm.add_node(daft.Node("S", r"$S_{AB}$", 2, 2.5))
    pgm.add_node(daft.Node("T", r"$T$", 2, 1.5))

    pgm.add_edge("alpha", "theta")
    pgm.add_edge("theta", "X")

    pgm.add_edge("beta", "pi")
    pgm.add_edge("pi", "Y")
    pgm.add_edge("theta", "T")
    pgm.add_edge("theta", "S")
    pgm.add_edge("S", "T")
    pgm.add_edge("pi", "T")

    # First round polls
    #pgm.add_plate(daft.Plate([0.5, 0.5, 1, 1]))

    # Second round polls
    #pgm.add_plate(daft.Plate([2.5, 0.5, 1, 1]))

    # Second rounds
    pgm.add_plate(daft.Plate([2.4, 0.4, 1.2, 2.2]))

    # Render and save.
    pgm.render()
    pgm.figure.savefig(path, dpi=300)
