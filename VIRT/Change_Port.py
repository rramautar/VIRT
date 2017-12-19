class Change_Port:
    def Change_Port(self):
        try:
            port = int(input("We're starting! Which port would you like to use?\n"))
        except ValueError:
            print("This is not a valid port number. Using default")
            port = 8000



        antw = str(input("Is port: " + str(port) + " the right port?(y/n)\n"))
        if antw == '' or antw == 'y':
            print('OK, Using port '+ str(antw))

        elif antw not in ['y', '']:
            while antw is not "y":
                port = input("Which port would you like to use?\n")
                antw = str(input("Is port: " + str(port) + " the right port?(y/n)\n"))

    Change_Port(None)
