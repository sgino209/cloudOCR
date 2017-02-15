from sys import stdout
from os import path
from AbbyyOnlineSdk import *

# Recognize a file at filePath and save result to resultFilePath
def recognizeFile(processor, filePath, resultFilePath, language, outputFormat):

    prediction = {}

    print "Uploading.."
    settings = ProcessingSettings()
    settings.Language = language
    settings.OutputFormat = outputFormat
    task = processor.ProcessImage(filePath, settings)
    if task is None:
        print "Error"
        return
    print "Id = %s" % task.Id
    print "Status = %s" % task.Status

    # Wait for the task to be completed
    stdout.write("Waiting..")
    # Note: it's recommended that your application waits at least 2 seconds
    # before making the first getTaskStatus request and also between such requests
    # for the same task. Making requests more often will not improve your
    # application performance.
    # Note: if your application queues several files and waits for them
    # it's recommended that you use listFinishedTasks instead (which is described
    # at http://ocrsdk.com/documentation/apireference/listFinishedTasks/).

    while task.IsActive():
        time.sleep(5)
        stdout.write(".")
        task = processor.GetTaskStatus(task)

    print "Status = %s" % task.Status

    if task.Status == "Completed":
        if task.DownloadUrl is not None:
            prediction = processor.DownloadResult(task, resultFilePath)
            print "Result was written to %s" % resultFilePath
    else:
        print "Error processing task"

    return prediction

def main_abbyy(args):

    prediction = {}

    # Load ABBYY SDK and feed credentials:
    processor = AbbyyOnlineSdk()
    processor.ApplicationId = args.abbyy_appid
    processor.Password = args.abbyy_pwd

    if args.img_type == 'URL':
        print('Sending URL paths to ABBYY is not supported, please upload a local image file')

    else:
        sourceFile = args.img_path
        targetFile = path.join(args.res_path, path.basename(sourceFile) + '.abbyy.out')
        language = 'English'
        outputFormat = 'txt'

        if path.isfile(sourceFile):
            prediction = recognizeFile(processor, sourceFile, targetFile, language, outputFormat)
        else:
            print "No such file: %s" % sourceFile

    return prediction
