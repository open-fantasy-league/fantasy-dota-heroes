from fantasydota import DBSession
from fantasydota.models import Hero
from pyramid.view import view_config


@view_config(route_name="hero", renderer="json")
def hero(request):
    session = DBSession()
    week = int(request.params.get('week', '1'))
    hero_values = session.query(Hero).filter(Hero.league == week).all()
    return {'week': week, 'heroes': hero_values}