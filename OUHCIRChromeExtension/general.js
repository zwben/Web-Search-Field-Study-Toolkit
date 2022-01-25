if (debug) console.log("General Page is Loaded!");

mPage.initialize = function () {
    mPage.click_results = new Array();
    mPage.click_others = new Array();
    if (window.location.href.slice(0,21)!="http://127.0.0.1:8000") {
        mPage.book_mark();
        mPage.view_description();
    }
    mPage.init_content();
};

var bmreload = function () {
    if (window.location.href.slice(0,20)!="https://www.bing.com" && window.location.href.slice(0,21)!="http://127.0.0.1:8000") {
        if ($("button#bm-btn").length==0 || $("button#bm-btn")==null) {
            window.location.reload();
        }
    }    
}

setTimeout(bmreload, 5000);

mPage.init_content = function () {
    mPage.title = document.title;
    mPage.html = document.documentElement.outerHTML;
    // mPage.page_docs = $("body").html();
};

mPage.book_mark = function () {
    var bm_button = document.createElement("button");
    bm_button.setAttribute("id", "bm-btn");
    bm_button.innerHTML = "Bookmark";
    bm_button.style = "top:10%;right:5%;position:fixed;z-index: 9999;font-size:25px;color: #fff;background-color: #1abc9c;border-color: #1abc9c"
    document.body.appendChild(bm_button);
    $("button#bm-btn").click(
        function () {
            if (mPage.bookmark==0) {
                mPage.bookmark=1;
                this.innerText="Bookmarked";
                alert("You bookmarked this page!");
            }
            else if (mPage.bookmark==1) {
                mPage.bookmark=0;
                this.innerText="Bookmark";
                alert("Bookmark cancelled!");
            }
        })

}

mPage.view_description = function () {
    var task_description = document.createElement("div");
    task_description.setAttribute("id", "td-btn");
    var task_link = document.createElement("a");
    task_link.setAttribute("href", "http://127.0.0.1:8000/task/home/");
    task_link.setAttribute("target", "_blank");
    task_link.innerText = "Task Description";
    task_link.style = "font-size:25px;color: #1abc9c;background-color: #fff"
    task_description.appendChild(task_link);
    task_description.style = "top:20%;right:5%;position:fixed;z-index: 9999;"
    document.body.appendChild(task_description);
}

setTimeout(mPage.init_content, 1500);
setTimeout(mPage.init_content, 3000);

mPage.update = function () {
    $("a").each(function (id, element) {
        if ($(element).attr("bindclick") == undefined) {
            $(element).attr("bindclick", true);
            $(element).click(function (event) {
                var click_time = (new Date()).getTime();
                var href = $($(this).get(0)).attr("href");
                if (href[0] !== "h") {
                        var url = window.location.href;
                        var start_id = url.search('.com');
                        href =  url.slice(0, start_id + 4) + href;
                    }
                var content = this.innerText;
                if (content == null) {
                    content = "";
                }
                var e = event || window.event;
                var pos_x = e.screenX;
                var pos_y = e.screenY;
                mPage.clickother(href, pos_x, pos_y, click_time, content);
            });
        }
    });
};

setTimeout(mPage.update, 1500);