# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import sklearn.utils as sk


class EmbedFactory(object):

    def __init__(self, vectorizer):
        self.vectorizer = vectorizer

    def _count_txt_file_lines(self, src):
        def count(f):
            return sum(1 for line in f)

        if isinstance(src, str):
            with open(src, 'r') as f:
                return count(f)

        return count(src)

    def _chunks(self, l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]

    def _create_batch_gen(self, src, batch_size):
        data_size = self._count_txt_file_lines(src)
        # 1 in range(1, _): ignore the header line
        indices = np.random.permutation(range(1, data_size))

        for chunk in self._chunks(indices, batch_size):
            res = pd.read_csv(src, skiprows=lambda n: n not in chunk,
                              header=None)
            yield sk.shuffle(res)

    def create_batch_gen(self, src, batch_size):

        for txt_df in self._create_batch_gen(src, batch_size):
            yield [{'id': r[0],
                   'label': r[1],
                    'text': self.vectorizer.vectorize(r[2])} for k, r
                   in txt_df.iterrows()]
