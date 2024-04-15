const dropzoneElem = document.getElementById('drop-zone');
const inputElem = document.getElementById('file');
const messageElem = document.getElementById('upload-message');
const previewElem = document.getElementById('preview');

dropzoneElem.addEventListener('dragover', (event) => {
  event.preventDefault();
  dropzoneElem.classList.add('dragover');
});

dropzoneElem.addEventListener('dragleave', (event) => {
  event.preventDefault();
  dropzoneElem.classList.remove('dragover');
});

dropzoneElem.addEventListener('drop', (event) => {
  event.preventDefault();
  dropzoneElem.classList.remove('dragover');
  handleFiles([...event.dataTransfer.files]);
});

inputElem.addEventListener('change', (event) => {
  handleFiles([...inputElem.files]);
});

function handleFiles(files) {
  messageElem.innerHTML = '';
  previewElem.innerHTML = '';

  if (files.length === 0) {
    messageElem.innerHTML = '请选择文件。';
    return;
  }

  files.forEach((file) => {
    const previewItem = document.createElement('img');
    previewItem.src = URL.createObjectURL(file);
    previewElem.appendChild(previewItem);
  });

  messageElem.innerHTML = `已选择 ${files.length} 个文件：`;

  const sizeInMB = calculateTotalSizeInMB(files);
  messageElem.innerHTML += `，总大小为 ${sizeInMB.toFixed(2)} MB。`;
}

function calculateTotalSizeInMB(files) {
  const totalSizeInBytes = files.reduce((acc, file) => acc + file.size, 0);
  const totalSizeInMB = totalSizeInBytes / 1024 / 1024;
  return totalSizeInMB;
}