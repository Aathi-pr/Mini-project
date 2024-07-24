def connectdb():
    import pymysql
    con = pymysql.connect(host="adithyan01.mysql.pythonanywhere-services.com", user="adithyan01", passwd="qwerty@1234", database="adithyan01$tuktukbase")
    return con

def currentDate():
    import datetime

    now = datetime.datetime.now()

    year = now.year
    month = now.month
    day = now.day

    CurrentData = str(year) + "-" + str(month) + "-" + str(day)

    return CurrentData

# def currentTime():
#     from django.utils import timezone

#     current_time = timezone.now().time()
#     return current_time

