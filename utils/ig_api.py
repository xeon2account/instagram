import requests

def fetch_ig_media(url: str):
    """
    Call the external API to get Instagram media download link.
    """
    API_ENDPOINT = "https://api-aswin-sparky.koyeb.app/api/downloader/igdl"
    try:
        resp = requests.get(API_ENDPOINT, params={"url": url}, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"[ERROR] API call failed: {e}")
        return {"status": False, "data": []}
