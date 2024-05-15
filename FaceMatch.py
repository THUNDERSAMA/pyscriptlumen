from flask import Flask, request, jsonify
from deepface import DeepFace
import base64
import uuid

#create class
class ImageVerifier:
    def __init__(self):
        pass

    def verify_images(self,x,id_string):
    
        base64_string = x
        image_data = base64.b64decode(base64_string)
        input_image_path= str(uuid.uuid4())+".jpg"
        with open(input_image_path, "wb") as f:
            f.write(image_data)
        similar_name_count = 7
        verified_count = 0
        for i in range(1, similar_name_count + 1):
            # .jpeg to be changed to jpg during production or testing
            image_check = "ph/"+id_string+"_"+"% s" % i+".jpg"

            try:
                result = DeepFace.verify(input_image_path, image_check, model_name='ArcFace', enforce_detection=False)
                print(result)
                if result["verified"]:
                    verified_count += 1

            except ValueError as ve:
                print(f"Error processing {image_check}: {ve}")
        accuracy = (verified_count / similar_name_count) * 100 if similar_name_count != 0 else 0

        return jsonify({
            "verified_count": verified_count,
            "total_count": similar_name_count,
            "accuray": accuracy
        })


