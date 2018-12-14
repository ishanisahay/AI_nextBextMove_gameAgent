import time
import sys
import operator
import math

inputItems = {}
lahsaApplicants = []
splaApplicants = []
availableApplicants = []
applicantDetails = {}
availableApplicantsSPLA = []
availableApplicantsLAHSA = []
availableApplicantsForBoth = []
remainingBedSpace = 0
remainingParkingSpace = 0
maxAllotedParking = 0
maxAllotedBeds = 0
md = 10
initialParkingAllocated = [0] * 7
initialBedSpaceAllocated = [0] * 7


def isValidApplicantAssignment(applicantId, maximum, curSpaceAllotment, isSpla, isLahsa):
    global applicantDetails

    if isSpla == 1:
        if checkIfValidForSPLA(applicantId) == 0:
            return False
    if isLahsa == 1:
        if checkIfValidLAHSA(applicantId) == 0:
            return False

    if int(maximum) < int(applicantDetails[applicantId]["Mon"] + curSpaceAllotment[0]):
        return False
    if int(maximum) < int(applicantDetails[applicantId]["Tue"] + curSpaceAllotment[1]):
        return False
    if int(maximum) < int(applicantDetails[applicantId]["Wed"] + curSpaceAllotment[2]):
        return False
    if int(maximum) < int(applicantDetails[applicantId]["Thurs"] + curSpaceAllotment[3]):
        return False
    if int(maximum) < int(applicantDetails[applicantId]["Fri"] + curSpaceAllotment[4]):
        return False
    if int(maximum) < int(applicantDetails[applicantId]["Sat"] + curSpaceAllotment[5]):
        return False
    if int(maximum) < int(applicantDetails[applicantId]["Sun"] + curSpaceAllotment[6]):
        return False
    return True


def checkIfValidForSPLA(applicantId):
    global applicantDetails
    if applicantDetails[applicantId]["car"] == "Y" and applicantDetails[applicantId]["dl"] == "Y" and applicantDetails[applicantId]["medicalCond"] == "N":
        return 1
    else:
        return 0


def checkIfValidLAHSA(applicantId):
    global applicantDetails
    if applicantDetails[applicantId]["pets"] == "N" and int(applicantDetails[applicantId]["age"]) > 17 and applicantDetails[applicantId]["gender"] == "F":
        return 1
    else:
        return 0


def getListOfApplicants(listOfIdAndVal):
    temp = []
    for k in listOfIdAndVal:
        temp.append(k[0])
    return temp


def checkIfShouldCut(alpha, beta):
    if alpha != None and beta != None:
        if alpha + beta >= 0:
            return True
    return False


def checkIfAlphaBetaToUpdate(maxVal, curVal):
    if maxVal is None or curVal > maxVal:
        return True
    return False


def parseinput(lines):
    global inputItems
    global applicantDetails
    global initialParkingAllocated
    global initialBedSpaceAllocateds
    global availableApplicantsSPLA
    global availableApplicantsLAHSA
    global availableApplicantsForBoth

    availableForSPLABasedOnDays = {}
    availableForLAHSABasedOnDays = {}
    availableForBothBasedOnDays = {}

    inputItems["noOfBeds"] = lines[0]
    inputItems["noOfParkingSpaces"] = lines[1]
    inputItems["noOfLAHSAChosen"] = lines[2]
    no_LAHSA = int(inputItems["noOfLAHSAChosen"])
    k = 3
    for i in range(0, no_LAHSA):
        lahsaApplicants.append(lines[k])
        k = k + 1
    inputItems["LAHSAapplicantsSoFar"] = lahsaApplicants

    no_SPLA = int(lines[k])
    inputItems["noOfSPLAChosen"] = no_SPLA
    k = k + 1
    for i in range(0, no_SPLA):
        splaApplicants.append(lines[k])
        k = k + 1
    inputItems["SPLAaapplicantsSoFar"] = splaApplicants

    inputItems["totalNoApplicants"] = lines[k]
    k = k + 1
    for i in range(0, int(inputItems["totalNoApplicants"])):
        availableApplicants.append(lines[k])
        k = k + 1
    inputItems["allApplicants"] = availableApplicants

    for item in availableApplicants:
        temp = {}
        applicantId = item[0:5]
        gender = item[5]
        age = item[6:9]
        pets = item[9]
        medicalCond = item[10]
        car = item[11]
        dl = item[12]
        daysreqd = item[13:20]
        applicantDetails[applicantId] = {}
        applicantDetails[applicantId]["gender"] = gender
        applicantDetails[applicantId]["age"] = age
        applicantDetails[applicantId]["pets"] = pets
        applicantDetails[applicantId]["medicalCond"] = medicalCond
        applicantDetails[applicantId]["car"] = car
        applicantDetails[applicantId]["dl"] = dl
        applicantDetails[applicantId]["days"] = daysreqd
        cnt = 0
        for k in daysreqd:
            if k == "1":
                cnt = cnt + 1
        applicantDetails[applicantId]["noOfDaysReqd"] = cnt

        i =  0

        applicantDetails[applicantId]["Mon"] = int(daysreqd[i])
        applicantDetails[applicantId]["Tue"] = int(daysreqd[i + 1])
        applicantDetails[applicantId]["Wed"] = int(daysreqd[i + 2])
        applicantDetails[applicantId]["Thurs"] = int(daysreqd[i + 3])
        applicantDetails[applicantId]["Fri"] = int(daysreqd[i + 4])
        applicantDetails[applicantId]["Sat"] = int(daysreqd[i + 5])
        applicantDetails[applicantId]["Sun"] = int(daysreqd[i + 6])

        if checkIfValidForSPLA(applicantId) == 1 and checkIfValidLAHSA(applicantId) == 1 and applicantId not in splaApplicants and applicantId not in lahsaApplicants:
            availableForBothBasedOnDays[applicantId] = applicantDetails[applicantId]["noOfDaysReqd"]

        if checkIfValidForSPLA(applicantId) == 1 and applicantId not in splaApplicants and applicantId not in lahsaApplicants:
            availableForSPLABasedOnDays[applicantId] = applicantDetails[applicantId]["noOfDaysReqd"]

        if checkIfValidLAHSA(applicantId) == 1 and applicantId not in splaApplicants and applicantId not in lahsaApplicants:
            availableForLAHSABasedOnDays[applicantId] = applicantDetails[applicantId]["noOfDaysReqd"]


    sortedAvailableForBothBasedOnDays1 = sorted(availableForBothBasedOnDays.items(),key=operator.itemgetter(0))
    sortedAvailableForBothBasedOnDays2 = sorted(sortedAvailableForBothBasedOnDays1, key=operator.itemgetter(1), reverse=True)
    sortedAvailableForSPLABasedOnDays1 = sorted(availableForSPLABasedOnDays.items(), key=operator.itemgetter(0))
    sortedAvailableForLAHSABasedOnDays1 = sorted(availableForLAHSABasedOnDays.items(), key=operator.itemgetter(0))
    sortedAvailableForSPLABasedOnDays2 = sorted(sortedAvailableForSPLABasedOnDays1, key=operator.itemgetter(1), reverse=True)
    sortedAvailableForLAHSABasedOnDays2 = sorted(sortedAvailableForLAHSABasedOnDays1, key=operator.itemgetter(1), reverse=True)
    #print sortedAvailableForSPLABasedOnDays
    #print and check if order is correct
    availableApplicantsSPLA = getListOfApplicants(sortedAvailableForSPLABasedOnDays2)
    availableApplicantsLAHSA = getListOfApplicants(sortedAvailableForLAHSABasedOnDays2)
    availableApplicantsForBoth = getListOfApplicants(sortedAvailableForBothBasedOnDays2)

    #print availableApplicantsSPLA
    #print availableApplicantsLAHSA
    #print availableApplicantsForBoth

    for k in splaApplicants:
        initialParkingAllocated[0] += int(applicantDetails[k]["Mon"])
        initialParkingAllocated[1] += int(applicantDetails[k]["Tue"])
        initialParkingAllocated[2] += int(applicantDetails[k]["Wed"])
        initialParkingAllocated[3] += int(applicantDetails[k]["Thurs"])
        initialParkingAllocated[4] += int(applicantDetails[k]["Fri"])
        initialParkingAllocated[5] += int(applicantDetails[k]["Sat"])
        initialParkingAllocated[6] += int(applicantDetails[k]["Sun"])

    for k in lahsaApplicants:
        initialBedSpaceAllocated[0] += int(applicantDetails[k]["Mon"])
        initialBedSpaceAllocated[1] += int(applicantDetails[k]["Tue"])
        initialBedSpaceAllocated[2] += int(applicantDetails[k]["Wed"])
        initialBedSpaceAllocated[3] += int(applicantDetails[k]["Thurs"])
        initialBedSpaceAllocated[4] += int(applicantDetails[k]["Fri"])
        initialBedSpaceAllocated[5] += int(applicantDetails[k]["Sat"])
        initialBedSpaceAllocated[6] += int(applicantDetails[k]["Sun"])


def maximizeSpaceSPLA(start, d, alpha, beta, availableApplicantsSPLA, curAllotedParking, p, b, availableApplicantsLAHSA,
                      curAllotedBeds, availableApplicantsForBoth):
    global applicantDetails
    global md
    #print "SPLA"
    #print d
    cnt = 0
    '''if md == d:
        return sum(curAllotedParking)'''

    if len(availableApplicantsSPLA) == 0 and len(availableApplicantsLAHSA) == 0:
        return sum(curAllotedParking)

    if len(availableApplicantsSPLA) == 0:
        return maximizeSpaceLAHSA(start, d, alpha, beta, availableApplicantsSPLA, curAllotedParking, p, b, availableApplicantsLAHSA,
                      curAllotedBeds, availableApplicantsForBoth)

    maxVal = None

    for k in availableApplicantsSPLA:
        if time.time() - start >= 176:
            break

        '''if int(cnt) == int(p):
            break'''

        #if int(cnt) >= int(p)-int(d/2):
            #break

        if isValidApplicantAssignment(k, p, curAllotedParking, 1, 0):
            cnt = cnt + 1
            availableApplicantsSPLA_copy = availableApplicantsSPLA[:]
            availableApplicantsSPLA_copy.remove(k)
            availableApplicantsLAHSA_copy = availableApplicantsLAHSA[:]
            availableApplicantsForBoth_copy = availableApplicantsForBoth[:]
            if k in availableApplicantsForBoth:
                availableApplicantsLAHSA_copy.remove(k)
                availableApplicantsForBoth_copy.remove(k)

            curAllotedParkingCopy = curAllotedParking[:]

            curAllotedParkingCopy[0] += int(applicantDetails[k]["Mon"])
            curAllotedParkingCopy[1] += int(applicantDetails[k]["Tue"])
            curAllotedParkingCopy[2] += int(applicantDetails[k]["Wed"])
            curAllotedParkingCopy[3] += int(applicantDetails[k]["Thurs"])
            curAllotedParkingCopy[4] += int(applicantDetails[k]["Fri"])
            curAllotedParkingCopy[5] += int(applicantDetails[k]["Sat"])
            curAllotedParkingCopy[6] += int(applicantDetails[k]["Sun"])

            if len(availableApplicantsLAHSA_copy) == 0 and len(availableApplicantsSPLA_copy) == 0:
                return  sum(curAllotedParkingCopy)

            curVal = maximizeSpaceLAHSA(start, d+1, alpha, beta, availableApplicantsSPLA_copy, curAllotedParkingCopy, p, b,
                                        availableApplicantsLAHSA_copy,curAllotedBeds, availableApplicantsForBoth_copy)
            curVal = -1 * curVal

            if checkIfAlphaBetaToUpdate(maxVal, curVal) == True:
                maxVal = curVal
                alpha = maxVal

            if checkIfShouldCut(alpha, beta) == True:
                break

    if maxVal is None:
        return sum(curAllotedParking)
    return maxVal


def maximizeSpaceLAHSA(start, d, alpha, beta, availableApplicantsSPLA, curAllotedParking, p, b, availableApplicantsLAHSA,
                       curAllotedBeds, availableApplicantsForBoth):
    global applicantDetails
    maxVal = None
    global md
    cnt = 0
    #print "LAHSA"
    #print d
    # call max value spla for remaining candidates eligible for spla
    '''if d == md:
        return sum(curAllotedBeds)'''

    if len(availableApplicantsLAHSA) == 0 and len(availableApplicantsSPLA) == 0:
        return sum(curAllotedBeds)

    if len(availableApplicantsLAHSA) == 0:
        return maximizeSpaceSPLA(start, d, alpha, beta, availableApplicantsSPLA, curAllotedParking, p, b, availableApplicantsLAHSA,
                       curAllotedBeds, availableApplicantsForBoth)

    for k in availableApplicantsLAHSA:

        if time.time() - start >= 176:
            break

        '''if int(cnt) == int(b):
            break'''

        #if int(cnt) >= int(b) - int(d/2):
            #break

        if isValidApplicantAssignment(k, b, curAllotedBeds, 0, 1):
            cnt = cnt + 1

            availableApplicantsLAHSA_copy = availableApplicantsLAHSA[:]
            availableApplicantsLAHSA_copy.remove(k)
            availableApplicantsSPLA_copy = availableApplicantsSPLA[:]
            availableApplicantsForBoth_copy = availableApplicantsForBoth[:]
            if k in availableApplicantsForBoth:
                availableApplicantsSPLA_copy.remove(k)
                availableApplicantsForBoth_copy.remove(k)

            curAllotedBedsCopy = curAllotedBeds[:]

            curAllotedBedsCopy[0] += int(applicantDetails[k]["Mon"])
            curAllotedBedsCopy[1] += int(applicantDetails[k]["Tue"])
            curAllotedBedsCopy[2] += int(applicantDetails[k]["Wed"])
            curAllotedBedsCopy[3] += int(applicantDetails[k]["Thurs"])
            curAllotedBedsCopy[4] += int(applicantDetails[k]["Fri"])
            curAllotedBedsCopy[5] += int(applicantDetails[k]["Sat"])
            curAllotedBedsCopy[6] += int(applicantDetails[k]["Sun"])

            if len(availableApplicantsLAHSA_copy) == 0 and len(availableApplicantsSPLA_copy) == 0:
                return  sum(curAllotedBedsCopy)

            curVal = maximizeSpaceSPLA(start, d+1, alpha, beta, availableApplicantsSPLA_copy, curAllotedParking, p, b, availableApplicantsLAHSA_copy,
                      curAllotedBedsCopy, availableApplicantsForBoth_copy)
            curVal = -1 * curVal

            if checkIfAlphaBetaToUpdate(maxVal, curVal) == True:
                maxVal = curVal
                beta = maxVal

            if checkIfShouldCut(alpha, beta) == True:
                break

    if maxVal is None:
        return (sum(curAllotedBeds))
    return maxVal

def main():
    start = time.time()
    fp = open("grading_case/input22.txt", 'r')
    lines = fp.read().splitlines()
    fp.close()
    global applicantDetails
    global initialParkingAllocated
    global initialBedSpaceAllocated
    global availableApplicantsSPLA
    global availableApplicantsLAHSA
    global availableApplicantsForBoth
    global inputItems

    alpha = None
    beta = None
    maxId = None
    maxVal = None

    parseinput(lines)

    for k in availableApplicantsSPLA:
        #assign for SPLA
        if time.time() - start >= 176:
            break

        if isValidApplicantAssignment(k, inputItems["noOfParkingSpaces"], initialParkingAllocated, 1, 0):

            #check if id should be removed from remaining spla since here we assign for spla
            #and that updated copy should be sent to ONlySPLAPicks
            availableApplicantsSPLA_copy = availableApplicantsSPLA[:]
            availableApplicantsSPLA_copy.remove(k)
            availableApplicantsLAHSA_copy = availableApplicantsLAHSA[:]
            availableApplicantsForBoth_copy = availableApplicantsForBoth[:]
            if k in availableApplicantsForBoth:
                availableApplicantsLAHSA_copy.remove(k)
                availableApplicantsForBoth_copy.remove(k)

            curAllotedParkingCopy = initialParkingAllocated[:]
            #update the parking copy list
            curAllotedParkingCopy[0] += int(applicantDetails[k]["Mon"])
            curAllotedParkingCopy[1] += int(applicantDetails[k]["Tue"])
            curAllotedParkingCopy[2] += int(applicantDetails[k]["Wed"])
            curAllotedParkingCopy[3] += int(applicantDetails[k]["Thurs"])
            curAllotedParkingCopy[4] += int(applicantDetails[k]["Fri"])
            curAllotedParkingCopy[5] += int(applicantDetails[k]["Sat"])
            curAllotedParkingCopy[6] += int(applicantDetails[k]["Sun"])

            curVal = maximizeSpaceLAHSA(start, 0, alpha, beta, availableApplicantsSPLA_copy, curAllotedParkingCopy, inputItems["noOfParkingSpaces"], inputItems["noOfBeds"], availableApplicantsLAHSA_copy,
                       initialBedSpaceAllocated, availableApplicantsForBoth_copy)
            curVal = -1 * curVal
            print str(k) + "** " + str(abs(curVal))

            if  maxVal is None:
                maxVal = curVal
                alpha = maxVal
                maxId = k
            elif abs(curVal) > abs(maxVal):
                maxVal = curVal
                alpha = maxVal
                maxId = k
            elif curVal == maxVal:
                if (int(k)) < int(maxId):
                    maxId = k
            print "maxId" + "____" + str(maxId)


    applicantID = maxId
    #print maxId
    #print time.time() - start
    fp = open("output.txt", 'w')
    fp.write(str(applicantID))
    fp.close()

if __name__ == "__main__":
    main()

