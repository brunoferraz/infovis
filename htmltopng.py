import os
import time
from selenium import webdriver
from os import listdir
import imgkit
import os
import sys
print(os.path.dirname(sys.executable))

# browser = webdriver.Firefox()
# browser.get('https://www.google.com') 
 
delay=5
path = './paginas'
l = listdir('./paginas')
# # #Open a browser window...
# # #..that displays the map...
# imgkit.from_file('mapa_0.html', 'out.jpg')
for i in range(len(l)):
    n = l[i].split('.')[0].split("_")[1]
    browser = webdriver.Firefox()
    browser.maximize_window()
    browser.get('file:///C:/Users/Bruno/Documents/dev/infovis/paginas/'+l[i])

# # # #Give the map tiles some time to load
    time.sleep(delay)
# # # #Grab the screenshot
    browser.save_screenshot('plot/mapa_'+str(n)+'.png')

# # #Close the browser
    browser.quit()