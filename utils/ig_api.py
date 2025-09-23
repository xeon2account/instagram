import requests

def fetch_ig_media(url):
    api_url = f"https://api-aswin-sparky.koyeb.app/api/downloader/igdl?url={url}"
    response = requests.get(api_url)
    return response.json()
