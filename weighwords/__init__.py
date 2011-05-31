#!/usr/bin/env python

# Copyright 2011 University of Amsterdam
# Author: Lars Buitinck

from collections import defaultdict
from heapq import nlargest
import logging
import numpy as np


logger = logging.getLogger(__name__)


class WeighWords(object):
    def __init__(self, documents, w, thresh=0):
        '''Build corpus (background) model.

        Parameters
        ----------
        documents : array of arrays of terms
        w : float
            Weight of document model (1 - weight of corpus model)
        thresh : int
            Don't include words that occur < thresh times

        Returns
        -------
        vocab : dict of term -> int
            Mapping of terms to numeric indices
        p_corpus : array of float
            Log prob of terms
        '''

        logger.info('Building corpus model')

        self.thresh = thresh
        self.w = w
        self.vocab = vocab = {} # Vocabulary: maps terms to numeric indices
        cf = defaultdict(int)   # Corpus frequency

        for d in documents:
            for tok in d:
                i = vocab.setdefault(tok, len(vocab))
                cf[i] += 1

        c_size = np.log(sum(cf.itervalues()))

        self.p_corpus = np.zeros(len(self.vocab))    # log P(t|C)
        for i, f in cf.iteritems():
            self.p_corpus[i] = np.log(f) - c_size


    def top(self, k, d, n_iter=None, w=None):
        '''Get the top k terms of a document d.

        Parameters
        ----------
        n_iter : int
            Number of iterations to run. Defaults to 50.
        w : float
            Weight of document model; overrides value given to __init__
        '''

        tf, p_term = self._document_model(d)
        p_term = self._EM(tf, p_term, w, n_iter)

        return nlargest(k, self.vocab.iterkeys(),
                        lambda t: p_term[self.vocab[t]])


    def _document_model(self, d):
        '''Build document model.

        Parameters
        ----------
        d : array of terms

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

        tf = np.zeros(len(self.vocab))   # Term frequency

        for tok in d:
            tf[self.vocab[tok]] += 1

        rare = (tf < self.thresh)
        tf -= rare * tf
        n_distinct = (tf > 0).sum()

        p_term = np.log(tf > 0) - np.log(n_distinct)

        return tf, p_term


    def _EM(self, tf, p_term, w, n_iter=None):
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

        if w is None:
            w = self.w
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