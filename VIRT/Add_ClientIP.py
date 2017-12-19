class Add_ClientIP:

    def Add_IP(IpAdressen):
        while True:
            NieuwIP = input("Wilt u een nieuw IP adres toevoegen voor de connectie?(y/n) ")
            if NieuwIP == 'n' or '':
                break
            toevoeg = input("Welk IP adres wilt u toevoegen?: \n")
            IpAdressen.append(toevoeg)

        # check of ip goed gaat
        print(IpAdressen)
        print('Dank u, een moment.')
        return IpAdressen