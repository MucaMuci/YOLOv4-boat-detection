import os

def incrementNumber(number):
    global globalCounter
    globalCounter[number] += 1

def openFile(fileName):
    global folderList
    file = open(folderList +"/"+fileName).readlines()
    for line in file:
        line = line.split()
        incrementNumber(int(line[0]))

folderList = r''    # put in folder path where all the txt files are located
globalCounter = [0, 0, 0, 0, 0, 0, 0, 0, 0]
suma = 0


listOfFiles = os.listdir(folderList)
for fileName in listOfFiles:
    if 'Luka' in fileName:
        if '.txt' in fileName:
            openFile(fileName)

for i in globalCounter:
    suma += i

print(f"Broj Katamarana je {globalCounter[0]}")
print(f"Broj Kruzera je {globalCounter[1]}")
print(f"Broj Trajekata je {globalCounter[2]}")
print(f"Broj Jetskijeva je {globalCounter[3]}")
print(f"Broj Jedrilica je {globalCounter[4]}")
print(f"Broj Malih brodova je {globalCounter[5]}")
print(f"Broj Glisera je {globalCounter[6]}")
print(f"Broj Turističkih brodova je {globalCounter[7]}")
print(f"Broj Jahti je {globalCounter[8]}")

print(f"Sveukupno brodova labelirano: {suma} ")