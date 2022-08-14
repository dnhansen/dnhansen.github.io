$(window).on('load', function(){
    var win = $(window);
    var links = $('.toclink');    
    var anchors = links.map(function(){
        var anchorname = $(this).attr("href").substr(1);
        var a = $("[id='" + anchorname + "']");
        return a.offset().top;
    });
    var active;
    win.scroll(function(){
        var newactive;
        for (var i=anchors.length-1; i>=0; i--) {
            if (win.scrollTop() > anchors[i] - 1) {
                newactive = i;
                break;
            }
        }
        if (newactive != active) {
            links.removeClass("active");
            if (newactive != undefined)
                $(links[newactive]).addClass("active");
        }
        active = newactive;
    });
});