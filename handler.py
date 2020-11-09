from urllib import request
import logging
import re
log = logging.getLogger(__name__)

def get_html(url, user_agent):
    """
    Get raw HTML from a webpage URL
    """
    log.debug('Getting HTML from {url} with UA as {ua}'.format(url=url, ua=user_agent))
    req = request.Request(url, data=None, headers={ 'User-Agent': user_agent})
    html = request.urlopen(req).read().decode('utf-8').strip()
    log.debug('Retrieved HTML from {url} as {html}'.format(url=url, html=html))
    return html

def get_jackpot_value(html, reg):
    """
    Use regex to extract jackpotvalue from HTML
    """
    log.debug('Getting Jackpot value from HTML using regex: {reg}'.format(reg=reg))
    jackpot_value = re.search(reg, html).group(1)
    log.debug('Jackpot value retrieved from HTML: {jv}'.format(jv=jackpot_value))
    return jackpot_value

def jackpot_playable(jackpot_limit, jackpot_value):
    """
    If jackpot is above or equal to our limit we can play
    """
    num_jack = int(jackpot_value.replace(',',''))
    if num_jack >= jackpot_limit:
        title = 'Euromillions is ready to play!'
        msg_content = '<h2>{title} </h2> <font color="green">PLAY OK!</font></h2>\n'.format(title=title)
    else:
        title = 'Euromillions is not ready to play!'
        msg_content = '<h2>{title} </h2> <font color="red">Do not play!</font></h2>\n'.format(title=title)
    return msg_content



def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """
    Url = "https://www.lottery.ie/draw-games/euromillions"
    
    UserAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
    
    html = get_html(Url, UserAgent)

    Regex = "<div class=\"countdown-banner__prize prizeamount\">\n<span> €([0-9,]*?) million</span>"

    jack_val = get_jackpot_value(html, Regex)

    Limit = 100


    res = jackpot_playable(Limit, jack_val)

    return "<html><body>{res}</body></html>".format(res=res)
