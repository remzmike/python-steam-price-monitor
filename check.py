# http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml
import urllib2, sys, os, socket
from datetime import datetime
from bs4 import BeautifulSoup
libpath = os.path.join(os.getcwd(), '..\lib')
sys.path.append(libpath)
from kmessage import send_message

def discount(price, discount):
    return price * (1-discount)
assert discount(9.99, .25) == 7.4925

# a bunch of ways to verify we got a valid page
# <a href="http://store.steampowered.com/login/?redir=app%2F236090">
# <a href="http://store.steampowered.com/share/twitter/app/236090"
# <a href="http://store.steampowered.com/share/reddit/app/236090"
# <a class="linkbar" href="http://steamcommunity.com/app/236090/discussions/">
# <a class="linkbar" href="http://steamcommunity.com/stats/236090/achievements">
# <a class="linkbar" href="http://store.steampowered.com/news/?feed=steam_updates&appids=236090">
# <a class="linkbar" href="http://store.steampowered.com/news/?appids=236090">

watchlist = [
#    # alex stuff
#    (  7200, discount(29.99, .50), 'trackmania united'), # removed in favor of trackmania 2
#    #(228760, discount(19.99, .25), 'trackmania 2 canyon'), # still on here, in case i want a copy
#    #(232910, discount( 9.99, .25), 'trackmania 2 stadium'),
#    #(233450, discount(29.99, .50), 'prison architect'), # not really for alex imo
#    # my stuff
#    (224440, discount(19.99, .30), 'folk tale'),
#    (233980, discount( 7.99, .50), 'unepic'),
#    (238240, discount(11.99, .50), 'edge of space'),          
#    (241410, discount( 9.99, .30), 'castlestorm'),      
#    (225280, discount(19.99, .50), 'full mojo rampage'),      
#    (244710, discount( 9.99, .50), 'shelter'),      
#    (231160, discount(14.99, .75), 'the swapper'),
#    (250110, discount(14.99, .50), 'assault android cactus'),
    (218820, discount(14.99, .50), 'mercenary kings'),    
#    (222640, discount(20.99, .70), 'aarklash'), # will buy at 70%+, was 40% at 2013 xmas
    (219830, discount(9.99, .50), 'king arthurs gold'),    
#    # delver's drop, not on steam yet, greenlight
#    # assault android cactus, not on steam yet, greenlight
]

def is_work():
    return socket.gethostname().lower() in ['mkesl','ganymede']   

def get_price_and_html(appid):

    url = 'http://store.steampowered.com/app/{0}/'.format(appid)
    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', 'birthtime=378720001')) # yay. age check bypass
    html = opener.open(url).read()

    # 2013-06-11 : finally, verification that this is the proper page response
    verify = '<a href="http://store.steampowered.com/login/?redir=app%2F{0}">'.format(appid)
    if not verify in html:
        return None, html
        
    soup = BeautifulSoup(html, "lxml")
    pricediv = soup.find(itemprop='price')

    price = pricediv.string.strip()
    assert price.startswith('$')
    price = price[1:]
    price = float(price)
    
    assert type(price) == float
    return price, html

def main(msg=None):
    if msg!=None:
        send_message(msg, 'steamprice')

    for appid, target, name in watchlist:
        actual, html = get_price_and_html(appid)
        ts = datetime.now().isoformat().replace(':','.')
        if actual == None:
            msg = 'no result, {0} cost is unknown, logged invalid html'.format(name)
            print msg
            mkdir('html')            
            fn = 'html/{0}#{1}#invalid'.format(ts, name, actual)
            save_file(fn, html)
        elif actual <= target + .01: # add a penny for safety
            msg = '"{0}" is currently on sale for ${1:.2f}'.format(name, actual)
            print msg
            send_message(msg, 'steamprice')
            mkdir('html')
            fn = 'html/{0}#{1}#{2}#valid'.format(ts, name, actual)
            save_file(fn, html)
        else:            
            msg = 'no result, {0} costs ${1:.2f}, target cost is ${2:.2f} or less'.format(name, actual, target)
            print msg
            #send_message(msg, 'steamprice')

def mkdir(s):
    if not os.path.isdir(s):
        os.mkdir(s)

def save_file(fn, s):
    with open(fn, 'w') as f:
        f.write(s)

# ---
# http://code.activestate.com/recipes/496767/
def setpriority(pid=None,priority=1):
    """ Set The Priority of a Windows Process.  Priority is a value between 0-5 where
        2 is normal priority.  Default sets the priority of the current
        python process but can take any valid process ID. """
        
    import win32api,win32process,win32con
    
    priorityclasses = [win32process.IDLE_PRIORITY_CLASS,
                       win32process.BELOW_NORMAL_PRIORITY_CLASS,
                       win32process.NORMAL_PRIORITY_CLASS,
                       win32process.ABOVE_NORMAL_PRIORITY_CLASS,
                       win32process.HIGH_PRIORITY_CLASS,
                       win32process.REALTIME_PRIORITY_CLASS]
    if pid == None:
        pid = win32api.GetCurrentProcessId()
    handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
    win32process.SetPriorityClass(handle, priorityclasses[priority])

if __name__=='__main__':
    if is_work():
        if False:
            item = list(watchlist[0])
            item[1] = 50 # megaprice
            item = tuple(item)
            watchlist = [item]
    setpriority()
    main()