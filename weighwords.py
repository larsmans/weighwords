#!/usr/bin/env python

# Copyright 2011 University of Amsterdam
# Author: Lars Buitinck

from collections import defaultdict
from heapq import nlargest
import logging
import numpy as np


logger = logging.getLogger(__name__)


class WeighWords(object):
    def __init__(self, documents, w):
        '''Build corpus (background) model.

        Parameters
        ----------
        documents : array of arrays of terms
        w : float
            Weight of document model (1 - weight of corpus model)

        Returns
        -------
        vocab : dict of term -> int
            Mapping of terms to numeric indices
        p_corpus : array of float
            Log prob of terms
        '''

        logger.info('Building corpus model')

        self.vocab = {}              # Vocabulary: maps terms to numeric indices
        cf = defaultdict(int)   # Corpus frequency

        for d in documents:
            for tok in d:
                i = vocab.setdefault(tok, len(vocab))
                cf[i] += 1

        c_size = np.log(sum(cf.itervalues()))

        self.p_corpus = np.zeros(len(vocab))    # log P(t|C)
        for i, f in cf.iteritems():
            p_corpus[i] = np.log(f) - c_size


    def top(self, k, d, n_iter=None):
        '''Get the top k terms of a document d.

        Parameters
        ----------
        n_iter : int
            Number of iterations to run. Defaults to 50.
        '''

        tf, p_term = self.document_model(d)
        p_term = self.EM(tf, p_term, n_iter)

        return nlargest(k, self.vocab.iterkeys(), lambda t: p_term[t])


    def _document_model(self, d):
        '''Build document model.

        Parameters
        ----------
        d : array of terms
        vocab : see @corpus_model

        Returns
        -------
        tf : array of int
            Term frequencies
        p_term : array of float
            Term log probabilities

        Initial p_term is 1/n_distinct for terms with non-zero tf,
        0 for terms with 0 tf.
        '''

        logger.info('Gathering term probabilities')

        tf = np.zeros(len(vocab))   # Term frequency
        p_term = np.empty(tf.shape[0])
        p_term.fill(-np.inf)        # lg 0

        n_distinct = 0
        for tok in d:
            i = self.vocab[tok]
            if tf[i] == 0:
                p_term[i] = 0.      # lg 1
                n_distinct += 1
            tf[i] += 1.

        p_term -= np.log(n_distinct)

        return tf, p_term


    def _EM(self, tf, p_term, n_iter=None):
        '''Expectation maximization.

        Parameters
        ----------
        tf : array of float
            Term frequencies, as returned by document_model
        p_term : array of float
            Term probabilities, as returned by document_model
        n_iter : int
            Number of iterations to run. Defaults to 50.

        Returns
        -------
        p_term : array of float
            A posteriori term probabilities.
        '''

        logger.info('EM')

        if n_iter is None:
            n_iter = 50

        w_ = np.log(1 - w)
        w = np.log(w)

        p_corpus = self.p_corpus + w_
        tf = np.log(tf)

        E = np.empty(tf.shape[0])

        p_term = np.array(p_term)
        for i in xrange(n_iter):
            # E-step
            p_term += w
            E = tf + p_term - np.logaddexp(p_corpus, p_term)

            # M-step
            p_term = E - np.logaddexp.reduce(E)

        return p_term
