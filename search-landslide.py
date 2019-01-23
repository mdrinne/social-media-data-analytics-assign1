# Sample Python code for user authorization

import os
import datetime

import google.oauth2.credentials

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "client_secret_306317465773-k7nojmeanjhlmuudhcofgt33aqeajrc1.apps.googleusercontent.com.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def get_video_view_count(service, **kwargs):
    result = service.videos().list(**kwargs).execute()

    return result['items'][0]['statistics']['viewCount']

def search_list_by_keyword(service, **kwargs):
    results = service.search().list(
                                      **kwargs
                                      ).execute()
                                      
    for result in results.get("items",[]):
          print('%s\t%s\t%s' %
                (result['id']['videoId'],
                 result['snippet']['title'],
                 get_video_view_count(service,
                                      part='statistics',
                                      id=result['id']['videoId'])))
    return results['nextPageToken']

if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    service = get_authenticated_service()
    print('2018-01-01 00:00:00\t2018-12-31 23:59:59')
    token = search_list_by_keyword(service,
                                   part='snippet',
                                   maxResults=50,
                                   order='viewCount',
                                   publishedAfter='2018-01-01T00:00:00Z',
                                   publishedBefore='2018-12-31T23:59:59Z',
                                   q='landslide',
                                   type='video')
                           
    search_list_by_keyword(service,
                           part='snippet',
                           maxResults=50,
                           order='viewCount',
                           pageToken=token,
                           publishedAfter='2018-01-01T00:00:00Z',
                           publishedBefore='2018-12-31T23:59:59Z',
                           q='landslide',
                           type='video')
