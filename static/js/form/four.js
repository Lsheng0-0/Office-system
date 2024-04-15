window.getLanuage = function (key) {
                if (!window.Lanuages) {
                    return "";
                }
                var val = Lanuages[key];
                if (!val || val == "") {
                    val = key;
                }
                return val
            }
            Date.prototype.format = function (fmt) {
                var o = {
                    "M+": this.getMonth() + 1,                 //月份
                    "d+": this.getDate(),                    //日
                    "h+": this.getHours(),                   //小时
                    "m+": this.getMinutes(),                 //分
                    "s+": this.getSeconds(),                 //秒
                    "q+": Math.floor((this.getMonth() + 3) / 3), //季度
                    "S": this.getMilliseconds()             //毫秒
                };
                if (/(y+)/.test(fmt))
                    fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
                for (var k in o)
                    if (new RegExp("(" + k + ")").test(fmt))
                        fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
                return fmt;
            }
            var searchApp = new Vue({
                el: '#toolbar',
                data: {
                    placeholder: ' 搜索账号',
                    searchInput: '',
                                'depart_id__title__exact': '',
                                'content__exact': '',
                },
                created: function () {
                    var self = this;
                    var date_field = [];
                    $('.form-params').each(function () {
                        var key = $(this).attr('data-name');
                        var value = $(this).val();
                        self[key] = value;
                    });
                    try {
                        date_field.forEach(key => {
                            var start = self[key + "__gte"];
                            var end = self[key + "__lte"];
                            self[key] = [start, end];
                        });
                    } catch (e) {
                        console.warn('日期值回显失败，也许是django版本问题，请至github报告此问题：https://github.com/newpanjing/simpleui/issues');
                    }
                },
                watch: {
                },
                methods: {
                    changeDate: function (d1, d2) {
                        console.log(arguments)
                    },
                    changeDatetime: function (d1, d2) {
                        console.log(arguments)
                    },
                    formSubmit: function () {
                        preSubmit();
                        document.getElementById('changelist-search').submit();
                    }
                }
            })