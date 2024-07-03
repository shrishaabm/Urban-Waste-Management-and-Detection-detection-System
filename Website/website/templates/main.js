document.addEventListener('DOMContentLoaded', (event) => {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const photo = document.getElementById('photo');
    const captureButton = document.getElementById('capture');
    const submitButton = document.getElementById('submit');
    const userIdInput = document.getElementById('userId');
    let stream;
    let capturedImage;
    let currentLocation;

    // Initialize the map
    let map;
    let marker;
    function initMap() {
        map = L.map('map').setView([0, 0], 2);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
        }).addTo(map);
    }

    // Function to start the camera
    function startCamera() {
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            navigator.mediaDevices.getUserMedia({ video: true }).then(s => {
                stream = s;
                video.srcObject = stream;
                video.style.display = 'block';
            });
        } else {
            alert('Your browser does not support camera access');
        }
    }

    // Function to stop the camera
    function stopCamera() {
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
            video.style.display = 'none';
        }
    }

    // Enable the capture button if user ID is valid
    userIdInput.addEventListener('input', () => {
        if (userIdInput.value.length >= 4) {
            captureButton.disabled = false;
        } else {
            captureButton.disabled = true;
        }
    });

    // Capture photo and fetch location
    captureButton.addEventListener('click', () => {
        startCamera();
        setTimeout(() => {
            const context = canvas.getContext('2d');
            context.drawImage(video, 0, 0, 640, 640);
            capturedImage = canvas.toDataURL('image/png');
            photo.setAttribute('src', capturedImage);

            stopCamera();
            fetchLocation();
            submitButton.disabled = false;
        }, 1000); // Allow some time for the camera to start
    });

    // Fetch location
    function fetchLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(position => {
                currentLocation = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                };

                if (!marker) {
                    map.setView(currentLocation, 13);
                    marker = L.marker(currentLocation).addTo(map);
                } else {
                    marker.setLatLng(currentLocation);
                    map.panTo(currentLocation);
                }

                displayAddress(currentLocation);
                console.log('Latitude:', currentLocation.lat);
                console.log('Longitude:', currentLocation.lng);
            }, error => {
                alert('Error: Unable to retrieve your location. ' + error.message);
            }, {
                enableHighAccuracy: true,
                maximumAge: 0,
                timeout: 27000
            });
        } else {
            alert('Your browser does not support geolocation');
        }
        return currentLocation
    }

    // Display address
    function displayAddress(latLng) {
        const proxy = 'https://cors-anywhere.herokuapp.com/';
        const url = `https://nominatim.openstreetmap.org/reverse?format=json&lat=${latLng.lat}&lon=${latLng.lng}`;
        cor=fetchLocation()

        fetch(proxy + url).then(response => {
            })
            .then(data => {
                if (data.address) {
                    document.getElementById('output').innerHTML = 'longitude: ' + latLng.lat; 
                } else {
                    document.getElementById('output').innerHTML = 'No address found for these coordinates';
                }
            })
            .catch(err => {
                document.getElementById('output').innerHTML = ' ' + err.message;
            });
            console.log('Latitude:', currentLocation.lat);
            console.log('Longitude:', currentLocation.lng);
    }

    // Submit data
    submitButton.addEventListener('click', () => {
        const formData = new FormData();
        formData.append('image', dataURItoBlob(capturedImage));

        fetch('http://localhost:8000/upload-image', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            alert('Image submitted successfully!');
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('success');
        });
    });

    // Convert dataURI to Blob
    function dataURItoBlob(dataURI) {
        const byteString = atob(dataURI.split(',')[1]);
        const mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];
        const ab = new ArrayBuffer(byteString.length);
        const ia = new Uint8Array(ab);
        for (let i = 0; i < byteString.length; i++) {
            ia[i] = byteString.charCodeAt(i);
        }
        return new Blob([ab], { type: mimeString });
    }

    initMap();
});
