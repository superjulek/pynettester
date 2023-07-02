# IPSEC
ifconfig 10 add fc::02/120
ps
ike_control -i fc::01
ps
udps fc::01 100
ps
udps fc::01 500
ps
udps fc::01 1000
ps

# DTLS
ifconfig 10 add fc::02/120
ps
dtlss fc::01 0
ps
dtlss fc::01 100
ps
dtlss fc::01 500
ps
dtlss fc::01 1000
ps
