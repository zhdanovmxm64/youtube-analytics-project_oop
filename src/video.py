import os
from googleapiclient.discovery import build


class Video:

    api_key: str = os.getenv('YT_API_KEY')  # берет значение переменной окружения
    youtube: str = build('youtube', 'v3', developerKey=api_key)  # создает объект для работы с API

    def __init__(self, video_id: str) -> None:
        self.video_id: str = video_id  # id видео

        # Пробуем получить данные видео по api
        try:
            video: dict = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails', id=self.video_id).execute()
            checking_video_data_is_empty = video['items'][0]
        # Если получить данные невозможно = None
        except IndexError:
            self.title = None  # название видео
            self.url = None  # ссылка на видео
            self.viewCount = None  # количество просмотров
            self.like_count = None  # количество лайков
        # Создаем атрибуты
        else:
            self.title: str = video['items'][0]['snippet']['title']  # название видео
            self.url: str = f"https://www.youtube.com/watch?v={video['items'][0]['id']}"  # ссылка на видео
            self.viewCount: int = video['items'][0]['statistics']['viewCount']  # количество просмотров
            self.like_count: int = video['items'][0]['statistics']['likeCount']  # количество лайков

    def __str__(self) -> str:
        return self.title


class PLVideo(Video):

    def __init__(self, video_id, pl_id):
        super().__init__(video_id)
        self.pl_id = pl_id