import re

def extract_bitmap(filepath):
    with open(filepath, 'r') as f:
        for line in f:
            if "ss_bmp=" in line:
                #  extract bitmap 
                bitmap_str = re.search(r"ss_bmp=\s*(.*)", line).group(1)
                return [int(x.strip()) for x in bitmap_str.split(",") if x.strip() in ['0', '1']]
    raise ValueError(f"No ss_bmp= found in {filepath}")

def write_bitmap(filepath, original_header, result_bitmap):
    with open(filepath, 'w') as f:
        f.write(original_header)
        f.write("ss_bmp= " + ", ".join(map(str, result_bitmap)) + "\n")



# read bitmap
bmp1 = extract_bitmap("s2/s2_bmp.txt")
bmp2 = extract_bitmap("s3/s3_bmp.txt")

# check length of 2 bitmaps
if len(bmp1) != len(bmp2):
    raise ValueError("Bitmap lengths do not match!")

# do bitwise OR
bmp_or = [b1 | b2 for b1, b2 in zip(bmp1, bmp2)]

# add log string for later comparison with s1_bmp.txt
original_header = "Obtaining JSON from switch...\nDone\nControl utility for runtime P4 table manipulation\nRuntimeCmd: "

# 
write_bitmap("s2_s3_bitmap_or.txt", original_header, bmp_or)

print("Done OR Operation!")

