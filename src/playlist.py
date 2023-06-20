import os
from googleapiclient.discovery import build
import isodate
from datetime import timedelta


class PlayList:
    """Класс для плейлиста"""

    api_key: str = os.getenv('YT_API_KEY')  # берет значение переменной окружения
    youtube: str = build('youtube', 'v3', developerKey=api_key)  # создает объект для работы с API

    def __init__(self, playlist_id: str) -> None:
        """Экземпляр инициализируется по id видео """
        self.playlist_id: str = playlist_id  # id плейлиста

        # Получаем данные о плейлисте по api
        playlist: dict = self.youtube.playlistItems().list(playlistId=self.playlist_id, part='snippet,contentDetails', maxResults=50,).execute()
        # Получаем данные о видео в плейлисте по api
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist['items']]
        video_response: object = self.youtube.videos().list(part='contentDetails,statistics', id=','.join(video_ids)).execute()
        duration = timedelta(0)  # задаем переменную для расчета суммарной длительности плейлиста
        best_count_of_likes = 0  # переменная для поиска максимального числа лайков видео
        # Суммируем длительность всех видео и ищем самое популярное видео:
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']  # in ISO 8601 format
            duration += isodate.parse_duration(iso_8601_duration)  # in timedelta format
            likes_count = int(video['statistics']['likeCount'])
            if likes_count > best_count_of_likes:
                best_count_of_likes = likes_count
                self.best_video_link = f"https://youtu.be/{video['id']}"  # формируем ссылку на самое популярное видео

        # Создаём необходимые атрибуты
        self.title: str = playlist['items'][0]['snippet']['title']  # название плейлиста
        self.url: str = f"https://www.youtube.com/playlist?list={playlist['items'][0]['snippet']['playlistId']}"  # ссылка на плейлист
        self.__total_duration = duration  # суммарная длительность плейлиста

    @property
    def total_duration(self) -> timedelta:
        """Возвращает объект класса datetime.timedelta с суммарной длительностью плейлиста """
        return self.__total_duration

    def show_best_video(self) -> str:
        """Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)"""
        return self.best_video_link