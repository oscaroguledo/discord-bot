import os
from discord.ext import commands
from discord import Intents
import discord
import requests

PREFIX = "?"
OWNERS_IDS = [913196257101643907]
guild_id=1123685329812066374
role_id=None
token="MTEyOTczNjcwOTQzMzc0MTMyMg.G9Jjdp.KrVVHZje2Cx7bLW-qRIRpEmK1GtM0a1neKInDE"


def assign_guild_role(guildid, token, role_id, user_id):
    """with open(os.getcwd()+"/app/token", "r", encoding="utf-8") as t:
        token = t.read()"""
    headers = {
        'Content-Type': 'application/json',
        'authorization': f'Bot {token}'
    }
    url = f"https://discord.com/api/v9/guilds/{guildid}/members/{user_id}/roles/{role_id}"
    response = requests.request("PUT", url=url, headers=headers)
    # print(response.status_code)

    if response.status_code == 204:
        res = {"isSuccess": True,
               "role_id": role_id}
        return res
    else:
        res = {"isSuccess": False,
               "role_id": role_id,
               "discord status": response.status_code}
        return res


def discord_invite(server_owner_ids, guild_id, role_id, token):
    invite_link = []
    invites = {}
    intents = Intents.default()
    intents.members = True
    intents.message_content=True
    intents.messages = True
    intents.guilds = True
    client = commands.Bot(command_prefix="?", owner_ids=server_owner_ids, intents=intents)
    print("running bot...")

    # Close the bot
    @client.command()
    @commands.is_owner()
    async def shutdown(context):
        print("bot is shut down")
        await context.close()

    @client.event
    async def on_ready():  # gets the invite link when the bot is ready
        print("bot is ready...")
        for guild in client.guilds:
            invites[guild.id] = await guild.invites()
            print("waiting for someone to join via invite link")

    @client.event
    async def on_message(message):
        print(message,"======")
        role_id=message.content
        print(role_id)
    # find invite code
    def search_invite_by_code(invite_list, code):
        for i in invite_list:
            if i.code == code:
                return i

    # excecutes when a member joins
    @client.event
    async def on_member_join(member):

        channel = client.get_guild(guild_id).text_channels[0]
        await channel.send(f"{member} has joined the server")

        invites_before_join = invites[member.guild.id]
        invites_after_join = await member.guild.invites()

        for invite in invites_before_join:
            if invite.uses < search_invite_by_code(invites_after_join, invite.code).uses:
                print(f"Member {member.name} - ({member.id}) has Joined")
                print(f"Invite link: https://discord.gg/{invite.code}")
                print(f"Inviter: {invite.inviter}")
                invites[member.guild.id] = invites_after_join

                # assigning a role when a user joins with link-------
                assign_guild_role(guild_id, token, role_id, member.id)

                return

    @client.event
    async def on_member_remove(member):
        print(f"{member} has left the server")
        channel = client.get_guild(guild_id).text_channels[0]
        await channel.send(f"{member} has left the server")

    @client.event
    async def on_(member):
        print(f"{member} has left")
        channel = client.get_guild(guild_id).text_channels[0]
        await channel.send(f"{member} has left the server")

    # with open(os.getcwd()+"/app/token", "r", encoding="utf-8") as t:
    #    token = t.read()
    # token file is the token for the bot created
    client.run(token=token)
    return invite_link


#with open(os.getcwd()+"/token", "r", encoding="utf-8") as t:
#        token = t.read()
discord_invite(server_owner_ids=OWNERS_IDS, guild_id=guild_id,
                token=token, role_id=role_id)
