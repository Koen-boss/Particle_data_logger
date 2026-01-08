from datetime import datetime

SBA_IDs = ["SBA23-001","SBA23-002"] #Machine IDs

filePath = "/home/kotamech/Desktop/SBA_Log.txt"

def SBA_Processor(name, data):
    print("SBA Processor started")
    with open(filePath, "a") as file:
            writeLine = name + "|" + data +" | " + str(datetime.now()) + "\n"
            file.write(str(writeLine)) #write received data