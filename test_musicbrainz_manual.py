import asyncio

from services.musicbrainz import search_group

async def main(): 
    
    result = await search_group("SKZ")

    if result is None : 
        print("Auncun group trouvé")
        return

    print("Groupe trouvée !")
    print(f"Nom : {result.get('name')}")
    print(f"Type : {result.get('type')}")
    print(f"Pays : {result.get('country')}")
    print(f"MBID : {result.get('id')}")
    print(f"Score : {result.get('score')}")
    print(f"Début : {result.get('life-span', {}).get('begin')}")

asyncio.run(main())