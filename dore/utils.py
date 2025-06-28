from datetime import datetime, timezone

def format_datetime(dt: datetime, fmt: str = "%d/%m/%Y %H:%M") -> str:
    """
    Formata um objeto datetime para string formatada.
    Retorna string vazia se dt for None.
    """
    if dt is None:
        return ""
    return dt.strftime(fmt)

def now_utc() -> datetime:
    """
    Retorna o datetime atual em UTC com timezone awareness.
    """
    return datetime.now(timezone.utc)

def duration_in_hours(start: datetime, end: datetime) -> float:
    """
    Calcula a duração entre duas datas em horas (float).
    Retorna 0 se alguma data for None ou end < start.
    """
    if not start or not end or end < start:
        return 0
    delta = end - start
    return delta.total_seconds() / 3600

def sanitize_tags(tags_str: str) -> list[str]:
    """
    Recebe uma string de tags separadas por vírgula e retorna lista limpa, sem espaços e vazios.
    Ex: " limpeza, jardinagem ,  " -> ["limpeza", "jardinagem"]
    """
    if not tags_str:
        return []
    return [tag.strip() for tag in tags_str.split(",") if tag.strip()]
