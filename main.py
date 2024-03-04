from fastapi import FastAPI, HTTPException, File, UploadFile, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from typing import Annotated
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from io import BytesIO

from image_db import save_img_data,fetch_img_data,fetch_min_max_depth
from image_handler import resize_image


# init FastAPI
app = FastAPI()

templates = Jinja2Templates(directory="templates")

# display the upload-page    
@app.get("/")
async def home(request: Request):
	return templates.TemplateResponse("index.html",{"request":request})

# define endpoint
@app.get("/default")
async def fetch_frames():
    try:
        image_csv_path = r'csv_img.csv'

        resized_image = resize_image(image_csv_path)
        save_img_data(resized_image)

        #Filter out depth values
        min_max_depth = fetch_min_max_depth()
        depth_min = min_max_depth.get("min_depth")
        depth_max = min_max_depth.get("max_depth")
        filtered_frames = fetch_img_data(depth_min,depth_max)
        
        #AppExtracted Image Frames
        img_frames = filtered_frames.values
        img_frames = img_frames[:,:-1]
        img_frames = img_frames.astype(np.uint8)

        color_map_type = 'plasma'
        color_map = plt.get_cmap(color_map_type)
        color_mapped_frames = color_map (img_frames)

        img_name = 'result_frames.png'
       
        Image.fromarray((color_mapped_frames[:, :, :3] * 255).astype(np.uint8)).save(img_name)
        
        return FileResponse('result_frames.png', media_type='application/octet-stream',filename=img_name)
    except:
        raise HTTPException(status_code=404, detail="Error")

# display the upload-page    
@app.get("/upload-page")
async def home(request: Request):
	return templates.TemplateResponse("upload.html",{"request":request})

# post endpoint to handle upload
@app.post('/upload')
def upload(colormap: Annotated[str, Form()], file: UploadFile = File(...)):
    try:

        contents = file.file.read()
        buffer = BytesIO(contents) 
        resized_image = resize_image(contents)
        save_img_data(resized_image)
        #Filter out depth values
        min_max_depth = fetch_min_max_depth()
        depth_min = min_max_depth.get("min_depth")
        depth_max = min_max_depth.get("max_depth")
        filtered_frames = fetch_img_data(depth_min,depth_max)
        #AppExtracted Image Frames
        img_frames = filtered_frames.values
        img_frames = img_frames[:,:-1]
        img_frames = img_frames.astype(np.uint8)
        color_map = plt.get_cmap(colormap)
        # Apply the colormap like a function to any array:
        color_mapped_frames = color_map (img_frames)

        img_name = 'result_frames.png'

        print(color_mapped_frames)

        Image.fromarray((color_mapped_frames[:, :, :3] * 255).astype(np.uint8)).save(img_name)

    except:
        raise HTTPException(status_code=500, detail='Something went wrong')
    finally:
        buffer.close()
        file.file.close()
    
    return FileResponse('result_frames.png', media_type='application/octet-stream',filename=img_name)
