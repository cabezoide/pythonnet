# snmp_cisco_vulns.py
#Script that obtains Cisco Vulns given IPv4 host list and snmp community

#You must provide your API Keys from OpenVulnAPI and once obtained, change these lines in script

# Cisco Openvuln API pre-set variables, change accordingly

CLIENT_ID =  'YOUR_API_KEY_HERE'
CLIENT_SECRET = 'YOUR_API_CLIENT_SECRET_HERE'

----------------------------------------------------------------------------------

Usage: python snmp_cisco_vulns.py -f [hostfile] -c [snmpcommunity]

  -f FILE, --file FILE  .csv or plain-text file with IP or hostname list, one
                        per line
                        
  -c SNMP_COMMUNITY, --community SNMP_COMMUNITY
                        SNMP v1/v2c read-only community e.g: public
__________________________________________________________________________________
