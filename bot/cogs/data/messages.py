from nextcord import Embed, Color
from .images import spell_gifs, failed_spell_gifs
import random

def no_permissions():
    embed = Embed(
        title = "No permissions.",
        description = "You do not have the required permissions to run this command.",
        color=Color.red())
    return embed

def message_not_found(message_id):
    embed = Embed(
        title = "Message not found.",
        description = f"A message with ID {message_id} was not found in the database.",
        color=Color.red())
    return embed

def keyword_found(author, channel, message_id):
    embed = Embed(
        title = "Message sent contains keyword.",
        description = f"A message posted by {author} in {channel} contains one or more or more keywords.",
        color=Color.red())
    embed.set_footer(text=f"Message ID: {message_id}")
    return embed

def message_deleted(author, channel, content, message_id):
    embed = Embed(
        title = "Message deleted.",
        description = f"A message posted by {author} in {channel} has been deleted.\nMessage content: {content}",
        color=Color.red()
    )
    embed.set_footer(text=f"Message ID: {message_id}")
    return embed

def message_retreived(author, channel, content, timestamp, message_id):
    embed = Embed(
        title = "Message record.",
        description = f"Message retreived from database.\nAuthor: {author}\nChannel: {channel}\nTimestamp: {timestamp}\n\Message content: {content}",
        color=Color.green()
    )
    embed.set_footer(text=f"Message ID: {message_id}")
    return embed

def mod_deleted_message(message_id):
    embed = Embed(
        title = "Message deleted by moderator.",
        description = f"A message with ID {message_id} has been deleted by a moderator.",
        color=Color.green()
    )
    return embed

def keyword_added(keyword, keywords):
    embed = Embed(
        title = "Keyword added.",
        description = f"Keyword `{keyword}` has been added to the database.\nAll keywords: `{keywords}`",
        color=Color.green()
    )
    return embed

def keyword_deleted(keyword):
    embed = Embed(
        title = "Keyword deleted.",
        description = f"Keyword `{keyword}` has been deleted from the database.",
        color=Color.green()
    )
    return embed

def keyword_not_found(keyword):
    embed = Embed(
        title = "Keyword not found.",
        description = f"Keyword `{keyword}` was not found in the database.",
        color=Color.red()
    )
    return embed

def keyword_list(keywords):
    embed = Embed(
        title = "Keywords in database.",
        description = f"Keywords in the database: {keywords}",
        color=Color.green()
    )
    return embed

def cast_spell(spell, target, response, success):
    if success:
        embed = Embed(
            title = f"I CAST {spell.upper()}",
            description = f"Spell **SUCCEEDED** cast against {target}\n\n*{response}*",
            color=Color.green()
        )
        embed.set_image(url=spell_gifs[random.randint(0, len(spell_gifs) - 1)])
    else:
        embed = Embed(
            title = f"I CAST {spell.upper()}",
            description = f"Spell cast **FAILED** against {target}\n\n*{response}*",
            color=Color.red()
        )
        embed.set_image(url=failed_spell_gifs[random.randint(0, len(failed_spell_gifs) - 1)])
    return embed