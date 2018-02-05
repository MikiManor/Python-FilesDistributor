import os
import sys
import shutil
import getopt
from UsefulUtilities import Utils
import datetime


def main():
    maxRC = 0
    argv = sys.argv[2:]
    today = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    fileName = None
    subDirName = None
    logger,logFile, errorFile = Utils.loggerUtil()
    try:
        numOfArgs = len(sys.argv)
        if numOfArgs <= 1:
            raise Exception("no arguments sent! check it!", 9, logger.name)
        try:
            opts, args = getopt.getopt(argv, 'hf:d:e:', ["Help", "FileName=", "Dir=", "Env="])
        except getopt.GetoptError as ge:
            raise Exception(ge.msg, 99, logger.name)
        if len(opts) == 0:
            raise Exception("No Var Name sent! \'-v\' flag should be used", 9, logger.name)
        elif len(opts) < 3:
            raise Exception("Missing parameters: -f | -n | -p")
        for opt, arg in opts:
            if opt == '-h':
                print(" -f FileName -d DirName -e Env")
                sys.exit()
            elif opt in ("-f", "--FileName"):
                fileName = arg
            elif opt in ("-d", "--Dir"):
                subDirName = arg
            elif opt in ("-e", "--Env"):
                env = arg

        logger.info("Got The following : File = {}, sub Dir = {}, Env = {}".format(fileName, subDirName, env))
        if env == "Test":
            sourcePath = r'\\ntsrv1\IVR_TEAM\gcti\DYN_Messages_Test\he-IL'
            numOfServers = 2
            serversPrefix = "stctimcp0"
        elif env == "Prod":
            sourcePath = r'\\ntsrv1\IVR_TEAM\gcti\DYN_Messages\he-IL'
            numOfServers = 6
            serversPrefix = "pctimcp0"
        else:
            raise Exception("Unknown environment specified : {}".format(env))
        destPath = r'D$\gcti\DYN_Messages\he-IL'
        destServersNum = list(range(1, numOfServers+1))
        destServersNum = list(map(str, destServersNum))
        dirsList = [
            "IVR_points",
            "Dynamic_Menus",
            "Special_Days",
            "DNIS_WelcomeMessages"
        ]
        baseFileName, fileExt = os.path.splitext(fileName)
        fileNameNoNum = baseFileName.split("_")[:-1]
        if not fileNameNoNum:
            raise Exception("Filename isn't In *_.* format!",9)
        fileNameNoNum = ''.join(map(str, fileNameNoNum))

        logger.info("The Files starting with {} will be proceed".format(fileNameNoNum))
        if subDirName in dirsList:
            for num in destServersNum:
                curFileName = fileNameNoNum + "_" + num + fileExt
                fullSourcePath = os.path.join(sourcePath, os.path.join(subDirName,curFileName))
                fullFailurePath = os.path.join(sourcePath, os.path.join(subDirName,
                                                                            os.path.join("failed", curFileName)))
                if os.path.exists(fullSourcePath):
                    backUpFileName = fileNameNoNum + "_" + num + "-" + str(today) + fileExt
                    fullBackUpPath = os.path.join(sourcePath, os.path.join(subDirName,
                                                                            os.path.join("backup", backUpFileName)))
                    fullDestPath = os.path.join(r"\\" + serversPrefix + num, os.path.join(destPath,
                                                                            os.path.join(subDirName, fileNameNoNum + fileExt)))
                    try:
                        shutil.copyfile(fullSourcePath, fullDestPath)
                        logger.info("File - {} copied successfully to {}".format(curFileName, fullDestPath))
                        logger.info("Going To backup the file to {}".format(fullBackUpPath))
                        shutil.move(fullSourcePath, fullBackUpPath)
                        logger.info("Backed Up.")
                    except Exception as e:
                        logger.error("< {}::{} > ".format(subDirName, fileName) + str(e), exc_info=True)
                        shutil.move(fullSourcePath, fullFailurePath)
                        maxRC = 3
                        continue
                else:
                    logger.warn("File {} doesn't exist".format(curFileName))
                    maxRC = 2
                    continue
        else:
            raise Exception("Unknown Directory name provided: {}".format(subDirName))
    except Exception as e:
        exception = e.args[0]
        logger.error("< {}::{} > ".format(subDirName, fileName) + str(exception), exc_info=True)
        if len(e.args) > 1:
            exitCode = e.args[1]
            exit(exitCode)
        else:
            raise
    exit(maxRC)


if __name__ == '__main__':
    main()


