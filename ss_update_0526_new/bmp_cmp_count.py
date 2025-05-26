import re

def extract_bitmap(filepath):
    with open(filepath, 'r') as f:
        for line in f:
            if "ss_bmp=" in line:
                bitmap_str = re.search(r"ss_bmp=\s*(.*)", line).group(1)
            elif "ss_bmp2=" in line:
                bitmap_str = re.search(r"ss_bmp2=\s*(.*)", line).group(1)
            elif "ss_bmp1=" in line:
                bitmap_str = re.search(r"ss_bmp1=\s*(.*)", line).group(1)
                return [int(x.strip()) for x in bitmap_str.split(",") if x.strip() in ['0', '1']]
    raise ValueError(f"No ss_bmp= found in {filepath}")

#read bmp

bmp1 = extract_bitmap("merged_ss_bmp1.txt")
bmp2 = extract_bitmap("s1_ss_bmp1.txt")

if len(bmp1) != len(bmp2):
    raise ValueError("Bitmap lengths do not match!")

# XOR --> 1 bit
diff_count = sum(b1 != b2 for b1, b2 in zip(bmp1, bmp2))

print(f"Total : {diff_count} different bits")

