from pytube import YouTube


def download_video(video_url: str):
    video = YouTube(video_url)
    video = video.streams.get_lowest_resolution()
    video.download('./videos')
    return video
