import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from typing import List
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .data.database import MessageRecord, KeyWord, DATABASE_URLS
from .data.messages import keyword_found, message_deleted, message_retreived, message_not_found, mod_deleted_message, keyword_added, keyword_deleted, keyword_not_found, keyword_list, no_permissions
from .data.environment import AUDIT_CHANNEL_ID, SERVER_ID

class Audit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message: List[MessageRecord] = []
        self.engine = create_engine(DATABASE_URLS['messages'])
        self.Session = sessionmaker(bind=self.engine)
    
    def find_keywords(self, content):
        session = self.Session()
        records = session.query(KeyWord).all()
        keywords = [record.keyword for record in records]
        if any(word in content.lower() for word in keywords):
            return True
        else:
            return False
    
    @commands.Cog.listener()
    async def on_message(self, message):

        # Ignore messages from the bot itself
        if message.author == self.bot.user:
            return
        
        # Record the message
        record = MessageRecord(
            message_id=message.id,
            message_content=message.content,
            author_id=message.author.id,
            author_name=message.author.name,
            channel_id=message.channel.id,
            channel_name=message.channel.name

        )

        session = self.Session()

        session.add(record)
        session.commit()
        session.close()

        self.message.append(record)

        if self.find_keywords(message.content):
            audit_channel = self.bot.get_channel(AUDIT_CHANNEL_ID)
            await audit_channel.send(embed=keyword_found(message.author.mention, message.channel.mention, message.id))
    
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        print("Message Deleted")
        audit_channel = self.bot.get_channel(AUDIT_CHANNEL_ID)
        await audit_channel.send(embed=message_deleted(message.author.mention, message.channel.mention, message.content, message.id))
    
    @nextcord.slash_command(name="get-messages", description="Get a discord message by ID.", guild_ids=[SERVER_ID])
    async def get_message(self, interaction: Interaction, message_id):
        session = self.Session()
        message = session.query(MessageRecord).filter_by(message_id=message_id).first()
        session.close()
        if message:
            await interaction.response.send_message(embed=message_retreived(message.author_name, message.channel_name, message.message_content, message.timestamp, message_id))
            return
        else:
            await interaction.response.send_message(embed=message_not_found(message_id))
            return
    
    @nextcord.slash_command(name="delete-message", description="Delete a discord message by ID.", guild_ids=[SERVER_ID])
    async def delete_message(self, interaction: Interaction, message_id):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(embed=no_permissions(), ephemeral=True)
            return
        session = self.Session()
        message = session.query(MessageRecord).filter_by(message_id=message_id).first()
        if message:
            session.delete(message)
            session.commit()
            session.close()
            await interaction.response.send_message(embed=mod_deleted_message(message_id))
            return
        else:
            await interaction.response.send_message(embed=message_not_found(message_id))
            return
    
    @nextcord.slash_command(name="add-keyword", description="Add a keyword to the filter.", guild_ids=[SERVER_ID])
    async def add_keyword(self, interaction: Interaction, keyword: str):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(embed=no_permissions(), ephemeral=True)
            return
        session = self.Session()
        record = KeyWord(keyword=keyword)
        session.add(record)
        records = session.query(KeyWord).all()
        keywords = ','.join([record.keyword for record in records])
        session.commit()
        session.close()
        await interaction.response.send_message(embed=keyword_added(keyword, keywords))
    
    @nextcord.slash_command(name="delete-keyword", description="Delete a keyword from the filter.", guild_ids=[SERVER_ID])
    async def delete_keyword(self, interaction: Interaction, keyword: str):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(embed=no_permissions(), ephemeral=True)
            return
        session = self.Session()
        record = session.query(KeyWord).filter_by(keyword=keyword).first()
        if record:
            session.delete(record)
            session.commit()
            session.close()
            await interaction.response.send_message(embed=keyword_deleted(keyword))
            return
        else:
            await interaction.response.send_message(embed=keyword_not_found(keyword))
            return
    
    @nextcord.slash_command(name="list-keywords", description="List all keywords in the filter.", guild_ids=[SERVER_ID])
    async def list_keywords(self,interaction: Interaction):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(embed=no_permissions(), ephemeral=True)
            return
        session = self.Session()
        records = session.query(KeyWord).all()
        keywords = ','.join([record.keyword for record in records])
        session.close()
        await interaction.response.send_message(embed=keyword_list(keywords))
    
def setup(bot):
    bot.add_cog(Audit(bot))