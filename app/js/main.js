var ws = new WebSocket("ws://localhost:8878/ws");
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

    }
};



function productchild(data, _root) {
    for (var i in data) {
        if (data[i] != null) {
            var u = $("<ul>");
            var li = $("<li><span id=" + i + "><i class='icon-minus-sign'></i>" + group_name[i] + "</span>");
            var u_s = $("<ul>");
            li.append(u_s);
            u.append(li);
            console.log(data, data[i]);
            temp = productchild(data[i], u_s);
            u.append("</li></ul>");
            _root.append(u);
        } else {
        	var u = _root.find('ul');
            var li = $("<li><span id=" + i + "><i class='icon-leaf'></i>" + group_name[i] + "</span>");
            u.append(li);
            // _root.append("<ul><li><span id=" + i + "><i class='icon-leaf'></i>" + group_name[i] + "</span></li>")
        }
    };
    $(function() {
        console.log('add eeeeee');
        $('.tree li:has(ul)').addClass('parent_li');
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
        $('.tree li >span').on('click', function(e) {
            console.log($(this));
        });
    });
}




var DT = function() {
    ws.send("initv");
    // ws.send("q_tree");
}
setTimeout('DT()', 100);

$("#q_tree").bind("click", function() {
    ws.send("q_tree");
});