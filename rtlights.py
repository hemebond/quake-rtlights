#!/bin/env python3

import sys
import argparse
import re
import operator
import logging


logging.basicConfig(level=logging.DEBUG)
logging.warning('hello')



ops = {
	'<':  operator.lt,
	'<=': operator.le,
	'==': operator.eq,
	'!=': operator.ne,
	'>=': operator.ge,
	'>':  operator.gt,
}
mod_ops = {
	'*':  operator.mul,
	'=':  '=',
}

field_names = [
	'origin',
	'angles',
	'color',
	'radius',
	'corona',
	'style',
	'shadows',
	'cubemap',
	'coronasize',
	'ambient',
	'diffuse',
	'specular',
	'normalmode',
	'realtimemode',
]

#
# Filtering and number ranges
# --filter="style==32" --filter="style==33" --filter="style>=5" --filter="style<=10"
# --filter="cubemap==cubemaps/12"
#


#
# Modifying
# --radius="+64"
# --originz="+32"
#


#
# rtlights fields
#

# &origin[0], &origin[1], &origin[2], &radius, &color[0], &color[1], &color[2], &style, cubemapname, &corona, &angles[0], &angles[1], &angles[2], &coronasizescale, &ambientscale, &diffusescale, &specularscale, &flags);

# 338.000000 1512.000000 576.000000 137.500000 85.937500 90.234375 107.421875 0
#
# Origin       : 338.000000 1512.000000 676.000000
# Angles       : 0.000000 0.000000 0.000000
# Color        : 85.937500 90.234375 107.421875
# Radius       : 137.500000
# Corona       : 0.000000
# Style        : 0
# Shadows      : yes
# Cubemap      :
# CoronaSize   : 0.250000
# Ambient      : 0.000000
# Diffuse      : 1.000000
# Specular     : 1.000000
# NormalMode   : no
# RealTimeMode : yes

# 152.000000 1448.000000 648.000000 230.000000 206.640625 215.625000 229.101562 0 "" 0.000000 0.000000 230.000000 0.000000
# 152.000000 1448.000000 648.000000 230.000000 206.640625 215.625000 229.101562 0 "" 0.200000 12.000000 13.000000 14.000000 0.250000 0.100000 1.000000 1.000000 2
# 152.000000 1448.000000 648.000000 230.000000 206.640625 215.625000 229.101562 0 "" 0.200000 12.000000 13.000000 14.000000 0.250000 0.100000 1.000000 1.000000 1
# no shadows
# !152.000000 1448.000000 648.000000 230.000000 206.640625 215.625000 229.101562 0 "" 0.200000 12.000000 13.000000 14.000000 0.250000 0.100000 1.000000 1.000000 2
#
# Origin       : 152.000000 1448.000000 648.000000
# Angles       : 12.000000 13.000000 14.000000
# Color        : 206.640625 215.625000 229.101562
# Radius       : 230.000000
# Corona       : 0.200000
# Style        : 0
# Shadows      : yes
# Cubemap      :
# CoronaSize   : 0.250000
# Ambient      : 0.100000
# Diffuse      : 1.000000
# Specular     : 1.000000
# NormalMode   : no
# RealTimeMode : yes


RTLIGHT_MODE_NORMAL = 1
RTLIGHT_MODE_REALTIME = 2


class Point:
	def __init__(self, x, y, z):
		self.x = float(x)
		self.y = float(y)
		self.z = float(z)

	def __str__(self):
		return '{}, {}, {}'.format(self.x, self.y, self.z)


class Color:
	def __init__(self, r, g, b):
		self.r = float(r)
		self.g = float(g)
		self.b = float(b)

	def __str__(self):
		return '{}, {}, {}'.format(self.r, self.g, self.b)


class RTLight:
	pass


def pretty_format_rtlight(light):
	template = '''
Origin       : {:f} {:f} {:f}
Angles       : {:f} {:f} {:f}
Color        : {:f} {:f} {:f}
Radius       : {:f}
Corona       : {:f}
Style        : {}
Shadows      : {}
Cubemap      : {}
CoronaSize   : {:f}
Ambient      : {:f}
Diffuse      : {:f}
Specular     : {:f}
NormalMode   : {}
RealTimeMode : {}
	'''

	output = template.format(
		light.origin.x,
		light.origin.y,
		light.origin.z,
		light.angles.x,
		light.angles.y,
		light.angles.z,
		light.color.r,
		light.color.g,
		light.color.b,
		light.radius,
		light.corona,
		light.style,
		'yes' if light.shadows else 'no',
		light.cubemap,
		light.corona_size,
		light.ambient,
		light.diffuse,
		light.specular,
		'yes' if light.mode in [RTLIGHT_MODE_NORMAL, RTLIGHT_MODE_NORMAL + RTLIGHT_MODE_REALTIME] else 'no',
		'yes' if light.mode in [RTLIGHT_MODE_REALTIME, RTLIGHT_MODE_NORMAL + RTLIGHT_MODE_REALTIME] else 'no',
	)
	return output


def line_format_rtlight(light):
	template = '{}{:f} {:f} {:f} {:f} {:f} {:f} {:f} {} "{}" {:f} {:f} {:f} {:f} {:f} {:f} {:f} {:f} {}'
	output = template.format(
		'!' if not light.shadows else '',
		light.origin.x,
		light.origin.y,
		light.origin.z,
		light.radius,
		light.color.r,
		light.color.g,
		light.color.b,
		light.style,
		light.cubemap,
		light.corona,
		light.angles.x,
		light.angles.y,
		light.angles.z,
		light.corona_size,
		light.ambient,
		light.diffuse,
		light.specular,
		light.mode,
	)
	return output


def parse_rtlight(light_str):
	light = RTLight()

	# Is the line starts with an exclamation mark
	# shadows are disabled for this light
	if light_str[0] == '!':
		light.shadows = False
		light_str = light_str[1:]
	else:
		light.shadows = True

	f = light_str.split(' ')

	light.origin = Point(f[0], f[1], f[2])
	light.radius = float(f[3])
	light.color  = Color(f[4], f[5], f[6])
	light.style = int(f[7])

	try:
		light.cubemap = f[8].strip('"')
		light.corona = float(f[9])
		light.angles = Point(f[10], f[11], f[12])
	except IndexError:
		light.cubemap = ''
		light.corona = float(0)
		light.angles = Point(0, 0, 0)

	try:
		light.corona_size = float(f[13])
		light.ambient = float(f[14])
		light.diffuse = float(f[15])
		light.specular = float(f[16])
	except IndexError:
		light.corona_size = 0.25
		light.ambient = 0.0
		light.diffuse = 1.0
		light.specular = 1.0

	#                | realtimemode no | realtimemode yes
	# ---------------+-----------------+------------------
	# normalmode no  | 0               | 2
	# normalmode yes | 1               | 3

	try:
		light.mode = int(f[17])
	except IndexError:
		light.mode = RTLIGHT_MODE_REALTIME

	return light



def my_filter(list_item, attr_name, comparison, value):
	if value in field_names:
		value = getattr(list_item, value)

	try:
		value = float(value)
	except:
		pass

	try:
		if '.' in attr_name:
			field_main, field_sub = attr_name.split('.')
			parent_attr = getattr(list_item, field_main)
			attr = getattr(parent_attr, field_sub)
		else:
			attr = getattr(list_item, attr_name)

		operation = ops.get(comparison)

		return operation(attr, value)
	except AttributeError as e:
		print(e)
		return False



parser = argparse.ArgumentParser(description='Alter lights in an rtlights file.')
parser.add_argument('infile',  nargs='?', type=argparse.FileType('r'), default=sys.stdin)
# parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)

parser.add_argument('--filters', help='Only modify lights that match these tests', nargs='*')
parser.add_argument('--modify', help='Modify light values', nargs='*')
parser.add_argument('--only-matches', help='Only print out lights that matched all the filters', action='store_true')
parser.add_argument('--pretty', help='Print out the light data in a human-readable format', action='store_true')
parser.add_argument('--normalise-color', help='Normalise all colour values to be between 0 and 1', action='store_true')
parser.add_argument('--exclude', help='Do not return any lights that match the filters.', action='store_true')

args = parser.parse_args()
logging.debug(args)

rtlights = []

if args.infile:
	for i, line in enumerate(args.infile.read().splitlines()):
		logging.debug(line)
		light = parse_rtlight(line)
		light.idx = i
		rtlights.append(light)
	args.infile.close()

filtered_list = list(rtlights)

if args.filters:
	for fltr in args.filters:
		attr_name, comparison, value = re.split('([!<>=]+)', fltr)
		filtered_list = filter(lambda x: my_filter(x, attr_name, comparison, value), filtered_list)

if args.modify:
	for m in args.modify:
		logging.debug(m)

		mod_attr, mod_operation, mod_value = re.split('([\*=])', m)

		if mod_attr in ['radius', 'ambient', 'diffuse'] or mod_attr.startswith('color'):
			try:
				mod_value = float(mod_value)
			except:
				pass


		operation = mod_ops.get(mod_operation)

		for light in filtered_list:
			if '.' in mod_attr:
				attr_name, sub_attr_name = mod_attr.split('.')

				attr_value = getattr(light, attr_name)
				sub_attr_value = getattr(attr_value, sub_attr_name)

				if operation == '=':
					new_sub_attr_value = mod_value
				else:
					new_sub_attr_value = operation(sub_attr_value, mod_value)

				setattr(attr_value, sub_attr_name, new_sub_attr_value)
				setattr(light, attr_name, attr_value)
			else:
				attr_value = getattr(light, mod_attr)

				if isinstance(attr_value, (Point, Color)):
					for sub_attr_name, sub_attr_value in vars(attr_value).items():
						if operation == '=':
							new_sub_attr_value = mod_value
						else:
							new_sub_attr_value = operation(sub_attr_value, mod_value)
						setattr(attr_value, sub_attr_name, new_sub_attr_value)
					new_value = attr_value
				else:
					if operation == '=':
						new_value = mod_value
					else:
						new_value = operation(attr_value, mod_value)

				setattr(light, mod_attr, new_value)


if args.normalise_color:
	for light in filtered_list:
		maximum_value = max(light.color.r, light.color.g, light.color.b)

		light.color.r = light.color.r / maximum_value
		light.color.g = light.color.g / maximum_value
		light.color.b = light.color.b / maximum_value

		light.diffuse = maximum_value

if args.pretty:
	render_func = pretty_format_rtlight
else:
	render_func = line_format_rtlight


if args.only_matches:
	for light in filtered_list:
		print(render_func(light))
else:
	# Put the modified lights back into the original list
	for light in filtered_list:
		rtlights[light.idx] = light

	for light in rtlights:
		print(line_format_rtlight(light))
