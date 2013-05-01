
import re
from datetime import date

exact_match_dates_numerical = r'\d{1,4}[\-/\.\:]\d{1,2}[\-/\.\:]\d{1,4}'


class dater(object):

	#########################################
	############# public methods ############
	#########################################

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
		print dates
		print dates_to_return


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
		print year
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
		month = darr_copy[0]
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
		if len(day) == 1:
			day = '0' + day
		return day



s = 'hello it is march 2nd 2013 2013-01-03 2012.1.2 03.21.13 3.2.8'
d = dater()
d.get_dates_numerical(s)
