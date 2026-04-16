SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR3OtmgAYtqeTFqohCHU_jtr-4ml_YJvWTyElPtgjMVERcE2K9freCbwEslfQcgzEYA4g7UgR13OAZW/pub?gid=0&single=true&output=csv"


def get_drive_id(url: str | None) -> str | None:
    """Извлекает Google Drive file ID из ссылки вида /d/<id>/ или ?id=<id>."""
    if not url:
        return None
    if '/d/' in url:
        return url.split('/d/')[1].split('/')[0]
    if 'id=' in url:
        return url.split('id=')[1].split('&')[0]
    return None
