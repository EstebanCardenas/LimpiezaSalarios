import re
import unicodedata

unknown_cities = set()

def clean_city(city):
    city = str(city).strip().lower()

    # Clean city
    city = re.sub(r'\(.*\)', '', city) # Rm parenthesis
    city = re.sub(r'[\-/_]', ' ', city) # Change delimiters to spaces first
    city = re.sub(r'\.', '', city) # Rm periods
    city = unicodedata.normalize('NFKD', city).encode('ascii', 'ignore').decode('utf-8') # Remove accents
    city = re.sub(r'[^\w\s]', '', city) # Rm special characters
    city = re.sub(r'\s{2,}', ' ', city) # Rm extra spaces
    city = city.strip()
    if len(city) == 0 or len(city) == 1: return "Unknown"

    # Patterns for unknown values
    unknown_patterns = [
        r'\bn/a\b', r'\bn\sa\b', r'\bna\b', r'\bnan\b', r'anonymous', r'^-+$', r'^\d+$', r'^[\.]+\s*$', r'^/$', r'too small',
        r'can\'t', r'60k', r'prefer not to', r'^x+', r'\bidentifiable\b', r'\btoo\b', r'\bmuch\b',
    ]
    for pattern in unknown_patterns:
        if re.search(pattern, city):
            unknown_cities.add(city)
            return "Unknown"
    
    # Replace acronyms
    city_map = {
        'nyc': 'New York',
        'new york city': 'New York',
        'new york': 'New York',
        'ny': 'New York',
        'brooklyn': 'New York',
        'manhattan': 'New York',
        'sf': 'San Francisco',
        'sf bay': 'San Francisco',
        'sf bay area': 'San Francisco',
        'san francisco bay area': 'San Francisco',
        'la': 'Los Angeles',
        'dc': 'Washington D.C.',
        'washington dc': 'Washington D.C.',
        'washington': 'Washington D.C.',
        'milwaukee area': 'Milwaukee',
        'stlouis': 'St Louis',
        'st  louis': 'St Louis',
        'saint louis': 'St Louis',
        'seattle wa': 'Seattle',
        'seattle area': 'Seattle',
        'wfh': 'Remote',
        'honolilu': 'Honolulu',
        'philly': 'Philadelphia',
    }
    if city in city_map: return city_map[city]

    return city.title()

def clean_country(country):
    country = str(country).strip().lower()
    
    if not country: return None

    # Handle US flag emoji, not the letters "us"
    if '🇺🇸' in country:
        return 'United States'
    
    country = re.sub(r'\.', '', country) # Rm periods
    country = re.sub(r'>', '', country) # Rm greater than
    country = country.replace('\"', '') # Rm quotes
    country = unicodedata.normalize('NFKD', country).encode('ascii', 'ignore').decode('utf-8') # Remove accents and emojis
    country = re.sub(r'\s{2,}', ' ', country) # Rm extra spaces
    country = country.strip()
    
    if not country: return None

    # Handle invalid entries
    invalid_patterns = [
        r'^.?we\sdon\'?t.*$', r'^i\searn\scommission.*$',
        r'posted\soverseas.*', r'^contracts$', r'^global$', r'^international$', r'^remote$',
        r'^currently finance$', r'^uxz$', r'^y$', r'^1$', r'^na$', r'^policy$', r'^ss$',
        r'^dbfemf$', r'^ff$', r'^europe$', r'^africa$', r'^united y$',
        r'^n/a.*', r'^bonus based on.*', r'^\$.*deducted.*', r'^i was brought in.*',
        r'^loutreland.*'
    ]
    for pattern in invalid_patterns:
        if re.search(pattern, country):
            return None

    country_map = {
        'usa': 'United States',
        'us': 'United States',
        'u s': 'United States',
        'the us': 'United States',
        'the united states': 'United States',
        'america': 'United States',
        'usa-- virgin islands': 'United States',

        # US typos
        'usd': 'United States',
        'uss': 'United States',
        'usaa': 'United States',
        'united state': 'United States',
        'unite states': 'United States',
        'uniyes states': 'United States',
        'united statws': 'United States',
        'uniyed states': 'United States',
        'united stattes': 'United States',
        'united statesp': 'United States',
        'united statees': 'United States',
        'uniited states': 'United States',
        'unted states': 'United States',
        'united sates': 'United States',
        'united statea': 'United States',
        'uniteed states': 'United States',
        'united sttes': 'United States',
        'unitied states': 'United States',
        'untied states': 'United States',
        'united statues': 'United States',
        'united statew': 'United States',
        'uniter statez': 'United States',
        'united stateds': 'United States',
        'unitef stated': 'United States',
        'united statss': 'United States',
        'unites states': 'United States',
        'united status': 'United States',
        'united stated': 'United States',
        'united stares': 'United States',
        'unitedstates': 'United States',
        'united states of americas': 'United States',
        'united states of america': 'United States',
        'united states is america': 'United States',
        'united state of america': 'United States',
        'united states of american': 'United States',
        'united sates of america': 'United States',
        'us of a': 'United States',
        'is': 'United States',
        'isa': 'United States',
        'ua': 'United States',

        # US Regions/Cities to Country
        'california': 'United States',
        'san francisco': 'United States',
        'virginia': 'United States',
        'new york': 'United States',
        'hartford': 'United States',
        
        # Complex US mappings
        'us govt employee overseas, country withheld': 'United States',
        'i work for a uae-based organization, though i am personally in the us': 'United States',

        # England
        'england, uk': 'United Kingdom',
        'england, united kingdom': 'United Kingdom',
        'united kingdom (england)': 'United Kingdom',
        'uk (england)': 'United Kingdom',
        'england/uk': 'United Kingdom',
        'england, gb': 'United Kingdom',
        'englang': 'England',
        'uk (northern england)': 'United Kingdom',

        # Wales
        'wales, united kingdom': 'Wales',
        'wales, uk': 'Wales',
        'united kingdom (wales)': 'Wales',
        'uk (wales)': 'Wales',
        'wales/uk': 'Wales',
        'wales, gb': 'Wales',
        'wales (uk)': 'Wales',
        'wales (united kingdom)': 'Wales',

        # United Kingdom
        'uk': 'United Kingdom',
        'united kindom': 'United Kingdom',
        'unites kingdom': 'United Kingdom',
        'united kingdomk': 'United Kingdom',
        'great britain': 'United Kingdom',
        'britain': 'United Kingdom',
        'uk for us company': 'United Kingdom',
        'uk, remote': 'United Kingdom',
        'uk, but for globally fully remote company': 'United Kingdom',
        'london': 'United Kingdom',

        # Other countries
        'australi': 'Australia',
        'australian': 'Australia',
        'the netherlands': 'Netherlands',
        'nederland': 'Netherlands',
        'nl': 'Netherlands',
        'scotland, uk': 'Scotland',
        'nz': 'New Zealand',
        'new zealand aotearoa': 'New Zealand',
        'aotearoa new zealand': 'New Zealand',
        'from new zealand but on projects across apac': 'New Zealand',
        'canda': 'Canada',
        'can': 'Canada',
        'canad': 'Canada',
        'canadw': 'Canada',
        'csnada': 'Canada',
        'canadá': 'Canada',
        'canada, ottawa, ontario': 'Canada',
        'i am located in canada but i work for a company in the us': 'Canada',
        'canada and usa': 'Canada',
        'hong konh': 'Hong Kong',
        'hong kongkong': 'Hong Kong',
        'mainland china': 'China',
        'italia': 'Italy',
        'italy (south)': 'Italy',
        'brasil': 'Brazil',
        'danmark': 'Denmark',
        'mexico': 'Mexico',
        'ceska republika': 'Czech Republic',
        'czechia': 'Czech Republic',
        'uae': 'United Arab Emirates',
        'united arab emirates': 'United Arab Emirates',
        
        # New Mappings
        'austria, but i work remotely for a dutch/british company': 'Austria',
        'i work for an us based company but i\'m from argentina': 'Argentina',
        'i work for an us based company but im from argentina': 'Argentina',
        'argentina but my org is in thailand': 'Argentina',
        'remote (philippines)': 'Philippines',
        'company in germany i work from pakistan': 'Pakistan',
        'nigeria + uk': 'Nigeria',
        'ibdia': 'India',
        'burma': 'Myanmar',
        'luxemburg': 'Luxembourg',
        'the bahamas': 'Bahamas',
        'catalonia': 'Spain',
        'isle of man': 'Isle of Man',
        'jersey, channel islands': 'Jersey',
        'panama': 'Panama',
    }
    if country in country_map: return country_map[country].title()

    # Clean up some ending punctuation that might prevent matches
    if country.endswith('.'):
        country = country[:-1]
        if country in country_map: return country_map[country]

    us_patterns = [
        r'^united states.*', r'based in us.*', r'^usa.*$'
    ]
    for pattern in us_patterns:
        if re.search(pattern, country):
            return 'United States'

    if re.search(r'northern ireland.*', country):
        return 'Northern Ireland'

    if re.search(r'^japan.*', country):
        return 'Japan'
    if re.search(r'^from romania.*$', country):
        return 'Romania'
    if re.search(r'.*new zealand.*', country):
        return 'New Zealand'

    return country.title()

def clean_other_currency(currency):
    currency = str(currency).strip().lower()
    
    # Clean text similar to clean_city
    currency = re.sub(r'\(.*\)', '', currency) # Rm parenthesis
    currency = unicodedata.normalize('NFKD', currency).encode('ascii', 'ignore').decode('utf-8') # Remove accents
    currency = re.sub(r'\s{2,}', ' ', currency) # Rm extra spaces
    currency = currency.strip()

    if currency == 'nan': return None

    currency_map = {
        'peso argentino': 'ARS',
        'argentinian peso': 'ARS',
        'argentine peso': 'ARS',
        'canadian': 'CAD',
        'indian rupees': 'INR',
        'rupees': 'INR',
        'rs': 'INR',
        'br$': 'BRL',
        'brl r$': 'BRL',
        'mexican pesos': 'MXN',
        'american dollars': 'USD',
        'us dollar': 'USD',
        'australian dollars': 'AUD',
        'polish zloty': 'PLN',
        'czech crowns': 'CZK',
        'norwegian kroner': 'NOK',
        'danish kroner': 'DKK',
        'taiwanese dollars': 'TWD',
        'ntd': 'TWD',
        'philippine peso': 'PHP',
        'philippine pesos': 'PHP',
        'china rmb': 'CNY',
        'rmb': 'CNY',
        'aud australian': 'AUD',
        'korean won': 'KRW',
        'euro': 'EUR',
        'thai baht': 'THB',
        'croatian kuna': 'HRK',
        'singapore dollara': 'SGD',
        'pesos colombianos': 'COP',
        'israeli shekels': 'ILS',
        'ils/nis': 'ILS',
        'nis': 'ILS',
        'rm': 'MYR',
    }
    if currency in currency_map: return currency_map[currency].upper()

    if re.match(r'^\w{3}$', currency): return currency.upper()
    return None
