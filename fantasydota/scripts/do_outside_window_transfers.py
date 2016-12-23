import urllib2
from operator import and_

import transaction
from fantasydota.lib.session_utils import make_session
from fantasydota.models import TeamHero, User


def main():
    session = make_session()
    with transaction.manager:
        thero_q = session.query(TeamHero).filter(and_(TeamHero.active == True, TeamHero.to_trade == True))
        for thero in thero_q.all():
            print "Deleting hero %s for user: %s" % (thero.hero, thero.user)
        thero_q.delete()
        thero_q_2 = session.query(TeamHero).filter(and_(TeamHero.active != True, TeamHero.to_trade == True))
        for thero in thero_q_2.all():
            print "Making active hero %s for user: %s" % (thero.hero, thero.user)
            thero.active = True
            thero.to_trade = False


        transaction.commit()
    response = urllib2.urlopen("https://www.fantasydota.eu/tran012345678901234567890looptheloop?state=open")  # open transfer window
    print response

if __name__ == "__main__":
    main()
