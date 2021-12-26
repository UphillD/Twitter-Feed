# Implements all GUI-related functions
import datetime
import os
import re
import requests
import string
import tkinter

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from config import *
from twitter import *

# Properly wraps tweet text
def wrap_text(text, width, font):
	# https://stackoverflow.com/questions/11159990/write-text-to-image-with-max-width-in-pixels-python-pil
	text_lines = []
	text_line = []
	text = text.replace('\n', ' [br] ')
	words = text.split()

	for word in words:
		if word == '[br]':
			text_lines.append(' '.join(text_line))
			text_line = []
			continue
		text_line.append(word)
		w, h = font.getsize(' '.join(text_line))
		if w > width:
			text_line.pop()
			text_lines.append(' '.join(text_line))
			text_line = [word]

	if len(text_line) > 0:
		text_lines.append(' '.join(text_line))

	return text_lines

def get_media(url, standard_height):
	response = requests.get(url, stream=True)
	try:
		media = Image.open(response.raw)
		width, height = media.size
	except:
		media = False
	else:
		media = media.convert(img_mode)
		new_width = int(width * (standard_height / height))
		media = media.resize((new_width, standard_height), Image.ANTIALIAS)
		media_width = media.size[0]

	return media_width, media



def get_image(status):
   # Get profile image
	profileimg_width, profileimg = get_media(status['includes']['users'][0]['profile_image_url'], avatar_height)
	# Wrap tweet text
	text = ''.join(s for s in status['data']['text'] if s in string.printable)	# Remove non-printable characters
	text = re.sub(r'https://t.co\S+', '', text)		# Remove t.co urls
	name = ''.join(s for s in status['includes']['users'][0]['name'] if s in string.printable)

	screenname = status['includes']['users'][0]['username']
	place = ('from ' + status['includes']['places'][0]['full_name'] if 'places' in status['includes'] else '')
	created_at = datetime.datetime.strptime(status['data']['created_at'], "%Y-%m-%dT%H:%M:%S.000%z").astimezone(tmz).strftime("%d %b, %H:%M:%S")

	fulltext = 'name\n' + text + '\ndate\n' # + created_at + place

	text = wrap_text(fulltext, tweet_width + hmargins[2], font)

	# create tweet image
	textheight = font.getsize(text[0])[1] * len(text) + len(text) * line_space
	mediaheight = (media_height if 'media' in status['includes'] else 0)
	img = Image.new(img_mode, (img_width, vmargins[0] + textheight + vmargins[1] + mediaheight + vmargins[2]), color_bg)
	draw = ImageDraw.Draw(img)

	# draw text
	x, y = hmargins[0] + profileimg_width + hmargins[1], vmargins[0]
	for line in text:
		if y == vmargins[0]:
			# First line with twitter handle (bold) and date (gray)
			#name = status['includes']['users'][0]['name'] + ' ' #"@" +  + " "
			draw.text((x, y), name, color_fg, font=font_bold)
			w, h = font_bold.getsize(name)
			#username = '@' + status['includes']['users'][0]['username']
			draw.text((x + w, y), ' @' + screenname, color_fg_gray, font=font)
			y = y + font_size+line_space*2
		elif line and line.startswith('date'):
			y += line_space*2
			draw.text((x, y), created_at + ' ' + place, color_fg_gray, font=font)
			y = y + font_size+line_space
		else:
			# Other lines: tweet text
			draw.text( (x,y), line, color_fg, font=font)
			y = y + font_size+line_space

	# draw profile img if possible
	if profileimg is not False:
		img.paste(profileimg, (hmargins[0], vmargins[0]))
	if 'media' in status['includes']:
		y += line_space * 2
		x_pos = hmargins[0] + profileimg_width + hmargins[1]
		for media in status['includes']['media']:
			mediaurl = (media['preview_image_url'] if 'preview_image_url' in media else media['url'])
			media_width, mediaimg = get_media(mediaurl, media_height)
#			if 'preview_image_url' in media:
#				media_width, mediaimg = get_media(media['preview_image_url'], media_height)
#			elif 'url' in media:
#				media_width, mediaimg = get_media(media['url'], media_height)
			if x_pos + media_width >= hmargins[0] + profileimg_width + hmargins[1] + tweet_width:
				break
			else:
				img.paste(mediaimg, (x_pos, y))
				x_pos += media_width + hmargins[1]

	return img

def draw_tweet(tweet):
	text = tweet['data']['text']
	# Check if tweet includes geolocation
	place = (tweet['includes']['places'][0] if 'places' in tweet['includes'] else None)
	# Generate the tweet image
	image = get_image(tweet)
	#image = image.convert("P") # 8-bit => smaller fileisze
	image.save('tmp.png', 'PNG', optimize = True)
	try:
		image = tkinter.PhotoImage(file='tmp.png')
	except:
		image = -1
	os.remove('tmp.png')

	return image


def init_gui():
	master = tkinter.Tk()
	master.resizable(False, False)
	master.title("Twitter Feed")
	master.protocol("WM_DELETE_WINDOW", lambda e: master.destroy())
	master.bind('<Escape>', lambda e: master.destroy())
	favicon = tkinter.PhotoImage(file=twitter_icon)
	master.call('wm', 'iconphoto', master._w, favicon)
	frame = tkinter.Frame(master, width = omargins[3] + img_width + omargins[1], height = 3*(omargins[0] + omargins[2]))
	frame.pack(expand=True, fill=tkinter.BOTH)
	canvas = tkinter.Canvas(frame, width = omargins[3] + img_width + omargins[1], height = 3*(omargins[0] + omargins[2]))
	vbar=tkinter.Scrollbar(frame,orient=tkinter.VERTICAL)
	vbar.pack(side=tkinter.RIGHT,fill=tkinter.Y)
	vbar.config(command=canvas.yview)
	canvas.config(scrollregion = canvas.bbox('all'))
	canvas.config(yscrollcommand=vbar.set)
	canvas.pack(side=tkinter.LEFT,expand=True,fill=tkinter.BOTH)

	return master, frame, canvas
