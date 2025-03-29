import gzip

def extract_sample_info_from_geo(file_path="./GSE19804_series_matrix.txt.gz"):
    with gzip.open(file_path, 'rt', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    sample_info = {}
    current_gsm_ids = []

    for line in lines:
        if line.startswith("!Sample_geo_accession"):
            current_gsm_ids = line.strip().split("\t")[1:]
        elif line.startswith("!Sample_characteristics_ch1") or line.startswith("!Sample_source_name_ch1"):
            values = line.strip().split("\t")[1:]
            for gsm, val in zip(current_gsm_ids, values):
                val = val.lower()
                if gsm not in sample_info:
                    sample_info[gsm] = []
                sample_info[gsm].append(val)

    # Κατηγοριοποίηση βάσει keywords
    tumor_samples = []
    normal_samples = []

    for gsm, descriptions in sample_info.items():
        description_text = " ".join(descriptions)
        if "tumor" in description_text or "cancer" in description_text or "adenocarcinoma" in description_text:
            tumor_samples.append(gsm)
        elif "normal" in description_text or "non-tumor" in description_text:
            normal_samples.append(gsm)

    return tumor_samples, normal_samples


# Χρήση της συνάρτησης
tumor_samples, normal_samples = extract_sample_info_from_geo()

print("Tumor samples found:", len(tumor_samples))
print("Normal samples found:", len(normal_samples))


with open("cancer.txt", "a") as f:
    for gsm in tumor_samples:
        f.write(gsm + "\n")

with open("normal.txt", "a") as f:
    for gsm in normal_samples:
        f.write(gsm + "\n")
