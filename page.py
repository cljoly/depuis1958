#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from os.path import join
import datetime
import shutil
import locale
import argparse
import subprocess
import sys

import numpy as np
import pandas as pd

from jinja2 import Environment, FileSystemLoader

from model import sortby, all_possible_second_rounds
from graphs import violin_vert, pgm, time_plot
import exdata
from polls import PollCollection, second_round_poll_file
from election import ElectionModel, TimeElectionModel

def percent(x):
    "HTML rendering of a percentage value"
    return "{0:.1f}&nbsp;%".format(100*x)

def context_total(election_model, settings):
    # Total probabilities
    context = []

    def key(x):
        "Sort by (inverse) win probability, then alphabetical if equal"
        # Use minus here, not reverse=True because alphabetical is correct order already
        return (-x[1], exdata.candidates_alphabetical_index[x[0]])

    for i, (c, v) in enumerate(sorted(election_model.total_win_probability().items(), key=key)):
        context.append((c, percent(v)))

    return context

def context_duos(model, second_rounds, settings):
    context = []

    def key(x):
        "Sort by (inverse) duo probability, then alphabetical if equal"
        # Use minus here, not reverse=True because alphabetical is correct order already
        duo, prob = x
        c1, c2 = list(duo)
        return (-prob,
                min(exdata.candidates_alphabetical_index[c1], exdata.candidates_alphabetical_index[c2]),
                max(exdata.candidates_alphabetical_index[c1], exdata.candidates_alphabetical_index[c2]))

    # Probability duos from most to least probable
    for i, (duo, prob_duo) in enumerate(sorted(model.probability_duos().items(), key=key)):
        candidates = second_rounds[duo].candidates
        probs = second_rounds[duo].probability_win()


        if second_rounds[duo].sum() > 2:
            # Sort by conditional winner
            indexes = np.argsort(probs)[::-1]
        else:
            # Sort alphabetical
            indexes = np.argsort([exdata.candidates_alphabetical_index[candidates[0]], exdata.candidates_alphabetical_index[candidates[1]]])

        # Sort
        c1, c2 = sortby(candidates, indexes)
        prob_c1, prob_c2 = sortby(probs, indexes)

        klass = "hiddable" if i+1 > settings["show_n_duos"] else ""

        # Render "-" if no conditional poll, not "50 %"
        rendered_prob_c1 = percent(prob_c1) if second_rounds[duo].sum() > 2 else "-"
        rendered_prob_c2 = percent(prob_c2) if second_rounds[duo].sum() > 2 else "-"

        context.append([percent(prob_duo), c1, c2, rendered_prob_c1, rendered_prob_c2, klass])
    return context

def equivalent_score_2012(candidates, results_2012):
    "Vector of scores in 2012 election (thyself or party equivalent)"
    scores = np.zeros(len(candidates))
    for i, c in enumerate(candidates):
        if c in results_2012.keys():
            scores[i] = results_2012[c] / 100
        elif c in exdata.candidates_2012_equivalents.keys():
            scores[i] = results_2012[exdata.candidates_2012_equivalents[c]] / 100
    return scores

def context_individuals(model, settings):
    # Probabilities of second round
    probs_second_round = model.probability_second_round()
    probs_third = model.probability_rank(2) # rank is 0-based here

    results_2012 = exdata.elections["2012"]["official_results"]
    ref = equivalent_score_2012(model.candidates, results_2012)
    probs_better_last = model.probability_better_than(ref)

    # Sort by inverse second round prob, then alphabetical
    # yes this is black magic
    indices = sorted(range(len(probs_second_round)), key=lambda x: (-probs_second_round[x], exdata.candidates_alphabetical_index[model.candidates[x]]))

    return [(c, percent(p1), percent(p2), percent(p3) if c in dict(results_2012, **exdata.candidates_2012_equivalents) else "-")
            for c, p1, p2, p3 in zip(np.array(model.candidates)[indices],
                                     probs_second_round[indices],
                                     probs_third[indices],
                                     probs_better_last[indices])]

def context_source(election):
    # set() to get unique sources
    sources = set()
    for date, first_round_filename in election["first_round_filenames"]:
        first = pd.read_csv(first_round_filename)
        for s in first.loc[:, "source"]:
            sources.add(str(s))

        candidates = first.columns[5:]

    for duo in all_possible_second_rounds(candidates):
        second_file = second_round_poll_file(election["second_round_prefix"], duo)
        if os.path.isfile(second_file):
            for s in pd.read_csv(second_file).loc[:, "source"]:
                sources.add(str(s))

    # sorted() so the html output is deterministic
    return "&nbsp;• ".join(sorted(list(sources)))

def context_polls(year):
    root = "data/{}/".format(year)
    names = sorted(os.listdir(root))
    return [(name, join(root, name)) for name in names]

def trace(s):
    print(s)
    sys.stdout.flush()

def context_full(election, settings, quick):
    trace("{}...".format(election["date_first_round"].year))

    context = {
        "election": election,
        "settings": settings,
        "last_update": datetime.datetime.today().strftime("%d/%m/%Y à %H:%M")
    }
    year = election["date_first_round"].year

    trace("Building main election model with latest hypothesis...")
    first_round_filename = election["first_round_filenames"][-1][1]
    poll_collection = PollCollection(election, first_round_filename)
    election_model = ElectionModel(election, poll_collection, election["date_second_round"], settings["number_of_samples_base"], settings)

    context["number_of_valid_polls"] = election_model.poll_collection.number_of_first_round_polls() + election_model.poll_collection.number_of_second_round_polls()

    # Number of samples formatted with space thousands separator
    locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")
    context["formatted_number_of_samples"] = locale.format("%d", settings["number_of_samples_base"], grouping=True)

    # Violin plots
    trace("Violin plots...")
    filename_violin = "violin-" + repr(year) + ".png"
    context["violin_path"] = filename_violin
    #title = "Premier tour {} - Densités marginales aposteriori".format(year)
    violin_vert(election_model.model_first_round, join("public", filename_violin), title=None, ground_truth=election["official_results"])

    # Conditional violin plots
    for duo, conditional_model in election_model.models_second_rounds.items():
        filename_violin = "violin-" + repr(year) + repr(conditional_model.candidates) + ".png"
        gs = None
        if election["official_results_second_round"] and duo == frozenset(election["official_results_second_round"].keys()):
            gs = election["official_results_second_round"]
        if conditional_model.sum() > 2:
            violin_vert(conditional_model, join("public", "violins", filename_violin), title=None, ground_truth=gs)

    # Time plot
    trace("Time election models...")
    dated_time_election_models = [
        (date, TimeElectionModel(election, PollCollection(election, first_round_filename), settings, quick))
        for date, first_round_filename in election["first_round_filenames"]]
    filename_time_plot = "time-plot-" + repr(year) + "-" + datetime.datetime.now().isoformat() + ".png"
    context["time_plot_path"] = filename_time_plot
    winning_duo = None
    if election["official_results_second_round"] is not None:
        winning_duo = frozenset(election["official_results_second_round"].keys())
    trace("Time plot...")
    time_plot(join("public", filename_time_plot), election, dated_time_election_models, winning_duo, interpolation="linear")

    # PGM
    pgm(join("public", "pgm.png"))

    context["prediction"] = {
        "probability_total": context_total(election_model, settings),
        "duos": context_duos(election_model.model_first_round, election_model.models_second_rounds, settings),
        "individuals": context_individuals(election_model.model_first_round, settings),
    }

    context["data_source"] = context_source(election)

    context["list_of_polls"] = context_polls(election["date_first_round"].year)

    return context

# settings is a read-only dict of parameters
# context is a write-only dict for rendering
default_settings = {
    "number_of_samples_base": 5000000,
    "number_of_samples_time_plot": 1000000,
    "constant_precision": 400, # Equivalent sample size for a single poll on election day
    "election_cycle_duration": 130, # parameter for the time coefficient, in days, None to not use a time factor
    "keep_only_latest": True,
    "show_n_duos": 5,
}

def render(env, template, target, context):
    with open(target, "w") as f:
        html = env.get_template(template).render(context)
        f.write(html)

def make_public(quick):
    "Make public website"

    os.makedirs("public", exist_ok=True)
    os.makedirs("public/methodologie", exist_ok=True)
    os.makedirs("public/apropos", exist_ok=True)
    os.makedirs("public/2002", exist_ok=True)
    os.makedirs("public/2007", exist_ok=True)
    os.makedirs("public/2012", exist_ok=True)
    os.makedirs("public/violins", exist_ok=True)

    settings = default_settings

    if quick:
        settings["number_of_samples_base"] = 2000

    context2002 = context_full(exdata.elections["2002"], settings, quick)
    context2007 = context_full(exdata.elections["2007"], settings, quick)
    context2012 = context_full(exdata.elections["2012"], settings, quick)
    context2017 = context_full(exdata.elections["2017"], settings, quick)

    print("Rendering html...")
    env = Environment(loader=FileSystemLoader("templates"))
    env.globals.update(get_candidate_color=exdata.candidates_colors.get)

    # Render 2002 prediction page
    context2002["nav"] = {"previous": None, "next": {"label": "2007", "link": "/2007/"}}
    render(env, "prediction.html", join("public", "2002", "index.html"), context2002)

    # Render 2007 prediction page
    context2007["nav"] = {"previous": {"label": "2002", "link": "/2002/"}, "next": {"label": "2012", "link": "/2012/"}}
    render(env, "prediction.html", join("public", "2007", "index.html"), context2007)

    # Render 2012 prediction page
    context2012["nav"] = {"previous": {"label": "2007", "link": "/2007/"}, "next": {"label": "2017", "link": "/"}}
    render(env, "prediction.html", join("public", "2012", "index.html"), context2012)

    # Render all 2017 pages
    context2017["nav"] = {"previous": {"label": "2012", "link": "/2012/"}, "next": None}
    render(env, "prediction.html", join("public", "index.html"), context2017)
    render(env, "methodologie.html", join("public", "methodologie", "index.html"), context2017)
    render(env, "apropos.html", join("public", "apropos", "index.html"), context2017)

    # Copy static ressources
    shutil.copyfile("templates/style.css", "public/style.css")
    shutil.copyfile("templates/main.js", "public/main.js")
    shutil.copyfile("templates/email.js", "public/email.js")
    shutil.copyfile("web/logo_with_math.png", "public/logo.png")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Depuis 1958")
    parser.add_argument("--quick", action="store_true", help="Quick build")
    args = parser.parse_args()

    make_public(args.quick)
