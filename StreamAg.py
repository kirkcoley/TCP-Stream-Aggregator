#! /usr/bin/python3
import sys
from subprocess import PIPE, Popen

# Function to run bash cmds + return the output
def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True,
        universal_newlines=True
    )
    return process.communicate()[0]

# Take pcap filename from cmd line
pcap_file = sys.argv[1]

output_file_name = pcap_file.split('.')[0]+'_streams.txt'
output_file = open(output_file_name, 'w')
# Count the streams
count = 0
while True:
    # Use the -z option to follow tcp traffic between nodes, ouput ascii and use 'count' as the stream index
    cmd = 'tshark -r %s -z follow,tcp,ascii,%s'%(pcap_file,count)
    # Run the tshark cmd and add lines to the output to increase readability
    stream = cmdline(cmd)
    stream = stream.split('==============================================================================\n')[1]
    stream += "\n--------------------\n"
    # Test to see if we should keep going or not
    if 'Node 0: :0' not in stream:
        output_file.write(stream)
    else:
        break
    count += 1
output_file.close()