from datetime import datetime


def footerDateGen():
    now = datetime.now()
    formatted_now = now.strftime("%m/%d/%Y %I:%M %p")
    formatted_now = formatted_now.replace(" 0", " ")
    return formatted_now
