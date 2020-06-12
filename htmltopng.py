import os
import time
from selenium import webdriver
from os import listdir

 
delay=5
 
# #Save the map as an HTML file
# fn='testmap.html'
# tmpurl='file://{path}/{mapfile}'.format(path=os.getcwd(),mapfile=fn)
# m.save(fn)
path = './paginas/'  

l = listdir('./paginas')
# #Open a browser window...
browser = webdriver.Firefox()
# #..that displays the map...
browser.get(path + '/' + l[0])
# #Give the map tiles some time to load
time.sleep(delay)
# #Grab the screenshot
# browser.save_screenshot('map.png')
# #Close the browser
# browser.quit()