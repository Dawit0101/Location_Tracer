# pip3 install maxminddb-geolite2
from geolite2 import geolite2
import socket, subprocess 

cmd = r"/Applications/Wireshark.app/Contents/MacOS/tshark"

# if you are using windows change the above path 
# cmd = r"C:\Program Files\Wireshark\tshark.exe"

process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
my_ip = socket.gethostbyname(socket.gethostname())
reader = geolite2.reader()

def get_ip_location(ip):
    location = reader.get(ip)
    
    try:
        country = location["country"]["names"]["en"]
    except:
        country = "Unknown"

    try:
        subdivision = location["subdivisions"][0]["names"]["en"]
    except:
        subdivision = "Unknown"    

    try:
        city = location["city"]["names"]["en"]
    except:
        city = "Unknown"
    try:
        postal_code = location["postal"]["code"]["names"]["en"]
    except:
        postal_code = "Unknown"
    
    return country, subdivision, city, postal_code


for line in iter(process.stdout.readline, b""):
    columns = str(line).split(" ")

    if "SKYPE" in columns or "UDP" in columns:
        
        # for different tshark versions
        if "->" in columns:
            src_ip = columns[columns.index("->") - 1]
        elif "\\xe2\\x86\\x92" in columns:
            src_ip = columns[columns.index("\\xe2\\x86\\x92") - 1]
        else:
            continue
            
        if src_ip == my_ip:
            continue

        try:
            country, sub, city, postal_code = get_ip_location(src_ip)
            print(">>> " + country + ", " + sub + ", " + city + ", " + postal_code)
        except:
            try:
                real_ip = socket.gethostbyname(src_ip)
                country, sub, city, postal_code = get_ip_location(real_ip)
                print(">>> " + country + ", " + sub + ", " + city + ", " + postal_code)
            except:
                print("Not found")