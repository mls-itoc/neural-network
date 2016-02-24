#imageフォルダの中にホワイト20個、ブラック20個、ライトグレイ20個、ダークグレイ20個が入っている。
#その中から各色ごとに15個ずつは学習用で、残り5個ずつはテスト用に使う。
#
#ここでは学習用のファイルとテスト用のファイルを「train.txt」と「test.txt」のそれぞれ書き込んでいる。
#またPictureフォルダの中のフォルダ名から分類名を取得して書き込んでいる。

import sys
import argparse
import commands
import subprocess
import os

parser = argparse.ArgumentParser(
    description='Image inspection using chainer')
parser.add_argument('--source','-s',default='Picture', help='Path to inspection image file')
args = parser.parse_args()

def cmd(cmd):
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	p.wait()
	stdout, stderr = p.communicate()
	return stdout.rstrip()

#make directries
cmd("mkdir images")

#copy images and make train.txt
imageDir = "images"
train = open('train.txt','w')
test = open('test.txt','w')
labelsTxt = open('labels.txt','w')

labels=os.listdir(args.source)
classNo=0
cnt = 0
#label = labels[classNo]


for label in labels:
	workdir = args.source+"/"+label
	labelsTxt.write(label+"\n")
	imageCnt=0
	images=os.listdir(workdir)
	startCnt=cnt
	length = len(images)
	for image in images:
		imagepath = imageDir+"/image%07d" %cnt +".jpg"
		cmd("cp "+workdir+"/"+image+" "+imagepath)
		if cnt-startCnt < length*0.75:
			train.write(imagepath+" %d\n" % classNo)
		else:
			test.write(imagepath+" %d\n" % classNo)
		print imagepath 
		cnt += 1
	
	classNo += 1

train.close()
test.close()
labelsTxt.close()
