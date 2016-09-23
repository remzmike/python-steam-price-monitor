# http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml
from bs4 import BeautifulSoup
import urllib

#url = 'http://store.steampowered.com/app/209190/' # stealth bastard
url = 'http://store.steampowered.com/app/205100/' # dishonored

if False:
    html = '''
    		<div class="game_purchase_action" itemprop="offers" itemscope itemtype="http://schema.org/Offer">
    						<div class="game_purchase_action_bg">
    																			<div class="game_purchase_price price"  itemprop="price">
    							&#36;9.99						</div>
    													<div class="btn_addtocart">
    					<div class="btn_addtocart_left"></div>
    					 
    						<a class="btn_addtocart_content" href="javascript:addToCart( 18344);">Add to Cart</a>
    										<div class="btn_addtocart_right"></div>
    				</div>
    			</div>
    		</div>
    '''
else:
    html = urllib.urlopen(url).read()

#soup = BeautifulSoup(html)
#soup = BeautifulSoup(html, "html5lib")
soup = BeautifulSoup(html, "lxml")

# list
pricediv = soup.find(itemprop='price')

price = pricediv.string.strip()
assert price.startswith('$')
price = price[1:]

print price

