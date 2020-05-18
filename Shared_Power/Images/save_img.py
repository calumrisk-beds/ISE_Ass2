"""
pic_name = "C:/Users/calum/OneDrive/Pictures/Image Testing/sb-18-l--0231700_20s_51.jpg"
# pic = Image.open(pic_name)
# with open(pic_name, 'rb') as pic_rb:
  #  f = pic_rb.read()
   # print(f)
#with open(pic_name, 'wb') as pic_wb:
 #   f = pic_wb.read()
  #  print(f)

f = open(pic_name, 'rb')
newfile = open('newfile.jpg', 'wb')
# newfile.write(f.readlines()) #
for line in f:
    newfile.write(line)
"""

import os
from os.path import join, dirname, abspath
import shutil
import sqlite3
import Shared_Power.DB.sql_create as sqlc
import Shared_Power.DB.sql_read as sqlr
from Shared_Power.Classes.tool import Tool

path = join(dirname(dirname(abspath(__file__))), 'DB/shared_power.db')
conn = sqlite3.connect(path)

# Copying file into directory
src = r"C:/Users/calum/OneDrive/Pictures/Image Testing/sb-18-l--0231700_20s_51.jpg"
dst = join(dirname(dirname(abspath(__file__))), 'Images')
newfile = shutil.copy(src, dst)

# Read file as binary
f = open(newfile, 'rb')
rf = f.read()
print(rf)


# Store binary file in Database
def store_img_to_db():
    tl = Tool(tool_id='', tool_owner='', tool_name='', descr='', day_rate='', halfd_rate='', prof_pic=rf)
    sqlc.insert_tool(tl)


# store_img_to_db()

# Retrieve file from Database
tid = 1
get_tl = sqlr.get_tool_by_id(tid)
pic_store = get_tl[0][6]

# Write new file
with open('temp.jpg', 'wb') as f:
    f.write(pic_store)

# Delete files
os.remove(newfile)
os.remove('temp.jpg')


