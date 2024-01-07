document.getElementById('addImage').addEventListener('click', function() {
        var container = document.getElementById('imageUploadContainer');
        var input = document.createElement('input');
        input.type = 'file';
        input.name = 'images';
        container.appendChild(input);
    });