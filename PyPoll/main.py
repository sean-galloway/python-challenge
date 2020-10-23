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
gInputFile = os.path.join("Resources", "election_data.csv")
gOutputFile = os.path.join("Analysis", "election_analysis.txt")
gGetCWD = os.path.dirname(os.path.abspath(__file__))


###############################################################################
# parse CSV File
###############################################################################
def parseCSV(csvFile):
    # Create the DCT object the Holds the Tally information
    elctionDict = collections.OrderedDict()
    # Open the input file
    try:
        reader = csv.reader(open(csvFile))
    except IOError:
        print("Error, could not open CSV File: " + csvFile)
        sys.exit(1)

    # Read the file into an Election Dictionary and total the votes
    totalVotes = 0
    try:
        line = -1
        for row in reader:
            line += 1
            if line == 0:
                continue
            # print("Line: " + str(line))
            # colVoter = row[0]
            # colCounty = row[1]
            colCandidate = row[2]
            totalVotes += 1
            if colCandidate not in elctionDict:
                elctionDict[colCandidate] = 1
            else:
                elctionDict[colCandidate] += 1

    except csv.Error as e:
        sys.exit('Error reading CSV File: ' + csvFile + " line number " +
                 str(line) + " error: " + str(e))
   # Return the results
    return totalVotes, elctionDict

###############################################################################
# Tally the results and write them out
###############################################################################
def writeResult(totalVotes, elctionDict, outputFile):
    # Initialize Variables
    fileText = ""
    fileText += "Election Results\n"
    fileText += "-------------------------\n"
    fileText += f"Total Votes: {totalVotes}\n"
    fileText += "-------------------------\n"

    # Do the Analysis
    sortedResults = sorted(elctionDict.items(), key=lambda x: x[1], reverse=True)
    winner = sortedResults[0][0]
    for i in sortedResults:
        candidate = i[0]
        votes = i[1]
        percentVotes = 100 * votes/totalVotes
        fileText += f"{candidate}: {percentVotes:.3f}% ({votes})\n"
    fileText += "-------------------------\n"
    fileText += f"Winner: {winner}\n"
    fileText += "-------------------------\n"

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
    totalVotes, elctionDict = parseCSV(gInputFile)
    writeResult(totalVotes, elctionDict, gOutputFile)

###############################################################################
# Run Main
###############################################################################
if __name__ == "__main__":
    main()