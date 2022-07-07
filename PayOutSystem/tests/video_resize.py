import os
import threading
import platform

# python 文件名  路径 要压缩的文件 压缩之后的文件
class Compress_Pic_or_Video(object):
    def __init__(self, filePath, inputName, outName=""):
        self.filePath = filePath  #文件地址
        self.inputName = inputName #输入的文件名字
        self.outName = outName  #输出的文件名字
        self.system_ = platform.platform().split("-",1)[0]
        self.fileInputPath = self.filePath + inputName
        self.fileOutPath = self.filePath + outName
        if  self.system_ ==  "Windows":
            self.filePath = self.filePath.replace('/', '\\')
        elif self.system_ == "Linux":
           self.filePath = self.filePath

        self.fileInputPath = self.filePath + inputName
        print("压缩文件输入路径：%s" % self.fileInputPath)
        self.fileOutPath = self.filePath + outName
        print("压缩文件输出路径：%s" % self.fileOutPath)

    @property
    def is_video(self):
        videoSuffixSet = {"WMV","ASF","ASX","RM","RMVB","MP4","3GP","MOV","M4V","AVI","DAT","MKV","FIV","VOB"}
        suffix = self.fileInputPath.rsplit(".",1)[-1].upper()
        if suffix in videoSuffixSet:
            return True
        else:
            return False

    def SaveVideo(self):
        print("===============>开启线程：对上传的视频进行压缩，文件：%s <=================" % self.outName)
        fpsize = os.path.getsize(self.fileInputPath) / 1024
        if fpsize >= 150.0: #大于150KB的视频需要压缩
            if self.outName:
                compress = "ffmpeg -i {} -r 10 -pix_fmt yuv420p -vcodec libx264 -preset veryslow -profile:v baseline  -crf 23 -acodec aac -b:a 32k -strict -5 {}".format(self.fileInputPath, self.fileOutPath)
                if self.system_ == "Windows":
                    os.system('chcp 65001')
                isRun = os.system(compress)
            else:
                compress = "ffmpeg -i {} -r 10 -pix_fmt yuv420p -vcodec libx264 -preset veryslow -profile:v baseline  -crf 23 -acodec aac -b:a 32k -strict -5 {}".format(self.fileInputPath, self.fileInputPath)
                if self.system_ == "Windows":
                    os.system('chcp 65001')
                isRun = os.system(compress)
            if isRun != 0:
                return (isRun,"没有安装ffmpeg")

            print("================> 视频 %s 压缩完成 <==================" % self.fileOutPath)
            return True
        else:
            return True

    def Compress_Video(self):
        # 异步保存打开下面的代码，注释同步保存的代码
        thr = threading.Thread(target=self.SaveVideo)
        thr.start()
        #下面为同步代码
        # fpsize = os.path.getsize(self.fileInputPath) / 1024
        # if fpsize >= 150.0:  # 大于150KB的视频需要压缩
        #     compress = "ffmpeg -i {} -r 10 -pix_fmt yuv420p -vcodec libx264 -preset veryslow -profile:v baseline  -crf 23 -acodec aac -b:a 32k -strict -5 {}".format(
        #         self.fileInputPath, self.fileOutPath)
        #     isRun = os.system(compress)
        #     if isRun != 0:
        #         return (isRun, "没有安装ffmpeg")
        #     return True
        # else:
        #     return True
