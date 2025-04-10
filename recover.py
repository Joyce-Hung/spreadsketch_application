#!/usr/bin/env python3
# recover.py
import socket
from collections import defaultdict
def clean_raw_text(text):
    # remove useless message, keep only the register record line
    lines = text.strip().splitlines()
    for line in lines:
        if "ss_" in line and "=" in line:
            return line.strip()
    raise ValueError("No valid register data found.")
    
    
def read_comma_separated_register(content, value_base=10):
    
    # analyze register content ex :'ss_key= 123, 456, 789,...', return: {index: value}
    
    if '=' not in content:
        raise ValueError(f"Unexpected format in {filename}")
    values_str = content.split('=')[1].strip()
    values = values_str.split(',')
    reg = {}
    for idx, val in enumerate(values):
        val = val.strip()
        if val:
            reg[idx] = int(val, base=value_base)
    return reg

def parse_clean_file(filename, value_base=10):
    with open(filename) as f:
        raw = f.read()
    cleaned = clean_raw_text(raw)
    return read_comma_separated_register(cleaned, value_base=value_base)

def count_bitmap_bits(bitmap, base_index, level):
   
    # count # of "bit = 1" in bitmap, according to start index and level 
    # each layer's bitmap has 2^level bits

    offset = level << 5  # level * 32
    bitmap_range = range(base_index + offset, base_index + offset + (1 << level))
    return sum(bitmap.get(i, 0) for i in bitmap_range)

def analyze_spread(keys, levels, bitmap):
    #traverse all buckets, calculate spread count of each ip from  bitmap
    spread_table = {}
    for bucket_idx, ip in keys.items():
        level = levels.get(bucket_idx, 0)
        base_index = bucket_idx << 7  # each bucket corresponding to 128 bits
        spread = count_bitmap_bits(bitmap, base_index, level)
        spread_table[ip] = spread_table.get(ip, 0) + spread
    return spread_table

# read 3 layer
keys0   = parse_clean_file("trace3_ss_key.txt")
levels0 = parse_clean_file("trace3_ss_level.txt")
bmp0    = parse_clean_file("trace3_ss_bmp.txt")

keys1   = parse_clean_file("trace3_ss_key1.txt")
levels1 = parse_clean_file("trace3_ss_level1.txt")
bmp1    = parse_clean_file("trace3_ss_bmp1.txt")

keys2   = parse_clean_file("trace3_ss_key2.txt")
levels2 = parse_clean_file("trace3_ss_level2.txt")
bmp2    = parse_clean_file("trace3_ss_bmp2.txt")

# analyze each layer
spread0 = analyze_spread(keys0, levels0, bmp0)
spread1 = analyze_spread(keys1, levels1, bmp1)
spread2 = analyze_spread(keys2, levels2, bmp2)

# merge result
final_spread = defaultdict(int)
for table in [spread0, spread1, spread2]:
    for ip, count in table.items():
        final_spread[ip] += count

# Gathering top-5 superspreader ===
top_k = sorted(final_spread.items(), key=lambda x: x[1], reverse=True)[100:120]
print("Top-k Superspreaders:")
for ip, spread in top_k:
    try:
        ip_str = socket.inet_ntoa(ip.to_bytes(4, 'big'))
    except Exception:
        ip_str = f"[Invalid IP {ip}]"
    print(f"IP: {ip_str}, Spread: {spread}")

