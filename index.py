from flask import Flask,render_template
from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup
import textwrap
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
import requests
import ssl
import certifi
from urllib import request as rq
from io import BytesIO
from flask import request
import time
from flask import send_from_directory

upload_care_api = '9a802627dbaf41542e8d'
upload_care_secret_key = '03aa************e9f0'


app = Flask(__name__,template_folder='template')

img_url = []
nombre = ''
page = requests.get("https://www.entrekids.cl/actividad-evento/el-extraordinario-circo-de-halloween")
soup = BeautifulSoup(page.content, 'html.parser')
url_productos = [
      'https://www.entrekids.cl/producto/sandalia-outdoor-nina-fagus-1ss1122',
      'https://www.entrekids.cl/actividad-evento/el-extraordinario-circo-de-halloween'
      ]


@app.route("/")
def home():
   return render_template('template.html', **locals())

@app.route("/new-scrapp", methods=['GET', 'POST'])
def categories():
   formate_string = []
   print(request.method)
   if request.method == 'POST':
      username = request.form.get('username').lstrip()
      string_lit = username.rstrip("\n")
      string_lit = username.split(",")
     
      instagram_path = []
      nameImg = []
      realImageName = []
      string_lit = [i.strip() for i in string_lit]
      print(string_lit)
      #seven_day = soup.find(class_="h1-alert")
      #nombre = seven_day.get_text()
      #time.sleep(3)
      if True:
         for i in range(len(string_lit)):
            driver = webdriver.Firefox(executable_path = '../geckodriver')
            driver.get(string_lit[i])
            #headlines = driver.find_element_by_class_name("h1-alert")
            img = driver.find_element_by_class_name("loadeding-lazy")
            img_url = img.get_attribute('src')
            print(img_url)
            response = requests.get(img_url)
            Image.open(BytesIO(response.content)).convert('RGBA').save('static/image-' + str(i) + '.png')

            platform = ['facebook', 'instagram', 'historia']

            imageFlot = Image.open('static/image-' + str(i) + '.png', 'r')

            imageTop = Image.open('top.png', 'r')
            imageBottom = Image.open('bottom.png', 'r')

            for j in range(len(platform)):
               if True:
                  if str(platform[j]) == 'facebook':
                     name = 'facebook-'
                     instaW = 1080
                     instaH = 1080
                  if str(platform[j]) == 'instagram':
                     name = 'instagram-'
                     instaW = 1080
                     instaH = 1350
                  if str(platform[j]) == 'historia':
                     name = 'historia-'
                     instaW = 1080
                     instaH = 1920
               
                  instaSize = instaW, instaH

                  #Medidas facebook 

                  #facebook: 1080 x 1080
                  #instagram: 1080 x 1350
                  #historia: 1080 x 1920

                  
                  imageTop.thumbnail(instaSize, Image.ANTIALIAS)
                  imageBottom.thumbnail(instaSize, Image.ANTIALIAS)
                  img_wB, img_hB = imageBottom.size

                  #Medidas de facebook
                  w = 500 # 100 pixels wide
                  h = 400 # 100 pixels high
                  print('size ' + str(imageFlot.size[0]))
                  if imageFlot.size[0] == 750 and imageFlot.size[1] == 500:
                     imageFlot = imageFlot.resize((750,500), Image.ANTIALIAS)
                  else:

                     if imageFlot.size[0] >= 850 or imageFlot.size[0] <= 850:
                        imageFlot = imageFlot.resize((850,850), Image.ANTIALIAS)
                        print(1)
                     else:
                        print(0)
                        size = 850, 850
                        imageFlot.thumbnail(size, Image.ANTIALIAS)
                     
                  img_w, img_h = imageFlot.size

                  background = Image.new('RGBA', (instaW, instaH),  color=(255, 255, 255, 255))
                  bg_w, bg_h = background.size
               
                  offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
               
                  #canvas = ImageDraw.Draw(imageFlot)
                  canvas = ImageDraw.Draw(background)
                  font = ImageFont.truetype('Pangram-Bold.otf', size=44)
                  text_width, text_height = canvas.textsize('Hello World', font=font)
                  x_pos = int((w - text_width) / 2)
                  y_pos = int((h - text_height) / 2)

                  text = "Audífonos manos libres Samsung Original ergonómico con goma EG920"
                  #Formateo de fuente y text
                  lines = textwrap.wrap(text, width=30)
                  y_text = bg_h
                  for line in lines:
                     print(y_text)
                     width, height = font.getsize(line)
                     #draw.text(((w - width) / 2, y_text), line, font=font, fill=FOREGROUND)
                     #canvas.text(((instaW - width) / 2, y_text - 400), line, font=font, fill='#000000')
                     y_text += height

                  #canvas.text((0, y_pos), 'hola', font=font, fill='#000000')


                  background.paste(imageFlot,  offset)
                  background.paste(imageTop,  (0, 0))
                  background.paste(imageBottom,  (0, instaH - img_hB))
                  background.save('static/output/' + str(name) + 'image-' + str(i) + '.png')
                  background.show()
                  nameImg.append(name)
                  realImageName.append(str(name) + 'image-' + str(i) + '.png')
                  instagram_path.append('output/' + str(name) + 'image-' + str(i) + '.png')
                  

      return render_template('categories.html', **locals())
   else:
      print(0)
      return render_template('categories.html')


@app.route("/email", methods=['GET', 'POST'])
def email():
   image = request.form.get('image')
   print(image)
   return render_template('email.html', **locals())


@app.route('/database_download/<filename>')
def database_download(filename):
    return send_from_directory('static/output/', filename, as_attachment=True)




if __name__=="__main__":
   #app.run(debug=True)
   app.run(host='192.168.100.4', port=5000, debug=True, threaded=False)