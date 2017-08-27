#!/usr/bin/python

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

#
# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
#
DEVELOPER_KEY = "AIzaSyAIxeoTroXwAFjgoe0N2LGvYPeRR9FIza8"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

#
# Call this to create a new v3 Youtube Service to Operate On.
#
def getService():
    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
      developerKey=DEVELOPER_KEY)

# SIMPLE SEARCH FUNCTION
#
# search_list_by_keyword(service,
#   part='snippet',
#   maxResults=25,
#   q='surfing',
#   type='')
#
def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  #
  search_response = youtube.search().list(
    q=options.q,
    part="id,snippet",
    maxResults=options.max_results
  ).execute()

  videos = []
  channels = []
  playlists = []

  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
      videos.append("%s (%s)" % (search_result["snippet"]["title"],
                                 search_result["id"]["videoId"]))
    elif search_result["id"]["kind"] == "youtube#channel":
      channels.append("%s (%s)" % (search_result["snippet"]["title"],
                                   search_result["id"]["channelId"]))
    elif search_result["id"]["kind"] == "youtube#playlist":
      playlists.append("%s (%s)" % (search_result["snippet"]["title"],
                                    search_result["id"]["playlistId"]))

  print "Videos:\n", "\n".join(videos), "\n"
  print "Channels:\n", "\n".join(channels), "\n"
  print "Playlists:\n", "\n".join(playlists), "\n"


#
# HELPER FUNCTION: Remove keyword arguments that are not set
#
def remove_empty_kwargs(**kwargs):
  good_kwargs = {}
  if kwargs is not None:
    for key, value in kwargs.iteritems():
      if value:
        good_kwargs[key] = value
  return good_kwargs

# API Call to get info on an individual video.
#
# Ex.)
# videos_list_by_id(service,
#   part='snippet,contentDetails,statistics',
#   id='gu_PQBmk-6c')
#
def videos_list_by_id(service, **kwargs):
  kwargs = remove_empty_kwargs(**kwargs) # See full sample for function
  results = service.videos().list(
    **kwargs
  ).execute()

  return results

# Lookup channel based on ID
#
# ex). channels_list_by_id(service,
#        part='snippet,contentDetails,statistics',
#        id='UC_x5XG1OV2P6uZZ5FSM9Ttw')
#
def channels_list_by_id(service, **kwargs):
  kwargs = remove_empty_kwargs(**kwargs) # See full sample for function
  results = service.channels().list(
    **kwargs
  ).execute()

  print(results)

# Lists Some data based on search by Username
#
# ex) channels_list_by_username(service, part='snippet,
#     contentDetails,statistics', forUsername='GoogleDevelopers')
#
def channels_by_username(service, **kwargs):
  results = service.channels().list(
    **kwargs
  ).execute()

  print('This channel\'s ID is %s. Its title is %s, and it has %s views. The Uploads Playlist is \'%s\'' %
       (results['items'][0]['id'],
        results['items'][0]['snippet']['title'],
        results['items'][0]['statistics']['viewCount'],
        results['items'][0]['contentDetails']['relatedPlaylists']['uploads']))

  return results

# Get object containing the items in a playlist.
# Takes the playlist ID, which can be gathered from using other
# API operations or manually entered after finding it in a browser
#
#
# Ex) playlist_items_list_by_playlist_id(service,
#       part='snippet,contentDetails',
#       maxResults=25,
#       playlistId='PLBCF2DAC6FFB574DE')
#
#
def playlist_items_list_by_playlist_id(service, **kwargs):
  kwargs = remove_empty_kwargs(**kwargs) # See full sample for function
  results = service.playlistItems().list(
    **kwargs
  ).execute()

  return results

# Retrieves the total number of items in a playlist.
# Useful because we must implement our own pagination
# since this API only allows for retrieval of 50 videos at a time :/
#
#
def get_total_number_in_playlist_by_pid(service, id):
  results = playlist_items_list_by_playlist_id(service,
    part = 'snippet,contentDetails',
    maxResults = 50,
    playlistId = id, prettyPrint = True)

  return results['pageInfo']['totalResults']

# Uses pagination to build a list with all items of a playlist
# Returns an array set containing the ID of each video in the playlist.
# This list can then be iterated over to build out datasets.
#
#
def get_list_of_videos_in_playlist_by_playlist_id(service, id):
  total_results = get_total_number_in_playlist_by_pid(service, id)

  nextToken = ''
  flag = False
  results = []

  while flag != True:
    current = playlist_items_list_by_playlist_id(service,
      part = 'snippet,contentDetails',
      maxResults = 50,
      playlistId = id,
      prettyPrint = True,
      pageToken = nextToken)

    try:
      nextToken = current['nextPageToken']
    except Exception, e:
      flag = True

    print("Next Page Token: %s" % (nextToken))
    for item in current['items']:
      videoId = item['contentDetails']['videoId']
      results.append(videoId)
    print("Current result set total: %s" %  (len(results)))
    print("Page token available: %s \n" % (current.has_key('nextPageToken')))

  print ("\nTotal videos in playlist: %s \n" % (total_results))
  return results

# Log some details of the video object that the API spits out.
# For this function I chose some values I saw as most relevant, however
# feel free to check out the documentation
# https://developers.google.com/youtube/v3/docs/videos/list
# to see what is available to collect.
#
#
def print_vid(vidObject):
  print("\nVideo ID: %s" % (vidObject['items'][0]['id']))
  print("Title: %s" % (vidObject['items'][0]["snippet"]['title']))
  print("Published: %s" % (vidObject['items'][0]["snippet"]['publishedAt']))
  print("Tags: %s\n" % (vidObject['items'][0]["snippet"]['tags']))

  stats = vidObject['items'][0]["statistics"]

  if stats.has_key('viewCount'):
    print("Views: %s" % (stats['viewCount']))
  if stats.has_key('likeCount'):
    print("Likes: %s" % (stats['likeCount']))
  if stats.has_key('dislikeCount'):
    print("Dislikes: %s" % (stats['dislikeCount']))
  if stats.has_key('favoriteCount'):
    print("Favorites: %s" % (stats['favoriteCount']))
  if stats.has_key('commentCount'):
    print("Comments: %s" % (stats['commentCount']))
