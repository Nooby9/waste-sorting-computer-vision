// src/components/CameraComponent.js
import React, { useRef, useEffect } from 'react';

const CameraComponent = ({ onFrameCaptured }) => {
  const videoRef = useRef(null);

  useEffect(() => {
    // Request camera access
    navigator.mediaDevices.getUserMedia({ video: true })
      .then(stream => { videoRef.current.srcObject = stream; });

    return () => {
      // Stop the camera when component unmounts
      if (videoRef.current.srcObject) {
        videoRef.current.srcObject.getTracks().forEach(track => track.stop());
      }
    };
  }, []);

  return (
    <div>
      <video ref={videoRef} autoPlay playsInline muted width="100%"></video>
    </div>
  );
};

export default CameraComponent;
