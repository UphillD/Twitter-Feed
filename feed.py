import json
import sys
import tkinter

from config import *
from imagefy import *
from twitter import *



# Get old rules
old_rules = get_rules()
print('Old rules received.')

# Delete old rules
delete_response = delete_rules(old_rules)
print('Old rules deleted.')

# Generate new rules
query_rules = generate_rules()
print(str(len(query_rules)) + ' new rules generated.')

# Set new rules
set_response = set_rules(query_rules)
created_rules = str(set_response['meta']['summary']['created'])
print(created_rules + ' new rules set.')

# Initialize the GUI
master, frame, canvas = init_gui()
print('GUI Initialized')

# Start the stream
print()
print('Stream starting...')
print('Pause-Resume with CTRL+C, Exit with ESC')
print()

# Initialize tweet counter
cnt = 0
# Lists to hold image and canvas objects
images = []
canvas_images = []
while(True):
	response = requests.get(url_stream, auth=bearer_oauth, params=query_params, stream=True)
	if response.status_code != 200:
		raise Exception("Cannot get stream (HTTP {}): {}".format(response.status_code, response.text))

	try:
		for response_line in response.iter_lines():
			if response_line:
				# Grab tweet
				tweet = json.loads(response_line)
				# Grab resulting image & priority flag
				image = draw_tweet(tweet)
				if image == -1: exit()
				# Increment & print counters
				cnt += 1
				print('Tweet received, {} total tweets'.format(cnt))
				# Add resulting image object to image list
				images.append(image)
				# If canvas fits more tweets, resize it
				if (int(canvas.cget('height')) < min_tweet_height * max_onscreen_tweets):
					frame.config(width=int(canvas.cget('width')), height=int(canvas.cget('height')) + image.height() + omargins[2])
					canvas.config(width=int(canvas.cget('width')), height=int(canvas.cget('height')) + image.height() + omargins[2])

				# Iterate through all canvas images
				for canvas_image in canvas_images:
					# Move the previous tweet lower
					canvas.move(canvas_image, 0, image.height() + omargins[2])
					# If onscreen tweet limit exceeded, delete oldest tweet
					if len(canvas_images) > max_tweets:
						canvas.delete(canvas_images[0])
						canvas_images.pop(0)
						images.pop(0)
				# Paste new tweet
				canvas_images.append(canvas.create_image(omargins[3], omargins[1], anchor=tkinter.NW, image=image))
			canvas.update_idletasks()
			canvas.update()
	# Catch CTRL-C interrupt
	except KeyboardInterrupt:
		print('TRL+C detected, stream stopped.')
		print('Press CTRL+C again to resume.')
		while(True):
			try:
				canvas.update()
			except KeyboardInterrupt:
				print('TRL+C detected, resuming stream..')
				print()
