import argparse
import json
import base64
from itertools import cycle
from dotnetfile import DotNetPE


parser = argparse.ArgumentParser(description="Redline config extractor")
parser.add_argument("-f","--file", help="Input file", required=True)
parser.add_argument("-o","--output", help="Output file", required=False)
args = parser.parse_args()


dotnet_file = DotNetPE(args.file)
us_strings = dotnet_file.get_user_stream_strings()

string_count = len(us_strings)
conf_key = us_strings[string_count-1]
conf_id = us_strings[string_count-2]
conf_ip = us_strings[string_count-3]

decode_ip = base64.b64decode(conf_ip)

decrypted_ip = bytes(a ^ b for a, b in zip(decode_ip, cycle(bytes(conf_key, 'utf-8'))))
dec_ip = base64.b64decode(decrypted_ip).decode('utf-8')

config_data = {"key": conf_key, "id":conf_id, "ip":conf_ip, "decrypted_ip":dec_ip}
if args.output:
    with open(args.output, "w") as f:
        f.write(json.dumps(config_data, indent=4))
else:
    print(json.dumps(config_data, indent=4))

