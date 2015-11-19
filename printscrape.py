from lxml import html
import requests

import re

filename = 'printer_ip.txt'

def scrape_dummy(model):
	dummy = {"name":"???", "order":"???", "percent":"???"}

	return {"yellow":dummy, "black":dummy, "magenta":dummy, "cyan":dummy}

def scrape_M451dn(model):
	yellow = {}
	black = {}
	magenta = {}
	cyan = {}

	toner_tree = tree.xpath("//td[contains(text(), 'Yellow Cartridge')]/text()")
	toner_perc_tree = tree.xpath("//td[contains(text(), 'Yellow')]/following-sibling::td/text()")

	yellow['name']    = re.sub(r'\s+', ' ', toner_tree[0]).strip()
	yellow['order']   = re.sub(r'\s+', ' ', toner_tree[1]).strip()
	yellow['percent'] = re.sub(r'\s+', ' ', toner_perc_tree[0]).strip()

	if not yellow['percent']:
		yellow['percent'] = "Low"

	toner_tree = tree.xpath("//td[contains(text(), 'Black Cartridge')]/text()")
	toner_perc_tree = tree.xpath("//td[contains(text(), 'Black')]/following-sibling::td/text()")

	black['name']    = re.sub(r'\s+', ' ', toner_tree[0]).strip()
	black['order']   = re.sub(r'\s+', ' ', toner_tree[1]).strip()
	black['percent'] = re.sub(r'\s+', ' ', toner_perc_tree[0]).strip()

	if not black['percent']:
		black['percent'] = "Low"

	toner_tree = tree.xpath("//td[contains(text(), 'Magenta Cartridge')]/text()")
	toner_perc_tree = tree.xpath("//td[contains(text(), 'Magenta')]/following-sibling::td/text()")

	magenta['name']    = re.sub(r'\s+', ' ', toner_tree[0]).strip()
	magenta['order']   = re.sub(r'\s+', ' ', toner_tree[1]).strip()
	magenta['percent'] = re.sub(r'\s+', ' ', toner_perc_tree[0]).strip()

	if not magenta['percent']:
		magenta['percent'] = "Low"

	toner_tree = tree.xpath("//td[contains(text(), 'Cyan')]/text()")
	toner_perc_tree = tree.xpath("//td[contains(text(), 'Cyan')]/following-sibling::td/text()")

	cyan['name']       = re.sub(r'\s+', ' ', toner_tree[0]).strip()
	cyan['order']      = re.sub(r'\s+', ' ', toner_tree[1]).strip()
	cyan['percent']    = re.sub(r'\s+', ' ', toner_perc_tree[0]).strip()

	if not cyan['percent']:
		cyan['percent'] = "Low"

	return {"yellow":yellow, "black":black, "magenta":magenta, "cyan":cyan}

with open(filename) as f:
	data = f.readlines()

for i in data:
	ip = i.rstrip('\n')

	url = 'http://' + ip + '/'

	try:
		r = requests.get(url, timeout = 1)
	except:
		continue

	tree = html.fromstring(r.content)

	title_list = tree.xpath('//title/text()')

	if not title_list:
		pass
	else:
		title = title_list[0]

		supply = {}

		if "Web Image Monitor" in title:
			model = "Generic Savin"

		if "Brother" in title:
			model = "Generic Brother"

		if "LaserJet" in title:
			if "M401dn" in title:
				model = "M401dn"

				supply = scrape_dummy(model)

			if "M401n" in title:
				model = "M401n"

				supply = scrape_dummy(model)

			if "M451dw" in title:
				model = "M451dw"

				supply = scrape_dummy(model)

			if "M451dn" in title:
				model = "M451dn"

				supply = scrape_M451dn(model)

			if "LaserJet 1320" in title:
				model = "1320"

				supply = scrape_dummy(model)

			if "LaserJet 4240" in title:
				model = "4240"

				supply = scrape_dummy(model)

			if "M375nw" in title:
				model = "M375nw"

				supply = scrape_dummy(model)

			if "M1536dnf" in title:
				model = "M1536dnf"

				supply = scrape_dummy(model)

			if "CP2025dn" in title:
				model = "CP2025dn"

				supply = scrape_dummy(model)

			if "M251nw" in title:
				model = "M251nw"

				supply = scrape_dummy(model)

			print("[" + ip + "] HP " + model)
			print(supply['black']['name'] + " " + supply['black']['order'] + " " + supply['black']['percent'])
			print(supply['yellow']['name'] + " " + supply['yellow']['order'] + " " + supply['yellow']['percent'])
			print(supply['magenta']['name'] + " " + supply['magenta']['order'] + " " + supply['magenta']['percent'])
			print(supply['cyan']['name'] + " " + supply['cyan']['order'] + " " + supply['cyan']['percent'])
			print()

		if "Hewlett Packard" in title:
			model = "Generic Hewlett Packard"
