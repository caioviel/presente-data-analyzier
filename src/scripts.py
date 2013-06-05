#!/usr/bin/env python
# -*- coding: utf-8 -*-


from presente import *
from users import *

def time_str(sec):
	hours = int(sec / 3600)
	temp = sec % 3600
	minutes = int (temp / 60)
	seconds = temp % 60

	return '%dh %dm %ds' % (hours, minutes, seconds)

def init_lecture3():
	lecture = Lecture()
	lecture.add_segment_label('module1_video0', 0)
	lecture.add_segment_label('module1_video0_begin', 0)

	lecture.add_segment_label('module1_video0_milestone_1', 0.5)
	for i in range(1,50):
		lecture.add_segment_label('module1_video0_milestone_' + str(i), i*20)

	

	xml = '''
		<root>
        <area id="module1_video0_poi2_1" begin="0.5s"/>
        <area id="module1_video0_poi3_1" begin="0.5s"/>
        <area id="module1_video0_poi1_1" begin="4.16666666667s"/>
        <area id="module1_video0_poi1_2" begin="26.25s"/>
        <area id="module1_video0_poi1_3" begin="33.3333333333s"/>
        <area id="module1_video0_poi3_2" begin="47.0833333333s"/>
        <area id="module1_video0_poi1_4" begin="55.0s"/>
        <area id="module1_video0_poi3_3" begin="72.9166666667s"/>
        <area id="module1_video0_poi1_5" begin="77.0833333333s"/>
        <area id="module1_video0_poi3_4" begin="210.833333333s"/>
        <area id="module1_video0_poi2_2" begin="212.916666667s"/>
        <area id="module1_video0_poi3_5" begin="277.5s"/>
        <area id="module1_video0_poi3_6" begin="315.416666667s"/>
        <area id="module1_video0_poi3_7" begin="392.916666667s"/>
        <area id="module1_video0_poi3_8" begin="497.083333333s"/>
        <area id="module1_video0_poi2_3" begin="515.416666667s"/>
        <area id="module1_video0_poi3_9" begin="594.166666667s"/>
        <area id="module1_video0_poi3_10" begin="625.833333333s"/>
        <area id="module1_video0_poi3_11" begin="638.75s"/>
        <area id="module1_video0_poi1_6" begin="654.166666667s"/>
        <area id="module1_video0_poi1_7" begin="700.0s"/>
        <area id="module1_video0_poi1_8" begin="710.0s"/>
        <area id="module1_video0_poi3_12" begin="719.583333333s"/>
        <area id="module1_video0_poi1_9" begin="723.75s"/>
        <area id="module1_video0_poi1_10" begin="745.416666667s"/>
        <area id="module1_video0_poi3_13" begin="750.833333333s"/>
        <area id="module1_video0_poi3_14" begin="767.5s"/>
        <area id="module1_video0_poi1_11" begin="777.083333333s"/>
        <area id="module1_video0_poi1_12" begin="800.833333333s"/>
        <area id="module1_video0_poi1_13" begin="815.416666667s"/>
        <area id="module1_video0_poi1_14" begin="822.916666667s"/>
        <area id="module1_video0_poi1_15" begin="843.75s"/>
        <area id="module1_video0_poi3_15" begin="855.416666667s"/>
        <area id="module1_video0_poi1_16" begin="867.916666667s"/>
        <area id="module1_video0_poi3_16" begin="870.0s"/>
        <area id="module1_video0_poi1_17" begin="892.5s"/>
        <area id="module1_video0_poi3_17" begin="936.666666667s"/>
        <area id="module1_video0_poi2_4" begin="957.916666667s"/>
        <area id="module1_video0_poi2_5" begin="972.5s"/>
         <area id="module4_video0" begin="0s"/>
         <area id="module4_video0_begin" begin="0s"/>
        <area id="module4_video0_poi2_1" begin="0.5s"/>
        <area id="module4_video0_poi3_1" begin="0.5s"/>
        <area id="module4_video0_poi1_1" begin="33.3333333333s"/>
        <area id="module4_video0_poi1_2" begin="45.0s"/>
        <area id="module4_video0_poi3_2" begin="115.416666667s"/>
        <area id="module4_video0_poi3_3" begin="244.166666667s"/>
        <area id="module4_video0_poi3_4" begin="288.75s"/>
        <area id="module4_video0_poi3_5" begin="337.083333333s"/>
        <area id="module4_video0_poi1_3" begin="366.666666667s"/>
        <area id="module4_video0_milestone_1" begin="0.5s"/>
        <area id="module4_video0_milestone_2" begin="20s"/>
        <area id="module4_video0_milestone_3" begin="40s"/>
        <area id="module4_video0_milestone_4" begin="60s"/>
        <area id="module4_video0_milestone_5" begin="80s"/>
        <area id="module4_video0_milestone_6" begin="100s"/>
        <area id="module4_video0_milestone_7" begin="120s"/>
        <area id="module4_video0_milestone_8" begin="140s"/>
        <area id="module4_video0_milestone_9" begin="160s"/>
        <area id="module4_video0_milestone_10" begin="180s"/>
        <area id="module4_video0_milestone_11" begin="200s"/>
        <area id="module4_video0_milestone_12" begin="220s"/>
        <area id="module4_video0_milestone_13" begin="240s"/>
        <area id="module4_video0_milestone_14" begin="260s"/>
        <area id="module4_video0_milestone_15" begin="280s"/>
        <area id="module4_video0_milestone_16" begin="300s"/>
        <area id="module4_video0_milestone_17" begin="320s"/>
        <area id="module4_video0_milestone_18" begin="340s"/>
        <area id="module4_video0_milestone_19" begin="360s"/>
        </root>
    '''
	root = ET.fromstring(xml)
	childs = root.iterchildren()
	for elem in childs:
		area_id = elem.get('id')
		area_time = elem.get('begin')
		area_time = int(float(area_time[:len(area_time)-1]))
		lecture.add_segment_label(area_id, area_time)
	return lecture


lecture = init_lecture3()
sessions = []

def test():
	provider = DataProvider('raw_data.txt')
	provider.open()

	last_document = provider.next
	last_date = last_document.date
	while provider.has_next:
		document = provider.next
		dd = document.date - last_document.date
		if dd.seconds > 30:
			print dd, dd.seconds
			print last_document, '\n', document
			raw_input()

class Elem():
	def __init__(self):
		self.times = 0
		self.users = []

	def add_user(self, user):
		if user not in self.users:
			self.users.append(user)

	def inc_time(self):
		self.times += 1

	def count_users(self):
		return len(self.users)

def extract_video():
	all_segments = []
	for user in User.all_users():
		for session in user.all_sessions():
			session.close()
			if session.duration < 60:
				continue
			
			try:
				segments = session.get_video_segments_of_module('module1')
				#print segments
				#raw_input('wait')
				for seg in segments:
					all_segments.append( seg )
			except:
				pass
				logger.exception('Error:')


	seconds = [ [ 0 for x in range(4)] for y in range(1050) ]
	for segment in all_segments:
		segment_begin = lecture.get_segment_begin(segment[1])
		#print segment[0]
		#print segment_begin, segment[1]
		#print range(int(segment_begin), segment_begin + int(segment[1]))
		#raw_input('teste')
		for index in range(int(segment_begin), int(segment_begin + segment[2])):
			seconds[index][segment[0]] += 1

	index = 0
	for elem in seconds:
		print '%d\t%d\t%d\t%d\t%d' % (index, elem[0], elem[1], elem[2], elem[3])
		index = index +1
		#raw_input('wait')

def extract_segment_times():
	all_segments = []
	for user in User.all_users():
		for session in user.all_sessions():
			session.close()
			if session.duration < 60:
				continue
			
			try:
				#print 'duration:', session.duration
				#session.print_segments()
				segments = session.get_segments_of_module('module1')
				#raw_input('wait')
				for seg in segments:
					all_segments.append( (seg, user) )
			except:
				pass
			#logger.exception('Error:')


	seconds = [Elem() for x in range(1050)]
	for segment, user in all_segments:
		segment_begin = lecture.get_segment_begin(segment[0])
		#print segment[0]
		#print segment_begin, segment[1]
		#print range(int(segment_begin), segment_begin + int(segment[1]))
		#raw_input('teste')
		for index in range(int(segment_begin), int(segment_begin + segment[1])):
			seconds[index].inc_time()
			seconds[index].add_user(user)

	index = 0
	for elem in seconds:
		print '%d\t%d\t%d' % (index, elem.times, elem.count_users())
		index = index +1
		#raw_input('wait')

def extract_one_student_statistics(user, module_id):
	all_segments = []
	sessions = user.all_sessions()
	for session in user.all_sessions():
		session.close()
		#session.print_segments()
		#raw_input('waiting...')
		#if session.duration < 60:
		#	continue
			
		try:
			segments = session.get_segments_of_module(module_id)
			for seg in segments:
				all_segments.append( seg )
		except:
			pass
			#logger.exception('Error:')



	print 'Segments:\n', '-'*50 
	counter = 0
	seconds = [0 for x in range(2000)]
	for segment in all_segments:
		segment_begin = lecture.get_segment_begin(segment.interface)
		begin_point = int(segment_begin)
		paused_time = int(segment.paused_time)
		duration = None
		end_point = None

		try:
			end_point = int(segment_begin + segment.length)
			duration = int(segment.duration)
		except:
			#print 'incomplete segment found'
			continue
		print begin_point, end_point, 
		print paused_time, duration, '\n\n'
		#raw_input('wait...')

		#for index in range(begin_point, end_point):
		#	seconds[counter] = index
		#	counter += 1

	#index = 0
	#for elem in seconds:
	#	print '%d\t%d' % (index, elem)
	#	index = index +1
	#	#raw_input('wait')

def extract_interaction_statistics(users = None):
	poi_timeline = 0
	poi_buttons = 0
	module = 0
	video = 0
	milestones = 0
	presentation = 0

	for session in sessions:
		if users is not None:
			if session.user.id not in users:
				continue
		duration = session.duration
		interactions = session.interactions
		if duration < 240:
			continue

		poi_timeline +=  session.poi_navegation_timeline
		poi_buttons += session.poi_navegation_buttons
		module += session.module_navegation
		video += session.video_focus
		milestones += session.milestones_navegation
		presentation += session.presentation_control

	print u'Navegação por POI (botões):', poi_buttons
	print u'Navegação por POI (timeline):', poi_timeline
	print u'Navegação por milestones:', milestones
	print u'Seleção de Vídeo Principal:', video
	print u'Navegação por Módulos:', module
	print u'Controle da Apresentação:', presentation


def extract_students_statistics(users = None):

	duration_sum = 0
	interaction_sum = 0
	sessions_number = 0
	max_value = 0
	min_value = 99999999999999
	all_values = []

	for session in sessions:
		if users is not None:
			#print users.id
			#print session.user
			#raw_input('pause')
			if session.user.id not in users:
				continue
		
		duration = session.duration
		interactions = session.interactions
		if duration < 240:
			continue

		if duration > max_value:
			max_value = duration

		if duration < min_value:
			min_value = duration

		all_values.append( (duration, interactions) )
		duration_sum += duration
		interaction_sum += interactions
		sessions_number += 1


	duration_average = duration_sum/float(sessions_number)
	interactions_average = interaction_sum/float(sessions_number)

	standard_deviation_duration = 0
	standard_deviation_interactions = 0
	for duration, interactoins in all_values:
		temp1 = duration - duration_average
		temp2 = interactoins - interactions_average
		#print value
		standard_deviation_duration += temp1*temp1
		standard_deviation_interactions += temp2*temp2

	standard_deviation_duration = math.sqrt(standard_deviation_duration/(sessions_number-1))
	standard_deviation_interactions = math.sqrt(standard_deviation_interactions/(sessions_number-1))


	
	print u'Número de Sessões Consideradas:', sessions_number
	print u'Duração Média:', duration_average, '+/-', standard_deviation_duration
	print u'Duração Máxima:', max_value
	print u'Duração Mínima:', min_value
	all_values.sort()
	#print all_values
	print u'Duração Mediana:', all_values[len(all_values)/2]
	print u'Interações Média:', interactions_average, '+/-', standard_deviation_interactions
	#print duration_sum, interaction_sum
	print u'Interações / segundo:', duration_sum/float(interaction_sum)

	print '-'*50
	users_time = []
	for user in User.all_users():
		if users is not None:
			if user.id not in users:
				continue
			
		timespent = 0
		interactions = 0
		for session in user.all_sessions():
			timespent = timespent + session.duration
			interactions = interactions + session.interactions

		if timespent > 240:
			users_time.append( (user.id, timespent, interactions) )
	
	import operator
	users_time.sort(key=operator.itemgetter(1))

	for user, time, interactions in users_time:
		print '%s\t%d\t%d' % (user, time, interactions)





def main():
	provider = DataProvider('../data/raw_data.txt')
	provider.open()
	current_sessions = {}

	while provider.has_next:
		document = provider.next

		#if document.type == 'node' and document.event =='start':
		#	print '-'*40, '\n'
		#	print document
		#	raw_input("Press Enter to continue...")
		

		if document.type == 'presentation' and document.event == 'START':
			user = User.get_user(document.user)
			session = Session(document.url, document.ip, user)
			sessions.append(session)
			current_sessions[(document.url, document.ip, user)] = session
			session.add_document(document)

		else:
			user = User.get_user(document.user)
			session = None
			try:
				session = current_sessions[(document.url, document.ip, user)]
			except:
				continue
			session.add_document(document)

	#extract_segment_times()
	#extract_students_statistics()
	#extract_students_statistics(presential_students.keys())
	#extract_students_statistics(ead_students.keys())
	#extract_video()
	#extract_one_student_statistics(User.get_user('414220'), 'module1')
	#extract_one_student_statistics(User.get_user('414441'), 'module4')
	#extract_one_student_statistics(User.get_user('312568'), 'module1')
	extract_interaction_statistics()
	print '\n\n'
	extract_interaction_statistics(presential_students.keys())
	print '\n\n'
	extract_interaction_statistics(ead_students.keys())
	print '\n\n'

	user = User.get_user('414220')


def test():
	vector = [(16, 14), (3, 9), (4, 30), (6, 18), (5, 15), (8, 34), (10,43), (5,14), (7,05), (3,47), (3,51), (3,51)]
	time = 0
	for m, s in vector:
		time += m*60 + s

	print u'Duração da Apresentação:', time,  time_str(time)

if __name__ == "__main__":
	#test()
	main()
	#init_lecture3()