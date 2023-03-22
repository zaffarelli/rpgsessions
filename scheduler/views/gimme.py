from scheduler.utils.mechanics import FMT_DATE, DOWS
from scheduler.utils.mechanics import oudin, MONTHS_COLORS
from datetime import datetime, date, timedelta


def gimme_new_session(request, param):
    from scheduler.models.session import Session
    s = Session()
    s.title = f'Nouvelle Partie'
    s.mj = request.user.profile
    s.date_start = date.fromisoformat(param.replace('_', '-'))
    s.save()
    context = {'session': s}
    return context


def gimme_session(request, s):
    context = s.to_json
    context['episode_tag'] = s.episode_tag
    context['user_wanted'] = s.wanted_list
    context['max_players'] = s.max_players
    context['code_link'] = s.code_link
    context['mj'] = gimme_profile(s.mj.id)
    if s.campaign:
        context['campaign'] = s.campaign.to_json
    if s.game:
        context['game'] = gimme_game(s.game)
    context['inscriptions'] = gimme_inscriptions(s)
    if request:
        context['owner'] = (s.mj == request.user.profile)
        context['user_requested'] = str(request.user.profile.id) in s.wanted.split(';')
    context['user_subscribed'] = False
    return context


def gimme_spot(request, s):
    context = s.to_json
    context['episode_tag'] = s.session.episode_tag
    context['user_wanted'] = s.session.wanted_list
    context['max_players'] = s.session.max_players
    context['mj'] = gimme_profile(s.session.mj.id)
    if s.campaign:
        context['campaign'] = s.session.campaign.to_json
    if s.game:
        context['game'] = gimme_game(s.session.game)
    context['inscriptions'] = gimme_inscriptions(s.session)
    if request:
        context['owner'] = (s.session.mj == request.user.profile)
        context['user_requested'] = str(request.user.profile.id) in s.session.wanted.split(';')
    context['user_subscribed'] = False
    return context


def gimme_game(g):
    context = g.to_json
    context['artefact'] = g.svg_artefact
    context['mj'] = gimme_profile(g.mj.id)
    return context


def gimme_profile(x):
    from scheduler.models.profile import Profile
    context = {'Status': f'The parameter {x} is not a user profile id'}
    elems = Profile.objects.filter(pk=x)
    if len(elems) == 1:
        elem = elems.first()
        if isinstance(elem, Profile):
            context = elem.to_json
            context['status'] = "ok"
            # context['silhouette_symbol'] = elem.silhouette_symbol
            # context['shield_symbol'] = elem.shield_symbol
            # context['shieldstyle_display'] = elem.get_shieldstyle_display()
            # context['iconstyle_display'] = elem.get_iconstyle_display()
            # context['artefact'] = elem.build_svg_artefact()
            context['face_artefact'] = elem.build_face_artefact()
            context['games_run'] = elem.games_run
            context['games_played'] = elem.games_played

    return context


def gimme_profile_sober(elem):
    from scheduler.models.profile import Profile

    context = {'Status': f'The parameter {elem} is not a user profile'}
    # print(elem)
    if isinstance(elem, Profile):
        context = elem.to_json
        context['status'] = "ok"
        # context['silhouette_symbol'] = elem.silhouette_symbol
        # context['shield_symbol'] = elem.shield_symbol
        # context['shieldstyle_display'] = elem.get_shieldstyle_display()
        # context['iconstyle_display'] = elem.get_iconstyle_display()
        # context['artefact'] = elem.build_svg_artefact()
        context['face_artefact'] = elem.build_face_artefact()
        # context['games_run'] = elem.games_run
        # context['games_played'] = elem.games_played
    return context


def gimme_campaign(x):
    from scheduler.models.campaign import Campaign
    c = Campaign.objects.get(pk=x)
    context = c.to_json
    context['game'] = gimme_game(c.game)
    context['wanted_list'] = c.wanted_list
    context['mj'] = gimme_profile(c.mj.id)
    context['episodes'] = c.sessions_summary
    return context


def gimme_profile_campaigns(x):
    from scheduler.models.campaign import Campaign
    from scheduler.models.profile import Profile
    p = Profile.objects.get(pk=x)
    campaigns = Campaign.objects.filter(mj=p)
    camps = []
    for x in campaigns:
        camps.append(gimme_campaign(x.id))
    return camps


def gimme_profile_games(x):
    from scheduler.models.game import Game
    from scheduler.models.profile import Profile
    p = Profile.objects.get(pk=x)
    games = Game.objects.filter(mj=p).order_by('name')
    gs = []
    for g in games:
        gs.append(gimme_game(g))
    return gs


def gimme_profile_propositions(request, x):
    from scheduler.models.session import Session
    from scheduler.models.profile import Profile
    p = Profile.objects.get(pk=x)
    sessions = Session.objects.filter(mj=p, date_start=None)
    props = []
    for s in sessions:
        props.append(gimme_session(request, s))
    return props


def gimme_all_propositions(request, x):
    from scheduler.models.session import Session
    from scheduler.models.profile import Profile
    p = Profile.objects.get(pk=x)
    sessions = Session.objects.filter(date_start=None, is_visible=True)
    props = []
    for s in sessions:
        props.append(gimme_session(request, s))
    return props


def gimme_inscriptions(s):
    inscriptions = []
    for i in s.inscription_set.all().order_by('profile__user_id'):
        inscriptions.append(gimme_profile(i.profile.id))
    return inscriptions


def gimme_new_campaign(request, param):
    from scheduler.models.campaign import Campaign
    s = Campaign()
    s.title = f'Nouvelle campagne'
    s.mj = request.user.profile
    s.save()
    context = {'session': s}
    return context


def gimme_day(request, d):
    is_current_day = (d.strftime(FMT_DATE) == datetime.today().strftime(FMT_DATE))
    day_body = {}
    day_body['sessions'] = gimme_sessions_of_the_day(request, d)
    # f'{DOWS[d.weekday()]}<BR/><small>{d.strftime(FMT_DATE_PRETTY)}</small>'

    day_off = False
    off_message = ''
    if d.weekday() > 4:  # Weekend
        day_off = True
    if (oudin(d) + timedelta(days=1)).strftime(FMT_DATE) == d.strftime(FMT_DATE):  # Lundi de Pâques
        day_off = True
        off_message = 'Pâques'
    if (oudin(d) + timedelta(days=50)).strftime(FMT_DATE) == d.strftime(FMT_DATE):  # Pentecôte
        day_off = True
        off_message = 'Pentecôte'
    if (oudin(d) + timedelta(days=39)).strftime(FMT_DATE) == d.strftime(FMT_DATE):  # Ascension
        day_off = True
        off_message = 'Ascension'
    if d.strftime("%d/%m") == '15/08':  # Assomption
        day_off = True
        off_message = 'Assomption'
    if d.strftime("%d/%m") == '01/11':  # Toussaint
        day_off = True
        off_message = 'Toussaint'
    if d.strftime("%d/%m") == '14/07':  # Bastille
        day_off = True
        off_message = 'Bastille'
    if d.strftime("%d/%m") == '25/12':  # Noël
        day_off = True
        off_message = 'Noël'
    if d.strftime("%d/%m") == '01/01':  # Premier de l'an
        day_off = True
        off_message = "Jour de l'an"
    if d.strftime("%d/%m") == '11/11':  # Armistice
        day_off = True
        off_message = "Arm. 1918"
    if d.strftime("%d/%m") == '08/05':  # Armistice
        day_off = True
        off_message = "Arm. 1945"
    day_info = f"<div class='dia'>{DOWS[d.weekday()][:3]}</div><div class='dib'><i class='fas fa-eye'></i><br/>{off_message}</div><div class='dic'>{d.strftime('%d')}</div>"

    context = {'day_info': day_info,
               'day_off': day_off,
               'off_message': off_message,
               'current_day': is_current_day,
               'day': d.strftime(FMT_DATE),
               'day_body': day_body,
               'month_color': MONTHS_COLORS[d.month - 1]
               }
    context['availabilities'] = gimme_all_availabilities(request, d, request.user.profile.id)
    return context


def gimme_sessions_of_the_day(request, d):
    from scheduler.models.session import Session
    all = Session.objects.filter(date_start=d).order_by('time_start')
    sessions = []
    for s in all:
        sessions.append(gimme_session(request, s))
    return sessions


def gimme_spots_of_the_day(request, d):
    from scheduler.models.spot import Spot
    all = Spot.objects.filter(date_start=d).order_by('time_start')
    spots = []
    for s in all:
        spots.append(gimme_spot(request, s))
    return spots


def gimme_all_availabilities(request, d, id):
    from scheduler.models.availability import Availability
    from scheduler.models.follower import Follower
    context = {}
    availables = []
    absents = []
    absents_title = []
    availables_title = []
    my_followers = []
    all_followers = Follower.objects.filter(profile__user_id=id)
    for f in all_followers:
        my_followers.append(f.target.id)
    here_entries = Availability.objects.filter(when=d, absent_mode=False)

    availables_count = 0
    absents_count = 0

    for here in here_entries:
        if here.profile.id in my_followers:
            availables.append(gimme_profile(here.profile.id))
            availables_title.append(gimme_profile(here.profile.id)['nickname'])
            availables_count += 1
    off_entries = Availability.objects.filter(when=d, absent_mode=True)
    # if len(off_entries) > 0:
    #     print(all_followers, my_followers, off_entries)
    for off in off_entries:
        if off.profile.id in my_followers:
            absents.append(gimme_profile(off.profile.id))
            absents_title.append(gimme_profile(off.profile.id)['nickname'])
            absents_count += 1

    context['availables'] = availables
    context['availables_count'] = availables_count
    context['absents'] = absents
    context['absents_count'] = absents_count
    if len(absents_title) > 0:
        context['absents_title'] = "Absent(es): " + ', '.join(absents_title)
    else:
        context['absents_title'] = 'Rien à signaler'
    if len(availables_title) > 0:
        context['availables_title'] = "Disponible(s): " + ', '.join(availables_title)
    else:
        context['availables_title'] = 'Rien à signaler'
    return context


def gimme_set_followers(id):
    from scheduler.models.follower import Follower
    from scheduler.models.profile import Profile
    f_list = []
    list = []
    it = Profile.objects.get(pk=id)
    all_profiles = Profile.objects.order_by('nickname')
    all_followers = Follower.objects.filter(profile=it)
    for f in all_followers:
        f_list.append(f.target.id)
    for p in all_profiles:
        list.append({'profile': gimme_profile(p.id), 'is_follower': p.id in f_list})
    return list
