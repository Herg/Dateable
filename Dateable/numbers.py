
import re

numbers = [
	['fourteen','14'],
	['sixteen','16'],
	['seventeen','17'],
	['eighteen','18'],
	['nineteen','19'],
	['sixty','6 0'],
	['seventy','7 0'],
	['eighty','8 0'],
	['ninety','9 0'],
	['one','1'],
	['two','2'],
	['three','3'],
	['four','4'],
	['five','5'],
	['six','6'],
	['seven','7'],
	['eight','8'],
	['nine','9'],
	['ten','10'],
	['eleven','11'],
	['twelve','12'],
	['thirteen','13'],
	['fifteen','15'],
	['twenty','2 0'],
	['thirty','3 0'],
	['forty','4 0'],
	['fifty','5 0'],
	['hundred','00'],
	['thousand','000'],
	['million','000000'],
	['billion','000000000'],
	['trillion','000000000000'],
	]


word_split_re = r'\b[a-zA-Z]+\b'

class numberer(object):

	# returns a number pulled from query
	def get_number(self, query):
		word_list = re.findall(word_split_re, query)
		num_list = []
		for word in word_list:
			for num in numbers:
				if word.find(num[0]) > -1:
					num_arr = num[1].split()
					num_list.extend(num_arr)
					word = word.replace(num[0],'')
		num_list = self._fix_zeros(num_list)
		total = 0
		for num in num_list:
			total = total + int(num)
		return total



	def _fix_zeros(self, num_list):
		# [position, zero value]
		zero_list = []
		for i in range(len(num_list)):
			if int(num_list[i]) == 0:
				zero_list.append([i,num_list[i]])
		for i in range(len(zero_list)):
			for n in range(i+1, len(zero_list)):
				if len(zero_list[n][1]) > len(zero_list[i][1]):
					zero_list[i][1] = zero_list[i][1] + zero_list[n][1]
					break
		for pos, zero in zero_list:
			num_list[pos] = zero
		for i in range(1, len(num_list)):
			if int(num_list[i]) == 0:
				num_list[i-1] = num_list[i-1] + num_list[i]
		return num_list

"""
s = 'thirty'
n = numberer()
total = n.get_numbers(s)
print str(total)
"""
