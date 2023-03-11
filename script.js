const canvas = document.getElementById('canvas');
const context = canvas.getContext('2d');
let uploadedImage;

const fileInput = document.getElementById('fileInput');
const viewButton = document.getElementById('viewButton');
const saveButton = document.getElementById('saveButton');
const textInput = document.getElementById('textInput');
const textButton = document.getElementById('textButton');

fileInput.addEventListener('change', () => {
  const file = fileInput.files[0];
  const reader = new FileReader();
  reader.addEventListener('load', () => {
    const image = new Image();
    image.addEventListener('load', () => {
      canvas.width = image.width;
      canvas.height = image.height;
      context.drawImage(image, 0, 0);
      uploadedImage = true;
    });
    image.src = reader.result;
  });
  reader.readAsDataURL(file);
});

viewButton.addEventListener('click', () => {
  if (uploadedImage) {
    canvas.style.display = 'block';
  }
});

saveButton.addEventListener('click', () => {
  if (uploadedImage) {
    const link = document.createElement('a');
    link.download = 'image.png';
    link.href = canvas.toDataURL('image/png');
    link.click();
  }
});

textButton.addEventListener('click', () => {
  if (uploadedImage) {
    context.fillStyle = 'white';
    context.font = '30px Arial';
    context.fillText(textInput.value, 50, 50);
  }
});
