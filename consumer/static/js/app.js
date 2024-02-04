$(document).ready(function () {


    const MAX_DATA_COUNT = 10;
  
    var socket = io.connect();
  
   
    socket.on("update_ui", function (msg) {
      console.log(msg);
    });
    socket.on("response", function (msg) {
      console.log(msg);
    });
  
    const imageContainer0 = document.getElementById('image-container0');
    const imageContainer1 = document.getElementById('image-container1');
    const imageContainer2 = document.getElementById('image-container2');
  
    socket.on('passimage0', function(imageData) {
      // console.log(imageData);
      console.log("passimage0 ui called");
    // Extract the data array
    const [imageName, imgBase64, frameNo] = imageData['data'];
      // Update UI with received image data
      renderImage({ imageName, imgBase64, frameNo });
    });
  
  
  function renderImage({ imageName, imgBase64, frameNo }) {
    // console.log(imageName);
  
    // Create an image element
    const imageElement = new Image();
    imageElement.src = `data:image/jpeg;base64,${imgBase64}`;
  
    // Create a div to display image details
    const imageDetails = document.createElement('div');
    imageDetails.innerHTML = `<p>Video Name: ${imageName}</p><p>Frame Number: ${frameNo}</p>`;
  
    // Clear existing content and append new content to the container
    imageContainer0.innerHTML = '';
    imageContainer0.appendChild(imageElement);
    imageContainer0.appendChild(imageDetails);
  }
  
  socket.on('passimage1', function(imageData) {
    // console.log(imageData);
    console.log("passimage1 ui called");
    // Extract the data array
    const [imageName, imgBase64, frameNo] = imageData['data'];
    // Update UI with received image data
    console.log(imageName);
  
    // Create an image element
    const imageElement = new Image();
    imageElement.src = `data:image/jpeg;base64,${imgBase64}`;
  
    // Create a div to display image details
    const imageDetails = document.createElement('div');
    imageDetails.innerHTML = `<p>Video Name: ${imageName}</p><p>Frame Number: ${frameNo}</p>`;
  
    // Clear existing content and append new content to the container
    imageContainer1.innerHTML = '';
    imageContainer1.appendChild(imageElement);
    imageContainer1.appendChild(imageDetails);
  
  });
  
  socket.on('passimage2', function(imageData) {
    // console.log(imageData);
    console.log("passimage2 ui called");
    // Extract the data array
    const [imageName, imgBase64, frameNo] = imageData['data'];
    // Update UI with received image data
    console.log(imageName);
  
    // Create an image element
    const imageElement = new Image();
    imageElement.src = `data:image/jpeg;base64,${imgBase64}`;
  
    // Create a div to display image details
    const imageDetails = document.createElement('div');
    imageDetails.innerHTML = `<p>Video Name: ${imageName}</p><p>Frame Number: ${frameNo}</p>`;
  
    // Clear existing content and append new content to the container
    imageContainer2.innerHTML = '';
    imageContainer2.appendChild(imageElement);
    imageContainer2.appendChild(imageDetails);
  
  });
  
  
  });
  