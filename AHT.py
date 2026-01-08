from datetime import datetime

AHT_IDs = ["AHT25001", "AHT25002"] #machine ids

filePath = "/home/kotamech/Desktop/AHT_Log.txt"

def AHT_Processor(name, data):
    print("AHT Processor started")
    with open(filePath, "a") as file:
            writeLine = name + "|" + data +" | " + str(datetime.now()) + "\n"
            file.write(str(writeLine)) #write received data