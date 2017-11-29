import csv

import requests
from tqdm import tqdm

from lxml import html as html_dom


csvfile = open('pars.csv', 'w')
writer = csv.writer(csvfile)

writer.writerow(['Название',
                 'Время',
                 'Превью',
                 'Каегории',
                 'Теги',
                 'Ссылка на видео'])

PAGES = ['https://www.diretube.com/browse-comedy-videos-%s-date.html' % i
         for i in range(1, 78)]


# Селекторы для категорий и тегов
cat_selector = '.pm-video-description dl > dd:nth-child(2) a'
tage_slector = '.pm-video-description dl > dd:nth-child(4) a'


def get_dom(url):
    html = requests.get(url).text
    return html_dom.fromstring(html)


def get_video_url(dom):
    # Фрейм с видосом
    iframe = dom.cssselect('#Playerholder iframe')

    # Линк на просмотр видоса
    embed = dom.cssselect('meta[itemprop="embedURL"]')[0].get('content')

    if iframe:
        # Если есть фрейм
        frame_src = iframe[0].get('src')

        # Короче тут можешь еще один иф стоять если есть 3й сервис для видосов
        # Кроме ютуба например

        if 'jwplatform' in frame_src:
            # Если это jwplatform
            # //content.jwplatform.com/players/uJVUNMF4-WMnI212I.html
            # Получаем id видео для подзапроса "uJVUNMF4"
            video_id = frame_src.replace(
                '//content.jwplatform.com/players/', '').split('-')[0]

            api_url = 'https://cdn.jwplayer.com/v2/media/%s' % video_id
            video_data = requests.get(api_url).json()

            try:
                # Самое больше разрешение
                return video_data['playlist'][0]['sources'][-2]['file']
            except IndexError:
                # Могут быть ошибоньги, хз там много видосов, может не работать
                print('Ошибка jw api для: %s' % video_id)

                return embed

    else:
        # Если фрейма нет возвращаем просто embedURL
        return embed


# tqdm это прогресс бар
for page_url in tqdm(PAGES, 'Pages'):
    page_dom = get_dom(page_url)
    videos = page_dom.cssselect('.thumbnail')

    for video in tqdm(videos, 'Videos on page %s' % page_url):
        name = video.cssselect('.caption a')[0].text
        url = video.cssselect('.caption a')[0].get('href')
        time = video.cssselect('.pm-video-since time')[0].text

        # Запрашиваем стр с видосом
        v_dom = get_dom(url)
        video_img = v_dom.cssselect(
            'meta[itemprop="thumbnailUrl"]')[0].get('content')

        # Категории и теги через запятую
        categories = ','.join([i.text for i in v_dom.cssselect(cat_selector)])
        tags = ','.join([i.text for i in v_dom.cssselect(tage_slector)])

        download_url = get_video_url(v_dom)

        # Все тут все в файлик добавляешь все дерьмо собраное
        continue
        writer.writerow()
