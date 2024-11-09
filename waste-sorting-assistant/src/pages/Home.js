// src/pages/Home.js
import React, { useEffect, useState } from 'react';
import CameraComponent from '../components/CameraComponent';
import ImageUploadComponent from '../components/ImageUploadComponent';
import { runModel } from '../config/model';

const Home = () => {
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    setIsMobile(window.innerWidth <= 768); // Check if on mobile device
  }, []);

  const handleImageUpload = async (imageSrc) => {
    // Placeholder for running the model when an image is uploaded
    const result = await runModel(imageSrc);
    console.log("Inference result:", result);
  };

  return (
    <div>
      <h1>Waste Sorting Assistant</h1>
      {isMobile ? (
        <CameraComponent onFrameCaptured={handleImageUpload} />
      ) : (
        <ImageUploadComponent onImageUpload={handleImageUpload} />
      )}
    </div>
  );
};

export default Home;
