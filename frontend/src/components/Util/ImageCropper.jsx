import React, { useState, useCallback } from 'react'
import Cropper from 'react-easy-crop'


const ImageCropper = ({ img, setCroppedImage }) => {
  const [crop, setCrop] = useState({x:0, y:0})
  const [zoom, setZoom] = useState(1)
  const [croppedAreaPixels, setCroppedAreaPixels] = useState(null)


  const onCropComplete = useCallback((croppedArea, croppedAreaPixels) => {
    setCroppedAreaPixels(croppedAreaPixels)
  }, [])

  const handleCrop = async () => {
    const croppedImage = await getCroppedImg(
      img,
      croppedAreaPixels
    )
    
    setCroppedImage(croppedImage)
  }


  return (
    <div className='fixed top-0 left-0 flex flex-col w-full h-full'>
      <Cropper
        image={img}
        crop={crop}
        zoom={zoom}
        aspect={1}
        onCropChange={setCrop}
        onCropComplete={onCropComplete}
        onZoomChange={setZoom}
      />
      <div className='flex items-center justify-center w-full'>
        <button 
          className='absolute z-20 w-1/2 p-2 font-bold text-white rounded-md bottom-20 bg-primary'
          onClick={handleCrop}
        > 
          Crop 
        </button>
      </div>
    </div>

  )
}

export default ImageCropper

export const readImageFile = (file) => {
  return new Promise((resolve) => {
    const reader = new FileReader()
    reader.addEventListener('load', () => resolve(reader.result), false)
    reader.readAsDataURL(file)
  })
}

export const getCroppedImg = (imageSrc, cropArea) => {
  return new Promise((resolve, reject) => {
    const image = new Image();
    image.src = imageSrc;
    image.onload = () => {
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');

      const maxSize = Math.max(image.width, image.height);
      const safeArea = 2 * ((maxSize / 2) * Math.sqrt(2));

      canvas.width = safeArea;
      canvas.height = safeArea;

      ctx.drawImage(
        image,
        safeArea / 2 - image.width * 0.5,
        safeArea / 2 - image.height * 0.5
      );

      const data = ctx.getImageData(0, 0, safeArea, safeArea);

      canvas.width = cropArea.width;
      canvas.height = cropArea.height;

      ctx.putImageData(
        data,
        0 - safeArea / 2 + image.width * 0.5 - cropArea.x,
        0 - safeArea / 2 + image.height * 0.5 - cropArea.y
      );

      const base64image = canvas.toDataURL('image/jpeg');
      resolve(base64image);
    };
    image.onerror = reject;
  });
};