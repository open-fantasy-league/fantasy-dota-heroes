import transaction
from fantasydota.lib.session_utils import make_session
from fantasydota.models import Hero, Result


def main():
    session = make_session()
    with transaction.manager:
        mvh = []
        heroes = session.query(Hero).all()
        for hero in heroes:
            points = 0
            value = hero.value
            results = session.query(Result).filter(Result.tournament_id == 4874).filter(Result.hero == hero.hero_id).filter(Result.date > 1481251149)
            for result in results:
                points += Result.result_to_value(result.result_str)

            valRatio = points / value
            mvh.append({"hero": hero.name, "ratio": valRatio, "points": points, "value": value})
        mvh = sorted(mvh, key=lambda x: x["ratio"], reverse=True)
        for i, entry in enumerate(mvh[:5]):
            print "Highest value heroes:"
            print "%s: %s with %s" % (i+1, entry["hero"], entry["ratio"])
        for i, entry in enumerate(sorted(mvh, key=lambda x: x["ratio"])[:5]):
            print "Worst value heroes:"
            print "%s: %s with %s" % (i+1, entry["hero"], entry["ratio"])

        # max_points = 0
        # mvh = list(filter(lambda x: x["points"] > 0, mvh))
        # for h1 in mvh:
        #     mvh2 = list(filter(lambda x: 50 - h1["value"] - x["value"] > 0, mvh))
        #     for h2 in mvh2:
        #         if h2["hero"] == h1["hero"]:
        #             continue
        #         mvh3 = list(filter(lambda x: 50 - h1["value"] - h2["value"] - x["value"] > 0, mvh2))
        #         for h3 in mvh3:
        #             if h3["hero"] in (h1["hero"], h2["hero"]):
        #                 continue
        #             mvh4 = list(filter(lambda x: 50 - h1["value"] - h2["value"] - h3["value"] - x["value"] > 0, mvh3))
        #             for h4 in mvh4:
        #                 if h4["hero"] in (h1["hero"], h2["hero"], h3["hero"]):
        #                     continue
        #                 mvh5 = list(filter(lambda x: 50 - h1["value"] - h2["value"] - h3["value"] - h4["value"]
        #                                              - x["value"] > 0, mvh4))
        #                 for h5 in mvh5:
        #                     totalval = h1["value"] + h2["value"] + h3["value"] + h4["value"] + h5["value"]
        #                     if h5["hero"] in (h1["hero"], h2["hero"], h3["hero"], h4["hero"]) or totalval > 50:
        #                         continue
        #                     points = h5["points"] + h1["points"] + h2["points"] + h3["points"] + h4["points"]
        #                     # if points > 195:
        #                     #     print "Points: %s" % points
        #                     #     print "Value: %s" % totalval
        #                     #     print "Heroes: %s, %s, %s, %s, %s" % (h1["hero"], h2["hero"], h3["hero"], h4["hero"],
        #                     #                                           h5["hero"])
        #                     if points > max_points:
        #                         max_points = points
        #                         print h1["value"], h2["value"], h3["value"], h4["value"], h5["value"]
        #                         print h1["points"], h2["points"], h3["points"], h4["points"], h5["points"]
        #                         print "Points: %s" % max_points
        #                         print "Value: %s" % totalval
        #                         print "Heroes: %s, %s, %s, %s, %s" % (h1["hero"], h2["hero"], h3["hero"], h4["hero"],
        #                             h5["hero"])


if __name__ == "__main__":
    main()
