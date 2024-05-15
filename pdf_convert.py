# from flask import  jsonify
# import base64
# import fitz
# import io
# import os
# import json
# from io import BytesIO

# class convrt:
#     def __init__(self):
#         pass
#     def process_image(self,file_path):
#         if file_path[:2] == b'\xFF\xD8':  # Check if it's a JPEG file
#            img = io.BytesIO(file_path)
#            img.seek(0)
#            encd_img = base64.b64encode(img.read())
#            b_data = encd_img
#            j_data = b_data.decode('utf-8')
#            return j_data

#         elif file_path[:8] == b'\x89PNG\r\n\x1a\n':  # Check if it's a PNG file
#            img = io.BytesIO(file_path)
#            img.seek(0)
#            end = base64.b64encode(img.read())
#            b_d = end
#            js_data = b_d.decode('utf-8')
#            return js_data
#     def cnvrt(self, file_path):
#       print(file_path[:5])
#       if file_path[:5] == b'%PDF-':
#         doc = fitz.open(stream=BytesIO(file_path))
        
#         for page_number, page in enumerate(doc, start=1):
#             pix = page.get_pixmap(matrix=fitz.Identity, dpi=None,
#                                   colorspace=fitz.csRGB, clip=None, alpha=True, annots=True)
#             pix.save("image.png")  # Save the image to a file

#             with open("image.png", "rb") as f:
#                 image_bytes = f.read()

#             encoded_image = base64.b64encode(image_bytes)
#             bytes_data = encoded_image
#             json_serializable_data = bytes_data.decode('utf-8')
#             jd=json.dumps(json_serializable_data)
#             # print(jd)
#         return {'message': 'success','data':jd}



#         doc.close()

#       else:
#         data = []
#         image_files=file_path
#         for file in image_files:
#            encoded_image = self.process_image(file)
#            if encoded_image:
#               data.append(encoded_image)
#         return data
#       # elif file_path[:2] == b'\xFF\xD8':
#       #   img = io.BytesIO(file_path)
#       #   img.seek(0)
#       #   encd_img = base64.b64encode(img.read())
#       #   b_data = encd_img
#       #   j_data = b_data.decode('utf-8')
#       #   jd=json.dumps(j_data)
#       #   print(jd)
#       #   return {'message': 'success','data':jd}


#       # elif file_path[:8] == b'\x89PNG\r\n\x1a\n':
#       #   img = io.BytesIO(file_path)
#       #   img.seek(0)
#       #   end = base64.b64encode(img.read())
#       #   b_d = end
#       #   js_data = b_d.decode('utf-8')
#       #   jd=json.dumps(js_data)
#       #   print(jd)
#       #   return {'message': 'success','data':jd}
#       # return {'message': 'failed'}
import io
import base64
import json
import fitz

class convrt:
    def __init__(self):
        pass
    
    def process_image(self, file_path):
        if file_path[:2] == b'\xFF\xD8':  # Check if it's a JPEG file
            img = io.BytesIO(file_path)
            img.seek(0)
            encd_img = base64.b64encode(img.read())
            b_data = encd_img
            j_data = b_data.decode('utf-8')
            return j_data
        elif file_path[:8] == b'\x89PNG\r\n\x1a\n':  # Check if it's a PNG file
            img = io.BytesIO(file_path)
            img.seek(0)
            end = base64.b64encode(img.read())
            b_d = end
            js_data = b_d.decode('utf-8')
            return js_data
    def convert_pdf_to_images(self, pdf_data):
        images = []
        doc = fitz.open(stream=io.BytesIO(pdf_data))  # Open the PDF from bytes data
        for page_number, page in enumerate(doc, start=1):
            pix = page.get_pixmap(matrix=fitz.Identity, dpi=None,
                              colorspace=fitz.csRGB, clip=None, alpha=True, annots=True)
        # Convert the page to an image
            # image_bytes = io.BytesIO()
            # pix._writeIMG(image_bytes,"jpg", 95)

            #pix._writeIMG(image_bytes)
            pix.save("image.png")  # Save the image to a file

            with open("image.png", "rb") as f:
                image_bytes = f.read()

            encoded_image = base64.b64encode(image_bytes)
            images.append(encoded_image.decode('utf-8'))  # Append the encoded image to the list
        doc.close()  # Close the PDF document
        print(images)
        return {'messages': 'success', 'data': images}


    def cnvrt(self, file_paths):
        data = []
        for file in file_paths:
            if self.is_pdf(file.filename):
                data.append(self.convert_pdf_to_images(file.read()))
            else:
                data.append(self.process_image(file.read()))
        return {'message': 'success', 'data': data}
    
    def is_pdf(self, filename):
        return filename.lower().endswith('.pdf')
        
       #return {'message': 'success', 'data': data}
