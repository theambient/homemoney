
import collections
import re
import csv

from colors import *


class Record(object):

    def __init__(self):
        self.date = ''
        self.account = ''
        self.category = ''
        self.total = 0
        self.currency = ''
        self.description = ''
        self.transfer = ''


class RecordsPerDay(object):

    def __init__(self):

        self._set = set()

    def insert(self, r):
        self._set.add(r)

    def total_amount(self):

        return sum(map(lambda r: r.amount, self._set))

    def __str__(self):
        s = ''
        for x in self._set:
            s += '\t' + str(x) + '\n'

        return s

def analyze(tb, hm, matcher, account_name, strict=False):

    recs = []

    tbd = collections.defaultdict(RecordsPerDay)
    hmd = collections.defaultdict(RecordsPerDay)

    for r in tb:
        tbd[r.date].insert(r)
        hmd[r.date]

    for r in hm:
        hmd[r.date].insert(r)
        tbd[r.date]

    keys = set(tbd.keys()) | set(hmd.keys())
    keys = sorted(keys)

    for k in keys:

        hm = hmd[k]
        tb = tbd[k]

        if abs(hm.total_amount() - tb.total_amount()) > 0.01:
            print('sums for day {} do not match: {} <> {}'.format(k, hm.total_amount(), tb.total_amount()))

            # print('hm:', hm)
            # print('tb:', tb)

            ld = hm._set.difference(tb._set)
            rd = tb._set.difference(hm._set)

            if len(ld) > 0:
                print_red('found records in homemoney but not in telebank statement')
                for x in ld:
                    print_red('\t{}'.format(x))

            if len(rd) > 0:
                if strict:
                    print_dim('found records in telebank but not homemoney statement')
                for x in rd:
                    r = Record()
                    r.date = k
                    r.account = account_name
                    r.currency = x.currency
                    r.total = x.amount
                    r.description = x.description

                    kind, name = matcher.match(x.description)
                    if kind != '':
                        setattr(r, kind, name)
                    else:
                        print_yellow('\tfailed to match category for {}'.format(x.description))

                    recs.append(r)

                    if strict:
                        print_dim('\t{} -> {}:{}'.format(x, kind, name))
        else:
            print_green('sums for day {} matched'.format(k))

    return recs

class Matcher(object):

    def __init__(self, path):

        fd = open(path)


        self.patterns = []

        reader = csv.reader(fd, delimiter=" ")

        for row in reader:
            assert len(row) == 3, "invalid format of patterns file"
            assert row[0] in ['transfer', 'category']

            self.patterns.append(row)

    def match(self, s):

        if s.startswith('commission for '):
            return 'category', 'Комиссии'

        for p in self.patterns:
            if re.match(p[2], s):
                return p[0], p[1]


        return '', ''

