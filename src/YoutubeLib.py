from pprint import pprint
from googleapiclient.discovery import build


#TODO::Channel ID and API key into GetEnvFile

YoutubeObject=None

def InitializeYoutube():
    global YoutubeObject
    api_key = 'PUTKEYHERE'
    YoutubeObject= build('youtube','v3',developerKey=api_key)
    if YoutubeObject==None:
        sys.exit("Youtube failed")


def GetVideosList(request):
    VideosList=[]
    response = request.execute()
    for single_item in response["items"]:
        VideosList.append({
                "Title":single_item["snippet"]["title"],
                "Url":"https://www.youtube.com/watch?v="+single_item["id"]["videoId"],
            #    "Description":single_item["snippet"]["description"]
                "Thumbnail":single_item["snippet"]["thumbnails"]["default"]["url"]
            })
    return VideosList


def GetRandomHonestVideos():
    global YoutubeObject
    request = YoutubeObject.search().list(
        part="snippet",
        maxResults=100,
	channelId="CHNLID",
	type='video'
    )
    return GetVideosList(request)

def GetRecentHonestVideos(Max=3):
    global YoutubeObject
    request = YoutubeObject.search().list(
        part="snippet",
        maxResults=Max,
        channelId="CHNLID",
        type='video',
        order='date'
    )
    return GetVideosList(request)

def GetHonestByQuery(SearchQuery):
    global YoutubeObject
    print("Query:",SearchQuery)
    request = YoutubeObject.search().list(
        part="snippet",
        maxResults=1,
        channelId="CHNLID",
        type='video',
        q=SearchQuery
    )
    return GetVideosList(request)


InitializeYoutube()
