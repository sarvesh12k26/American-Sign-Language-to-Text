# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 18:36:28 2019

@author: Sarvesh
"""
import os,shutil
src="C:\\Users\\Sarvesh\\Desktop\\JavaPrac\\BE-ASL\\gestures\\train\\"
dest="C:\\Users\\Sarvesh\\Desktop\\JavaPrac\\BE-ASL\\gestures\\test\\"

for i in range(36):
    os.mkdir(dest+str(i))


for i in range(36):
    files=[os.path.splitext(f)[0] for f in os.listdir(src+str(i))]
    files.sort(key=int)
    files=[str(f)+".jpg" for f in files]
    
    testfiles=files[2000:]
    
    foldersrc=os.path.join(src,str(i))
    folderdest=os.path.join(dest,str(i))
    for t in testfiles:
        shutil.move(os.path.join(foldersrc,t),folderdest)
