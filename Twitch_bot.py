#Imports
import socket
import urllib.request
from json import loads
import threading

#Variables
botCommands = []
botReplies = []
mods = []
mod_list = []
reply = ""
modcommand = ""
reply_list = []
queue = 0
with open('commands.txt') as f:
    botCommands = [line.rstrip('\n') for line in open('commands.txt')]
f.close()
with open('replies.txt') as f:
    replies = [line.rstrip('\n') for line in open('replies.txt')]
f.close()
with open('mods.txt') as f:
    mod_list = [line.rstrip('\n') for line in open('mods.txt')]
f.close()
user = ""
command = ""


#Bot Login Information / Logging in
ircConnection = socket.socket()
ircConnection.connect(("irc.twitch.tv", 6667))
ircConnection.sendto("PASS oauth:bxfh0vin70ab1m9fv6c1vcht7rv7cw\r\n".encode(), ("irc.twitch.tv", 6667))
ircConnection.sendto("USER bothannah 0 * : bothannah\r\n".encode(), ("irc.twitch.tv", 6667))
ircConnection.sendto("NICK bothannah\r\n".encode(), ("irc.twitch.tv", 6667))
ircConnection.sendto("JOIN #hannahryan\r\n".encode(), ("irc.twitch.tv", 6667))
def qing():
    global queue
    queue = 0
    threading.Timer(15,qing).start()
qing()

def msg(message):
    global queue
    queue = queue + 1
    print(queue)
    if queue < 10:
        ircConnection.sendto("PRIVMSG #hannahryan :".encode() + message.encode() + "\r\n".encode(), ("irc.twitch.tv", 6667))
    else:
        print('Message deleted')

while(True):
    try:
        ircChat = ircConnection.recv(1204)
    except:
        print("[ERROR] Can not get ircChat")
    try:
        ircChatF = str(ircChat)
    except:
        print("[ERROR] Can not make ircChat into string")

    if ircChatF.find('PING') != -1:
        ircConnection.sendto("PING :PONG\r\n".encode(), ("irc.twitch.tv", 6667))
        ircConnection.sendto("PONG irc.twitch.tv\r\n".encode(), ("irc.twitch.tv", 6667))
        ircConnection.sendto("PONG tmi.twitch.tv\r\n".encode(), ("irc.twitch.tv", 6667))
        print("PONG")
    
    try:
        try:
            user = ircChatF.split("b':")[1]
            user = user.split("!")[0]
            print(user)
        except:
            print("[ERROR] Unable to find the user!")
    except:
        print("[ERROR] Can not convert user")
    try:
        try:
            command = ircChatF.split("b':")[1]
            command = command.split("#hannahryan :")[1]
            command = command[:-5]
            print(command)
            modcommand = ircChatF.split("b':")[1]
            modcommand = modcommand.split("#hannahryan :")[1]
            modcommand = modcommand[:-5]
            try:
                modcommand = modcommand.split(" ")[0]
            except:
                print("Can't modcommand")
        except:
            print("[ERROR] Failed to find command")
    except:
        print("[ERROR] Can not convert command")

    try:
        if(modcommand in botCommands):
            print(botCommands.index(modcommand))
            try:
                reply = replies[botCommands.index(modcommand)]
                if "@user@" in reply:
                    reply_list = reply.split()
                    reply_list[reply_list.index("@user@")] = user
                    reply = " ".join(reply_list)
                if "@touser@" in reply:
                    try:
                        touser = ircChatF.split("b':")[1]
                        touser = touser.split("#hannahryan :")[1]
                        touser = touser[:-5]
                        touser = touser.split(" ")[1]
                    except:
                        print("Can't modify touser")
                    reply_list = reply.split()
                    reply_list[reply_list.index("@touser@")] = touser
                    reply = " ".join(reply_list)
            except:
                print("Can not change value")
            try:
                msg(reply)
            except:
                    print("[ERROR] Can not reply to command")
    except:
        print("[ERROR] No command found")

    try:
        if command.startswith("!addcmd"):
            with open('mods.txt') as f:
                mod_list = [line.rstrip('\n') for line in open('mods.txt')]
            f.close()
            #API IS SLOW, DO NOT USE UNLESS YOU PLAN ON WAITING
            '''
            try:
                response = urllib.request.urlopen('https://tmi.twitch.tv/group/user/affibot/chatters')
                readable = response.read().decode('utf-8')
                chatlist = loads(readable)
                chatters = chatlist['chatters']
                mods = chatters['moderators']
                print(mods)
            except:
                print("[ERROR] Can't refresh mods")
            '''
            try:
                if user in mods or user in mod_list:
                    newcommand = command.split("!addcmd ")[1]
                    newcommand = newcommand.split(" ")[0]
                    newreply = command.split("addcmd " + newcommand + " ")[1]
                    with open("commands.txt", "a") as f:
                        f.write(newcommand + "\n")
                    f.close()
                    with open("replies.txt", "a") as f:
                        f.write(newreply + "\n")
                    f.close()
                    with open('commands.txt') as f:
                        botCommands = [line.rstrip('\n') for line in open('commands.txt')]
                    f.close()
                    with open('replies.txt') as f:
                        replies = [line.rstrip('\n') for line in open('replies.txt')]
                    f.close()
                    msg("Command added!")
                else:
                    msg("You are not a mod or the bot has not refreshed your mod status!")
            except:
                print("[ERROR] Could not write command/reply")
                msg("[ERROR] Can not add Command!")
    except:
        print("[ERROR] Can not add command")

    #API IS SLOW, DO NOT USE UNLESS YOU PLAN ON WAITING
    '''
    try:
        if command == "!mod_refresh":
            response = urllib.request.urlopen('https://tmi.twitch.tv/group/user/affibot/chatters')
            readable = response.read().decode('utf-8')
            chatlist = loads(readable)
            chatters = chatlist['chatters']
            mods = chatters['moderators']
            print(mods)
    except:
        print("[ERROR] Can't refresh mods")
    '''

    try:
        if command.startswith("!mod") and user in mod_list:
            new_mod = command.split("!mod ")[1]
            with open("mods.txt", "a") as f:
                f.write(new_mod + "\n")
            f.close()
            msg("Added " + new_mod + " to the modlist!")
    except:
        print("[ERROR] Can not add mod")

    try:
        with open('mods.txt') as f:
            mod_list = [line.rstrip('\n') for line in open('mods.txt')]
        f.close()
        if command.startswith("!delcommand") and user in mod_list:
            with open('commands.txt') as f:
                botCommands = [line.rstrip('\n') for line in open('commands.txt')]
            f.close()
            with open('replies.txt') as f:
                replies = [line.rstrip('\n') for line in open('replies.txt')]
            f.close()
            deleted_command = command.split("!delcommand ")[1]
            if deleted_command in botCommands:
                replies.remove(replies[botCommands.index(deleted_command)])
                botCommands.remove(deleted_command)
                print(botCommands)
                print(replies)
                with open("commands.txt", "w") as f:
                    f.write("")
                f.close()
                with open("replies.txt", "w") as f:
                    f.write("")
                f.close()
                for i in range(len(botCommands)):
                    with open("commands.txt", "a") as f:
                        f.write(botCommands[i] + "\n")
                    f.close()
                for i in range(len(replies)):
                    with open("replies.txt", "a") as f:
                        f.write(replies[i] + "\n")
                    f.close()
                msg("Command deleted!")
    except:
        print("[ERROR] Can not remove command/reply")

    if command == "!commands":
        with open('commands.txt') as f:
            botCommands = [line.rstrip('\n') for line in open('commands.txt')]
        f.close()
        msg("The current commands are: !followage, !uptime, " + ", ".join(botCommands))

    if command == "!followage":
        try:
            response = urllib.request.urlopen('https://apis.rtainc.co/twitchbot/following?channel=HANNAHRYAN&user=' + user)
            readable = response.read().decode('utf-8')
            msg(user + " has been following Hannah for " + readable)
        except:
            print("Can't do that m80")

    if command == "!uptime":
        try:
            response = urllib.request.urlopen('https://decapi.me/twitch/uptime?channel=Hannahryan')
            readable = response.read().decode('utf-8')
            msg("Hannah has been live for: " + readable)
        except:
            print("Can't do that m80")
