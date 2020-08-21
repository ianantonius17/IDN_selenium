from selenium import webdriver
from time import sleep
from excelModifier import excel
import copy
import inputText
#from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

class idnTimes():

    row = 1
    def __init__(self):
        self.driver = webdriver.Chrome()
        sleep(1)
        self.driver.get('https://www.idntimes.com')
        self.excel = excel('report.xls',0)
        sleep(5)

    #quit
    def quit(self):
        self.driver.quit()

    #scroll Down
    def scrollDown(self):
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    
    #back
    def back(self):
        self.driver.back()
    
    #forward
    def forward(self):
        self.driver.forward()

    #access link and wrtie status report
    def access(self,link, section):
        self.excel.addValue(self.row,0,section)
        try:
            link.click()
            self.excel.addValue(self.row,1,'sucess')
        except:
            self.excel.addValue(self.row,1,'fail')
        
        self.excel.save()
        self.row+= 1
   
   #auto scroll down current page up to 7 times
    def autoScrollDown(self):
        limit = 7
        cur = 0

        curHeight = self.driver.execute_script('return document.body.scrollHeight')
        finalHeight = curHeight +1

        while curHeight < finalHeight and cur < limit :
            self.scrollDown()
            sleep(1)
            cur += 1
            curHeight = copy.deepcopy(finalHeight)
            finalHeight = self.driver.execute_script('return document.body.scrollHeight')
        
        sleep(1)
        scrollCount = str(cur)
        if finalHeight > curHeight:
             scrollCount = scrollCount +'+'
        self.excel.addValue(self.row,2,scrollCount)

    #get content title list
    def getContentTitles(self,ul_xpath):
        ul = self.driver.find_element_by_xpath(ul_xpath)
        li_list = ul.find_elements_by_tag_name('li')
        contentTitle = ''
        
        for li in li_list:
            aTag = li.find_element_by_tag_name('a')
            title = aTag.get_attribute('title')
            contentTitle = contentTitle + title +' ,'

        finalResult = contentTitle.rstrip(',')
        return finalResult

    #check page is valid and write report    
    def checkPage(self):
        head = self.driver.find_element_by_tag_name('head')
        title = head.find_element_by_tag_name('title')
        titleMessage = str(title.get_attribute('innerHTML'))

        body = self.driver.find_element_by_tag_name('body')
        div = body.find_element_by_tag_name('div')
        divId = div.get_attribute('id')

        if titleMessage == 'Error 404' or titleMessage == 'Failed to open page' or 'error' in divId:
            self.excel.addValue(self.row-1,1,'fail')
            if 'error' in divId:
                self.excel.addValue(self.row-1,3,'error')
            else:
                self.excel.addValue(self.row-1,3,titleMessage)

    #access all links in the header
    def headersLink(self):
        headers = self.driver.find_element_by_xpath('//*[@id="header"]/div[1]/div/div/div[2]/nav/ul')
        li_list = headers.text.split('\n')
        idx = 1
        for li in li_list :
            if(idx > len(li_list)):
                break
            sleep(3)
            #test without login , Community link needs to sign in so it will be skipped
            if idx == 11:
                idx += 1
                continue
            
            link = self.driver.find_element_by_xpath('//*[@id="header"]/div[1]/div/div/div[2]/nav/ul/li['+str(idx)+']/a')
            section = li+' Link'
            self.access(link,section)

            if idx != 12 and idx != 13:
                sleep(2)
                self.autoScrollDown()
            
            print(str(idx) +' '+ section)
            idx+= 1

    #access links in the regional   
    def regionalLink(self):
        print('regional link')
        regional = self.driver.find_element_by_xpath('//*[@id="header"]/div[1]/div/div/div[2]/nav/ul/li[12]/a')
        hover = ActionChains(self.driver).move_to_element(regional)
        hover.perform()
        
        options = self.driver.find_element_by_xpath('//*[@id="header"]/div[1]/div/div/div[2]/nav/ul/li[12]/div/div/ul')
        li_list = options.text.split('\n')
        idx = 1

        for li in li_list:
            sleep(3)
            regional = self.driver.find_element_by_xpath('//*[@id="header"]/div[1]/div/div/div[2]/nav/ul/li[12]/a')
            hover = ActionChains(self.driver).move_to_element(regional)
            hover.perform()
            
            sleep(1)
            link = self.driver.find_element_by_xpath('//*[@id="header"]/div[1]/div/div/div[2]/nav/ul/li[12]/div/div/ul/li['+str(idx)+']/a')
            section = li + ' Link'
            self.access(link,section)
            
            #check page
            self.checkPage()

            sleep(2)
            self.autoScrollDown()
            
            sleep(1)
            self.back()
            print(str(idx) + ' '+ section)
            idx +=1

    #access all links in Kategori under Lainnya     
    def kategoriLainnyaLink(self):
        print('kategori lainnya link')
        lainnya = self.driver.find_element_by_xpath('//*[@id="header"]/div[1]/div/div/div[2]/nav/ul/li[13]/a')
        hover = ActionChains(self.driver).move_to_element(lainnya)
        hover.perform()

        options = self.driver.find_element_by_xpath('//*[@id="header"]/div[1]/div/div/div[2]/nav/ul/li[13]/div/div[1]/div[1]/ul')
        li_list = options.text.split('\n')
        idx = 1

        for li in li_list:
            sleep(3)
            lainnya = self.driver.find_element_by_xpath('//*[@id="header"]/div[1]/div/div/div[2]/nav/ul/li[13]/a')
            hover = ActionChains(self.driver).move_to_element(lainnya)
            hover.perform()
            
            sleep(1)
            link = self.driver.find_element_by_xpath('//*[@id="header"]/div[1]/div/div/div[2]/nav/ul/li[13]/div/div[1]/div[1]/ul/li['+str(idx)+']/a')
            section = li + ' Link'
            self.access(link,section)
            
            #check page
            self.checkPage()

            sleep(2)
            self.autoScrollDown()
            
            sleep(1)
            self.back()
            print(str(idx) + ' '+ section)
            idx +=1
    
    #access all links in Event under Lainnya
    def eventLainnyaLink(self):
        print('event lainnya link')
        lainnya = self.driver.find_element_by_xpath('//*[@id="header"]/div[1]/div/div/div[2]/nav/ul/li[13]/a')
        hover = ActionChains(self.driver).move_to_element(lainnya)
        hover.perform()

        options = self.driver.find_element_by_xpath('//*[@id="header"]/div[1]/div/div/div[2]/nav/ul/li[13]/div/div[1]/div[2]/ul')
        li_list = options.text.split('\n')
        idx = 1

        for li in li_list:
            sleep(3)
            lainnya = self.driver.find_element_by_xpath('//*[@id="header"]/div[1]/div/div/div[2]/nav/ul/li[13]/a')
            hover = ActionChains(self.driver).move_to_element(lainnya)
            hover.perform()
            
            sleep(1)
            link = self.driver.find_element_by_xpath('//*[@id="header"]/div[1]/div/div/div[2]/nav/ul/li[13]/div/div[1]/div[2]/ul/li['+str(idx)+']/a')
            section = li + ' Link'
            self.access(link,section)
            
            #check page
            self.checkPage()

            sleep(2)
            self.autoScrollDown()
            
            sleep(1)
            self.back()
            print(str(idx) + ' '+ section)
            idx +=1

    #access all links in channel under Lainnya
    def channelLainnyaLink(self):
        sleep(2)
        print('channel lainnya link')
        lainnya = self.driver.find_element_by_xpath('//*[@id="header"]/div[1]/div/div/div[2]/nav/ul/li[13]/a')
        hover = ActionChains(self.driver).move_to_element(lainnya)
        hover.perform()

        options = self.driver.find_element_by_xpath('//*[@id="header"]/div[1]/div/div/div[2]/nav/ul/li[13]/div/div[1]/div[3]/ul')
        li_list = options.find_elements_by_tag_name('li')
        idx = 1

        for li in li_list:
            sleep(3)
            lainnya = self.driver.find_element_by_xpath('//*[@id="header"]/div[1]/div/div/div[2]/nav/ul/li[13]/a')
            hover = ActionChains(self.driver).move_to_element(lainnya)
            hover.perform()

            http = li.find_element_by_tag_name('a')
            href = http.get_attribute('href')
            sleep(1)
            link = self.driver.find_element_by_xpath('//*[@id="header"]/div[1]/div/div/div[2]/nav/ul/li[13]/div/div[1]/div[3]/ul/li['+str(idx)+']/a')
            section = href + ' Link'
            self.access(link,section)
            sleep(3)
            
            print(str(idx) + ' '+ section)
            idx +=1

            before = self.driver.window_handles[0]
            after = self.driver.window_handles[1]
            self.driver.switch_to.window(after)

            #check page
            self.checkPage()
            

            self.driver.close()
            self.driver.switch_to.window(before)
            
    #perform search with existing keywords
    def search(self):
        link = self.driver.find_element_by_xpath('//*[@id="header"]/div[1]/div/div/div[1]/ul/li[1]/a/i')
        section = 'Search Button'
        self.access(link,section)
        sleep(3)

        textBox = self.driver.find_element_by_xpath('//*[@id="search-input"]')
        section = 'Search Input'
        searchText = inputText.searchInput

        for txt in searchText:
            self.excel.addValue(self.row,0,section+' '+txt)
            
            sleep(3)
            try:
                textBox.send_keys(txt)
                textBox.send_keys(Keys.ENTER)
                self.excel.addValue(self.row,1,'sucess')
            except:
                self.excel.addValue(self.row,1,'fail')
            self.excel.save()
            
            sleep(3)
            ul_xpath = '//*[@id="article"]/div/ul'
            contents = self.getContentTitles(ul_xpath)

            self.excel.addValue(self.row,3,contents)
            
            self.excel.save()
            sleep(1)
            print('search ' + txt)
            textBox.clear()
            self.row+= 1

        closeButton = self.driver.find_element_by_xpath('//*[@id="search-modal"]/div/div/div[1]/button')
        closeButton.click()

    def run(self):
        self.headersLink()
        self.regionalLink()
        self.kategoriLainnyaLink()
        self.eventLainnyaLink()
        self.channelLainnyaLink()
        self.search()
        self.quit()
    


bot = idnTimes()
sleep(15)
bot.run()

