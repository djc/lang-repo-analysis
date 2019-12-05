# data files contain output straight from git:
# `git log --no-merges --pretty=format:'%ai %ae'`

from datetime import date

LANGS = 'go', 'rust', 'swift'

def main():

	data = {}
	for lang in LANGS:
		with open(lang + '.data') as f:
			ldata = data[lang] = {}
			for ln in f:
				d = date(*(int(i) for i in ln[:10].split('-')))
				a = ln.split(' ')[3].rstrip()
				ldata.setdefault(d, []).append(a)

	timelines = {}
	for lang, ldata in sorted(data.iteritems()):
		start = None
		commits, author_set, authors = {}, set(), {}
		for d, das in sorted(ldata.iteritems()):
			if start is None:
				start = d
			di = (d - start).days
			for a in das:
				commits[di] = commits.get(di, 0) + 1
				if a not in author_set:
					authors[di] = authors.get(di, 0) + 1
					author_set.add(a)
		timelines[lang] = commits, authors

	maxes = {k: max(v[0]) for (k, v) in timelines.items()}
	max_len = max(maxes.values())
	with open('output.csv', 'w') as f:
		labels = ['days']
		for lang in LANGS:
			labels.append('%s-commits' % lang)
			labels.append('%s-authors' % lang)
		print >> f, ','.join(labels)
		prev = {lang: [0, 0] for lang in LANGS}
		for i in range(max_len):
			ln = [i]
			for lang in LANGS:

				if i > maxes[lang]:
					ln.append('')
					ln.append('')
					continue

				ldata = timelines[lang]
				if i in ldata[0]:
					prev[lang][0] += ldata[0][i]
				if i in ldata[1]:
					prev[lang][1] += ldata[1][i]

				ln.append(prev[lang][0])
				ln.append(prev[lang][1])

			print >> f, ','.join(str(v) for v in ln)

if __name__ == '__main__':
    main()
