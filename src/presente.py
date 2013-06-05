#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
from datetime import datetime
import dateutil.parser
import math
from lxml import etree as ET

import logging
logger = logging.getLogger('datacollector')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(levelname)s - %(name)s: %(message)s'))
logger.addHandler(handler)

class Lecture(object):
	def __init__(self):
		self.__segments_time_by_id = {}

	def add_segment_label(self, segment_id, time):
		self.__segments_time_by_id[segment_id] = time

	def get_segment_begin(self, segment_id):
		return self.__segments_time_by_id[segment_id]

class User(object):
	def __init__(self, user_id):
		self.__USERS_BY_ID[user_id] = self
		self.__id = user_id
		self.__sessions = []

	__USERS_BY_ID = {}

	@staticmethod
	def all_users():
		return User.__USERS_BY_ID.values()

	@staticmethod
	def get_user(user_id):
		if User.__USERS_BY_ID.has_key(user_id):
			return User.__USERS_BY_ID[user_id]
		else:
			return User(user_id)


	def all_sessions(self):
		return self.__sessions[:]

	@property
	def id(self):
		return self.__id

	def add_session(self, session):
		if session not in self.__sessions:
			self.__sessions.append(session)

	def get_sessions(self):
		return self.__sessions[:]

class NavegationSegment(object):
	def __init__(self, begin_fragment_point, node_id, interface_id=None):
		self.__node_id = node_id
		self.__interface_id = interface_id
		self.__begin_fragment = begin_fragment_point
		self.__end_fragment = None
		self.__pauses = []
		self.__pause_begin = None
		self.__paused_time = 0
		
	@property
	def current_pause_begin(self):
		return self.__pause_begin

	@property
	def module(self):
		return self.__node_id.split('_')[0]

	@property
	def node(self):
		return self.__node_id

	@property
	def interface(self):
		if self.__interface_id:
			return self.__interface_id
		else:
			return self.__node_id


	def get_pauses(self):
		return self.__pauses[:]

	@property
	def is_paused(self):
		return (self.__pause_begin != None)

	def pause(self, pause_begin):
		self.__pause_begin = pause_begin

	def resume(self, pause_end):
		if self.__pause_begin == None:
			return False

		self.__pauses.append( (self.__pause_begin, pause_end) )
		dd = pause_end - self.__pause_begin
		self.__paused_time += self.__to_seconds(dd)
		self.__pause_begin = None

	@property
	def paused_time(self):
		return self.__paused_time

	@property
	def length(self):
		return self.duration - self.paused_time

	@property
	def begin_segment(self):
		return self.__begin_fragment 

	@property
	def end_segment(self):
		return self.__end_fragment

	@end_segment.setter
	def end_segment(self, value):
		self.__end_fragment = value

	@property
	def duration(self):
		if self.__begin_fragment == None or self.__end_fragment == None:
			raise Exception("The fragment must have begin and end:\n" \
							+ str(self.__begin_fragment) + ',' \
							+ str(self.__end_fragment))

		dd = self.__end_fragment - self.__begin_fragment
		return self.__to_seconds(dd)


	def __to_seconds(self, dd):
		return dd.seconds + dd.microseconds / 1000000.0



class Session(object):
	static_counter = 1

	def get_pause_by_module(self, module_id):
		return self.__pause_by_modules[module_id]

	def __init__(self, url, ip, user, browser=None, lecture=None):
		self.url = url
		self.ip = ip
		self.user = user
		self.user.add_session(self)
		self.browser = browser
		self.__documents_id = []
		self.__documents = []
		self.__last_document = None
		self.__first_document = None
		self.lecture = lecture

		#(segment_id, duration)
		self.__segments_by_modules = {}

		self.__segments_video_by_modules = {}
		self.__current_main_video = 0
		self.__current_mini_video1 = 1
		self.__current_mini_video2 = 2
		self.__current_mini_video3 = 3

		self.__begin_video = None
		self.__begin_paused_video = None
		self.__video_paused_time = 0

		self.current_segment = None

		self.__interactions = []

		self.__milestones_navegation = []
		self.__poi_navegation_buttons = {}
		self.__poi_navegation_timeline = {}
		self.__module_navegation = []
		self.__presentation_control = []
		self.__video_focus = []
		self.__current_selected_poi = 0
		self.__current_main_video = 0
		

		self.__current_focus = None
		self._is_first_segment = True
		self.__closed = False

	def get_video_segments_of_module(self, module_id):
		return self.__segments_video_by_modules[module_id]

	@property 
	def milestones_navegation(self):
		return len(self.__milestones_navegation)

	@property 
	def poi_navegation_buttons(self):
		total = 0
		for vector in self.__poi_navegation_buttons.values():
			total += len(vector)

		return total

	@property 
	def poi_navegation_timeline(self):
		total = 0
		for vector in self.__poi_navegation_timeline.values():
			total += len(vector)

		return total

	@property 
	def module_navegation(self):
		return len(self.__module_navegation)

	@property 
	def presentation_control(self):
		return len(self.__presentation_control)

	@property 
	def video_focus(self):
		return len(self.__video_focus)

	@property
	def interactions(self):		
		return len(self.__interactions)


	def print_segments(self):
		print 'segments:', self.__segments_by_modules

	def get_segments_of_module(self, module_id):
		return self.__segments_by_modules[module_id]


	def add_segment(self, segment):		

		segments = None
		module_id = segment.module
		if self.__segments_by_modules.has_key(module_id):
			segments = self.__segments_by_modules[module_id]
		else:
			segments = []
			self.__segments_by_modules[module_id] = segments


		segment_id = self.current_segment_node_id
		if self.current_segment_interface_id != None:
			segment_id = self.current_segment_interface_id 

		segments.append( segment )


	def close(self):
		if self.current_segment == None:
			return

		end_time = self.__last_document.date
		if self.current_segment.is_paused:
			self.current_segment.resume(end_time)

		self.current_segment.end_segment = end_time
		self.add_segment(self.current_segment)

		self.current_segment = None


	def process_interactions(self, document):
		if document.type == 'input':
			if document.event == 'keyPress':

				#print self.__current_focus
				#raw_input('wait')

				if self.__current_focus == None:
					return

				#time_paused = self.current_segment_paused_time
				if self.current_segment == None:
					return
				
				time_paused = self.current_segment.paused_time
					
				if self.current_segment.is_paused:
					current_pause = document.date - self.current_segment.current_pause_begin
					current_pause = current_pause.seconds + current_pause.microseconds / 1000000.0

					time_paused += current_pause 

				#print document
				timeline = document.date - self.current_segment.begin_segment
				timeline = timeline.seconds + timeline.microseconds / 1000000.0
				timeline = timeline - time_paused

				#segment_id = self.current_segment.node

				#if self.current_segment.interface != None:
				segment_id = self.current_segment.interface 
					
				#print 'befero append'
				#print self.__interactions
				self.__interactions.append( (self.__current_focus, segment_id, timeline) )
				#print 'after append'
				#print self.__interactions
				#raw_input('pause')
				#print '\n\n'

				if self.__current_focus in ['iPause', 'iStart', 'iStop']:
					self.__presentation_control.append( (self.__current_focus, segment_id, timeline) )

				elif self.__current_focus in ['iMainVideo', 'iMiniVideo1', 'iMiniVideo2', 'iMiniVideo3', 'iResize']:
					self.__video_focus.append( (self.__current_focus, segment_id, timeline) )

				elif self.__current_focus.count('iMilestone_'):
					self.__milestones_navegation.append( (self.__current_focus, segment_id, timeline) )

				elif self.__current_focus.count('iPoint_'):
					poi_type = int(self.__current_focus.split('iPoint_')[1])

					vector = None
					if self.__poi_navegation_timeline.has_key(poi_type):
						vector = self.__poi_navegation_timeline[poi_type]
					else:
						vector = []
						self.__poi_navegation_timeline[poi_type] = vector

					vector.append( (self.__current_focus, segment_id, timeline) )

				elif self.__current_selected_poi == 0 and self.__current_focus in ['iNext', 'iPrevious']:

					self.__module_navegation.append( (self.__current_focus, segment_id, timeline) )

				elif self.__current_selected_poi != 0 and self.__current_focus in ['iNext', 'iPrevious', 'iBack']:

					poi_type = self.__current_selected_poi

					vector = None
					if self.__poi_navegation_buttons.has_key(poi_type):
						vector = self.__poi_navegation_buttons[poi_type]
					else:
						vector = []
						self.__poi_navegation_buttons[poi_type] = vector

					vector.append( (self.__current_focus, segment_id, timeline) )


				elif self.__current_focus == 'iModulo':
					self.__current_selected_poi = 0

				elif self.__current_focus.count('iPoi') and not self.__current_focus.count('Selected'):
					poi_type = int(self.__current_focus.split('iPoi')[1])
					self.__current_selected_poi = poi_type



			elif document.event == 'setFocus':
				self.__current_focus = document.focusIndex


	def process_segments(self, document):
		if document.type == 'node':
			if document.event == 'start':
				if self.is_forced_first and document.nodeId == "module1_video0" \
						and document.interfaceId == None:

					self.is_forced_first = False
					return

				self.is_forced_first = False


				if self.current_segment == None:
					self.current_segment =  NavegationSegment(document.date, 
															  document.nodeId, 
															  document.interfaceId)
				else:
					if self.current_segment.is_paused:
						self.current_segment.resume(document.date)

					self.current_segment.end_segment = document.date
					self.add_segment(self.current_segment)

					self.current_segment =  NavegationSegment(document.date, 
															  document.nodeId, 
															  document.interfaceId)

			elif document.event == 'pause':
				if self.current_segment:
					self.current_segment.pause(document.date)

			elif document.event == 'resume':
				if self.current_segment:
					self.current_segment.resume(document.date)


	def add_document(self, document):
		#if document.id in self.__documents_id:
		#	return False

		#print len(self.__documents), document
		#raw_input('pause')


		if self.__closed:
			return False

		if document.type == "presentation" and (document.event == "STOP" or document.event == "ABORT"):
			#print "presentation end"
			self.__closed = True

		if self.__last_document:
			dd = document.date - self.__last_document.date
			#if document.id == "5109a0cf70cbdcd045000085":
			#	print 'firt:', self.__first_document
			#	print 'last:', self.__last_document
			#	print dd
			#	print dd.seconds
			#	raw_input("Press Enter.")
			if dd.seconds > 600:
				#print 'Time out'
				#print dd, '\n', document, '\n', self.__last_document, 
				#print '\n\n'
				#rint document

				#raw_input("Returning.")
				self.__closed = True
				return False


		if self.__first_document == None:
			#print 'first setted'
			self.__first_document = document
			self.current_segment_node_id = 'module1_video0'
			self.current_segment_interface_id = None
			self.current_segment_begin = document.date
			#self.current_segment_paused_time = 0
			self.is_forced_first = True

		self.__documents_id.append(document.id)
		self.__documents.append(document)
		self.__last_document = document

		self.process_segments(document)
		self.process_interactions(document)
		#print 'Last Setted'

		return True

	@property
	def duration(self):
		if self.__last_document and self.__first_document:
			return (self.__last_document.date - self.__first_document.date).seconds
		else:
			return 0

	@property
	def begin_time(self):
		if self.__first_document:
			return self.__first_document.date
		else:
			return None

	@property
	def end_time(self):
		if self.__last_document:
			return self.__last_document.date
		else:
			return None



class DataDocument(object):
	def __init__(self):
		self.id = None
		self.url = None
		self.ip = None
		self.user = None
		self.browser = None

		self.date = None
		self.type = None
		self.event = None
		self.property = None
		self.value = None
		self.nodeId = None
		self.interfaceId = None
		self.keyCode = None
		self.focusIndex = None


	def __str__(self):
		json_map = {}
		document = self
		if document.id:
			json_map['id'] = document.id

		if document.url:
			json_map['url'] = document.url

		if document.ip:
			json_map['ip'] = document.ip

		if document.user:
			json_map['user'] = document.user

		if document.browser:
			json_map['browser'] = document.browser


		if document.date:
			json_map['date'] = document.date.isoformat()

		if document.type:
			json_map['type'] = document.type

		if document.event:
			json_map['event'] = document.event

		if document.property:
			json_map['property'] = document.property

		if document.value:
			json_map['value'] = document.value

		if document.nodeId:
			json_map['nodeId'] = document.nodeId

		if document.interfaceId:
			json_map['interfaceId'] = document.interfaceId

		if document.keyCode:
			json_map['keyCode'] = document.keyCode

		if document.focusIndex:
			json_map['focusIndex'] = document.focusIndex

		return json.dumps(json_map, indent=4, separators=(',', ': '))



	@staticmethod
	def decode_map(map):
		document = DataDocument()
		if map.has_key('_id'):
			document.id = map['_id']

		if map.has_key('url'):
			document.url = map['url']

		if map.has_key('user'):
			document.user = map['user']

		if map.has_key('browser'):
			document.browser = map['browser']

		if map.has_key('ip'):
			document.ip = map['ip']

		if map.has_key('date'):
			document.date = dateutil.parser.parse(map['date'])

		if map.has_key('type'):
			document.type = map['type']

		if map.has_key('event'):
			document.event = map['event']

		if map.has_key('property'):
			document.property = map['property']

		if map.has_key('value'):
			document.value = map['value']

		if map.has_key('nodeId'):
			document.nodeId = map['nodeId']

		if map.has_key('interfaceId'):
			document.interfaceId = map['interfaceId']

		if map.has_key('keyCode'):
			document.keyCode = map['keyCode']

		if map.has_key('focusIndex'):
			document.focusIndex = map['focusIndex']

		return document





class DataProvider(object):

	def __init__(self, filename):
		self.filename = filename
		self.__has_next = False
		self.__next = None

	def open(self):
		self.raw_file = open(self.filename, 'r')
		try:
			json_object = self.__read_json()
			if json_object == None:
				self.__has_next = False
				self.__next = None
			else:
				self.__has_next = True
				self.__next = DataDocument.decode_map(json_object)
		except:
			logger.exception('Error:')


	@property
	def has_next(self):
		return self.__has_next

	@property
	def next(self):
		value_to_return = None
		if self.__has_next:
			value_to_return = self.__next
			json_object = self.__read_json()
			if json_object == None:
				self.__has_next = False
				self.__next = None
			else:
				self.__has_next = True
				self.__next = DataDocument.decode_map(json_object)

		return value_to_return



	def __read_json(self):
		json_string = ""
		line = self.raw_file.readline()
		if line == "": #EOF
			return None

		elif line.count('{') == 0:
			raise Exception('The data must starts with a "{".')

		json_string += line
		line = self.raw_file.readline()
		while line.count('}') == 0:
			if line == "":
				raise Exception('Premature EOF reached')

			if line.count("ObjectId") > 0:
				object_id = line.split("ObjectId(")[1].split(")")[0]
				line = '\t"_id" : %s,\n' % object_id


			if line.count("ISODate") > 0:
				iso_date = line.split("ISODate(")[1].split(")")[0]
				line = '\t"date" : %s\n' % iso_date

			json_string += line
			line = self.raw_file.readline()


		json_string += line

		return json.loads(json_string)


