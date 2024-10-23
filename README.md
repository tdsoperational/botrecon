## Summary
Botrecon is a reconnaissance tool to scrape servers mostly, specifically C2 servers.  
Simply said, you can control the data and basically the whole server with it, assuming the bot has admin permissions.  

This shouldn't be a concern, since discord rats need admin anyway to create channels.
You can get tokens fairly easily, since they are hardcoded into the binary of the rat.

> [!WARNING]
> Joining those servers on your main account is **a BAD idea**.  
> The servers are against discords ToS, since they use discord as command and control.  

> [!TIP]
> Tool is still in development, feel free to share bugs in the [issues tab](https://github.com/tdsoperational/botrecon/issues)  
> Ideas are also welcome, but it depends whether i implement them - discord bots cannot do **everything**  

## Features
- Dump messages from all channels or specific servers.  
- List recon info (server info, members, roles).  
- Send messages to servers.  
- List all members in a specified server.  
- Create a invite link for a specified server.  
- Grant admin to specified member.  
- Delete channels and ban members from servers.  
- Dump all files from servers.  
- Leave all servers the bot is in.
- Delete all webhooks the bot is in.  

Use !USAGE for commands ;)  

If you encounter them using a webhook to deliver stolen information, use !DELHOOK to fully delete it.  
If you want to disable a bot, use [this](https://tdsmental.pythonanywhere.com)  
If you need to submit them in bulk, use the [API](https://tdsmental.pythonanywhere.com/api-info)  
