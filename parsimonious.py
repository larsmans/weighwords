#!/usr/bin/env python

from collections import defaultdict
import logging
import numpy as np


def corpus_model(documents):
    logging.info('Gathering corpus statistics')

    vocab = {}              # Vocabulary: maps terms to numeric indices
    cf = defaultdict(int)   # Corpus frequency

    for d in documents:
        for ln in d:
            tok, pos, freq, rest = ln.split()
            i = vocab.setdefault((tok, pos), len(vocab))
            cf[i] += int(freq)

    c_size = np.log2(sum(cf.itervalues()))

    p_corpus = np.zeros(len(vocab))   # log P(t|C)
    for i, f in cf.iteritems():
        p_corpus[i] = np.log2(f) - c_size

    return vocab, p_corpus


def document_model(d, vocab):
    '''Returns (tf, p_term)

    Initial p_term is 1/n_distinct for terms with non-zero tf,
    0 for terms with 0 tf.'''

    logging.info('Gathering term probabilities')

    tf = np.zeros(len(vocab))   # Term frequency
    p_term = np.empty(len(tf))
    p_term.fill(-np.inf)        # lg 0

    n_distinct = 0
    for ln in d:
        tok, pos, freq, rest = ln.split()
        i = vocab[(tok, pos)]
        if tf[i] == 0:
            p_term[i] = 0.      # lg 1
            n_distinct += 1
        tf[i] += float(freq)

    p_term -= np.log2(n_distinct)

    return tf, p_term


def EM(tf, p_corpus, p_term, w_unigrams, w_bigrams, n_iter):
    '''Expectation maximization'''

    logging.info('EM')

    w_ = np.log2(1 - w_unigrams - w_bigrams)
    w_unigrams, w_bigrams = np.log2((w_unigrams, w_bigrams))

    p_corpus += w_
    tf = np.log2(tf)

    for i in xrange(n_iter):
        # E-step
        p_term += w_unigrams
        E = tf + p_term - np.logaddexp2(p_corpus, p_term)

        # M-step
        p_term = E - np.logaddexp2.reduce(E)

    return p_term
