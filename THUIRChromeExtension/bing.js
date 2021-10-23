if (debug) console.log("Bing Main Page is Loaded!");
var baseUrl = "http://127.0.0.1:8000/";

document.querySelectorAll('script[type="text/javascript"]').forEach(e => e.remove())
document.querySelectorAll('div[style="display:none"]').forEach(e => e.remove())

mPage.initialize = function () {
    mPage.preRate = -1;
    var random_seed = Math.random();
    if (random_seed <= 0.3) {
        mPage.pre_rate();
    }
    mPage.click_results = new Array();
    mPage.click_others = new Array();
    mPage.init_content();
};

mPage.init_content = function () {
    mPage.query = $("#sb_form_q").val();
    mPage.page_id = parseInt($("a.sb_pagS").text());
    mPage.html = document.documentElement.outerHTML;
    mPage.title = document.title;
    var url_pair = current_referrer + mPage.query;
    chrome.runtime.sendMessage({interface_request: url_pair}, function (response) {
        mPage.interface = response;

    });
};

mPage.pre_rate = function () {
    if (mPage.page_id >= 1) {
        return;
    }
    var start_timestamp = pageManager.start_timestamp;
    var isConfirm = window.confirm("Bonus! Please annotate for the query expectation!");
    if (isConfirm === true) {
        mPage.preRate = 1;
        window.open (baseUrl + "/task/pre_query_annotation/", 'newwindow','height=1000,width=1200,top=0,left=0,toolbar=no,menubar=no,scrollbars=no, resizable=no,location=no, status=no');
    }
};

setTimeout(mPage.init_content, 1500);
setTimeout(mPage.init_content, 3000);

function isFather(p, c2) {
    var c = c2;
    while(c.parentNode){
        c = c.parentNode;
        if(c === p | c.parentNode === p | c.parentNode.parentNode === p) {
            return true;
        }
    }
    return false;
}

mPage.update = function () {
    var flag = 0;

    $("li[data-menuurl='']").find("a").each(function (id, element) {
        $(element).click(function (event) {
            flag = 1;
            var click_time = (new Date()).getTime();
            var content = this.innerText;
            if (content === null) {
                content = "";
            }
            var e = event || window.event;
            var pos_x = e.screenX;
            var pos_y = e.screenY;
            mPage.click($(this).get(0), "tab", 0, click_time, pos_x, pos_y, content);
        });
    });
    $("li.b_algo").each(function (id, element) {

        $(element).find("a").each(function (child_id, child_element) {
            $(child_element).click(function (event) {
                if (flag === 0) {
                    flag = 1;
                    var click_time = (new Date()).getTime();
                    var content = this.innerText;
                    if (content === null) {
                        content = "";
                    }
                    var e = event || window.event;
                    var pos_x = e.screenX;
                    var pos_y = e.screenY;
                    mPage.click($(this).get(0), "content", id+1, click_time, pos_x, pos_y, content);
                }
            });        
        });
    });
 

    $("a").each(function (id, element) {
        if ($(element).attr("bindClick") == undefined) {
            $(element).attr("bindClick", true);}
        $(element).click(function (event) {
            var click_time = (new Date()).getTime();
            var href = $($(this).get(0)).attr("href");

            if (href[0] !== "h") {
                href = "https://www.bing.com" + href;
            }
            var content = this.innerText;
            if (content === null) {
                content = "";
            }
            var e = event || window.event;
            var pos_x = e.screenX;
            var pos_y = e.screenY;
            if (flag === 0) {
                mPage.clickother(href, pos_x, pos_y, click_time, content);
            }

            var rs = document.getElementsByClassName("b_vList")[0]
            var recommend = document.getElementsByClassName("ent-dtab-style-content")[0]
            var top_search = $("ol.items")[0];

            // var recommed = document.getElementsByClassName("opr-recommends-merge-content")[0];
            // var top_search = document.getElementsByClassName("FYB_RD")[0];
            if (isFather(rs, this)) {
                this_interface = 2;
            }
            if (isFather(recommend, this)) {
                this_interface = 3;
            }            
            else if (isFather(top_search, this)) {
                this_interface = 4;
            }
            // else if (isFather(recommed, this)) {
            //     this_interface = 3;
            // }
            // else if (isFather(top_search, this)) {
            //     this_interface = 4;
            // }

            chrome.runtime.sendMessage({
                link_store: "request_update",
                url: window.location.href,
                query: content,
                interface: this_interface
            }, function (response) {
                if (debug) console.log(response);
            });
        });        
    });
};

setTimeout(mPage.update, 1500);