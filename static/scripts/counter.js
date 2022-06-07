$(function() {
    var time =3, ch=1;
    $(window).scroll(function(){
        $('#line').each(function(){
            var
            counter =$(this).offset().top,
            topWindow =$(window).scrollTop();
            if (counter<topWindow+200) {
                if (ch<2) {
                $('.line-num').addClass('visible');
                $({blurRadius: 3}).animate({blurRadius: 0},{
        duration: 2000,
        easing: 'swing',
        step: function() {
            $('.line-num').css({
                "filter": "blur("+this.blurRadius+"px)"
            });
        }
    });
    $('.line-num').each(function(){
        var
        i=1,
        number=$(this).data('nmbr'),
        step = 1000*time/number,
        that=$(this),
        int=setInterval(function(){
            if (i<=number) {
                that.html(i);
            }
            else{
                ch=ch+2;
                clearInterval(int);
            }
            i++;
        },step);
    });
    }
    }
    });
    });
    });