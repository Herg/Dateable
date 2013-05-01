
import re
from datetime import date

months = {
	'january':'01',
	'february':'02',
	'march':'03',
	'april':'04',
	'may':'05',
	'june':'06',
	'july':'07',
	'august':'08',
	'september':'09',
	'october':'10',
	'november':'11',
	'december':'12'
}
months_abbrev = {
	'jan\.?\s':'january ',
	'feb\.?\s':'february ',
	'febr\.?\s':'february ',
	'mar\.?\s':'march ',
	'apr\.?\s':'april ',
	'jun\.?\s':'june ',
	'jul\.?\s':'jul ',
	'aug\.?\s':'august ',
	'sep\.?\s':'september ',
	'sept\.?\s':'september ',
	'oct\.?\s':'october ',
	'nov\.?\s':'november ',
	'dec\.?\s':'december '
}

exact_match_dates_numerical = r'\d{1,4}[\-/\.\:]\d{1,2}[\-/\.\:]\d{1,4}'
exact_match_dates_string_pattern1 = r'month\s(\d{1,2})\w{0,2}\,?\s(\d{2,4})'
exact_match_dates_string_pattern2 = r'(\d{1,2})\w{0,2}\smonth\,?\s(\d{2,4})'


class dater(object):
	#########################################
	############# public methods ############
	#########################################

	def get_dates_string(self, query):
		found = []
		for mon in months_abbrev:
			query = re.sub(mon, months_abbrev[mon], query)
		for month in months:
			if month in query:
				reg1 = exact_match_dates_string_pattern1.replace('month',month)
				reg2 = exact_match_dates_string_pattern2.replace('month',month)
				m1 = re.search(reg1, query)
				m2 = re.search(reg2, query)
				if m1 is not None:
					marr1 = m1.groups()
					m1 = self._clean_month(months[month])
					y1 = self._clean_year(marr1[1])
					d1 = self._clean_day(marr1[0])
					if m1 is not None and y1 is not None and d1 is not None:
						found.append(y1 + '-' + m1 + '-' + d1)
				if m2 is not None:
					marr2 = m2.groups()
					m2 = self._clean_month(months[month])
					y2 = self._clean_year(marr2[1])
					d2 = self._clean_day(marr2[0])
					if m2 is not None and y2 is not None and d2 is not None:
						d = y2 + '-' + m2 + '-' + d2
						if d not in found:
							found.append(d)
		return found


	def get_dates_numerical(self, date_str):
		m = re.findall(exact_match_dates_numerical, date_str)
		if m is None:
			return []
		return self._handle_dates_numerical(m)


	#########################################
	############ private methods ############
	#########################################


	def _handle_dates_numerical(self, dates):
		dates_to_return = []
		for d in dates:
			darr = re.findall(r'\d+', d)
			y = self._get_year_from_numerical_date(darr)
			m = self._get_month_from_numerical_date(darr)
			d = self._get_day_from_numerical_date(darr)
			if y is None or m is None or d is None:
				# couldn't come to agreement on a date, skip
				continue
			date_str = y + '-' +  m + '-' + d
			dates_to_return.append(date_str)
		return dates_to_return


	def _get_year_from_numerical_date(self, darr):
		darr_copy = []
		year = None
		for num in darr:
			darr_copy.append(num) 
		darr_copy.pop(1)
		twos = []
		for num in darr_copy:
			if len(num) == 4:
				year = num
				break
			if len(num) == 2:
				if int(num) > 12:
					year = num
					break
				twos.append(num)
		if year is None and len(twos) == 1:
			# aka 1-3-09
			year = twos[0]
		# if we reach here the date is of the form 03-01-09
		# it is anyone's guess at this point. im going to 
		# return the last number
		if year is None and len(twos) == 2:
			year = twos[1]
		if year is None:
			return year
		return self._clean_year(year)

	def _clean_year(self, year):
		if len(year) == 2:
			if int(year) + 2000 > date.today().year:
				year = str(int(year) + 1900)
			else:
				year = str(int(year) + 2000)
		return year


	def _get_month_from_numerical_date(self, darr):
		to_pop = []
		darr_copy = []
		month = None
		for num in darr:
			darr_copy.append(num)
		for i in range(len(darr_copy)):
			if int(darr_copy[i]) > 12 or len(darr_copy[i]) > 2:
				to_pop.append(i)
		to_pop.reverse()
		for i in to_pop:
			darr_copy.pop(i)
		if len(darr_copy) == 0:
			return None
		return self._clean_month(darr_copy[0])


	def _clean_month(self, month):
		if len(month) == 1:
			month = '0' + month
		return month


	def _get_day_from_numerical_date(self, darr):
		to_pop = []
		darr_copy = []
		day = None
		for num in darr:
			darr_copy.append(num)
		for i in range(len(darr_copy)):
			if int(darr_copy[i]) > 31 or len(darr_copy[i]) > 2:
				to_pop.append(i)
		to_pop.reverse()
		for i in to_pop:
			darr_copy.pop(i)
		if len(darr_copy) > 1:
			day = darr_copy[1]
		elif len(darr_copy) == 0:
			return None
		if day is None:
			day = darr_copy[0]
		return self._clean_day(day)


	def _clean_day(self, day):
		if len(day) == 1:
			day = '0' + day
		return day



s = '21st october, 1987 january 15th, 2005 mar. 1 09 2013-01-01 2012.1.9'
d = dater()
print d.get_dates_string(s)
print d.get_dates_numerical(s)
