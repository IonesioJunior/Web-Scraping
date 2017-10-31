#coding: utf-8
from selenium import webdriver
import time
class Dirlididi(object):
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
dirlididi = Dirlididi(ff)
dirlididi.navigate("http://dirlididi.com/client/index.html")
raw_input("Faça seu login na pagina do dirlididi (caso ja tenha feita apenas aperte enter) ...")
dirlididi.navigate("http://dirlididi.com/client/index.html#/courses")
time.sleep(5)
dirlididi.generate_log()
time.sleep(10)
only_true_list =  dirlididi.filter_data(dirlididi.get_submission_data(),u'true',4)
quest_list = dirlididi.filter_data(only_true_list,"OwJdqYJF2",2) + dirlididi.filter_data(only_true_list,"LsEjqKerA",2) + dirlididi.filter_data(only_true_list,"U61k02zZY",2)

people_dict = dirlididi.count_attrib(quest_list,1,3,0)
submission_file = open("submission_file.txt",'w')
for key, value in people_dict.iteritems():
    submission_file.write(str(key) + " " +  str(value) )

dirlididi.finish()
