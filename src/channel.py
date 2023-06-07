import json
import os

from googleapiclient.discovery import build
import isodate



class Channel:
    """Класс для ютуб-канала"""

    api_key = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id: str = channel_id
        self.channel = None

        self.channel: dict = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()

        self.title: str = self.channel['items'][0]['snippet']['title']  # название
        self.description: str = self.channel['items'][0]['snippet']['description']  # описание
        self.url: str = f"https://www.youtube.com/channel/{self.channel['items'][0]['id']}"  # ссылка
        self.subscriberCount: int = int(self.channel['items'][0]['statistics']['subscriberCount'])  # число подписчиков
        self.video_count: int = int(self.channel['items'][0]['statistics']['videoCount'])  # количество видео
        self.viewCount: int = int(self.channel['items'][0]['statistics']['viewCount'])  # просмотры

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls) -> object:
        """Возвращает объект для работы с YouTube API"""
        return cls.youtube

    def to_json(self, file_name) -> None:
        """Сохраняет в файл значения атрибутов экземпляра Channel"""
        dict = {"channel_id": self.channel_id,
                "title": self.title,
                "description": self.description,
                "url": self.url,
                "subscriberCount": self.subscriberCount,
                "videoCount": self.video_count,
                "viewCount": self.viewCount,
                }

        with open(file_name, "w") as outfile:
            json.dump(dict, outfile, ensure_ascii=False)
