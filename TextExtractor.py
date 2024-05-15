from flask import Flask, request, jsonify
import cv2
import numpy as np
import pytesseract
import base64
from PIL import Image
from io import BytesIO
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
# create class
class ImageProcessor:
    def __init__(self):
        pass
    def preprocess_image(self,image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 100, 200)
        return edges

    def filter_handwritten_text(self,image, contours):
        filtered_contours = []
        for contour in contours:
            area = cv2.contourArea(contour)
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = float(w) / h
            if area < 1000 and aspect_ratio > 1.5:
                filtered_contours.append(contour)
        return filtered_contours

    def crop_printed_text(self,image):
        image_width, image_height = image.shape[1], image.shape[0]
        aspect_ratio = image_width / image_height
        target_height = 1244
        target_width = int(aspect_ratio * target_height)
        resized_image = cv2.resize(image, (target_width, target_height))

        edges = self.preprocess_image(resized_image)

        roi_height = int(resized_image.shape[0] * 0.2)
        roi = edges[:roi_height, :]

        contours, _ = cv2.findContours(roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        filtered_contours = self.filter_handwritten_text(resized_image, contours)
        min_x = min(contour[:, :, 0].min() for contour in filtered_contours)
        min_y = min(contour[:, :, 1].min() for contour in filtered_contours)
        max_x = max(contour[:, :, 0].max() for contour in filtered_contours)
        max_y = max(contour[:, :, 1].max() for contour in filtered_contours)
        margin_percentage = 0.03  # Adjust the margin percentage as needed
        margin_x = int(target_width * margin_percentage)
        margin_y = int(target_height * margin_percentage)

        min_x = max(0, min_x - margin_x)
        min_y = max(0, min_y - margin_y)
        max_x = min(target_width, max_x + margin_x)
        max_y = min(target_height, max_y + margin_y)

        cropped_image = resized_image[min_y:max_y, :]

        return cropped_image

    def process_image(self,data):
        encoded_image = data
        decoded_image = base64.b64decode(encoded_image)
        image = cv2.imdecode(np.frombuffer(decoded_image, np.uint8), -1)
        #image=cv2.resize(image, (600,800))
        print('Image Width is',image.shape[1])
        print('Image Height is',image.shape[0])
        printed_text_boxes = self.crop_printed_text(image)
        gray = cv2.cvtColor(printed_text_boxes, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=0)
        invert = 255 - opening

        text = pytesseract.image_to_string(invert, lang='eng', config='--psm 6')
        print(text)
        return text


