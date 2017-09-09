var ws = new WebSocket("ws://localhost:9909/ws");
var group_name = [];
var role_name = [];
var g_selected, r_selected, u_selected, pu_selected;
var role_user = {};
var r_p_list = [];


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
        temp = getdata['r_p_list'];
        for (var i in temp) {
            console.log(i, temp[i]);
            r_p_list[i] = temp[i];
        }
    };
    if (getdata['name'] == 'q_tree') {
        temp = getdata['data'];
        var _tree = $('#g_tree');
        _tree.empty();
        productchild(temp, _tree);
        init_tree();
    };
    if (getdata['name'] == 'role_list') {
        temp = getdata['data'];
        var _tree = $('#r_tree');
        _tree.empty();
        productchild_easy(temp, _tree);
        init_tree();
    };
    if (getdata['name'] == 'per_list') {
        temp = getdata['data'];
        var _tree = $('#p_tree');
        _tree.empty();
        productchild_easy(temp, _tree);
        init_tree();
    };
    if (getdata['name'] == 'user_list') {
        temp = getdata['data'];
        var _tree = $('#u_tree');
        _tree.empty();
        productchild_easy(temp, _tree);
        init_tree();
        for (var i in temp) {
            row = temp[i];
            if (!(row[2] in role_user)) {
                role_user[row[2]] = [];
            }
            role_user[row[2]].push(row[0]);
        }
    };
};

var init_tree = function() {
    $('.tree li:has(ul)').addClass('parent_li');
    $('.tree li >span').on('click', function(e) {
        // console.log($(this));
        if ($(this).parents('div')[0].id == 'g_tree') {
            g_selected = $(this).context.id;
            // reset add group father name
            $('#g_a_f_name').html(group_name[g_selected]);
            $('#g_m_now_name').html(group_name[g_selected]);
            $('#g_d_now_name').html(group_name[g_selected]);
            afterselectgroup(g_selected);
            // end
            $('#g_tree li >span').filter('.selector').toggleClass('selector');
            $(this).toggleClass('selector');
        }
        if ($(this).parents('div')[0].id == 'r_tree') {
            $('#r_tree li >span').filter('.easy_selector').toggleClass('easy_selector');
            $(this).toggleClass('easy_selector');
            r_selected = $(this).context.id;
            // 将用户树中属于选中部门的员工添加颜色
            _u_root = $('#u_tree');
            coloruser(r_selected, role_user, _u_root);
            // 将权限树中属于选中部门的权限添加颜色
            _p_root = $('#p_tree');
            coloruser(r_selected, r_p_list, _p_root);
        }
        if ($(this).parents('div')[0].id == 'p_tree') {
            if ($('#p_tree li >span').filter('.easy_selector').length > 0) {
                $('#p_tree li >span').filter('.easy_selector').removeClass('easy_selector');
            }
            $(this).toggleClass('easy_selector');
            u_selected = $(this).context.id;
        }
        if ($(this).parents('div')[0].id == 'u_tree') {
            if ($('#u_tree li >span').filter('.easy_selector').length > 0) {
                $('#u_tree li >span').filter('.easy_selector').removeClass('easy_selector');
            }
            $(this).toggleClass('easy_selector');
            u_selected = $(this).context.id;
        }
    });
};

// 复杂添加树节点
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

// 简单添加树节点
function productchild_easy(data, _root) {
    for (var i in data) {
        var li = $("<li><span id=" + data[i][0] + "><i class='icon-leaf'></i>" + data[i][1] + "</span>");
        _root.append(li);
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

// 业务逻辑,添加部门
$("#q_a_g_s").bind("click", function() {
    console.log('add group');
    var new_name = $('#g_a_new_name').val();
    ws.send('addgroup,' + g_selected + ',' + new_name);
    $('#g_a_new_name').val('');
    g_selected = '';
});

// 业务逻辑,修改部门
$("#q_m_g_s").bind("click", function() {
    console.log('modify group');
    var new_name = $('#g_m_new_name').val();
    ws.send('modifygroup,' + g_selected + ',' + new_name);
    $('#g_m_new_name').val('');
    g_selected = '';
});

// 业务逻辑,删除部门
$("#q_d_g_s").bind("click", function() {
    console.log('delete group');
    var temp_status = $('#g_d_c').prop('checked');
    ws.send('deletegroup,' + g_selected + ',' + temp_status);
    g_selected = '';
});

// 业务逻辑,查询部门对应的角色及人员,更新树
function afterselectgroup(gid) {
    console.log('afterselectgroup', gid);
    ws.send('selectgroup,' + gid);
}

// 业务逻辑,添加权限
$("#p_a_s").bind("click", function() {
    console.log("add per");
    var temp_name = $('#p_a_name').val();
    ws.send("add_per," + temp_name);
    $('#p_a_name').val('');
})

// 添加用户树节点颜色
function coloruser(rid, _data, _root) {
    if (rid in _data) {
        temp = _data[rid];
        _root.find('li').each(function() {
            index = $.inArray(parseInt($(this).children()[0].id), temp);
            if (index > -1) {
                _temp = $($(this).find('span')[0]);
                _temp.addClass('selector');
            } else {
                _temp = $($(this).find('span')[0]);
                _temp.removeClass('selector');
            }
        })
    } else {
        _root.find('li').each(function() {
            _temp = $($(this).find('span')[0]);
            _temp.removeClass('selector');
        })
    }
}