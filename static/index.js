var data = $("#siteURL");
var body = $("#data");
var statusArea = $("#status");

$("#load").click(function() {
    body.empty();
    var url = data.val();
    document.title = "HSTS Status of: " + url;
    $.get("/api/" + url, undefined, function (data) {
           console.log(data);
            statusArea.text(data["preload_list"]["status"]);
            $.get("/static/browser_type.hbs", undefined, function (templateUncomp) {
               var template = Handlebars.compile(templateUncomp);
                body.html(template(data))
            });
    }, "json");
})