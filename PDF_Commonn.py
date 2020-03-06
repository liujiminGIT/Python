import PyPDF2
import os
import sys
import codecs
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger

root = os.path.dirname(__file__)
data_dir = os.path.join(root, "pdf_folder")
rotate_temp_dir = os.path.join(data_dir, "rotate")
output_file = os.path.join(data_dir, "000_total.pdf")

if os.path.exists(output_file):
    os.remove(output_file)

filelist = (
             ("00_0AAA.pdf",0)
            ,("01-1BBB.pdf",0)
            ,("02-1CCC.pdf",0)
        )


merger = PdfFileMerger()

for filename , rotate in filelist:
    print(filename, "処理開始！")
    input_file_org = os.path.join(data_dir, filename)
    input_file_merge = input_file_org
    
    # ページ回転必要な場合
    if rotate != 0:
        print(filename, "回転", rotate, "度")
        pdf_rotate_output_path = os.path.join(rotate_temp_dir, filename)
        if os.path.exists(pdf_rotate_output_path):
            os.remove(pdf_rotate_output_path)
        
        pdf_rotate_file_object = open(input_file_org, 'rb')
        pdf_rotate_reader = PyPDF2.PdfFileReader(pdf_rotate_file_object)
        num_of_pages = pdf_rotate_reader.getNumPages()

        pdf_rotate_output_object = open(pdf_rotate_output_path, 'wb')
        pdf_rotate_write = PyPDF2.PdfFileWriter()
        
        for p in range(num_of_pages):
            page = pdf_rotate_reader.getPage(p)
            page.rotateCounterClockwise(rotate)
            pdf_rotate_write.addPage(page)
        
        pdf_rotate_write.write(pdf_rotate_output_object)

        pdf_rotate_file_object.close()
        pdf_rotate_output_object.close()

        input_file_merge = pdf_rotate_output_path
    # ページ回転処理終了
    
    if os.path.exists(input_file_merge) == False:
        print(input_file_merge, "が存在していない")
        continue
    merger_file = codecs.open(input_file_merge, 'rb')
    merger_object = PdfFileReader(merger_file)
    if merger_object.isEncrypted == True:
        print(merger_object, "が暗号化されているため、マージできない")
        merger_file.close()
        continue
    merger.append(merger_object, bookmark=filename.replace(".pdf", ""), import_bookmarks=True)
    merger_file.close()

merger.write(output_file)
merger.close()
print("マージ処理完了しました。")

