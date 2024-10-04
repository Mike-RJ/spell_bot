import nextcord
from nextcord.ext import commands
from langchain_community.llms import Ollama
from .data.messages import cast_spell
from nextcord import Interaction
import random
from .data.environment import OLLAMA_URL, SERVER_ID

class SpellCaster(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.model = Ollama(
            model = "llama2-uncensored",
            base_url = OLLAMA_URL
        )

    @nextcord.slash_command(name="cast", description="Cast a spell against your worst foe.", guild_ids=[SERVER_ID])
    async def cast(self, interaction: Interaction, spell: str, target: str):
        # if not interaction.user.guild_permissions.administrator:
        #     await interaction.response.send_message(embed=no_permissions(), ephemeral=True)
        #     return
        await interaction.response.defer()
        successful = random.choice([True, False])
        if successful:
            response = self.model.invoke(
                f"You have cast the {spell} spell against {target} and it was successful. Describe the effects the spell had on your target in 50 words or less."
            )
        else:
            response = self.model.invoke(
                f"You have cast the {spell} spell against {target} and it was unsuccessful and might have backfired. Describe how the spell failed in 50 words or less."
            )
        await interaction.followup.send(embed=cast_spell(spell, target, response, successful))

def setup(bot):
    bot.add_cog(SpellCaster(bot))