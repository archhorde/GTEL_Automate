from netmiko import ConnectHandler
from cmd import Cmd

class MyPrompt(Cmd):

    intro = "First action must be to login to a router. Last action must be to exit."
    ROUTER = ''
    net_connect = ''

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
        speed = input("What do you want the speed to be?\n")
        duplex = input("What do you want the duplex to be?\n")

        config_commands = [interface,speed]
        output = net_connect.send_config_set(config_commands)
        print(output)

    def do_bye(self, arg):
        """Logs out of a router and exits the command shell"""
        global net_connect
        net_connect.disconnect()
        print("Disconnected from router, goodbye")
        return True

def main():

    prompt = MyPrompt()
    prompt.prompt = '>'
    prompt.cmdloop()


if __name__ == '__main__':
    main()
