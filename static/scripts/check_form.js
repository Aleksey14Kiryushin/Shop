function check(form) {

    // var name = document.querySelector('name');
    // var title = document.querySelector('title');
    // var url = document.querySelector('url');
    // var intro = document.querySelector('price');
    // var text = document.querySelector('intro');
    // var price = document.querySelector('text');

    if (form.name.value.trim() == ''){
        alert( "Заполните поле 'Name'!" )
        document.querySelector('#submit').disabled = true;
        return false;
    } else if (form.title.value.trim() == '' ){
        alert( "Заполните поле 'Title'!" );
        return false;
    } else if (form.url.value.trim() == ''){
        alert( "Заполните поле 'Url'!" );
        return false;
    } else if (form.intro.value.trim() == ''){
        alert( "Заполните поле 'Intro'!" );
        return false;
    } else if (form.text.value.trim() == ''){
        alert( "Заполните поле 'Text'!" );
        return false;
    } else if (form.price.value.trim() == ''){
        alert( "Заполните поле 'Price'!" );
        return false;
    } else if (form.name.value.length > 0 && form.title.value.length &&
                form.url.value.length && form.price.value.length &&
                form.intro.value.length && form.text.value.length){
        // alert( 'NAME = ', name);           
        alert( 'Все верно!\nМожете убедиться в этом сами, для этого перейдите в раздел "Posts"');        
        // редирект
        // function redirect(){
        //     const str = "/create-notice/"+${name}
        //     window.location = str
        // }
        return true;
    }


    // alert( "Заполняйте! 1" )
    // document.querySelector('#title').onkeyup = () => {
    //     if (document.querySelector('#title').value.length > 0){
    //         document.querySelector('#submit').disabled = false;
    //         alert( "Заполняйте! 2 " )
    //     } else {
    //         document.querySelector('#submit').disabled = true;
    //         alert( "Заполняйте! 3" )
    //     }
    // }

    // document.querySelector('#title').onkeyup = () => {
    //     if (document.querySelector('#title').value.length < 0){
    //         document.querySelector('#submit').disabled = true;
    //     } else {
    //         document.querySelector('#submit').disabled = false;
    //     }
    // }
    // document.querySelector('#url').onkeyup = () => { 
    //     if (document.querySelector('#url').value.length < 0){
    //         document.querySelector('#submit').disabled = true;
    //     } else {
    //         document.querySelector('#submit').disabled = false;
    //     }
    // }
    // document.querySelector('#price').onkeyup = () => { 
    //     if (document.querySelector('#price').value.length < 0){
    //         document.querySelector('#submit').disabled = true;
    //     } else {
    //         document.querySelector('#submit').disabled = false;
    //     }
    // }
    // document.querySelector('#price').onkeyup = () => { 
    //     if (document.querySelector('#intro').value.length < 0){
    //         document.querySelector('#submit').disabled = true;
    //     } else {
    //         document.querySelector('#submit').disabled = false;
    //     }
    // }
    // document.querySelector('#price').onkeyup = () => {
    //     if (document.querySelector('#text').value.length < 0){
    //         document.querySelector('#submit').disabled = true;
    //     } else {
    //         document.querySelector('#submit').disabled = false;
    //     }
    // } 
          
};

