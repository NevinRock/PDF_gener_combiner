import imgs2pdfs

# gene pdf
a = imgs2pdfs.PDFGener.list_read()
a.gene_from_file("偶像の子")
print('successful')

# combined pdf
a = imgs2pdfs.PDFCombiner.list_read()
a.PDF_combiner("偶像の子", 1, 3)