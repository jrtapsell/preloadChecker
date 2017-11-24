var data = $("#siteURL");
var body = $("#data");
var statusArea = $("#status");
var progressBar = $("#p2");

$("#load").click(function() {
    var url = data.val();
    window.location = "/" + url
});

$(function () {
   var url = window.location.pathname.substr(1);
   data.val(url);
   if (url !== "") {
       setLoading();
       loadURL(url);
   } else {
       setDone()
   }
});

function loadURL(url) {
    body.empty();
    document.title = "HSTS Status of: " + url;
    $.get("/api/" + url, undefined, function (data) {
           console.log(data);
            statusArea.text(data["preload_list"]["status"]);
            $.get("/static/browser_type.hbs", undefined, function (templateUncomp) {
               var template = Handlebars.compile(templateUncomp);
                body.html(template(data))
            });
            setDone();
    }, "json");
}

function setDone() {
    progressBar.removeClass("mdl-progress__indeterminate");
    progressBar[0].MaterialProgress.setProgress(100);
}

function setLoading() {
    progressBar.addClass("mdl-progress__indeterminate");
}