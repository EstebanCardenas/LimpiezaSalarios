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

def clean_industry(industry):
    industry = str(industry).strip()
    if industry.lower() in ['nan', 'none', '', 'n/a']:
        return None
        
    # Normalize
    industry_lower = industry.lower()
    
    # Pre-defined map for exact matches or strong aliases
    exact_map = {
        'computing or tech': 'Computing or Tech',
        'software': 'Computing or Tech',
        'tech': 'Computing or Tech',
        'technology': 'Computing or Tech',
        'it': 'Computing or Tech',
        'information technology': 'Computing or Tech',
        'saas': 'Computing or Tech',
        
        'education (higher education)': 'Education (Higher Education)',
        'higher education': 'Education (Higher Education)',
        'university': 'Education (Higher Education)',
        'academia': 'Education (Higher Education)',
        'academic': 'Education (Higher Education)',
        'higher ed': 'Education (Higher Education)',
        
        'nonprofits': 'Nonprofits',
        'nonprofit': 'Nonprofits',
        'non-profit': 'Nonprofits',
        'charity': 'Nonprofits',
        'ngo': 'Nonprofits',
        
        'health care': 'Health care',
        'healthcare': 'Health care',
        'health': 'Health care',
        'medical': 'Health care',
        'hospital': 'Health care',
        'nursing': 'Health care',
        'medicine': 'Health care',
        'pharma': 'Health care',
        'biotech': 'Health care',
        'pharmaceuticals': 'Health care',
        'biotechnology': 'Health care',
        
        'government and public administration': 'Government and Public Administration',
        'government': 'Government and Public Administration',
        'public administration': 'Government and Public Administration',
        'public sector': 'Government and Public Administration',
        'govt': 'Government and Public Administration',
        'civil service': 'Government and Public Administration',
        'library': 'Government and Public Administration',
        'libraries': 'Government and Public Administration',
        
        'accounting, banking & finance': 'Accounting, Banking & Finance',
        'accounting': 'Accounting, Banking & Finance',
        'banking': 'Accounting, Banking & Finance',
        'finance': 'Accounting, Banking & Finance',
        'financial services': 'Accounting, Banking & Finance',
        
        'engineering or manufacturing': 'Engineering or Manufacturing',
        'engineering': 'Engineering or Manufacturing',
        'manufacturing': 'Engineering or Manufacturing',
        'engineer': 'Engineering or Manufacturing',
        'automotive': 'Engineering or Manufacturing',
        
        'marketing, advertising & pr': 'Marketing, Advertising & PR',
        'marketing': 'Marketing, Advertising & PR',
        'advertising': 'Marketing, Advertising & PR',
        'pr': 'Marketing, Advertising & PR',
        'public relations': 'Marketing, Advertising & PR',
        
        'law': 'Law',
        'legal': 'Law',
        'legal services': 'Law',
        
        'business or consulting': 'Business or Consulting',
        'consulting': 'Business or Consulting',
        'business': 'Business or Consulting',
        'management consulting': 'Business or Consulting',
        
        'education (primary/secondary)': 'Education (Primary/Secondary)',
        'primary/secondary education': 'Education (Primary/Secondary)',
        'k-12': 'Education (Primary/Secondary)',
        'school': 'Education (Primary/Secondary)',
        'teacher': 'Education (Primary/Secondary)',
        'teaching': 'Education (Primary/Secondary)',
        
        'media & digital': 'Media & Digital',
        'media': 'Media & Digital',
        'digital': 'Media & Digital',
        'publishing': 'Media & Digital',
        'journalism': 'Media & Digital',
        
        'insurance': 'Insurance',
        
        'retail': 'Retail',
        'ecommerce': 'Retail',
        'e-commerce': 'Retail',
        
        'recruitment or hr': 'Recruitment or HR',
        'recruitment': 'Recruitment or HR',
        'hr': 'Recruitment or HR',
        'human resources': 'Recruitment or HR',
        
        'property or construction': 'Property or Construction',
        'property': 'Property or Construction',
        'construction': 'Property or Construction',
        'real estate': 'Property or Construction',
        
        'art & design': 'Art & Design',
        'art': 'Art & Design',
        'design': 'Art & Design',
        'arts': 'Art & Design',
        'creative': 'Art & Design',
        
        'utilities & telecommunications': 'Utilities & Telecommunications',
        'utilities': 'Utilities & Telecommunications',
        'telecommunications': 'Utilities & Telecommunications',
        'telecom': 'Utilities & Telecommunications',
        'energy': 'Utilities & Telecommunications',
        'oil & gas': 'Utilities & Telecommunications',
        'oil and gas': 'Utilities & Telecommunications',
        
        'transport or logistics': 'Transport or Logistics',
        'transport': 'Transport or Logistics',
        'logistics': 'Transport or Logistics',
        'supply chain': 'Transport or Logistics',
        'transportation': 'Transport or Logistics',
        
        'sales': 'Sales',
        
        'social work': 'Social Work',
        
        'hospitality & events': 'Hospitality & Events',
        'hospitality': 'Hospitality & Events',
        'events': 'Hospitality & Events',
        'food service': 'Hospitality & Events',
        'restaurant': 'Hospitality & Events',
        
        'entertainment': 'Entertainment',
        'gaming': 'Entertainment',
        'video games': 'Entertainment',
        
        'agriculture or forestry': 'Agriculture or Forestry',
        'agriculture': 'Agriculture or Forestry',
        'forestry': 'Agriculture or Forestry',
        'farming': 'Agriculture or Forestry',
        
        'leisure, sport & tourism': 'Leisure, Sport & Tourism',
        'leisure': 'Leisure, Sport & Tourism',
        'sport': 'Leisure, Sport & Tourism',
        'tourism': 'Leisure, Sport & Tourism',
        'fitness': 'Leisure, Sport & Tourism',
    }
    
    if industry_lower in exact_map:
        return exact_map[industry_lower]

    # Keyword matching
    if 'comput' in industry_lower or 'tech' in industry_lower:
        if 'bio' not in industry_lower: # Prevent Biotech -> Tech
            return 'Computing or Tech'
    
    if 'educ' in industry_lower or 'university' in industry_lower or 'academic' in industry_lower:
        if 'primary' in industry_lower or 'secondary' in industry_lower or 'k-12' in industry_lower or 'school' in industry_lower:
            return 'Education (Primary/Secondary)'
        return 'Education (Higher Education)'
        
    if 'health' in industry_lower or 'medic' in industry_lower or 'nurs' in industry_lower or 'pharma' in industry_lower or 'bio' in industry_lower:
        return 'Health care'
        
    if 'govern' in industry_lower or 'public' in industry_lower or 'librar' in industry_lower or 'defense' in industry_lower:
        if 'relation' not in industry_lower: # proper exclusion for Public Relations
             return 'Government and Public Administration'
    
    if 'bank' in industry_lower or 'financ' in industry_lower or 'account' in industry_lower:
        return 'Accounting, Banking & Finance'
        
    if 'engin' in industry_lower or 'manufactur' in industry_lower:
        return 'Engineering or Manufacturing'
        
    if 'market' in industry_lower or 'advert' in industry_lower or 'relation' in industry_lower:
        return 'Marketing, Advertising & PR'
        
    if 'consult' in industry_lower or 'business' in industry_lower:
        return 'Business or Consulting'
        
    if 'media' in industry_lower or 'publish' in industry_lower or 'journal' in industry_lower:
        return 'Media & Digital'
        
    if 'construct' in industry_lower or 'estate' in industry_lower or 'architec' in industry_lower:
        return 'Property or Construction'
        
    if 'retail' in industry_lower or 'e-comm' in industry_lower:
        return 'Retail'
        
    if 'art' in industry_lower or 'design' in industry_lower or 'museum' in industry_lower:
        return 'Art & Design'
        
    if 'recruit' in industry_lower or 'human' in industry_lower:
        return 'Recruitment or HR'
        
    if 'energy' in industry_lower or 'oil' in industry_lower or 'gas' in industry_lower or 'utilit' in industry_lower:
        return 'Utilities & Telecommunications'
        
    if 'transport' in industry_lower or 'supply' in industry_lower or 'logist' in industry_lower:
        return 'Transport or Logistics'
        
    if 'nonprofit' in industry_lower or 'charity' in industry_lower:
        return 'Nonprofits'
        
    if 'law' in industry_lower or 'legal' in industry_lower:
        return 'Law'
        
    if 'hospitality' in industry_lower or 'restaurant' in industry_lower or 'chef' in industry_lower:
        return 'Hospitality & Events'
        
    if 'entertain' in industry_lower or 'film' in industry_lower or 'video' in industry_lower or 'game' in industry_lower:
        return 'Entertainment'
        
    if 'agri' in industry_lower or 'farm' in industry_lower:
        return 'Agriculture or Forestry'
        
    if 'social work' in industry_lower:
        return 'Social Work'
    
    return industry.title()
