function change(input) {
    alert("HERE");
    
    var input_str = String(input.src).split('/')[5];

    alert("INPUT: "+input);

    if (input_str == "dis_heart.png"){
        input.src = "{{ url_for('static', filename='img/heart.png') }}";
        
    } else if (input_str == "heart.png"){
        input.src = "url_for('static', filename='img/dis_heart.png')";
    } 
};