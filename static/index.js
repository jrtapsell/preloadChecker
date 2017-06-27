var data = $("#siteURL");
var body = $("#data");
var statusArea = $("#status");

$("#load").click(function() {
    $.get("/api/" + data.val(), undefined, function (data) {
           console.log(data);
            statusArea.text(data["preload_list"]["status"]);
            $.get("/static/browser_type.hbs", undefined, function (templateUncomp) {
               var template = Handlebars.compile(templateUncomp);
                body.empty();
                body.html(template(data))
            });
    }, "json");
})