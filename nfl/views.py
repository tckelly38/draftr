#Embedded file name: /home/gobelogic/public_html/mysite/nfl/views.py
from django.shortcuts import render_to_response
import nfldb
import requests
from django.http import HttpResponse

def qb(request):
    """
     Passing Yards: 1 point per 25 yards passing
     Passing Touchdowns: 4 points
     Interceptions: -2 points
     Rushing Yards: 1 point per 10 yards
     Rushing Touchdowns: 6 points
     Receiving Yards: 1 point per 10 yards
     Receiving Touchdowns: 6 points
     Fumble Recovered for a Touchdown: 6 points
     2-Point Conversions: 2 points
     Fumbles Lost: -2 points
    """	
    #initialization of variables
    db = nfldb.connect()
    q = nfldb.Query(db)
    r = nfldb.Query(db)
    s = nfldb.Query(db)
    pos = 'QB'
    statToSortBy = 'passing_yds'
    curSType, curYear, curWeek = nfldb.current(db)
    lastWeek = curWeek - 1
    #initialization of arrays
    qbPastFive = []
    qbCurYear = []
    qbPastWeek = []

    #query of past five years
    q.game(season_year=range(2009, curYear), season_type='Regular')    
    qbPastFive = query(q, qbPastFive, pos, statToSortBy)
    
    #query of cur year	
    r.game(season_year=curYear, week=range(1, curWeek), season_type='Regular')
    qbCurYear = query(r, qbCurYear, pos, statToSortBy)
    
    
    #query last weeks data
    s.game(season_type=curSType, season_year=curYear, week=lastWeek)
    qbPastWeek = query(s, qbPastWeek, pos, statToSortBy)
    
    #return via django 
    return render_to_response('qb.html', {'qbPastFive': qbPastFive,
     'qbCurYear': qbCurYear,
     'qbPastWeek': qbPastWeek, 
     'lastWeek': lastWeek,
     'curYear': curYear})

def query(q, posArray, pos, statToSortBy):
    #select 'pos'
    q.player(position=pos).player
    #build array based on stat that would deem the best player (ie. passing_yds is a good indicator how well a QB is doing)
    for pp in q.sort(statToSortBy).limit(35).as_aggregate():
        posArray.append(pp)
    #change unneccesary attribute for pos and alter it with fantasy point algorithm
    posArray = calcFantasyPoints(posArray)
    return posArray
def kQuery(q, posArray, pos, statToSortBy):
   #select 'pos'
    q.player(position=pos).player
    #build array based on stat that would deem the best player (ie. passing_yds is a good indicator how well a QB is doing)
    for pp in q.sort(statToSortBy).limit(35).as_aggregate():
        posArray.append(pp)
    #change unneccesary attribute for pos and alter it with fantasy point algorithm
    posArray =KcalcFantasyPoints(posArray)
    return posArray
def truncate(f, n):
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
       return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])
def KcalcFantasyPoints(posArray):
    for pp in posArray:
        pp.punting_blk = (pp.passing_yds / 25) + (pp.passing_tds * 4) - (pp.passing_int * 2) + (pp.rushing_tds * 6) + (pp.rushing_yds / 10)+(pp.receiving_yds / 10) + (pp.receiving_tds * 6) + (pp.rushing_twoptm * 2) + (pp.receiving_twoptm * 2) + (pp.passing_twoptm * 2)+ (pp.kicking_xpmade)
        #avg fg made
        if pp.kicking_fga == 0 or pp.kicking_fgm == 0:
            print "."
        else:
            pp.defense_safe = truncate(((pp.kicking_fgm * 1.0) / pp.kicking_fga), 2) 
            pp.defense_tkl = truncate(((pp.kicking_fgm_yds * 1.0) / pp.kicking_fgm), 2)
    return posArray

	
def calcFantasyPoints(posArray):
    #need to add all components 
    """
     Offensive:
     Passing Yards: 1 point per 25 yards passing
     Passing Touchdowns: 4 points
     Interceptions: -2 points
     Rushing Yards: 1 point per 10 yards
     Rushing Touchdowns: 6 points
     Receiving Yards: 1 point per 10 yards
     Receiving Touchdowns: 6 points
     Fumble Recovered for a Touchdown: 6 points
     2-Point Conversions: 2 points
     Fumbles Lost: -2 points
   
     KICKING

     PAT Made: 1 point
     FG Made (0-49 yards): 3 points
     FG Made (50+ yards): 5 points

     DEFENSE TEAM

     Sacks: 1 point
     Interceptions: 2 points
     Fumbles Recovered: 2 points
     Safeties: 2 points
     Defensive Touchdowns: 6 points
     Kick and Punt Return Touchdowns: 6 points
     Points Allowed (0): 10 points
     Points Allowed (1-6): 7 points
     Points Allowed (7-13): 4 points
     Points Allowed (14-20): 1 points
     Points Allowed (21-27): 0 points
     Points Allowed (28-34): -1 points
     Points Allowed (35+): -4 points


     """
    #need to add kicking attributes and defence
    for pp in posArray:
        pp.punting_blk = (pp.passing_yds / 25) + (pp.passing_tds * 4) - (pp.passing_int * 2) + (pp.rushing_tds * 6) + (pp.rushing_yds / 10)+(pp.receiving_yds / 10) + (pp.receiving_tds * 6) + (pp.rushing_twoptm * 2) + (pp.receiving_twoptm * 2) + (pp.passing_twoptm * 2)+ (pp.kicking_xpmade)
    return posArray

def defense(request):       
    return render_to_response('defense.html')

def index(request):
    return render_to_response('home.html')

def rb(request):
    """
     Passing Yards: 1 point per 25 yards passing
     Passing Touchdowns: 4 points
     Interceptions: -2 points
     Rushing Yards: 1 point per 10 yards
     Rushing Touchdowns: 6 points
     Receiving Yards: 1 point per 10 yards
     Receiving Touchdowns: 6 points
     Fumble Recovered for a Touchdown: 6 points
     2-Point Conversions: 2 points
     Fumbles Lost: -2 points
    """
    #initialization of variables
    db = nfldb.connect()
    q = nfldb.Query(db)
    r = nfldb.Query(db)
    s = nfldb.Query(db)
    pos = 'RB'
    statToSortBy = 'rushing_yds'
    curSType, curYear, curWeek = nfldb.current(db)
    lastWeek = curWeek - 1
    #initialization of arrays
    rbPastFive = []
    rbCurYear = []
    rbPastWeek = []

    #query of past five years
    q.game(season_year=range(2009, curYear), season_type='Regular')
    rbPastFive = query(q, rbPastFive, pos, statToSortBy)
	
    #query of cur year
    r.game(season_year=curYear, week=range(1, curWeek), season_type='Regular')
    rbCurYear = query(r, rbCurYear, pos, statToSortBy)


    #query last weeks data
    s.game(season_type=curSType, season_year=curYear, week=lastWeek)
    rbPastWeek = query(s, rbPastWeek, pos, statToSortBy)

    #return via django
    return render_to_response('rb.html', {'rbPastFive': rbPastFive,
     'rbCurYear': rbCurYear,
     'rbPastWeek': rbPastWeek,
     'lastWeek': lastWeek,
     'curYear': curYear})

def fb(request):
    """
     Passing Yards: 1 point per 25 yards passing
     Passing Touchdowns: 4 points
     Interceptions: -2 points
     Rushing Yards: 1 point per 10 yards
     Rushing Touchdowns: 6 points
     Receiving Yards: 1 point per 10 yards
     Receiving Touchdowns: 6 points
     Fumble Recovered for a Touchdown: 6 points
     2-Point Conversions: 2 points
     Fumbles Lost: -2 points
    """
    #initialization of variables
    db = nfldb.connect()
    q = nfldb.Query(db)
    r = nfldb.Query(db)
    s = nfldb.Query(db)
    pos = 'FB'
    statToSortBy = 'rushing_yds'
    curSType, curYear, curWeek = nfldb.current(db)
    lastWeek = curWeek - 1
    #initialization of arrays
    fbPastFive = []
    fbCurYear = []
    fbPastWeek = []

    #query of past five years
    q.game(season_year=range(2009, curYear), season_type='Regular')
    fbPastFive = query(q, fbPastFive, pos, statToSortBy)
	
    #query of cur year
    r.game(season_year=curYear, week=range(1, curWeek), season_type='Regular')
    fbCurYear = query(r, fbCurYear, pos, statToSortBy)


    #query last weeks data
    s.game(season_type=curSType, season_year=curYear, week=lastWeek)
    fbPastWeek = query(s, fbPastWeek, pos, statToSortBy)

    #return via django
    return render_to_response('fb.html', {'fbPastFive': fbPastFive,
     'fbCurYear': fbCurYear,
     'fbPastWeek': fbPastWeek,
     'lastWeek': lastWeek,
     'curYear': curYear})
	 
	 
def wr(request):
    """
     Passing Yards: 1 point per 25 yards passing
     Passing Touchdowns: 4 points
     Interceptions: -2 points
     Rushing Yards: 1 point per 10 yards
     Rushing Touchdowns: 6 points
     Receiving Yards: 1 point per 10 yards
     Receiving Touchdowns: 6 points
     Fumble Recovered for a Touchdown: 6 points
     2-Point Conversions: 2 points
     Fumbles Lost: -2 points
    """
    #initialization of variables
    db = nfldb.connect()
    q = nfldb.Query(db)
    r = nfldb.Query(db)
    s = nfldb.Query(db)
    pos = 'WR'
    statToSortBy = 'receiving_yds'
    curSType, curYear, curWeek = nfldb.current(db)
    lastWeek = curWeek - 1
    #initialization of arrays
    wrPastFive = []
    wrCurYear = []
    wrPastWeek = []

    #query of past five years
    q.game(season_year=range(2009, curYear), season_type='Regular')
    wrPastFive = query(q, wrPastFive, pos, statToSortBy)
	
    #query of cur year
    r.game(season_year=curYear, week=range(1, curWeek), season_type='Regular')
    wrCurYear = query(r, wrCurYear, pos, statToSortBy)


    #query last weeks data
    s.game(season_type=curSType, season_year=curYear, week=lastWeek)
    wrPastWeek = query(s, wrPastWeek, pos, statToSortBy)

    #return via django
    return render_to_response('wr.html', {'wrPastFive': wrPastFive,
     'wrCurYear': wrCurYear,
     'wrPastWeek': wrPastWeek,
     'lastWeek': lastWeek,
     'curYear': curYear})
	 
def te(request):
    """
     Passing Yards: 1 point per 25 yards passing
     Passing Touchdowns: 4 points
     Interceptions: -2 points
     Rushing Yards: 1 point per 10 yards
     Rushing Touchdowns: 6 points
     Receiving Yards: 1 point per 10 yards
     Receiving Touchdowns: 6 points
     Fumble Recovered for a Touchdown: 6 points
     2-Point Conversions: 2 points
     Fumbles Lost: -2 points
    """
    #initialization of variables
    db = nfldb.connect()
    q = nfldb.Query(db)
    r = nfldb.Query(db)
    s = nfldb.Query(db)
    pos = 'TE'
    statToSortBy = 'receiving_yds'
    curSType, curYear, curWeek = nfldb.current(db)
    lastWeek = curWeek - 1
    #initialization of arrays
    tePastFive = []
    teCurYear = []
    tePastWeek = []

    #query of past five years
    q.game(season_year=range(2009, curYear), season_type='Regular')
    tePastFive = query(q, tePastFive, pos, statToSortBy)
	
    #query of cur year
    r.game(season_year=curYear, week=range(1, curWeek), season_type='Regular')
    teCurYear = query(r, teCurYear, pos, statToSortBy)


    #query last weeks data
    s.game(season_type=curSType, season_year=curYear, week=lastWeek)
    tePastWeek = query(s, tePastWeek, pos, statToSortBy)

    #return via django
    return render_to_response('te.html', {'tePastFive': tePastFive,
     'teCurYear': teCurYear,
     'tePastWeek': tePastWeek,
     'lastWeek': lastWeek,
     'curYear': curYear})
	 
def kicker(request):
    """
     PAT Made: 1 point
     FG Made (0-49 yards): 3 points
     FG Made (50+ yards): 5 points
    """
    #initialization of variables
    db = nfldb.connect()
    q = nfldb.Query(db)
    r = nfldb.Query(db)
    s = nfldb.Query(db)
    pos = 'K'
    statToSortBy = 'kicking_fgm'
    curSType, curYear, curWeek = nfldb.current(db)
    lastWeek = curWeek - 1
    #initialization of arrays
    kickerPastFive = []
    kickerCurYear = []
    kickerPastWeek = []

    #query of past five years
    q.game(season_year=range(2009, curYear), season_type='Regular')
    kickerPastFive = kQuery(q, kickerPastFive, pos, statToSortBy)
	
    #query of cur year
    r.game(season_year=curYear, week=range(1, curWeek), season_type='Regular')
    kickerCurYear = kQuery(r, kickerCurYear, pos, statToSortBy)


    #query last weeks data
    s.game(season_type=curSType, season_year=curYear, week=lastWeek)
    kickerPastWeek = kQuery(s, kickerPastWeek, pos, statToSortBy)

    #return via django
    return render_to_response('kicker.html', {'kickerPastFive': kickerPastFive,
     'kickerCurYear': kickerCurYear,
     'kickerPastWeek': kickerPastWeek,
     'lastWeek': lastWeek,
     'curYear': curYear})

