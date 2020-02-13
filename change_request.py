from netmiko import ConnectHandler
from cmd import Cmd

#Class for main command loop functions.
class MyPrompt(Cmd):

    intro = "First action must be to login to a router. Last action must be to exit."
    net_connect = ''

    ## TODO: Write show run, show log to file, clear counters, ping source

    def do_show_run(self,args):
        """Prints the running config"""
        global net_connect
        output = net_connect.send_command('show run')
        print(output)

    def do_show_log(self,args):
        """Prints the router's buffered log"""
        global net_connect
        output = net_connect.send_command('show log')
        print(output)

    def do_login(self,args):
        """Starts an SSH connection to a router"""
        global net_connect
        ip = input("Enter router IP:\n")
        uname = input("Enter Username:\n")
        pw = input("Enter Password:\n")

        ROUTER = {
            'device_type': 'cisco_ios',
            'username': uname,
            'password': pw,
            'ip': ip,
        }
        net_connect = ConnectHandler(**ROUTER)

    def do_change_speed_duplex(self,args):
        """Change the speed and duplex of a router"""
        global net_connect

        interface = input("Which interface do you want to change? Ex: int gi0/0/0, te0/0/2\n")
        speed = input("What do you want the speed to be? If this should not change enter n/a, if auto type auto\n")
        duplex = input("What do you want the duplex to be? If this should not change enter n/a, if auto type auto\n")

        if speed == 'n/a':
            duplex = 'duplex ' + duplex
            config_commands = [interface,duplex]
            output = net_connect.send_config_set(config_commands)
            print(output)
        elif speed == 'auto' and duplex == 'auto':
            duplex = 'duplex ' + duplex
            speed = 'speed ' + speed
            config_commands = [interface,speed,duplex]
            output = net_connect.send_config_set(config_commands)
            print(output)
        elif duplex == 'n/a':
            speed = 'speed ' + speed
            config_commands = [interface,speed]
            output = net_connect.send_config_set(config_commands)
            print(output)
        else:
            print("Must change at least speed or duplex")

    def do_bounce_interface(self,arg):
        """Shuts then no shut an interface"""
        global net_connect

        interface = input("Which interface do you want to bounce? Ex: int gi0/0/0, int te0/0/2\n")
        int_bounce = [interface,'shut','no shut']
        output = net_connect.send_config_set(int_bounce)
        print(output)

    def do_bye(self, arg):
        """Logs out of a router and exits the command shell"""
        global net_connect
        net_connect.disconnect()
        print("Disconnected from router, goodbye")
        return True

#Main loop of program
def main():

    prompt = MyPrompt()
    prompt.prompt = '>'
    prompt.cmdloop()


if __name__ == '__main__':
    main()
