
class Protocol:
    def __init__(self, pn, p):
        self.portnumber = pn
        self.protocol = p


def fillprotocollist(list):
    file = open("ports.txt", "r")
    for x in file:
        line = x.split("\t")
        p = Protocol(line[0], line[1])
        list.append(p)



