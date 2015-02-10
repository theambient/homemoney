#!/usr/bin/env python3

import os.path
import api
import parser
import analyzer

CURRENCY_MAP = {
	'RUR': 'руб'
}

def write_recs(recs, outdir):

	fd = None
	cnt = 0
	for idx, r in enumerate(recs):
		if idx % 50 == 0:
			if fd != None:
				fd.close()
			fd = open(os.path.join(outdir, 'stat{}.csv'.format(cnt)), 'w')
			fd.write('date;account;category;total;currency;description;transfer\n')
			cnt += 1

		fd.write('{};{};{};{};{};{};{}\n'.format(r.date, r.account, r.category, r.total, CURRENCY_MAP[r.currency], r.description, r.transfer))

	if fd != None:
		fd.close()

if __name__ == "__main__":
    # api.app.run(debug=True)

    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--outdir', dest='outdir', required=True, help='dir where csv files for export will be stored')
    parser.add_argument('-a', '--account-name', dest='account_name', required=True, help='account name as in homemoney')
    parser.add_argument('--hm-stat', dest='hm_stat',required=True, help='homemoney statement')
    parser.add_argument('--tb-stat', dest='tb_stat',required=True, help='telebank statement')
    parser.add_argument('-p', '--patterns', dest='tb_stat',required=True, help='patterns file')
    options = parser.parse_args()

    tbr = parser.read_tb(options.tb_stat)
    hmr = parser.read_hm(options.hm_stat, options.account_name)


    m = analyzer.Matcher(options.patterns)

    recs = analyzer.analyze(tbr, hmr, m, options.account_name, True)

    write_recs(recs, outpath)
