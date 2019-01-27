from tweepy import API, OAuthHandler
import urlparse


CONSUMER_KEY = 'G1tGNhvDZZREKSqHAHqRDGWTj'
CONSUMER_SECRET = 'pv1x67XZTKH48qN3YzBJGU44N8W8eRxp4szZwQm6oPis1ijum2'
ACCESS_TOKEN = '3915763813-M7VK6XNBkp4x7Av4CqZuUNKCKcBCWpMH3aEJrcq'
ACCESS_SECRET = 'Xfdn34PvSwY6B8X3wJa7PZEmRBXVoCzWOsnByL9UmELA5'


TWITTER_AUTH = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
TWITTER_AUTH.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
TWITTER_API = API(TWITTER_AUTH, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def get_original_url(status_url):
    '''

    :param status_url: url of the tweet copied
    :return: original_video_url of the video that the tweet contains
    '''
    url_object = urlparse.urlparse(status_url)
    path = url_object.path
    status_id = path.split('/')[-1]
    data = TWITTER_API.get_status(id=status_id, tweet_mode='extended')
    json_data = data._json
    video_urls = json_data['extended_entities']['media'][0]['video_info']['variants']
    resolutions=('640x360','360x640','404x718','718x404','406x720','720x406','778x360','360x778')
    for video in video_urls:
        url = video['url']
        url_object = urlparse.urlparse(url)
        url_path=url_object.path
        parts = url_path.split('/')
        if 'vid' in parts:
            vid_index=parts.index('vid')
            resolution = parts[vid_index+1]
            if resolution in resolutions:
                return url

    # if none of the defined resolutions are present
    # if /vid/ is present in the list of video urls given by the API , then that means the video is of mp4 format
    for video in video_urls:
        url=video['url']
        if '/vid/' in url:
            return url


url = 'https://twitter.com/i/status/1080347603592716288'
url_object = urlparse.urlparse(url)
# print(url_object.hostname)
if url_object.hostname == 'twitter.com':
    url = get_original_url(url)
    print(url)
# print(url)

















def check():
    if not TWITTER_API:
        print("cant authenticate")
    else:
        print('success')
    pass


