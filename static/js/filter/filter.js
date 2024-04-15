//判断现实状态，全1时要显示出来
var showType = "111111";//有几列，就有几个1

if (!String.prototype.trim) {
    String.prototype.trim = function () {
        return this.replace(/^\s+|\s+$/g, '');
    };
}
String.prototype.replaceAll = function (s1, s2) {
    return this.replace(new RegExp(s1, "gm"), s2);
}
var cols = 5;//结束列数
var start = 0;//开始列数
var tr = [];
var maxtablenum = 3;//表格的数量，
var starttablenum = 0;//表格开始数量为0
for (var tablenum = starttablenum; tablenum <= maxtablenum; tablenum++) {
    var table = jQuery_1_8_3("#sth_content").find("table").eq(tablenum);
    if (table.length > 0) {
        var header = table.find("tr").eq(0);
        tr[tablenum] = table.find("tr").not(header);
        for (var col = start; col <= cols; col++)  {
            if (tablenum > 0) {
                var colflag = Number(col + tablenum * (cols + 1));
            } else {
                var colflag = col;
            }
            eval("var init_status_" + colflag + "=1");
            var td = header.find("td").eq(col);
            td.attr("id", "td" + colflag);
            var wid = td.width() + 25 + 20;
            jQuery_1_8_3("body").append("<div style='border-style:solid;border-width:1px;display:none;border-color:#ccc;background-color:#FFFCF7;z-index:1000; position:absolute;width:" + wid + "px;overflow-y:auto;margin-top:40px;' id='gc" + colflag + "'></div>");
            var txt = td.text();
            td.html("<div style='text-align:center;'>" + txt + "▼</div>");
            td.click(function (e) {
                if (e.stopPropagation) {
                    e.stopPropagation();
                } else {
                    e.cancelBubble = true;
                }
            });
            //var n = new Array();
            eval("var n" + colflag + " = new Array()");
            jQuery_1_8_3.each(tr[tablenum], function (index, domEle) {
                var temp = domEle.getElementsByTagName("td")[col].innerText;
                var tmparray = eval("n" + colflag);
                //if(eval("n"+col+".indexOf(temp)") == -1)
                if (temp != '') {
                    if (eval("jQuery_1_8_3.inArray(temp,n" + colflag + ")") == -1) {
                        eval("n" + colflag + ".push(temp)");
                    }
                    jQuery_1_8_3(domEle).attr("showType", showType)
                }
            });
            var high = td.height();
            // 弹出选择列表框的点击事件不冒泡到body
            jQuery_1_8_3("#gc" + colflag).click(function (e) {
                if (e.stopPropagation) {
                    e.stopPropagation();
                }
            });
            td.mousedown(function (e) {
                var id = jQuery_1_8_3(this).attr('id').substring(2);
                if (document.getElementById('gc' + id).style.display == 'block' || document.getElementById('gc' + id).style.display == '') {
                    document.getElementById('gc' + id).style.display = 'none';
                    return;
                }
                document.getElementById('gc' + id).style.display = 'block';
                if (document.getElementById("u" + id + "99") == null) {
                    jQuery_1_8_3("#gc" + id).append("<div id='u" + id + "99' style='height:20px;width:auto;cursor:hand;text-align:left;'><input id='chkall' class='chkall_" + id + "' type='checkbox' onchange='showgc(this)'/><span> 全部</span></div>");
                }
                for (var v = 0; eval("v<=n" + id + ".length"); v++) {
                    if (document.getElementById("u" + id + v) == null && eval("n" + id + "[v]") != null) {
                        jQuery_1_8_3("#gc" + id).append("<div id='u" + id + v + "' style='height:20px;width:auto;cursor:hand;text-align:left;' ><input type='checkbox' onchange='showgc(this)' /><span> " + eval("n" + id + "[v]") + "</span></div>");
                    }
                    var gcdiv = document.getElementById("gc" + id);
                    gcdiv.style.left = getLeft(document.getElementById('td' + id)) + 5 + "px";
                    gcdiv.style.top = getTop(document.getElementById('td' + id)) + 25 + "px";
                }
                //jQuery_1_8_3("#gc"+id).parent().find("input[type='checkbox']").attr("checked",false);
                for (var j = 0; j <= cols * (tablenum + 1); j++) {
                    if (j != id) {
                        if (document.getElementById('gc' + j) != null) {
                            document.getElementById('gc' + j).style.display = 'none';
                        }
                    } else {
                        document.getElementById('gc' + j).style.display = '';
                    }
                }
            });
        }
    }
}
var end = cols * (tablenum + 1);
jQuery_1_8_3("body").click(function (e) {
    for (var j = 0; j <= end; j++) {
        if (document.getElementById('gc' + j) != null) {
            document.getElementById('gc' + j).style.display = 'none';
        }
    }
});
function maskOP(maskStrin, pos, bitValue) {
    var ipos = parseInt(pos);
    var tmp2 = maskStrin.substr(ipos + 1);
    var tmp1 = maskStrin.substr(0, ipos);
    return tmp1 + bitValue + tmp2;
}
function showgc(obj) {
    var jobj = jQuery_1_8_3(obj).parent();
    var oldid = jobj.parent().attr("id").substring(2);
    var id = jobj.parent().attr("id").substring(2);
    var tablenum2 = Math.floor(id / (cols + 1));
    if (tablenum2 <= 0) {
        tablenum2 = 0;
    } else {
        id -= tablenum2 * (cols + 1);
    }
    var selType = jobj.find("span").eq(0).text();
    var checkbox = jobj.find("input[type='checkbox']").eq(0);
    if (eval("init_status_" + oldid + "==1")) {
        jobj.parent().find("input[type='checkbox']").attr("checked", false);
        jQuery_1_8_3.each(tr[tablenum2], function (index, domEle) {
            var theShowType = maskOP(jQuery_1_8_3(domEle).attr("showType"), id, "0");
            jQuery_1_8_3(domEle).attr("showType", theShowType);
            domEle.style.display = "none";
        });
        checkbox.attr("checked", true);
        eval("init_status_" + oldid + "=0");
    }
    if (selType.trim() == "全部") {
        if (checkbox.attr("checked")) {
            //checkbox.attr("checked", false);
            jobj.parent().find("input[type='checkbox']").attr("checked", true);
            jQuery_1_8_3.each(tr[tablenum2], function (index, domEle) {
                var theShowType = maskOP(jQuery_1_8_3(domEle).attr("showType"), id, "1");
                jQuery_1_8_3(domEle).attr("showType", theShowType);
                if (theShowType == showType)
                    domEle.style.display = "";
            });
        } else {
            //checkbox.attr("checked", true);
            jobj.parent().find("input[type='checkbox']").attr("checked", false);
            jQuery_1_8_3.each(tr[tablenum2], function (index, domEle) {
                var theShowType = maskOP(jQuery_1_8_3(domEle).attr("showType"), id, "0");
                jQuery_1_8_3(domEle).attr("showType", theShowType);
                domEle.style.display = "none";
            });
        }
    } else {
        jobj.parent().find("input[type='checkbox']").eq(0).attr("checked", false);
        var allcheckbox = jobj.parent().find(".chkall[type='checkbox']").eq(0);
        if (!allcheckbox.attr('checked')) {
            allcheckbox.attr('checked', false);
        }
        jQuery_1_8_3.each(tr[tablenum2], function (index, domEle) {
            var temp = domEle.getElementsByTagName("td")[id].innerText;
            var theShowType = jQuery_1_8_3(domEle).attr("showType");
            if (temp.replace(/\s/g, '') == selType.replace(/\s/g, '')) {
                if (checkbox.attr("checked")) {
                    theShowType = maskOP(theShowType, id, "1");
                    if (theShowType == showType)
                        domEle.style.display = "";
                } else {
                    theShowType = maskOP(theShowType, id, "0");
                    domEle.style.display = "none";
                }
                jQuery_1_8_3(domEle).attr("showType", theShowType);
            }
        });
    }
    var gcdiv1 = document.getElementById("gc" + id);
    gcdiv1.style.left = getLeft(document.getElementById('td' + id)) + 5 + "px";
}
//获取元素的纵坐标
function getTop(e) {
    var offset = e.offsetTop;
    if (e.offsetParent != null) offset += getTop(e.offsetParent);
    return offset;
}
//获取元素的横坐标
function getLeft(e) {
    var offset = e.offsetLeft;
    if (e.offsetParent != null) offset += getLeft(e.offsetParent);
    return offset;
}
