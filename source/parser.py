
import csv
import re

class TbRecord(object):

    def __init__(self):
        self.date = ""
        self.amount = 0
        self.description = ""
        self.currency = ""

    def __str__(self):
        return '{} {} {} {}'.format(self.date, self.amount, self.currency, self.description)

    def __hash__(self):
        return hash('{}-{}-{}'.format(self.date, self.amount, self.currency))

    def __eq__(self, o):
        return self.date == o.date and self.amount == o.amount and self.currency == o.currency

def read_tb(path):

    fd = open(path, encoding='cp1251')

    reader = csv.reader(fd, delimiter=';')

    recs = []

    for i, row in enumerate(reader):
        if i < 12:
            continue

        if len(row) == 0:
            continue

        if row[8] != 'Исполнено':
            print('skipping operation (not processed):', ' '.join(row))
            continue

        r = TbRecord()

        r.date = row[1].split(' ')[0]
        r.amount = float(row[5])
        r.description = row[7]
        r.currency = row[6]

        if row[6] == row[4] and row[5] != row[3]:
            commission = float(row[5]) - float(row[3])
            print('commission detected of size', commission, row)
            r.amount = float(row[3])
            rc = TbRecord()

            rc.date = row[1].split(' ')[0]
            rc.amount = commission
            rc.description = 'commission for ' + row[7]
            rc.currency = row[6]
            recs.append(rc)

        recs.append(r)

    return recs

def read_hm(path, account_name, account_currency):

    fd = open(path)

    reader = csv.reader(fd, delimiter=';')

    recs = []

    currency_map = {
        'руб' : 'RUR'
    }

    # date;account;category;total;currency;description;transfer

    for i, row in enumerate(reader):
        if i < 1:
            continue

        if len(row) == 0:
            continue

        amount = float(row[3].replace(',', '.'))
        currency = currency_map.get(row[4], row[4])
        if row[1] != account_name:
            amount = -amount

            if currency != account_currency:
                r = re.compile(r'Конверсия из \w+ в \w+ по курсу ([\d\.]+)')
                m = r.match(row[5])
                assert m != None, "failed to match conversion operation regex (to determine exchange rate)"

                print('found exchange rate {} for {}'.format(m.group(1), ' '.join(row)))
                rate = float(m.group(1))

                old_amount = amount
                amount *= rate


                print('changed ammount from {} -> {} using exchange rate {}'.format(old_amount, amount, rate))

        if row[1] == account_name:
            assert currency == account_currency

        r = TbRecord()

        t = row[0].split('.')
        r.date = '{}-{}-{}'.format(t[2], t[1], t[0])
        r.amount = amount
        r.description = row[5]
        r.currency = account_currency
        recs.append(r)

    return recs
