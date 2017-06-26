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
                $.each(data["browsers"]["chrome"], function (name, data) {
                    var div = $("<div/>", {"class": "browser"});
                    $.each(data, function(build, pl) {
                        var itemShell = $("<div/>", {"class": "build"});
                        var data = {
                            "os": name,
                            "build": build,
                            "state": pl,
                            "text_state" : JSON.stringify(pl)
                        };
                        var item = template(data);
                        itemShell.html(item);
                        itemShell.appendTo(div);
                    });
                    div.appendTo(body);
                })
            });
    }, "json");
})