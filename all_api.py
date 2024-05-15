#all file class will be called then make a flask api make faceauth api , tobase64, text extractor, pharmeasyscrap

from flask import Flask, jsonify, request
from FaceMatch import ImageVerifier
from TextExtractor import ImageProcessor
from PharmeasyScrap import PriceScraper
from pdf_convert import convrt
from io import BytesIO
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
img=ImageVerifier()
img_p=ImageProcessor()
pscrp=PriceScraper()
cnv=convrt()
@app.route('/facematch', methods=['POST'])
def facematch():
    
    return img.verify_images(request.get_json()['imagecode'],request.get_json()['imageid'])

@app.route('/cnvimg', methods=['POST'])
def cnvimg():
   file = request.files.getlist('file')
   #file_data = file.read()
   #uploaded_file = request.files.get('file')
   result= cnv.cnvrt(file)
   with open('datas.txt', 'w') as f:
       f.write(json.dumps(result))
   result_dict = json.loads(json.dumps(result))
   if result_dict['message'] == 'success':
       return jsonify({'message': 'File processed successfully','data':result}), 200
   else:
       return jsonify({'error': 'File processing failed','return':result}), 500

@app.route('/processimage', methods=['POST'])
def processimage():
    return img_p.process_image(request.get_json()['imagecode'])



@app.route('/scrapeprice', methods=['POST'])
def scrp_price():
    
     return pscrp.scrape_price(request.get_json()['url'])

if __name__ == '__main__':
    app.run(debug=True)
