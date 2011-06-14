#!/usr/bin/env python

# Find terms that distinguish various novels by Charles Dickens.
# Note: if the w parameter is set wisely, no stop list is needed.

from weighwords import ParsimoniousLM
import gzip
import logging
import numpy as np
import re

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

top_k = 20  # How many terms per book to retrieve

books = [
    ('Oliver Twist',       '730'),
    ('David Copperfield',  '766'),
    ('Great Expectations', '1400'),
]

startbook = """*** START OF THIS PROJECT GUTENBERG EBOOK """


def read_book(title, num):
    """Returns generator over words in book num"""

    logger.info("Fetching terms from %s" % title)
    path = "%s.txt.utf8.gz" % num
    in_book = False
    for ln in gzip.open(path):
        if in_book:
            for w in re.sub(r"[.,:;!?\"']", " ", ln).lower().split():
                yield w
        elif ln.startswith(startbook):
            in_book = True


book_contents = [(title, list(read_book(title, num))) for title, num in books]

model = ParsimoniousLM([terms for title, terms in book_contents], w=.01)

for title, terms in book_contents:
    print("Top %d words in %s:" % (top_k, title))
    for term, p in model.top(top_k, terms):
        print("    %s %.4f" % (term, np.exp(p)))
    print("")
