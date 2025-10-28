import datetime

def format_time():
    """Devuelve la hora actual formateada."""
    return datetime.datetime.now().strftime("%H:%M:%S")

def format_username(user):
    """Devuelve un nombre limpio de usuario."""
    return f"{user.name}#{user.discriminator}"
