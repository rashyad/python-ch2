import cv2
import numpy as np
import pandas as pd


# Read image from data in csv and return it
def read_csv_file(csv_file_path):
    # Load the CSV file with image data
    csv_file = csv_file_path
    df = pd.read_csv(csv_file)
    return df

def resize_image(csv_file_path):
    # first read the csv, get image and depth data
    try:
        csv_image_data = read_csv_file(csv_file_path)
        image_data = csv_image_data.iloc[:, 1:].values
        depth_values = csv_image_data['depth'].values

        print(depth_values)
    except Exception as e:
        print("Error reading csv file", e)

    # Resize the image to 150 pixels width
    try:
        image_width = 150
        resized_images = []
        for img_data in image_data:
            img = np.array(img_data, dtype=np.uint8).reshape(1, -1)
            img = cv2.resize(img, (image_width, 1), interpolation=cv2.INTER_LINEAR)
            resized_images.append(img)
        
        #Form image from an array
        resized_images = np.vstack(resized_images)
        df =  pd.DataFrame(resized_images )
        df["d"] = depth_values
        return df
    except Exception as e:
        print("Issue in image resizing")



