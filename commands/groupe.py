import discord 

from discord import app_commands 

from discord.ext import commands

from services.musicbrainz import search_group, MusicBrainzError

class Groupe(commands.Cog): 

        def __init__(self, bot: commands.Bot): 
            self.bot = bot 

        @app_commands .command(
            name="groupe", 
            description="Affiche les informations d'un groupe K-POP"
        )

        @app_commands.describe(
            groupe="Nomd du groupe K-POP"
        )

        async def groupe(
            self, 
            interaction: discord.Interaction,
            groupe: str
        ):  
            """
            Recherche un groupe K-pop et affiche
            les informations trouvées.
            """
            print(f"Commande /groupe reçue : {groupe}")

            await interaction.response.defer()

            print("Recherche MusicBrainz...")
            try : 
                result = await search_group(groupe)
            except MusicBrainzError as error: 
                print(
                    f"MusicBrainz Error : {error}"
                )
            
                await interaction.followup.send(
                    "⚠️ MusicBrainz est temporairement indisponible. "
                    "Réessaie dans quelques instants."
                )
                return

            #print(f"Résultat MusicBrainz : {result}")

            if result is None :
                
                await interaction .followup.send(
                    f"❌Aucun groupe trouvé pour **{groupe}**"
                )

                return
        
            name = result.get(
                "name", 
                "Inconnu"
            )

            country = result.get(
                "country",
                "Non renseigné"
            )

            group_type = result.get(
                "type",
                "Non renseigné"
            )

            life_span = result.get(
                "life-span", 
                {}
            )

            begin = life_span.get(
                "begin",
                "Non renseigné"
            )
            
            print("Création de l'embed...")
            embed  = discord.Embed(
                title = f"{name}",
                description = f"Information sur **{name}**",
                color=discord.Color.purple()
            )

            embed.add_field(
                name="Début",
                value=begin, 
                inline=True
            )

            embed.add_field(
                name="Pays",
                value=country,
                inline=True
            )

            embed.add_field(
                name="Type",
                value=group_type,
                inline=True
            )

            embed.set_footer(
                text="Source : MusicBrainz"
            )

            print("Envoi de l'embed...")

            await interaction.followup.send(
                embed=embed
            )

            print("Embed envoyé !")

async def setup(bot: commands.Bot): 

    await bot.add_cog(
        Groupe(bot)
    )