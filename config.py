# Twitter Bearer token
bearer_token = 'insert your bearer token here'

# Timezone
import pytz
tmz = pytz.timezone('CET')

# Query filters
# https://developer.twitter.com/en/docs/twitter-api/v1/rules-and-filtering/search-operators
filters	= '-is:retweet -is:reply lang:en'

# Parameters to include in the return object
# https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/tweet
# https://developer.twitter.com/en/docs/twitter-api/expansions
query_params = {
	'tweet.fields'	: 'attachments,author_id,created_at,geo,lang',		# default:	id, text
	'user.fields'	: 'profile_image_url',								# default:	id, name, username
	'media.fields'	: 'preview_image_url,url',							# default:	media_key, type
	'poll.fields'	: '',												# default:	id, options
	'place.fields'	: 'contained_within,country,name',					# default:	full_name, id
	'expansions'	: 'author_id,attachments.media_keys,geo.place_id'	# default:	-
}


rules = [
	{ 'value' : 'dog ' + filters, 'tag': 'dog'},
	{ 'value' : 'cat ' + filters, 'tag': 'cat'},
]

# Feed Settings
min_tweet_height	= 58
tweet_width			= 600
img_width			= 668		# hmargins[0] + 48 + hmargins[1] + 500 + hmargins[2] + 48 + hmargins[3]
max_onscreen_tweets	= 12
max_tweets			= 40

# GUI Settings
hmargins		= (5, 5, 5, 5)	# left to right
vmargins		= (5, 5, 10)	# t, b
omargins		= (5, 5, 5, 5)	# t, r, b, l

line_space		= 2
font_size		= 20
img_mode		= "RGB" # the mode of the tweets image (=> filesize)

color_bg		= (255, 255, 255)	# background color
color_fg		= (0, 0, 0)			# text color normal
color_fg_gray	= (101, 119, 134)	# text color gray
color_fg_red	= (255, 0, 0)		# text color red

media_height	= 128
avatar_height	= 48

from PIL import ImageFont
font		= ImageFont.truetype("res/chirp_regular.otf", font_size)	# regular font
font_bold	= ImageFont.truetype("res/chirp_bold.otf", font_size)		# bold font for name
font_thin	= ImageFont.truetype("res/chirp_thin.otf", font_size)

url_rules	= "https://api.twitter.com/2/tweets/search/stream/rules"
url_stream	= "https://api.twitter.com/2/tweets/search/stream"

twitter_icon = 'res/twitter.ico'
#⨺ ⨹ ⚠
