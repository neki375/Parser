import csv

import requests

from lxml import html as html_dom

csvfile = open('pars.csv', 'w')
writer = csv.writer(csvfile)
#
writer.writerow(['Название', 'Время', 'Превью','Категории', 'Теги','Ссылка на видео'])

for page in range(1, 77 + 1):
    url = 'https://www.diretube.com/browse-comedy-videos-%s-date.html' % page
    html = requests.get(url).text
    dom = html_dom.fromstring(html)

# html = requests.get('https://www.diretube.com/browse-comedy-videos- \
# 1-date.html').text
# dom = html_dom.fromstring(html)


videos = dom.cssselect('.thumbnail')


for video in videos:
    video_name = video.cssselect('.caption a')[0].text
    video_url = video.cssselect('.caption a')[0].get('href')
    video_time = video.cssselect('.pm-video-since time')[0].text
    video_img = video.cssselect('.img-responsive')[0].get('src')

    html = requests.get(video_url).text
    video_dom = html_dom.fromstring(html)

    category = []
    for i in video_dom.cssselect('.pm-video-description dl > \
    dd:nth-child(2) a'):
        category.append(i.text)

    tags = []
    for i in video_dom.cssselect('.pm-video-description dl >  \
    dd:nth-child(4) a'):
        tags.append(i.text)

    videourls = video_dom.cssselect('#Playerholder')[0].get('src')

    # full = [video_name, video_time, video_img]
    # full.append(category, tags, videourls)

    writer.writerow([video_name, video_time, video_img, category, tags, videourls])

    # for videourl in videourls:
    #     url_video =

    # videourl = 'https://cdn.jwplayer.com/v2/media/%s' % video_id
    # html = requests.get(videourl).text




#
# images = dom.cssselect('.img-responsive').get('src')
# print(images)
#
# videos_url = dom.cssselect('.media_id')
# print(videos)
