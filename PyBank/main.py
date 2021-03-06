###############################################################################
# Imports
###############################################################################
import os
import sys
import collections
import pprint
# import json
import csv


###############################################################################
# Setup Globals
###############################################################################
gInputFile = os.path.join("Resources", "budget_data.csv")
gOutputFile = os.path.join("Analysis", "budget_analysis.txt")
gGetCWD = os.path.dirname(os.path.abspath(__file__))


###############################################################################
# parse CSV File
###############################################################################
def parseCSV(csvFile):
    # Open the input file
    try:
        reader = csv.reader(open(csvFile))
    except IOError:
        print("Error, could not open CSV File: " + csvFile)
        sys.exit(1)
    csvRecords = []

    # Read the file into a bunch of records
    try:
        line = -1
        for row in reader:
            line += 1
            if line == 0:
                continue
            # print("Line: " + str(line))
            colDate = row[0]
            colPnL = float(row[1])
            rec = {"date": colDate, "pnl": colPnL}
            csvRecords.append(rec)

    except csv.Error as e:
        sys.exit('Error reading CSV File: ' + csvFile + " line number " +
                 str(line) + " error: " + str(e))
   # Return the results
    return csvRecords

###############################################################################
# process CSV Records
###############################################################################
def processCSVRecords(csvRecords):
    # Create the DCT object the Holds the Tally information
    trackingDict = collections.OrderedDict()

    # Iterate thru the records
    for rec in csvRecords:
        key = rec["date"]
        pnl = rec["pnl"]

        if key not in trackingDict:
            trackingDict[key] = pnl
        else:
            trackingDict[key] += pnl

    # Return the results
    return trackingDict

###############################################################################
# Summarize results and write them out
###############################################################################
def writeResult(trackingDict, outputFile):

    # Do the Analysis
    totalMonths = len(trackingDict)
    totalPnL = 0
    lastPnL = 0
    blnFirst = True
    netChangePnL = 0
    currentChange = 0
    greatestInc_key = ""
    greatestInc_val = 0
    greatestDec_key = ""
    greatestDec_val = 0
    for key in trackingDict:
        pnl = trackingDict[key]
        totalPnL += pnl
        if blnFirst is False:
            currentChange = pnl - lastPnL
            # print(f"Current Change {currentChange}")
            netChangePnL += currentChange
        lastPnL = pnl
        blnFirst = False
        if currentChange > greatestInc_val:
            greatestInc_key = key
            greatestInc_val = currentChange
        if currentChange < greatestDec_val:
            greatestDec_key = key
            greatestDec_val = currentChange
    # print(f"netChangePnL {netChangePnL} totalMonths {totalMonths}")
    averageChangePnL = netChangePnL/(totalMonths-1)
    # print(f"averageChangePnL {averageChangePnL}")
    
    # Create the Analysis Text
    fileText = ""
    fileText += "Financial Analysis\n"
    fileText += "------------------------------------\n"
    fileText += f"Total Months: {totalMonths}\n"
    fileText += f"Total: {totalPnL:.2f}\n"
    fileText += f"Average Change: ${averageChangePnL:.2f}\n"
    fileText += f"Greatest Increase in Profits: {greatestInc_key} (${greatestInc_val:.2f})\n"
    fileText += f"Greatest Decrease in Profits: {greatestDec_key} (${greatestDec_val:.2f})\n"

    # Write the Analysis out
    print(fileText)
    fh = open(outputFile, "w")
    fh.write(fileText)
    fh.close()

###############################################################################
# Main
###############################################################################
def main():
    # Run the Functions here
    csvRecords = parseCSV(gInputFile)
    trackingDict = processCSVRecords(csvRecords)
    writeResult(trackingDict, gOutputFile)

###############################################################################
# Run Main
###############################################################################
if __name__ == "__main__":
    main()