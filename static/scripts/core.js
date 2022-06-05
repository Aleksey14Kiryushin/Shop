let wrapper = document.querySelector('.img__wrapper');

function download(input) {
    let file = input.files[0];
    // считывает инфу из file
    let reader = new FileReader();
    reader.readAsDataURL(file);
    console.log(file)

    reader.onload = function () {
        let img = document.createElement('img');
        wrapper.appendChild(img);
        img.src = reader.result;      
        // передаем в img resource url-картинки
    }
}