document.querySelector('.scroll-top').onclick = () => {
    window.scrollTo(0, 0);  
    
}

// let cords = ['scrollX','scrollY'];

// // Перед закрытием записываем в локалсторадж window.scrollX и window.scrollY как scrollX и scrollY
// window.addEventListener('load', e => cords.forEach(cord => localStorage[cord] = window[cord]));
// // Прокручиваем страницу к scrollX и scrollY из localStorage (либо 0,0 если там еще ничего нет)

// function scrollDelay(ms) {
//     return new Promise(res => setTimeout(res, ms));
// }

// // document.getElementById("slow-scroll-demo-button").onclick = async function() {
// //     for (var y = 0; y <= cords[1]; y += 1) {
// //         window.scrollTo({top: y, behavior: 'smooth'})
// //         await scrollDelay(1)
// //     }
// // }
// document.onreadystatechange = function(){
//     if(document.readyState === 'complete'){

//         for (var y = 0; y <= cords[1]; y += 1) {
//                 window.scrollTo({top: y, behavior: 'smooth'})
//                 await scrollDelay(1000)
//             }
//         // window.scrollBy({
//         //     top: cords[1],
//         //     behavior: 'smooth',
//         // });
//        // Ваш скрипт
//     //    window.scrollIntoView(cords.map(cord => localStorage[cord]));
//     }
//  }

