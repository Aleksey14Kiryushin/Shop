// нахождение формы
let wrapper = document.querySelector('.load_img');

function download(input) {
    let file = input.files[0];
    // считывает инфу из file
    let reader = new FileReader();
    reader.readAsDataURL(file);
    console.log(file)

    reader.onload = function () {
        // создание img
        let img = document.createElement('img');
        wrapper.appendChild(img);
        img.src = reader.result;      
        img.id = "img_1"
        alert( "Изображение успешно добавлено!\nSrc:",img.src)

        // создание текста img.src
        let input = document.createElement('input');
        wrapper.appendChild(input);
        input.value = reader.result;      
        input.id = "input_img_1"

    }
}