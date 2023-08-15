import glob
import os
pcap_files = glob.glob("*.pcap")
pcap_files.sort(key=os.path.getmtime, reverse=True)


files_to_delete = pcap_files[:]
for file in files_to_delete:
    os.remove(file)
        