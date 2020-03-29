# -*- coding: UTF-8 -*-
import json
import subprocess
import sys

def parse_cut_time(cut_time):
	parse_each = cut_time.split(':')
	if len(parse_each) == 3:
		hour = parse_each[0].rjust(2,'0')
		minute = parse_each[1].rjust(2,'0')
		second = parse_each[2].rjust(2,'0')
		return '%s:%s:%s'%(hour, minute, second)
	elif len(parse_each) == 2:
		minute = parse_each[0]
		second = parse_each[1].rjust(2,'0')
		hour = str(int(minute)//60).rjust(2,'0')
		minute = str(int(minute)%60).rjust(2,'0')
		return '%s:%s:%s'%(hour, minute, second)
	else:
		print('cut time format error')
		print('current cut time:')
		print(cut_time)
		print('correct format: %H:%M:%S or %M:%S')
		sys.exit()

def cut_mp3(input_file, output_text, prefix=None):
	output = open('./%s'%output_text, 'r', encoding='utf8')
	output_infomations = json.loads(output.read())
	for output_infomation in output_infomations:
		cut_time_start = parse_cut_time(output_infomation['start_time'])
		cut_time_end = parse_cut_time(output_infomation['end_time'])
		output_file_name = output_infomation['name']
		if prefix:
			output_file_name = prefix+output_file_name
		command = 'ffmpeg -i %s -ss %s -to %s -c copy ./cut_output/%s.mp3'%(input_file, cut_time_start, cut_time_end, output_file_name)
		result = subprocess.run(command)
		if result.returncode == 0:
			print("success:",result)
		else:
			print("error:",result)

if __name__ == "__main__":
	input_file = input('Please give source file name\n')
	output_text = input('Please give output infomation text name\n')
	prefix_title = input('Please give prefix title\n')
	cut_mp3(input_file, output_text, prefix_title)
	print('process done')