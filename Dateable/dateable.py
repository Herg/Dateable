
import re

exact_match_dates = r'\w+[\-/\s\.]\w+[\-\s\.]\w+'



class dater(object):
    
	def dates(self, date_str):
		m = re.findall(exact_match_dates, date_str)
		print m


s = 'hello it is march 2nd 2013 2013-01-03 2012.1.2'
d = dater()
d.dates(s)
