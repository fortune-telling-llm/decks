#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re

OUT = Path('tarot/stellar-mosaic-tarot')

SUITS = {
    'Wands': {
        'element': 'Fire', 'palette': 'ember orange, solar gold, crimson, indigo, and black',
        'domain': 'will, creativity, desire, courage, enterprise, vitality, and visible action',
        'object': 'faceted living wands lit from within',
        'health': 'energy, exertion, motivation, recovery from burnout, and sustainable pacing',
        'fast': 'days to a few weeks, especially when action has already begun',
    },
    'Cups': {
        'element': 'Water', 'palette': 'moonlit blue, silver, sea-green, rose, violet, and black',
        'domain': 'emotion, intimacy, receptivity, memory, intuition, imagination, and relationship',
        'object': 'silver-gold cups holding luminous water',
        'health': 'emotional regulation, hydration, rest, grief, connection, and nervous-system softness',
        'fast': 'one lunar phase or a few weeks, with timing shaped by emotional readiness',
    },
    'Swords': {
        'element': 'Air', 'palette': 'white, ice blue, steel, storm gray, violet, and black',
        'domain': 'thought, truth, decisions, communication, conflict, boundaries, and perception',
        'object': 'crystalline swords edged with cold starlight',
        'health': 'mental load, sleep, anxiety, communication stress, and the need for clear professional support',
        'fast': 'quickly once a decision or message is made, often within days',
    },
    'Pentacles': {
        'element': 'Earth', 'palette': 'forest green, mineral gold, ochre, copper, midnight blue, and black',
        'domain': 'resources, work, money, the body, routines, craft, security, and long-term results',
        'object': 'golden pentacles set like coins, seeds, or architectural seals',
        'health': 'the body, nourishment, mobility, routines, material access, and consistent care',
        'fast': 'weeks to months; progress is measured through repeated practical steps',
    },
}

RANKS = ['Ace','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Page','Knight','Queen','King']
RANK_NUMBER = {'Ace':'1 / Ace','Two':'2','Three':'3','Four':'4','Five':'5','Six':'6','Seven':'7','Eight':'8','Nine':'9','Ten':'10','Page':'Page','Knight':'Knight','Queen':'Queen','King':'King'}
RANK_ROLE = {
    'Ace':'raw potential entering form','Two':'choice, polarity, and the first sustained relationship between forces',
    'Three':'development, expression, and results beginning to extend beyond the self','Four':'structure, consolidation, and the question of what stability protects',
    'Five':'disruption, friction, and the revelation of what cannot continue unchanged','Six':'adjustment, exchange, recognition, and movement toward a new balance',
    'Seven':'testing, discernment, strategy, and maintaining a position under pressure','Eight':'concentrated movement, repetition, skill, or the consequences of momentum',
    'Nine':'near-completion, self-possession, resilience, and the final private test','Ten':'culmination, consequence, inheritance, saturation, and transition into another cycle',
    'Page':'curiosity, messages, apprenticeship, and the element in an early exploratory form','Knight':'pursuit, motion, commitment to a direction, and the risks of over-identifying with momentum',
    'Queen':'inward mastery, embodied wisdom, receptivity with authority, and mature self-possession','King':'outward mastery, stewardship, leadership, accountability, and the ethical use of power',
}
