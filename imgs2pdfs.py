from PIL import Image
import re
import os
from PyPDF2 import PdfMerger


class PDFGener:

    def __init__(self, file_list, pdf_name:str = 'GenPDF'):
        self.pdf_name = pdf_name
        self.__file_list = file_list

    @property
    def file_list(self):
        return self.__file_list

    @file_list.setter
    def file_list(self, file_list):
        self.__file_list = file_list

    @classmethod
    def list_read(cls, dir:str = "media/Picture"):
        file_list = os.listdir(dir)
        sorted_file_list = cls.natural_sort_key(file_list)
        return cls(sorted_file_list)

    @staticmethod
    def natural_sort_key(user_list):
       return sorted(user_list,key=lambda s: [int(text) if text.isdigit() else text for text in re.split(r'(\d+)', s)])

    @staticmethod
    def file_legal_type(pic_list):
        legal_type = ('.jpg', '.jpeg')

        for pic in pic_list:
            if pic.endswith(legal_type):
                pass
            else:
                pic_list.remove(pic)
                print(f"\033[91mInvalid file type: {pic}\033[0m")

        return pic_list

    def gene_from_file(self, pdf_name:str = None, count:str = 1):

        if pdf_name is None:
            pdf_name = self.pdf_name

        else:
            self.pdf_name = pdf_name

        for file_name in self.__file_list:
            images = []
            pic_list = os.listdir(f"media/Picture/{file_name}")

            # moldify file type
            pic_list = self.file_legal_type(pic_list)
            pic_list = self.natural_sort_key(pic_list)

            for pic_dir in pic_list:
                img = Image.open(f"media/Picture/{file_name}/{pic_dir}").convert("RGB")
                images.append(img)

            if images:
                output_name = f"{self.pdf_name}_{str(count)}.pdf"
                output_path = f"media/PDF/{output_name}"
                images[0].save(output_path, save_all=True, append_images=images[1:])
                print(f"PDF generate successful: {self.pdf_name}_{str(count)}.pdf")
                count += 1

            else:
                print(f"\033[91mNo valid PDF generated\033[0m")


    def gene_from_pic(self, pdf_name:str = None, count:str = 1):

        if pdf_name is None:
            pdf_name = self.pdf_name

        else:
            self.pdf_name = pdf_name

        # moldify file type
        pic_list = self.file_legal_type(self.__file_list)
        pic_list = self.natural_sort_key(pic_list)

        images = []

        for pic_dir in pic_list:
            img = Image.open(f"media/Picture/{pic_dir}").convert("RGB")
            images.append(img)

        if images:
            output_name = f"{self.pdf_name}_{str(count)}.pdf"
            output_path = f"media/PDF/{output_name}"
            images[0].save(output_path, save_all=True, append_images=images[1:])
            print(f"PDF generate successful: {self.pdf_name}_{str(count)}.pdf")
            count += 1

        else:
            print(f"\033[91mNo valid PDF generated\033[0m")


class PDFCombiner:
    def __init__(self, file_list, pdf_name:str = 'CombinedPDF'):
        self.__file_list = file_list
        self.pdf_name = pdf_name

    @property
    def file_list(self):
        return self.__file_list

    @file_list.setter
    def file_list(self, file_list):
        self.__file_list = file_list

    @classmethod
    def list_read(cls, dir: str = "media/PDF"):
        file_list = os.listdir(dir)
        sorted_file_list = cls.natural_sort_key(file_list)
        return cls(sorted_file_list)

    @staticmethod
    def natural_sort_key(user_list):
        return sorted(user_list,
                      key=lambda s: [int(text) if text.isdigit() else text for text in re.split(r'(\d+)', s)])

    @staticmethod
    def file_legal_type(pdf_list):
        legal_type = ('.pdf')

        for pdf in pdf_list:
            if pdf.endswith(legal_type):
                pass
            else:
                pdf_list.remove(pdf)
                print(f"\033[91mInvalid file type: {pdf}\033[0m")

        return pdf_list

    def PDF_combiner(self, pdf_name: str = None, count: int = 1, pdf_num: int = None):
        if pdf_name is None:
            pdf_name = self.pdf_name
        else:
            self.pdf_name = pdf_name

        pdf_list = self.file_legal_type(self.__file_list)
        pdf_list = self.natural_sort_key(pdf_list)

        output_dir = "media/PDF/Combined PDF"


        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        pic_num_count = 0
        merger = PdfMerger()

        for pdf in pdf_list:
            pic_num_count += 1
            merger.append(f"media/PDF/{pdf}")


            if pdf_num is not None and pic_num_count == pdf_num:
                self.write_merged_pdf(merger, count, output_dir)
                count += 1
                pic_num_count = 0
                merger = PdfMerger()


        if pic_num_count > 0:
            self.write_merged_pdf(merger, count, output_dir)

        merger.close()

    def write_merged_pdf(self, merger, count, output_dir):
        output_name = f"{self.pdf_name}_{str(count)}.pdf"
        output_path = os.path.join(output_dir, output_name)
        merger.write(output_path)
        print(f"Combined PDF generated: {output_name}")






if __name__ == "__main__":
    #gene pdf
    a = PDFGener.list_read()
    a.gene_from_file("偶像の子")
    print('successful')



    #combined pdf
    a = PDFCombiner.list_read()
    a.PDF_combiner("偶像の子",1,3)