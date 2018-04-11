# -*- coding: utf-8 -*-

import sys
from optparse import OptionParser

def run(options):
	print(type(options), options)
	options = eval(str(options))
	print(type(options),options)
	print(type(options.items()),options.items())
	print(options['province'])
	for item in options.items():
		print(item)
	options = {x: y for x, y in options.items() if options[x]}
	print('---',options)


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-k", "--kws", dest="kws", help="key words")
    parser.add_option("-u", "--users", dest="users", help="the prefix of mail receiver")
    parser.add_option("-p", "--province", dest="province", help="user location province")
    parser.add_option("-c", "--city", dest="city", help="user location city")
    parser.add_option("-a", "--age", dest="age", help="should be A_40_plus,A_25_29,A_30_39,A_0_24'")
    parser.add_option("-g", "--gender", dest="gender", help="should be male, female")
    parser.add_option("-P", "--path", dest="path", help="the path of multi user id files")
    parser.add_option("-f", "--file", dest="file", help="the file location of user id")

    (options, args) = parser.parse_args()
    run(options)