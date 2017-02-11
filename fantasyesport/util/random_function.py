import calendar
import datetime


def add_months(sourcedate,months):
    month = sourcedate.month - 1 + months
    year = int(sourcedate.year + month / 12 )
    month = month % 12 + 1
    day = min(sourcedate.day,calendar.monthrange(year,month)[1])
    return datetime.date(year,month,day)


def bprint(boring_string):
    print "-_______---___-----_---_---_-__--_-------_--__---_--_-__--__-"
    print boring_string
    print "---___--__--_--_--__--_---------___---_----_---_--_---__---_--__--"

