var ws = new WebSocket("ws://localhost:9909/ws");
var group_name = [];
var role_name = [];


ws.onmessage = function(e) {
    getdata = eval('(' + e.data + ')');
    console.log(getdata);
    if (getdata['name'] == 'v') {
        temp = getdata['g_name'];
        for (var i in temp) {
            group_name[temp[i][0]] = temp[i][1];
        }
        temp = getdata['r_name'];
        for (var i in temp) {
            role_name[temp[i][0]] = temp[i][1];
        }
    };
    if (getdata['ws'] == 'q_tree') {
        temp = getdata['data'];
        var _tree = $('#g_tree');
        productchild(temp, _tree);
        init_tree();

    }
};

var init_tree = function() {
    $('.tree li:has(ul)').addClass('parent_li');
    $('.tree li >span').on('click', function(e) {
        console.log($(this));
        $(this).toggleClass('selector');
    });
    $('.tree li.parent_li > span').on('click', function(e) {
        var children = $(this).parent('li.parent_li').find(' > ul > li');
        // console.log($(this));
        if (children.is(":visible")) {
            children.hide('fast');
            $(this).find(' > i').addClass('icon-plus-sign').removeClass('icon-minus-sign');
        } else {
            children.show('fast');
            $(this).find(' > i').addClass('icon-minus-sign').removeClass('icon-plus-sign');
        }
        e.stopPropagation();
    });
};

function productchild(data, _root) {
    for (var i in data) {
        if (data[i] != null) {
            var li = $("<li><span id=" + i + "><i class='icon-minus-sign'></i>" + group_name[i] + "</span>");
            var u_s = $("<ul>");
            productchild(data[i], u_s);
            li.append(u_s);
            _root.append(li);
        } else {
            // var u = _root.find('ul');
            // console.log(_root,u);
            var li = $("<li><span id=" + i + "><i class='icon-leaf'></i>" + group_name[i] + "</span>");
            _root.append(li);
        }
    };
}



// 初始化变量
var DT = function() {
    ws.send("initv");
}
setTimeout('DT()', 100);

// 业务逻辑,获得树
// todo empty tree
$("#q_tree").bind("click", function() {
    ws.send("q_tree");
});

