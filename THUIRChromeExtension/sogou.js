if (debug) console.log("Sogou Main Page is Loaded!");
var baseUrl = "http://166.111.138.86:15029";
// var baseUrl = "http://127.0.0.1:8000/";

mPage.initialize = function () {
    mPage.preRate = -1;
    var random_seed = Math.random();
    if (random_seed <= 0.3) {  //设置触发预期标注概率 0.3
        mPage.pre_rate();
    }
    mPage.click_results = new Array();
    mPage.click_others = new Array();
    mPage.init_content();
};


mPage.init_content = function () {
    mPage.query = $("#upquery").val();
    mPage.page_id = parseInt($("#pagebar_container span").text());
    mPage.html = document.documentElement.outerHTML;
    mPage.title = document.title;
    var url_pair = current_referrer + mPage.query;
    chrome.runtime.sendMessage({interface_request: url_pair}, function (response) {
        mPage.interface = response;
        // window.alert("interface"+ response);
    });
};

// 预先标注期望
mPage.pre_rate = function () {
    if (mPage.page_id >= 1) { //第二页结果就不需要标注了
        return;
    }
    var start_timestamp = pageManager.start_timestamp;
    var isConfirm = window.confirm("触发惊喜！请您预先标注本次查询的期望值~");
    if (isConfirm === true) {
        mPage.preRate = 1;
        window.open (baseUrl + "/task/pre_query_annotation/" + start_timestamp, 'newwindow','height=1000,width=1200,top=0,left=0,toolbar=no,menubar=no,scrollbars=no, resizable=no,location=no, status=no');
    }
};

setTimeout(mPage.init_content, 1500);
setTimeout(mPage.init_content, 3000);

function isFather(p, c2) {
    var c = c2;
    while(c.parentNode){
        c = c.parentNode;
        if(c === p) {
            return true;
        }
    }
    return false;
}

mPage.update = function () {
    var flag = 0; // 以下三类点击结果不可重复

    $("ul.searchnav").find("a").each(function (id, element) {
        if ($(element).attr("bindClick") == undefined) {
            $(element).attr("bindClick", true);
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
        }
    });
    $("div.results").children("div").each(function (id, element) {
        $(element).find("a").each(function (child_id, child_element) {
            if ($(child_element).attr("bindClick") == undefined) {
                $(child_element).attr("bindClick", true);
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
            }
        });
    });
    $("a").each(function (id, element) {
        if ($(element).attr("bindClick") == undefined) {
            $(element).attr("bindClick", true);
            $(element).click(function (event) {
                var click_time = (new Date()).getTime();
                var href = $($(this).get(0)).attr("href");
                // 站内链接
                if (href[0] !== "h") {
                    href = "https://www.sogou.com" + href;
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

                // 分析点击接口
                var rs = document.getElementById("hint_container");  // 相关搜索
                // var content_right = $("#con-ar");
                var recommed = document.getElementById("kmap_entity_div"); // 相关实体
                var top_search = document.getElementById("kmap_right_ranklist"); // 热搜榜
                if (isFather(rs, this)) {
                    this_interface = 2;
                    // window.alert(this_interface);
                }
                else if (isFather(recommed, this)) {
                    this_interface = 3;
                    // window.alert(this_interface);
                }
                else if (isFather(top_search, this)) {
                    this_interface = 4;
                    // window.alert(this_interface);
                }

                // 向background存储interface关系
                // window.alert(this_interface);
                chrome.runtime.sendMessage({
                    link_store: "request_update",
                    url: window.location.href,
                    query: content,
                    interface: this_interface
                }, function (response) {
                    if (debug) console.log(response);
                });
            });
        }
    });
};

setTimeout(mPage.update, 1500);