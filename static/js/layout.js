
$( document ).ready(function() {
    /*http://stackoverflow.com/questions/11533542/twitter-bootstrap-add-active-class-to-li*/
    var url = window.location;
    console.log("url", url);
    // Will only work if string in href matches with location
    $('ul.nav a[href="'+ url +'"]').parent().addClass('active');

    // Will also work for relative and absolute hrefs
    $('ul.nav a').filter(function() {
        return this.href == url;
    }).parent().addClass('active');
});

