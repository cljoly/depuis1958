# -*- coding: utf-8 -*-

import datetime

elections = {
    "2002": {
        "date_first_round": datetime.datetime(2002, 4, 21),
        "date_second_round": datetime.datetime(2002, 5, 5),
        "official_results": {
            "Bruno Mégret": 2.34,
            "Corinne Lepage": 1.88,
            "Daniel Gluckstein": 0.47,
            "François Bayrou": 6.84,
            "Jacques Chirac": 19.88,
            "Jean-Marie Le Pen": 16.86,
            "Christiane Taubira": 2.32,
            "Jean Saint-Josse": 4.23,
            "Noël Mamère": 5.25,
            "Lionel Jospin": 16.18,
            "Christine Boutin": 1.19,
            "Robert Hue": 3.37,
            "Jean-Pierre Chevènement": 5.33,
            "Alain Madelin": 3.91,
            "Arlette Laguiller": 5.72,
            "Olivier Besancenot": 4.25,
        },
        "official_results_second_round": {
            "Jacques Chirac": 82.21,
            "Jean-Marie Le Pen": 17.79,
        },
        "first_round_filenames": [
            (datetime.datetime(2002, 1, 1), "data/2002/premier-tour-mars.csv"),
            (datetime.datetime(2002, 4, 1), "data/2002/premier-tour-avril.csv"),
        ],
        "second_round_prefix": "data/2002/",
        "timeplot_start": datetime.datetime(2002, 1, 1),
    },
    "2007": {
        "date_first_round": datetime.datetime(2007, 4, 22),
        "date_second_round": datetime.datetime(2007, 5, 6),
        "official_results": {
            "Olivier Besancenot": 4.08,
            "Marie-George Buffet": 1.93,
            "Gérard Schivardi": 0.34,
            "François Bayrou": 18.57,
            "José Bové": 1.32,
            "Dominique Voynet": 1.57,
            "Philippe de Villiers": 2.23,
            "Ségolène Royal": 25.87,
            "Frédéric Nihous": 1.15,
            "Jean-Marie Le Pen": 10.44,
            "Arlette Laguiller": 1.33,
            "Nicolas Sarkozy": 31.18,
        },
        "official_results_second_round": {
            "Nicolas Sarkozy": 53.06,
            "Ségolène Royal": 46.94,
        },
        "first_round_filenames": [
            (datetime.datetime(2007, 1, 1), "data/2007/premier-tour.csv"),
        ],
        "second_round_prefix": "data/2007/",
        "timeplot_start": datetime.datetime(2007, 1, 1),
    },
    "2012": {
        "date_first_round": datetime.datetime(2012, 4, 22),
        "date_second_round": datetime.datetime(2012, 5, 6),
        "official_results": {
            "Nathalie Arthaud": 0.56,
            "François Bayrou": 9.13,
            "Jacques Cheminade": 0.25,
            "Nicolas Dupont-Aignan": 1.79,
            "François Hollande": 28.63,
            "Eva Joly": 2.31,
            "Marine Le Pen": 17.90,
            "Jean-Luc Mélenchon": 11.10,
            "Philippe Poutou": 1.15,
            "Nicolas Sarkozy": 27.18,
        },
        "official_results_second_round": {
            "Nicolas Sarkozy": 48.36,
            "François Hollande": 51.64,
        },
        "first_round_filenames": [
            (datetime.datetime(2012, 1, 1), "data/2012/premier-tour-janvier.csv"),
            (datetime.datetime(2012, 2, 1), "data/2012/premier-tour-fevrier.csv"),
            (datetime.datetime(2012, 3, 1), "data/2012/premier-tour-mars.csv"),
            (datetime.datetime(2012, 4, 1), "data/2012/premier-tour-avril.csv"),
        ],
        "second_round_prefix": "data/2012/",
        "timeplot_start": datetime.datetime(2012, 1, 1),
    },
    "2017": {
        "date_first_round": datetime.datetime(2017, 4, 23),
        "date_second_round": datetime.datetime(2017, 5, 7),
        "official_results": None,
        "official_results_second_round": None,
        "first_round_filenames": [
            (datetime.datetime(2017, 1, 1), "data/2017/premier-tour-sans-bayrou.csv"),
            (datetime.datetime(2017, 2, 24), "data/2017/premier-tour-sans-jadot.csv"),
            (datetime.datetime(2017, 3, 11), "data/2017/premier-tour-officiel.csv"),
        ],
        "second_round_prefix": "data/2017/",
        "timeplot_start": datetime.datetime(2017, 1, 7),
    },
}

# Candidates metadata
# The order of this list defines the "left-to-right" political association
# 'shortname' defines the identifier for the second round poll files and the alphabetical sort order
# 'tight' is a short name on two lines (for violin plots)
candidates_metadata = [
("Jacques Cheminade", {
    "color": "#C0B440",
    "tight": "Jacques\nCheminade",
    "shortname": "cheminade",
    }),
("Arlette Laguiller", {
    "color": "#BB0000",
    "tight": "Arlette\nLaguiller",
    "shortname": "laguiller",
    }),
("Daniel Gluckstein", {
    "color": "#BB0000",
    "tight": "Daniel\nGluckstein",
    "shortname": "gluckstein",
    }),
("Nathalie Arthaud", {
    "color": "#BB0000",
    "tight": "Nathalie\nArthaud",
    "shortname": "arthaud",
    }),
("Gérard Schivardi", {
    "color": "#4682B4",
    "tight": "Gérard\nSchivardi",
    "shortname": "schivardi",
    }),
("Arlette Laguiller", {
    "color": "#BB0000",
    "tight": "Arlette\nLaguiller",
    "shortname": "laguiller",
    }),
("Marie-George Buffet", {
    "color": "#BB0000",
    "tight": "Marie-George\nBuffet",
    "shortname": "buffet",
    }),
("Philippe Poutou", {
    "color": "#BB0000",
    "tight": "Philippe\nPoutou",
    "shortname": "poutou",
    }),
("Olivier Besancenot", {
    "color": "#BB0000",
    "tight": "Olivier\nBesancenot",
    "shortname": "besancenot",
    }),
("Robert Hue", {
    "color": "#DD0000",
    "tight": "Robert\nHue",
    "shortname": "hue",
    }),
("Jean-Luc Mélenchon", {
    "color": "#DD0000",
    "tight": "Jean-Luc\nMélenchon",
    "shortname": "melenchon",
    }),
("Jean-Pierre Chevènement", {
    "color": "#CC6666",
    "tight": "Jean-Pierre\nChevènement",
    "shortname": "chevenement",
    }),
("José Bové", {
    "color": "#00C000",
    "tight": "José\nBové",
    "shortname": "bove",
    }),
("Yannick Jadot", {
    "color": "#00C000",
    "tight": "Yannick\nJadot",
    "shortname": "jadot",
    }),
("Eva Joly", {
    "color": "#00C000",
    "tight": "Eva\nJoly",
    "shortname": "joly",
    }),
("Noël Mamère", {
    "color": "#00C000",
    "tight": "Noël\nMamère",
    "shortname": "mamere",
    }),
("Corinne Lepage", {
    "color": "#77FF77",
    "tight": "Corinne\nLepage",
    "shortname": "lepage",
    }),
("Dominique Voynet", {
    "color": "#00C000",
    "tight": "Dominique\nVoynet",
    "shortname": "voynet",
    }),
("Lionel Jospin", {
    "color": "#FF8080",
    "tight": "Lionel\nJospin",
    "shortname": "jospin",
    }),
("Christiane Taubira", {
    "color": "#FFD1DC",
    "tight": "Christiane\nTaubira",
    "shortname": "taubira",
    }),
("Benoît Hamon", {
    "color": "#FF8080",
    "tight": "Benoît\nHamon",
    "shortname": "hamon",
    }),
("Arnaud Montebourg", {
    "color": "#FF8080",
    "tight": "Arnaud\nMontebourg",
    "shortname": "montebourg",
    }),
("Vincent Peillon", {
    "color": "#FF8080",
    "tight": "Vincent\nPeillon",
    "shortname": "peillon",
    }),
("Manuel Valls", {
    "color": "#FF8080",
    "tight": "Manuel\nValls",
    "shortname": "valls",
    }),
("François Hollande", {
    "color": "#FF8080",
    "tight": "François\nHollande",
    "shortname": "hollande",
    }),
("Ségolène Royal", {
    "color": "#FF8080",
    "tight": "Ségolène\nRoyal",
    "shortname": "royal",
    }),
("Emmanuel Macron", {
    "color": "#ff9c2f",
    "tight": "Emmanuel\nMacron",
    "shortname": "macron",
    }),
("Jean Lassalle", {
    "color": "#6b848c",
    "tight": "Jean\nLassalle",
    "shortname": "lassalle",
    }),
("François Bayrou", {
    "color": "#FF9900",
    "tight": "François\nBayrou",
    "shortname": "bayrou",
    }),
("Christine Boutin", {
    "color": "#0000FF",
    "tight": "Christine\nBoutin",
    "shortname": "boutin",
    }),
("Jacques Chirac", {
    "color": "#0066CC",
    "tight": "Jacques\nChirac",
    "shortname": "chirac",
    }),
("Hervé Morin", {
    "color": "#00FFFF",
    "tight": "Hervé\nMorin",
    "shortname": "morin",
    }),
("Alain Madelin", {
    "color": "#00FFFF",
    "tight": "Alain\nMadelin",
    "shortname": "madelin",
    }),
("Charles Pasqua", {
    "color": "#003399",
    "tight": "Charles\nPasqua",
    "shortname": "pasqua",
    }),
("Jean Saint-Josse", {
    "color": "#0000FF",
    "tight": "Jean\nSaint-Josse",
    "shortname": "saintjosse",
    }),
("Dominique de Villepin", {
    "color": "#0066CC",
    "tight": "Dominique\nde Villepin",
    "shortname": "villepin",
    }),
("Nicolas Sarkozy", {
    "color": "#0066CC",
    "tight": "Nicolas\nSarkozy",
    "shortname": "sarkozy",
    }),
("François Fillon", {
    "color": "#0066CC",
    "tight": "François\nFillon",
    "shortname": "fillon",
    }),
("Frédéric Nihous", {
    "color": "#0000FF",
    "tight": "Frédéric\nNihous",
    "shortname": "nihous",
    }),
("Nicolas Dupont-Aignan", {
    "color": "#8040C0",
    "tight": "Nicolas\nDupont-Aignan",
    "shortname": "dupontaignan",
    }),
("Philippe de Villiers", {
    "color": "#8040C0",
    "tight": "Philippe\nde Villiers",
    "shortname": "villiers",
    }),
("François Asselineau", {
    "color": "#057c85",
    "tight": "François\nAsselineau",
    "shortname": "asselineau",
    }),
("Marine Le Pen", {
    "color": "#08105c",
    "tight": "Marine\nLe Pen",
    "shortname": "lepen",
    }),
("Jean-Marie Le Pen", {
    "color": "#08105c",
    "tight": "Jean-Marie\nLe Pen",
    "shortname": "lepen",
    }),
("Bruno Mégret", {
    "color": "#404040",
    "tight": "Bruno\nMégret",
    "shortname": "megret",
    }),
]

# Dictionnaries for access by name
candidates_colors = {name: metadata["color"] for name, metadata in candidates_metadata}
candidates_tight = {name: metadata["tight"] for name, metadata in candidates_metadata}
candidates_shortnames = {name: metadata["shortname"] for name, metadata in candidates_metadata}

# Sort orders
candidates_left_right_index = {name: index for (index, (name, metadata)) in enumerate(candidates_metadata)}
candidates_alphabetical_order = list(zip(*sorted(candidates_metadata, key=lambda x: x[1]["shortname"])))[0]
candidates_alphabetical_index = {c: candidates_alphabetical_order.index(c) for c in candidates_alphabetical_order}

# For each 2017 candidate, its 2012 "equivalent" candidate from the same political party
candidates_2012_equivalents = {
    "Yannick Jadot": "Eva Joly",
    "Benoît Hamon": "François Hollande",
    "François Fillon": "Nicolas Sarkozy",
}
