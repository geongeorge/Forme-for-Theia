import yaml
import os
import sys
import cv2
import glob
from terminaltables import AsciiTable
from progress.bar import Bar

def openAndResize(path,size):
    try:
        im = cv2.imread(path)
        old_size = im.shape[:2] # old_size is in (height, width) format

        ratio = float(size)/max(old_size)
        new_size = tuple([int(x*ratio) for x in old_size])

        # new_size should be in (width, height) format
        im = cv2.resize(im, (new_size[1], new_size[0]))

        delta_w = size - new_size[1]
        delta_h = size - new_size[0]
        top, bottom = delta_h//2, delta_h-(delta_h//2)
        left, right = delta_w//2, delta_w-(delta_w//2)

        color = [0, 0, 0]
        new_im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT,
            value=color)
        return 1,new_im
    except:
        print(sys.exc_info()[0])
        print("Error Image : ",path)
        return -1,[] #error


dir_path = os.path.dirname(os.path.realpath(__file__))
# no slash dir path
with open("config.yml", "r") as ymlfile:
    cfg = yaml.safe_load(ymlfile)

# {'input': {'folder': 'input'}, 'output': {'size': 32, 'folder': 'output'}}

inputPath = cfg['input']['folder']
outputPath = cfg['output']['folder']
imgSize = cfg['output']['size']

folders = [f for f in glob.glob(inputPath + "/*/", recursive=True)]

# Print input table
input_data = [
    ['Letter', 'count'],
]
total_count = 0
letters = []
for fol in folders:
    letter = fol.rsplit("/")[1]
    letters.append(letter)

    files = [f for f in glob.glob(fol + "**/*.png", recursive=True)]
    # Append to table
    #input/ആ/
    input_data.append([letter,len(files)])
    total_count+= len(files)

table = AsciiTable(input_data)
print("Input")
print(table.table)
print("Total :"+str(total_count))

count = 0
error_count = 0
bar = Bar('Processing', max=total_count)
for fol in folders:
    files = [f for f in glob.glob(fol + "**/*.png", recursive=True)]
    letter = fol.rsplit("/")[1]
    outputFolder = outputPath+"/"+letter+"/"
    #make output folder of not exist
    os.makedirs(outputFolder, exist_ok=True)
    current_count = 0
    for file in files:
        status,image = openAndResize(path=file,size=imgSize)
        filename = outputFolder+str(current_count)+".png"
        if(status != -1):
            cv2.imwrite(filename, image)
            count+=1
            current_count+=1
            bar.next()
        else:
            error_count+=1

print("\nDone!")
print("Success Images: "+str(count))
print("Error Images: "+str(error_count))

# files = [f for f in glob.glob(path + "**/*.txt", recursive=True)]

# r=root, d=directories, f = files
