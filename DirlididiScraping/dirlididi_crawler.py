#coding: utf-8
from selenium import webdriver
import time,os,urllib
from plotBars import *

class DirlididiPage(object):
	def __init__(self,driver):
		self.driver = driver
		self.submission = None
	def navigate(self,url):
		self.driver.get(url)

	def generate_log(self):
		buttons = self.driver.find_elements_by_class_name('btn')
		for i in range(len(buttons)):
			if( buttons[i].text == "Log"):
				buttons[i].click()
	def get_submission_data(self):
		head = self.driver.find_elements_by_css_selector("thead")
		body = self.driver.find_elements_by_css_selector("tbody")
		head_att = head[0].find_elements_by_css_selector("th")
		submit_table_title = []
		for i in range(len(head_att)):
			submit_table_title.append(head_att[i].text)
		submission = []
		for i in range(len(body)):
			body_att = body[i].find_elements_by_css_selector("td")
			body_text_list = []
			for j in range(len(body_att)):
				if( body_att[j].text == u'download' ):
					body_text_list.append(body_att[j].find_element_by_class_name('au-target').get_attribute('href'))
				else:
					body_text_list.append(body_att[j].text)
			submission.append(body_text_list)
		return submission
	
	def filter_data(self,submission_list,result,matrix_index):
		return [x for x in submission_list if x[matrix_index] == result ]
	
	def _process_date(self,date,begin,end):
		date_hours = int(date[0:2])
		date_mins = int(date[3:5])
		begin_hours = int(begin[0:2])
		begin_mins = int(begin[3:5])
		end_hours = int(end[0:2])
		end_mins = int(end[3:5])
		if(date_hours >= begin_hours and date_hours <= end_hours):
			if(date_hours < end_hours and date_mins >= begin_mins):
				return True
			else:
				if(date_mins <= end_mins):
					return True
				else:
					return False
		else:
			return False

	def filter_by_time(self,submission_list,date,begin,end):
		submission_day_list = [ x for x in submission_list if x[0][0:10] == date ]
		return [ x for x in submission_day_list if self._process_date(x[0][11:16],begin,end) ]

	def count_attrib(self,submission_list,right_index, left_index, element_index ):
		submission_set = set( tuple(x[right_index:left_index]) for x in submission_list )
		submission_dict = {}
		while( len(submission_set) != 0 ):
        		element = submission_set.pop()
        		if( element[0] in submission_dict ):
                		submission_dict[element[element_index]] += 1
        		else:
                		submission_dict[element[element_index]] = 1
		return submission_dict

	def finish(self):
		self.driver.quit()

ff = webdriver.Firefox()
dirlididi = DirlididiPage(ff)

def dirlididi_init():
	dirlididi.navigate("http://dirlididi.com/client/index.html")
	raw_input("Faça seu login na pagina do dirlididi (caso ja tenha feito apenas aperte enter) ...")

def get_users_results(questions,date,begin,end):
	dirlididi.navigate("http://dirlididi.com/client/index.html#/courses")
	time.sleep(3)
	dirlididi.generate_log()
	time.sleep(10)
	only_true_list =  dirlididi.filter_data(dirlididi.get_submission_data(),u'true',4)
	only_true_list = dirlididi.filter_by_time(only_true_list,date,begin,end)
	quest_list = []
	for question in questions:
		quest_list += dirlididi.filter_data(only_true_list,question,2)
	people_dict = dirlididi.count_attrib(quest_list,1,3,0)
	submission_file = open("submission_file.txt",'w')
	for key, value in people_dict.iteritems():
    		submission_file.write(str(key) + " " +  str(value)  + "\n")

def download_users_code(questions):
        dirlididi.navigate("http://dirlididi.com/client/index.html#/courses")
        time.sleep(3)
        dirlididi.generate_log()
        time.sleep(10)
        only_true_list =  dirlididi.filter_data(dirlididi.get_submission_data(),u'true',4)
        quest_list = [] 
	for question in questions:
                question_list = dirlididi.filter_data(only_true_list,question,2)
		if not os.path.exists(question):
			os.makedirs(question)
		for submission in question_list:
			dir_path = "./" + question + "/"
			try:
				urllib.urlretrieve(submission[3], filename= (dir_path + submission[1]))
			except:
				continue
def get_submission_chart(submission_list,date,hours):
	bin_list = []
	for i in range(len(hours)):
		bin_list.append( (hours[i][0] +"-"+ hours[i][1],len(dirlididi.filter_by_time(submission_list,date,hours[i][0],hours[i][1]))))
	plotBars(bin_list,"Horarios","Submissoes")

def get_problems_chart(submission_list,problems_list):
	bin_list = []
	for i in range(len(problems_list)):
		problem_list = dirlididi.filter_data(submission_list,problems_list[i],2)
		true_freq = len(dirlididi.filter_data(problem_list,u'true',4))
		false_freq = len(dirlididi.filter_data(problem_list,u'false',4))
		bin_list.append( (problems_list[i],true_freq,false_freq) )
	plotDualBars(bin_list,"Questions","Results")
		
if __name__ == "__main__":
	dirlididi_init()
        dirlididi.navigate("http://dirlididi.com/client/index.html#/courses")
        time.sleep(3)
        dirlididi.generate_log()
        time.sleep(10)
	submission_list = dirlididi.get_submission_data()
	get_problems_chart(submission_list,["LsEjqKerA","OwJdqYJF2","U61k02zZY"])
	dirlididi.finish()
