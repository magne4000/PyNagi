#!/usr/bin/env python3
#utf8

# Jerome COUSSANES
# 22 october 2012


import re
from datetime import datetime

def parse_dat_file(file_name):
    '''Read the file and return all data in a list of dictionary'''

    re_section=re.compile("(\S+)\s*{")
    re_content=re.compile("(\S+)\s*=\s*(\S+)")
    l_host=[]
    l_service=[]
    iH=-1
    iS=-1
    H=False

    with open(file_name,"r") as dat_file:
        for line in dat_file:
            line=line.strip()

            section=re_section.match(line)

            if section:
                # New section
                if section.group(1)=="hoststatus":
                    l_host.append(Host())
                    iH+=1
                    H=True
                elif section.group(1)=="servicestatus":
                    l_service.append(Service())
                    iS+=1
                    H=False
            else:
                # New content line in the current section
                content=re_content.match(line)
                if content:
                    if content.group(1)=="current_state" and H==True:
                        l_host[iH].state=int(content.group(2))
                    elif content.group(1)=="host_name" and H==True:
                        l_host[iH].hostname=content.group(2)
                    elif content.group(1)=="current_state" and H==False:
                        l_service[iS].state=int(content.group(2))
                    elif content.group(1)=="host_name" and H==False:
                        l_service[iS].hostname=content.group(2)
                    elif content.group(1)=="plugin_output" and H==True:
                        l_host[iH].plugin=content.group(2)
                    elif content.group(1)=="plugin_output" and H==False:
                        l_service[iS].plugin=content.group(2)
                    elif content.group(1)=="service_description":
                        l_service[iS].description=content.group(2)
        return datetime.now(),l_host,l_service

def calc_stat(lh,ls):
    up=down=unre=pend=ok=warn=crit=0

    for e in lh:
        if e.state==0:
            up+=1
        elif e.state==1:
            down+=1
        elif e.state==2:
            unre+=1
        elif e.state==3:
            pend+=1

    for e in ls:
        if e.state==0:
            ok+=1
        elif e.state==1:
            warn+=1
        elif e.state==2:
            crit+=1

    return "Critical: "+str(crit)+", warning: "+str(warn)+", ok: "+str(ok)+", up: "+str(up)+", down: "+str(down)+", unreachable: "+str(unre)+", pending: "+str(pend)

class Service:
    '''Data structure which contain all service usefull information'''

    def __init__(self):
        self.hostname=""
        self.state=0
        self.description=""
        self.plugin=""

    def strState(self):

        if self.state==0:
            return "Ok"
        elif self.state==1:
            return "Warning"
        elif self.state==2:
            return "Critical"

    def status(self,now):
        return str(now.year)+"/"+str(now.month)+"/"+str(now.day)+"  "+str(now.hour)+":"+str(now.minute)+" "+self.strState()+" "+str(self.hostname)+" "+str(self.description)+" "+str(self.plugin)


class Host:
    '''Data structure which contain all host usefull information'''

    def __init__(self):
        self.hostname=""
        self.state=0
        self.plugin=""

    def strState(self):

        if self.state==0:
            return "Up"
        elif self.state==1:
            return "Down"
        elif self.state==2:
            return "Unreachable"
        elif self.state==3:
            return "Pending"

    def status(self,now):
        return str(now.year)+"/"+str(now.month)+"/"+str(now.day)+"  "+str(now.hour)+":"+str(now.minute)+" "+self.strState()+" "+str(self.hostname)+" "+str(self.plugin)

if __name__ == "__main__":
    now,l1,l2=parse_dat_file("resource/status_icinga.dat")

    print("Host list: ")
    for e in l1:
        print(e.status(now))

    print("\nService list: ")
    for e in l2:
        print(e.status(now))

    print("\n\n"+calc_stat(l1,l2))

