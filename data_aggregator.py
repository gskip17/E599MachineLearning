# You should get everything you need to run this project by typing -
# pip install --upgrade google-api-python-client
# In your terminal

import service_helpers as SH
from pprint import pprint


# Declare Constants
CHANNELUSERNAME = 'TEDtalksDirector'

# creates a new instance of the service for the API
service = SH.getService()

# get the TEDTalk channel object using the username that owns it as search criteria
ted = SH.channels_by_username(service, part='snippet, contentDetails,statistics',
  forUsername=CHANNELUSERNAME)

# to get all the uploads we need the playlist ID of their aggregate 'upload' playlist
ted_playlist = ted['items'][0]['contentDetails']['relatedPlaylists']['uploads']

# Get all Items in the Playlist
playlistItems = SH.playlist_items_list_by_playlist_id(service,
  part = 'snippet,contentDetails',
  maxResults = 1,
  playlistId = ted_playlist, prettyPrint = True)

# Save the total number of items in the playlist - for logging.
total_results_num = SH.get_total_number_in_playlist_by_pid(service, ted_playlist)

# Get every single video ID that is in TED's uploads and puts each one in a
# nice list we can iterate through later.
videos = SH.get_list_of_videos_in_playlist_by_playlist_id(service, ted_playlist)

# Iterate through every Video ID, find the object using the API, and log some (not all)
# of the metrics we can work with.
#
# Need to implement some functions that write to a CSV because running this more than
# once takes a while since there is about 2.5k videos in this channel.
# Once in a CSV and the data we want is decided we have everything we need to start
# working on the maths.
#
count = 0
for vidID in videos:
  count += 1
  current = SH.videos_list_by_id(service,
    part='snippet,contentDetails,statistics',
    id=vidID)
  print("Video %s of %s" % (count, total_results_num))
  SH.print_vid(current)
