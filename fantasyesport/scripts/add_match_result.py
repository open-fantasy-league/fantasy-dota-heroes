import argparse
import time

import transaction
from fantasyesport.lib.session_utils import make_session
from fantasyesport.models import Result


def main():
    with transaction.manager:
        session = make_session()
        parser = argparse.ArgumentParser()
        parser.add_argument("set_", type=int, help="set")
        parser.add_argument("winner", type=int, help="winner")
        parser.add_argument("p1", type=int, help="p1")
        parser.add_argument("p2", type=int, help="p2")
        parser.add_argument("p3", type=int, nargs='?', help="p3")  # TODO make optional
        parser.add_argument("p4", type=int, nargs='?', help="p4")
        args = parser.parse_args()

        if args.winner > 2 or args.set_ > 5:
            print "Invalid arguments"
            return
        if args.winner == 1:
            if args.set_ == 3:
                if not (args.p3 and args.p4):
                    print "invalid arguments"
                    return
                session.add(Result(1, args.p1, 1, True, args.set_, time.time(), 1))
                session.add(Result(1, args.p2, 1, True, args.set_, time.time(), 1))
                session.add(Result(1, args.p3, 1, False, args.set_, time.time(), 1))
                session.add(Result(1, args.p4, 1, False, args.set_, time.time(), 1))
            else:
                session.add(Result(1, args.p1, 1, True, args.set_, time.time(), 1))
                session.add(Result(1, args.p2, 1, False, args.set_, time.time(), 1))
        else:
            if args.set_ == 3:
                session.add(Result(1, args.p1, 1, False, args.set_, time.time(), 1))
                session.add(Result(1, args.p2, 1, False, args.set_, time.time(), 1))
                session.add(Result(1, args.p3, 1, True, args.set_, time.time(), 1))
                session.add(Result(1, args.p4, 1, True, args.set_, time.time(), 1))
            else:
                session.add(Result(1, args.p1, 1, False, args.set_, time.time(), 1))
                session.add(Result(1, args.p2, 1, True, args.set_, time.time(), 1))
        transaction.commit()

if __name__ == "__main__":
    main()
