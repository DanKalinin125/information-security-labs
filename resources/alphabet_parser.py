import re
import csv

source_alphabet_file = open("source_alphabet.txt", "r", encoding="utf-8")
text = source_alphabet_file.read()
source_alphabet_file.close()

# Распознавание точек и подготовка данных
raw_matches = re.findall(r'\d+ .{1,10} \(\d+, \d+\)', text)
matches = []
for raw_match in raw_matches:
    split_raw_match = raw_match.split(" ")
    match = [split_raw_match[0],
             split_raw_match[1],
             split_raw_match[2][1:len(split_raw_match[2])-1:],
             split_raw_match[3][:len(split_raw_match[3])-1:]]
    matches.append(match)
matches.sort(key=lambda match: int(match[0]))
print(matches)

# Запись в csv
with open("alphabet.csv", mode="w", encoding='utf-8') as w_file:
    file_writer = csv.writer(w_file, delimiter = ",", lineterminator="\r")
    file_writer.writerow(["№", "Символ", "x", "y"])
    for match in matches:
        file_writer.writerow(match)