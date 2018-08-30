import socket, sys
import time
from struct import *
 
#Convert a string of 6 characters of ethernet address into a dash separated hex string
def eth_addr (a) :
  b = "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % (ord(a[0]) , ord(a[1]) , ord(a[2]), ord(a[3]), ord(a[4]) , ord(a[5]))
  return b
 
#create a AF_PACKET type raw socket (thats basically packet level)
#define ETH_P_ALL    0x0003          /* Every packet (be careful!!!) */
try:
    s = socket.socket( socket.AF_PACKET , socket.SOCK_RAW , socket.ntohs(0x0003))
except socket.error , msg:
    print 'Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

f = open('traindata2.txt','a') 
start=time.time()
# receive a packet
while True:
    packet = s.recvfrom(65565)
     
    #packet string from tuple
    packet = packet[0]
     
    #parse ethernet header
    eth_length = 14
     
    eth_header = packet[:eth_length]
    eth = unpack('!6s6sH' , eth_header)
    eth_protocol = socket.ntohs(eth[2])
    print ("Running...")
  
    #Parse IP packets, IP Protocol number = 8
    if eth_protocol == 8 :
        #Parse IP header
        #take first 20 characters for the ip header
        ip_header = packet[eth_length:20+eth_length]
         
        #now unpack them :)
        iph = unpack('!BBHHHBBH4s4s' , ip_header)
 
        version_ihl = iph[0]
        version = version_ihl >> 4
        ihl = version_ihl & 0xF
 
        iph_length = ihl * 4
 
        ttl = iph[5]
        protocol = iph[6]
        s_addr = socket.inet_ntoa(iph[8]);
        d_addr = socket.inet_ntoa(iph[9]);
        
 
        #TCP protocol
        if protocol == 6 :
            t = iph_length + eth_length
            tcp_header = packet[t:t+20]
 
            #now unpack them :)
            ctime=time.time()
            ptime=start
            rtime=(ptime-ctime)
            start=ctime
            tcph = unpack('!HHLLBBHHH' , tcp_header)
             
            source_port = tcph[0]
            dest_port = tcph[1]
            sequence = tcph[2]
            acknowledgement = tcph[3]
            doff_reserved = tcph[4]
            tcp_flags1 = tcph[5]
            list1=list(str(bin(tcp_flags1))[2:].zfill(8))
            flags=str(list1[0]+','+list1[2]+','+list1[3]+','+list1[4]+','+list1[5]+','+list1[6]+','+list1[6]+','+list1[7])
            tcph_length = doff_reserved >> 4
            f.write("\n"+str(eth_protocol))
            f.write(','+ str(ihl) + ',' + str(ttl) + ',' + str(protocol))
            f.write(',' + str(source_port) + ',' + str(dest_port) + ',' + str(sequence) + ',' + str(acknowledgement) + ','+ flags+',' + str(tcph_length))
            h_size = eth_length + iph_length + tcph_length * 4
            data_size = len(packet) - h_size
            f.write(','+str(abs(rtime))+','+str(data_size)+','+'BENIGN')
             
            #get data from the packet
            data = packet[h_size:]
            #print 'Data : ' + data
 
       
f.close()
