var ws = new WebSocket("ws://localhost:9909/ws");
var group_name = [];
var role_name = [];
var per_name = [];
var g_selected, r_selected, u_selected, p_selected;
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
        for (var i in temp) {
            per_name[temp[i][0]] = temp[i][1];
        }
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
            // 添加角色上的部门名称名称
            $('#r_a_now_name').html(group_name[g_selected]);
            // 获取选中部门的角色人员
            afterselectgroup(g_selected);
            // end
            $('#g_tree li >span').filter('.selector').toggleClass('selector');
            $(this).toggleClass('selector');
        }
        if ($(this).parents('div')[0].id == 'r_tree') {
            $('#r_tree li >span').filter('.easy_selector').toggleClass('easy_selector');
            $(this).toggleClass('easy_selector');
            // 将选中的id存到全局变量中
            r_selected = $(this).context.id;
            // 将用户树中属于选中部门的员工添加颜色
            _u_root = $('#u_tree');
            coloruser(r_selected, role_user, _u_root);
            // 将权限树中属于选中部门的权限添加颜色
            _p_root = $('#p_tree');
            coloruser(r_selected, r_p_list, _p_root);
            // 修改修改橘色模态框上的值
            $('#r_m_now_name').html(role_name[r_selected]);
            // 修改添加角色权限模态框上的值
            $('#p_a_r_name').html(role_name[r_selected]);
            // 修改删除角色权限模态框上的值
            $('#p_d_r_name').html(role_name[r_selected]);
        }
        if ($(this).parents('div')[0].id == 'p_tree') {
            if ($('#p_tree li >span').filter('.easy_selector').length > 0) {
                $('#p_tree li >span').filter('.easy_selector').removeClass('easy_selector');
            }
            $(this).toggleClass('easy_selector');
            // 将选中的id存到全局变量中
            p_selected = $(this).context.id;
            // 修改模态框上的值
            $('#p_d_name').html(per_name[p_selected]);
            // 修改添加角色权限模态框上的值
            $('#p_a_p_name').html(per_name[p_selected]);
            // 修改删除角色权限模态框上的值
            $('#p_d_p_name').html(per_name[p_selected]);
        }
        if ($(this).parents('div')[0].id == 'u_tree') {
            if ($('#u_tree li >span').filter('.easy_selector').length > 0) {
                $('#u_tree li >span').filter('.easy_selector').removeClass('easy_selector');
            }
            $(this).toggleClass('easy_selector');
            // 将选中的id存到全局变量中
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
    console.log('addgroup');
    var new_name = $('#g_a_new_name').val();
    ws.send('addgroup,' + g_selected + ',' + new_name);
    $('#g_a_new_name').val('');
    g_selected = '';
});

// 业务逻辑,修改部门
$("#q_m_g_s").bind("click", function() {
    console.log('modifygroup');
    var new_name = $('#g_m_new_name').val();
    ws.send('modifygroup,' + g_selected + ',' + new_name);
    $('#g_m_new_name').val('');
    g_selected = '';
});

// 业务逻辑,删除部门
$("#q_d_g_s").bind("click", function() {
    console.log('deletegroup');
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
    console.log("add_per");
    var temp_name = $('#p_a_name').val();
    ws.send("add_per," + temp_name);
    $('#p_a_name').val('');
})

// 业务逻辑,修改权限名称
$("#p_u_s").bind("click", function() {
    console.log("modify_per");
    var temp_name = $('#p_u_name').val();
    ws.send("modify_per," + p_selected + ',' + temp_name);
    $('#p_u_name').val('');
})

// 业务逻辑,删除权限
$("#p_d_s").bind("click", function() {
    console.log("delete_per");
    ws.send("delete_per," + p_selected);
    $('#p_d_name').val('');
})

// 业务逻辑,删除权限
$("#p_a_r_s").bind("click", function() {
    console.log("add_role_per");
    ws.send("add_role_per," + r_selected + "," + p_selected);
    $('#p_a_r_name').val('');
    $('#p_a_p_name').val('');
})

// 业务逻辑,删除权限
$("#p_d_r_s").bind("click", function() {
    console.log("delete_role_per");
    ws.send("delete_role_per," + r_selected + "," + p_selected);
    $('#p_d_r_name').val('');
    $('#p_d_p_name').val('');
})

// 业务逻辑,添加角色
$("#r_a_s").bind("click", function() {
    console.log("add role");
    var temp_name = $('#r_a_name').val();
    ws.send("add_role," + g_selected + "," + temp_name);
    $('#r_a_name').val('');
})

// 业务逻辑,修改角色
$("#r_m_s").bind("click", function() {
    console.log("modify role");
    var temp_name = $('#r_m_name').val();
    ws.send("modify_role," + r_selected + "," + temp_name+','+g_selected);
    $('#r_m_name').val('');
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