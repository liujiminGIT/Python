import PyPDF2
import os
import sys
import codecs
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger

title = 'title'
in_path = 'C:\\Users\\demon\\Pictures\\ControlCenter3\\Scan\\'
out_path = 'C:\\Users\\demon\\Pictures\\ControlCenter3\\output\\'

inDir = in_path + title
outDir = out_path + title


# 回転
for dir_path, dir_names, file_names in os.walk(inDir):
    for file_name in file_names:
        path = os.path.join(dir_path, file_name)
        outpath = os.path.join(outDir, file_name)

        pdf_file_obj = open(path, 'rb')
        pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)
        page = pdf_reader.getPage(0)
        page.rotateCounterClockwise(90)
 
        pdf_writer = PyPDF2.PdfFileWriter()
        pdf_writer.addPage(page)
 
        pdf_output_file = open(outpath, 'wb')
        pdf_writer.write(pdf_output_file)
        pdf_output_file.close()
        pdf_file_obj.close()
        print('转换前文件%s'%(path))
        print('转换后文件%s'%(outpath))


# ファイル一覧取得
filelist_out = []
for fpath, dirs, fs in os.walk(outDir):
    for f in fs:
        fi_d = os.path.join(fpath, f)
        if  os.path.splitext(fi_d)[1] == '.pdf':
            filelist_out.append(fi_d)
        else:
            pass

# マージ
merger = PdfFileMerger()
filelist = filelist_out
if len(filelist) == 0:
    print("当前目录及子目录下不存在pdf文件")
    sys.exit()
for filename in filelist:
    f = codecs.open(filename, 'rb')
    file_rd = PdfFileReader(f)
    short_filename = os.path.basename(os.path.splitext(filename)[0])
    if file_rd.isEncrypted == True:
        print('不支持的加密文件：%s'%(filename))
        continue
    merger.append(file_rd, bookmark=short_filename, import_bookmarks=True)
    print('合并文件：%s'%(filename))
    f.close()
out_filename=os.path.join(os.path.abspath(outDir), (title+".pdf"))
merger.write(out_filename)
print('合并后的输出文件：%s'%(out_filename))
merger.close()