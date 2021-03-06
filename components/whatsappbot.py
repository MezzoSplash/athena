from adb.client import Client as AdbClient
from time import sleep
import datetime
#from components.server import modules
class whatsappbot:
    def __init__(self):
        # Default is "127.0.0.1" and 5037
        client = AdbClient(host="127.0.0.1", port=5037)
        self.device = client.device("ZY2239Q9MP")
        self.GREEN = '\033[92m'
        self.BLUE = '\033[94m'
        self.YELLOW = '\033[93m'
        self.RED = '\033[91m'
        self.ENDC = '\033[0m'

    def logger(self, msg, type="info", colour="none"):
        msg = str(msg)
        predate = datetime.datetime.now()
        date = predate.strftime("%Y-%m-%d %H:%M")
        tag = "[{}] WHATSAPPBOT".format(str(date))
        if type == 'debug':
            msg = "{} DEBUG: {}".format(tag, msg)
        elif type == 'alert':
            msg = "{} ALERT: \### {} \###".format(tag, msg)
        elif type == 'msg':
            msg = "{} Received message: {}".format(tag, msg)
        elif type == 'info':
            msg = "{} INFORMATION: {}".format(tag, msg)
        with open("output.txt", "a") as f:
            f.write(msg + "\n")
        if colour == "none":
            print(msg)
        elif colour == "green":
            print(self.GREEN + msg + self.ENDC)
        elif colour == "blue":
            print(self.BLUE + msg + self.ENDC)
        elif colour == "yellow":
            print(self.YELLOW + msg + self.ENDC)
        elif colour == "red":
            print(self.RED + msg + self.ENDC)

    def buildmsg(self, notification):
        from components.server import modules
        commands =["debug", "motd", "help"]
        names = []
        title = notification[0]
        caller = notification[1]
        if "+" in caller:
            caller = caller[1:]
            caller = caller.replace(" ", "")
            caller = caller.replace("(", "")
            caller = caller.replace(")", "")
        names.append(caller)
        command = notification[2].split(" ")
        if not "bot" in command:
            command.insert(0, "bot")
        self.logger(command)
        if command[1] == "debug":
            self.logger("Received debug command from \"{}\" in \"{}\"".format(caller, title), "debug", "blue")
            text = r"debug output is: \"Just talk to a rubber duck\"."
            self.writemessage(title, names, text)
        elif command[1] == "motd":
            self.logger("Received motd command from \"{}\" in \"{}\"".format(caller, title), "debug", "blue")
            text = modules().getdaily(bot="yes") # bot=yes removes weather/location information
            text = text.replace("\"", r"\"")
            self.logger("Motd text is {}".format(text), colour="yellow")
            self.writemessage(title, names, text)
        elif command[1] == "help":
            self.logger("Received help command from \"{}\" in \"{}\"".format(caller, title), "debug", "blue")
            tmplist = []
            for value in commands:
                if value == commands[-1]:
                    tmplist.append("and " + r"\"" + value + r"\"")
                else:
                    tmplist.append(r"\"" + value + r"\"")
            listofcommands = r", ".join(tmplist)
            self.logger(listofcommands, "debug", "yellow")
            text = r"At the moment I can answer to: {}.".format(listofcommands)
            self.writemessage(title, names, text)
        elif command[1] == "empty":
            self.logger("Received empty command from \"{}\" in \"{}\"".format(caller, title), "debug", "blue")
            text = r"yes?"
            self.writemessage(title, names, text)
        elif "fuck you" in command:
            self.logger("Received cussing from \"{}\" in \"{}\"".format(caller, title), "debug", "blue")
            text = r"no fuck you."
            self.writemessage(title, names, text)
        else:
            self.logger("Received unknown command from \"{}\" in \"{}\"".format(caller, title), "debug", "blue")
            tmplist = []
            for value in commands:
                if value == commands[-1]:
                    tmplist.append("and " + r"\"" + value + r"\"")
                else:
                    tmplist.append(r"\"" + value + r"\"")
            listofcommands = r", ".join(tmplist)
            self.logger(listofcommands, "debug", "yellow")
            tmp2list = []
            for value in command:
                if value != command[0]:
                    if value == command[-1]:
                        tmp2list.append(value)
                    else:
                        tmp2list.append(value + " ")
            realcmd = "".join(tmp2list)
            text = r"Sorry, I don't know what \"{}\" means yet. At the moment I can answer to: {}.".format(realcmd, listofcommands)
            self.writemessage(title, names, text)

    def writemessage(self, title, names, text):
        device = self.device
        # all of these numbers are hardcoded to the size of my phone's screen. unless you have a motorola moto g4+
        #   it likely won't work.
        device.shell("am start -n com.whatsapp/com.whatsapp.HomeActivity") # start whatsapp
        device.shell("input tap 889 167") # tap search
        device.shell("input text '{}'".format(title)) # look for chat
        device.shell("input tap 559 491") # tap chat
        for name in names:
            device.shell("input text '@{}'".format(name)) # type name
            #sleep(2)
            device.shell("input tap 480 820") # tap name
        #sleep(1)
        device.shell("input text \"{}\"".format(text)) # type text
        #sleep(1)
        device.shell("input tap 992 945") # tap send
        device.shell("am start -n com.whatsapp/com.whatsapp.HomeActivity") # back to home screen

    def tagadmin(self, title, names, text):
        admin = "31614597694"
        device = self.device
        device.shell("am start -n com.whatsapp/com.whatsapp.HomeActivity") # start whatsapp
        device.shell("input tap 889 167") # tap search
        device.shell("input text '{}'".format(title)) # look for chat
        device.shell("input tap 559 491") # tap chat
        # call admin
        device.shell("input text '@{}'".format(admin)) # type name
        device.shell("input tap 480 820") # tap name
        device.shell("input text \"Please help me out with this..\"") # request assistance from admin
        device.shell("input tap 992 945") # tap send
        for name in names:
            device.shell("input text '@{}'".format(name)) # type name
            device.shell("input tap 480 820") # tap name
        device.shell("input text \"{}\"".format(text)) # type text
        device.shell("input tap 992 945") # tap send
        device.shell("am start -n com.whatsapp/com.whatsapp.HomeActivity") # back to home screen

