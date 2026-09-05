import aiohttp
import asyncio

from config import MUSICBRAINZ_API_URL

class MusicBrainzError(Exception): 
    """
    Exception levé lorsque MusicBrainz 
    est indisponible ou rencontre des erreurs
    """
    pass


HEADER = {
    "User-Agent": "KpopBot/0.1 (https://github.com/NgixBP/BotDiscordKpop)"
}

async def wait_before_new_attempt(delay: int = 2):
    """
    Attente avant nouvelle tentative de la requetes
    """

    print(f"New attempt in {delay} seconds...")
    await asyncio.sleep(delay)



async def search_group(group_name: str) -> dict | None: 

    url = f"{MUSICBRAINZ_API_URL}/artist"

    query = f'artist:"{group_name}" AND type:group'

    params = {
        "query" : query, 

        "fmt" : "json",

        "limit": 5
    }

    #Timeout de la requête 
    timeout = aiohttp.ClientTimeout(total=10)

    #Nombre max de tentatives de requête par commands
    max_attempts = 2

    for attempt in range(1, max_attempts + 1): 
        print(
            f"MusicBrainz - attempts {attempt}/{max_attempts} for {group_name}"
        )
        try: 
            async with aiohttp.ClientSession(
                headers=HEADER,
                timeout=timeout
            ) as session: 

                async with session.get(
                    url,
                    params=params
                ) as response: 
                    
                    if response.status != 200: 
                        print(
                            f"!!!!!!!!!! MusicBrainz EROOR : HTTP {response.status}!!!!!!!!!!!!!!!!!"
                        )

                        if attempt < max_attempts: 
                            await wait_before_new_attempt()
                            continue 
                        break

                    data = await response.json()
        
        # NetWork Error MusicBrainz 
        # Impossible to Connect
        except aiohttp.ClientError as error: 

            print(
                f"!!!!!!!!!!!!!!!NetWork MusicBrain ERRROR : {error} !!!!!!!!!!!!!!!!!!!!!!!"
            )

            # Wait de secondes avant de recommencer.
            if attempt < max_attempts:
                await wait_before_new_attempt()
                continue
            break
            
        #Timeout 
        except TimeoutError: 

            print(
                "MusicBrainz not responding"
            )

            # Wait de secondes avant de recommencer.
            if attempt < max_attempts:
                await wait_before_new_attempt()
                continue 
            break

        #print("Réponse MusicBrainz :", data)
        artists = data.get("artists",[])

        if not artists: 
            return None

        return artists[0]

    # Echec des tentatives
    raise MusicBrainzError(
        f"MusicBrainz is out of order after {max_attempts} attempts"
    )
