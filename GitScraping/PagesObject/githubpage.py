from selenium import webdriver


class PageObject(object):
	
	_driver = None
	_url = None
	_data_status = False
	def __init__(self,driver):
		self._driver = driver;
		
	def _navigate(self):
		self._driver.get(self._url)

	def _verify_data(self):
		if(self._data_status == False):
			self._navigate()
			self._get_data()

	def _get_data(self):
		raise Exception("You need implement this method!!")

	def tear_down(self):
		self._driver.quit()

class GithubMain(PageObject):
	
	_commits = None
	_commits_per_day_l = []
	def __init__(self,driver,url,account):
		super(GithubMain,self).__init__(driver)
		self._url = url + "/" + account
	
	def _get_data(self):
		self._get_year_commits()
		self._commits_per_day()
		self._data = True
		
	def _get_year_commits(self):
		self._commits = str(self._driver.find_elements_by_css_selector('h2.f4.text-normal.mb-2')[1].text)
	
	def _commits_per_day(self):
		commits_per_day = self._driver.find_elements_by_css_selector('rect.day')
		for i in range(len(commits_per_day)):
			self._commits_per_day_l.append(str(commits_per_day[i].get_attribute('data-count')))
	
	def return_data(self):
		self._verify_data()
		return [self._commits,self._commits_per_day_l]


class Repositories(GithubMain):

	_rep_name = []
	_rep_description = []
	_rep_main_languages = []
	_rep_colors = []
	_rep_href = []
	def __init__(self,driver,url,account):
		super(Repositories,self).__init__(driver,url,account)
		self._url = self._url + "?tab=repositories"

	def _get_data(self):
		results = self._driver.find_elements_by_css_selector('li.col-12.d-block.width-full.py-4.border-bottom.public.source')		
		for i in range(len(results)):
			self._rep_name.append(str(results[i].find_element_by_css_selector('a').text))
			self._rep_href.append(results[i].find_element_by_css_selector('a').get_attribute("href"))
			self._rep_description.append(str(results[i].find_element_by_css_selector('p.col-9.d-inline-block.text-gray.mb-2.pr-4').text))
			self._rep_main_languages.append(str(results[i].find_element_by_css_selector('span.mr-3').text))
			self._rep_colors.append(str(results[i].find_element_by_css_selector('span.repo-language-color.ml-0').value_of_css_property('background-color')))
		self._data = True

	def get_hrefs(self):
		return self._rep_href

	def return_data(self):
		self._verify_data()
		return [self._rep_name , self._rep_description , self._rep_main_languages, self._rep_colors]

class RepositoryPage(PageObject):
	
	_languages = []
	_number_of_commits = None
	_branches = None
	_releases = None
	_contribuitors = None
	_watches = None
	_stars = None
	_forks = None
	def __init__(self,driver,url):
		super(RepositoryPage,self).__init__(driver)
		self._url = url
	
	def _get_data(self):
		results  = self._driver.find_elements_by_css_selector('span.num.text-emphasized')
		self._number_of_commits = int(results[0].text)
		self._branches = int(results[1].text)
		self._releases = int(results[2].text)
		self._contribuitors = int(results[3].text)
		languages = self._driver.find_elements_by_css_selector('span.lang')
		for i in range(len(languages)):
			self._languages.append((str(languages[i].text) , str(self._driver.find_elements_by_css_selector('span.percent')[i].text)))

		social_counts = self._driver.find_elements_by_css_selector('a.social-count')
		self._watches = int(social_counts[0].text)
		self._stars = int(social_counts[1].text)
		self._forks = int(social_counts[2].text)
		self._data = True

	def get_graph_href(self):
		return self._url + "/graphs"
	
	def return_data(self):
		self._verify_data()
		return [self._languages,(self._number_of_commits,self._branches,self._releases, self._contribuitors), (self._watches , self._stars,self._forks)]
	
class GraphPage(PageObject):
	
	_infos = []
	_lines_of_code = None
	def __init__(self,driver,url):
		super(GraphPage,self).__init__(driver)
		self._url = url
	
	def _get_data(self):
		contrib = self._driver.find_elements_by_css_selector('a.aname')
		commits_per_contrib = self._driver.find_elements_by_css_selector('a.cmt')
		appends = self._driver.find_elements_by_css_selector('span.a')
		delete = self._driver.find_elements_by_css_selector('span.d')
		self._lines_of_code = 0
		for i in range(len(contrib)):
			self._infos.append(   
					     (
						 str(contrib[i].text),
						 str(commits_per_contrib[i].text),
						 int(
							str(appends[i].text)[0:len(appends[i].text)-3].replace(',','')
						    )
						 -
						 int(
							str(delete[i].text)[0:len(delete[i].text)-3].replace(',','')
						    )
					     )
					  )
			self._lines_of_code += self._infos[i][2]
		self._data = True
	
	def return_data(self):
		self._verify_data()
		return [self._infos,self._lines_of_code]


ff = webdriver.Firefox()
rep = Repositories(ff,"http://github.com","IonesioJunior")
rep.return_data()
rep_page = RepositoryPage(ff,rep.get_hrefs()[1])
gm = GraphPage(ff,rep_page.get_graph_href())
print gm.return_data()
gm.tear_down()
