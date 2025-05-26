def load_bmp_file(path):
    with open(path) as f:
        line = [l for l in f if "ss_bmp" in l and "=" in l][0]
    data = line.split("=")[1].strip().split(",")
    bmp = {}
    for idx, val in enumerate(data):
        val = val.strip()
        if val:
            bmp[idx] = int(val)
    return bmp

def merge_bitmaps(bmp1, bmp2):
    merged = {}
    all_keys = set(bmp1.keys()) | set(bmp2.keys())
    for k in all_keys:
        merged[k] = bmp1.get(k, 0) | bmp2.get(k, 0)
    return merged

def save_bmp_to_file(bmp, filename, label="ss_bmp"):
    values = [str(bmp.get(i, 0)) for i in range(max(bmp.keys()) + 1)]
    with open(filename, "w") as f:
        f.write(f"{label}= {', '.join(values)}\n")


bmp_layers = [
    ("s2_ss_bmp.txt",  "s3_ss_bmp.txt",  "merged_ss_bmp.txt",  "ss_bmp"),
    ("s2_ss_bmp1.txt", "s3_ss_bmp1.txt", "merged_ss_bmp1.txt", "ss_bmp1"),
    ("s2_ss_bmp2.txt", "s3_ss_bmp2.txt", "merged_ss_bmp2.txt", "ss_bmp2"),
]

for s2_path, s3_path, output_path, label in bmp_layers:
    s2_bmp = load_bmp_file(s2_path)
    s3_bmp = load_bmp_file(s3_path)
    merged_bmp = merge_bitmaps(s2_bmp, s3_bmp)
    save_bmp_to_file(merged_bmp, output_path, label)
    print(f"Merged and saved: {output_path}")

