import csv

with open('tasks.csv') as file_obj:
    # Create reader object by passing the file
    # object to reader method
    reader_obj = csv.reader(file_obj)

    # Iterate over each row in the csv
    # file using reader object
    for row in reader_obj:
        found = False
        for item in row:
            if 'Morytania' in item:
                found = True
                print(row[1])


'''
mory majors
hallow sepulchre TODO
nightmare TODO
barrows DONE
TOB wont bot
grotesque guardians TODO

desert
MTA DONE
giants foundry DONE
kq probably wont bot
TOA wont bot
pyramid plunder DONE

zeah
Tithe Farm DONE
Lake Molch Aerial Fishing DONE
The Wintertodt DONE
Soul Altar and Blood Altar TBD
Blast Mine prob need to fix up
vardorvis
lizard man shamans??
sarachnis


'''
