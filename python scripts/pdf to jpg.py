# import module

import pdf2image

pages = pdf2image.convert_from_path('example.pdf')

for i in range(len(pages)):

    pages[i].save('page'+ str(i) +'.jpg', 'JPEG')