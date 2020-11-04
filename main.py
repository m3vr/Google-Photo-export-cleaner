import os
import shutil
import argparse
import json
from datetime import datetime


parser = argparse.ArgumentParser(description='Organizes Google Photo exports.')
parser.add_argument('import_dir', type=str, help="location of the Google Photo export file.")
parser.add_argument('export_dir', type=str, help="location of the organized photos and videos.")
parser.add_argument("-v", "--verbose", help="increase output verbosity.", action="store_true")
args = parser.parse_args()
print(f"Searching for photos and videos in: \"{args.import_dir}\".")
print(f"Outputting the files in: \"{args.export_dir}\".")

outputFolder = "Organized photos"
outputDir = f"{args.export_dir}\\{outputFolder}"

try:
    os.mkdir(outputDir)
except OSError:
    if args.verbose: print(f"\"{outputFolder}\" folder already exists. Files will be merged.")
else:
    if args.verbose: print(f"Folder \"{outputDir}\" is created.")

for subdir, dirs, files in os.walk(args.import_dir):
    for file in files:
        if args.verbose: print(os.path.join(subdir, file))
        if file.lower().endswith(('.png,', '.jpg', '.jpeg', 'mp4')):
            filePath = f"{subdir}\\{file}"
            try:
                with open(filePath+'.json') as f:
                    meta = json.load(f)
            except:
                try:
                    with open(os.path.splitext(filePath)[0] + '.json') as f:
                        meta = json.load(f)
                except:
                    if args.verbose: print(f"Cannot find meta data for \"{filePath}\".")
                    destPath = f"{outputDir}\\uncategorized"
                    if not os.path.isdir(destPath):
                        os.mkdir(destPath)
                    try:
                        shutil.copyfile(filePath,f"{destPath}\\{file}")
                    except shutil.SameFileError:
                        pass

                    break

            timestamp = int(meta["photoTakenTime"]["timestamp"])
            photoTakenTime = datetime.fromtimestamp(timestamp)
            destPath = f"{outputDir}\\{photoTakenTime.year}"
            if not os.path.isdir(destPath):
                os.mkdir(destPath)

            ext = os.path.splitext(filePath)[1]
            fileName = f"{photoTakenTime.year}-{photoTakenTime.month}-{photoTakenTime.day}-{photoTakenTime.hour}-{photoTakenTime.minute}{ext}"
            try:
                shutil.copyfile(filePath,f"{destPath}\\{fileName}")
            except shutil.SameFileError:
                pass