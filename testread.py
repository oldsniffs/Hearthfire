import os
import re
locations_text_file = open('.\\locations.txt')

print(locations_text_file.readlines())

location_regex = re.compile(r'<zone>.*</zone>')
