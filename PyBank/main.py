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
gInputFile = "./Resources/budget_data.csv"
gOutputFile = "./Analysis/budget_analysis.txt"

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
            colPnL = row[1]
            rec = {"Date": colDate, "PnL": colPnL}
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
        key = rec["Date"]
        pnl = int(rec["PnL"])

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
    # Initialize Variable
    fileText = ""
    fileText += "Financial Analysis\n"
    fileText += "------------------------------------\n"


    # Do the Analysis
    totalMonths = len(trackingDict)
    totalPnL = 0
    greatestIncKey = ""
    greatestIncPnL = 0
    greatestDecKey = ""
    greatestDecPnL = 0
    for key in trackingDict:
        pnl = trackingDict[key]
        totalPnL += pnl
        if pnl > greatestIncPnL:
            greatestIncKey = key
            greatestIncPnL = pnl
        if pnl < greatestDecPnL:
            greatestDecKey = key
            greatestDecPnL = pnl
    
    # Create the Analysis Text
    fileText += "Total Months: " + str(totalMonths) + "\n"
    fileText += "Average Change: $" + str(totalPnL/totalMonths) + "\n"
    fileText += "Greatest Increase in Profits: " + greatestIncKey + " ($" + str(greatestIncPnL) + ")\n"
    fileText += "Greatest Decrease in Profits: " + greatestDecKey + " ($" + str(greatestDecPnL) + ")\n"

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