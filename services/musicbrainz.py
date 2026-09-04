import aiohttp 

from config import MUSICBRAINZ_API_URL

HEADER = {
    "User-Agent": "KpopBot/0.1 (https://github.com/NgixBP/BotDiscordKpop)"
}



async def search_group(group_name: str) -> dict | None: 

    url = f"{MUSICBRAINZ_API_URL}/artist"

    query = f'artist:"{group_name}" AND type:group'

    params = {
        "query" : query, 

        "fmt" : "json",

        "limit": 5
    }

    timeout = aiohttp.ClientTimeout(total=10)

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
                   
                    return None

                data = await response.json()
    
    # NetWork Error MusicBrainz 
    # Impossible to Connect
    except aiohttp.ClientError as error: 

        print(
            f"!!!!!!!!!!!!!!!NetWork MusicBrain ERRROR : {error} !!!!!!!!!!!!!!!!!!!!!!!"
        )

        return None
        
    #Timeout 
    except TimeoutError: 

        print(
            "MusicBrainz not responding"
        )

        return None
    
    artists = data.get("artists",[])

    if not artists: 
        return None

    return artists[0]