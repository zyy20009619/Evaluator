import csv

from arch_debt.maintenance_cost_measurement.basedata import ModifyDetail, CommitDetail
from arch_debt.maintenance_cost_measurement.gitlogprocessor import get_file_mc

commitCollection = list()

rootDir = 'D:\\data\\1.23\\groundtruth\\' #输出文件夹


def printAll(commitCollection):
    issues = 0
    for each in commitCollection:
        for issueId in each.issueIds:
            issues += 1

        '''
        print(each.commitId)
        print(each.author)
        print(each.date)
        print(each.issueIds)
        print(each.modifyDetail.fileList)
        print(each.modifyDetail.addList)
        print(each.modifyDetail.delList)
        print("\n")
        '''
    #print("issues", issues)


def computeCOR(commitCollection):
    allChangeCmtFiles = set()
    changeCmtFilesLapCount = 0
    allBugCmtFiles = set()
    bugCmtFilesLapCount = 0

    for oneCommit in commitCollection:
        issueIds = oneCommit.issueIds
        changeCmtFilesLapCount += len(oneCommit.modifyDetail.fileList)
        if len(issueIds) != 0:
            bugCmtFilesLapCount += len(oneCommit.modifyDetail.fileList)

        for fileName in  oneCommit.modifyDetail.fileList:
            allChangeCmtFiles.add(fileName)
            if len(issueIds) != 0:
                allBugCmtFiles.add(fileName)

    if len(allChangeCmtFiles) == 0:
        CCOR = "Null"
    else:
        CCOR = changeCmtFilesLapCount / float(len(allChangeCmtFiles))
    if len( allBugCmtFiles) == 0:
        BCOR = "Null"
    else:
        BCOR = bugCmtFilesLapCount / float(len(allBugCmtFiles))
    print("CCOR:", CCOR)
    print("BCOR:", BCOR)

    return CCOR, BCOR, len(allChangeCmtFiles), len(allBugCmtFiles)


def statisticCommiter(commitCollection):
    #statistic the files for each commiter
    changeCommiterDict = dict() #dict[commiter] = set[fileList]
    bugCommiterDict = dict()
    for oneCommit in commitCollection:
        issueIds = oneCommit.issueIds
        author = oneCommit.author

        if author not in changeCommiterDict:
            changeCommiterDict[author] = set()

        if len(issueIds) != 0 and author not in bugCommiterDict:
            bugCommiterDict[author] = set()

        for fileName in oneCommit.modifyDetail.fileList:
            changeCommiterDict[author].add(fileName)
            if len(issueIds) != 0:
                bugCommiterDict[author].add(fileName)
    return changeCommiterDict, bugCommiterDict

def computeCFOR(changeCommiterDict, bugCommiterDict):
    CCFOR = 0
    fileSet = set()
    for authorName in changeCommiterDict:
        aset = changeCommiterDict[authorName]
        CCFOR += len(aset)
        fileSet = fileSet.union(aset)
    if len(fileSet) == 0:
        CCFOR = "null"
    else:
        CCFOR = CCFOR / float(len(fileSet))
    print("CCFOR: ", CCFOR, len(fileSet))

    BCFOR = 0
    fileSet = set()
    for authorName in bugCommiterDict:
        aset = bugCommiterDict[authorName]
        BCFOR += len(aset)
        fileSet = fileSet.union(aset)
    if len(fileSet) == 0:
        BCFOR = "null"
    else:
        BCFOR = BCFOR / float(len(fileSet))
    print("BCFOR: ", BCFOR, len(fileSet))
    return CCFOR, BCFOR


def computePCO(changeCommiterDict, bugCommiterDict):
    cpcoList = list()
    for author1 in changeCommiterDict:
        fileSet1 = changeCommiterDict[author1]
        for author2 in changeCommiterDict:
            fileSet2 = changeCommiterDict[author2]
            if author1 != author2:
                if len(fileSet1.union(fileSet2)) == 0:
                    continue
                pco  = len(fileSet1.intersection(fileSet2))  / float( len(fileSet1.union(fileSet2)))
                cpcoList.append(pco)

    bpcoList = list()
    for author1 in bugCommiterDict:
        fileSet1 = bugCommiterDict[author1]
        for author2 in bugCommiterDict:
            fileSet2 = bugCommiterDict[author2]
            if author1 != author2:
                if len(fileSet1.union(fileSet2)) == 0:
                    continue
                pco  = len(fileSet1.intersection(fileSet2))  / float( len(fileSet1.union(fileSet2)))
                bpcoList.append(pco)

    if len(cpcoList) == 0:
        CPCO = "null"
    else:
        CPCO = sum(cpcoList) / float( len(cpcoList) )
    if len(bpcoList) == 0:
        BPCO = "null"
    else:
        BPCO = sum(bpcoList) / float( len(bpcoList) )
    print("CPCO: ", CPCO)
    print("BPCO: ", BPCO)
    return CPCO, BPCO






def writeCSV(aList, fileName):
    with open(fileName, "w", newline="") as fp:
        writer = csv.writer(fp, delimiter=",")
        writer.writerows(aList)

'''
def toIntList(listStr):
    resList = list()
    for tmp in listStr.split(";"):
        resList.append( int(tmp) )
    return resList
'''

def readHistory(historyFile):
    commitCollection = list()
    bugCommitLen = 0
    with open(historyFile, "r", newline="", encoding='utf-8') as fp:
        csv.field_size_limit(500 * 1024 * 1024)
        reader = csv.reader(fp, delimiter=",")
        for row in reader:
            [commitId, author, date, issueIdStr, filesStr, addsStr, delsStr] = row
            if(issueIdStr != ""):
                issueIds = issueIdStr.split(";")
                bugCommitLen += 1
            else:
                issueIds = list()
            fileList = filesStr.split(";")
            addList = addsStr.split(";")
            delList = delsStr.split(";")
            modifyDetail = ModifyDetail(fileList, addList, delList)
            oneCommit = CommitDetail(commitId, author, date, issueIds, modifyDetail)
            commitCollection.append(oneCommit)
    return commitCollection, len(commitCollection),bugCommitLen


def computeEntry(historyFile, project_name):
    CCOR_list = list()
    CCFOR_list = list()
    CPCO_list = list()
    [commitCollection, commitLen, bugCommitLen]  = readHistory(historyFile)

    #printAll(commitCollection)
    #print("len: ", len(commitCollection))

    [CCOR, BCOR, allChangeCmtFileCount, allbugCmtFileCount] = computeCOR(commitCollection)
    [changeCommiterDict, bugCommiterDict] = statisticCommiter(commitCollection)
    [CCFOR, BCFOR] = computeCFOR(changeCommiterDict, bugCommiterDict)
    [CPCO, BPCO] = computePCO(changeCommiterDict, bugCommiterDict)
    aList = [project_name, CCOR, BCOR, CCFOR, BCFOR, CPCO, BPCO]
    return aList


def com_gt(project_path, out_path, project_name, gt_list):
    filename_java = get_file_mc(project_path, out_path, project_name)
    aList = computeEntry(filename_java, project_name)
    gt_list.append(aList)




# def com_gt():
#     resList_all = list()
#
#
#     resList_java = list()
#     resList_java.append(title)
#
#     resList_notest = list()
#     resList_notest.append(title)
#     for projectName in projectNameList:
#         historyAllFile = rootDir + projectName + "\\mc\\history-all.csv"
#         historyJavaFile = rootDir + projectName + "\\mc\\history-java.csv"
#         historyNotestFile = rootDir + projectName + "\\mc\\history-notest.csv"
#
#
#
#     writeCSV(resList_all, rootDir + "new-mc-all.csv")
#     writeCSV(resList_notest, rootDir + "new-mc-notest.csv")
