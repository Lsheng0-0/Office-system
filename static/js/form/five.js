const layerApp = new Vue({
                    el: '#layer_app',
                    data: {
                        visible: false,
                        title: '弹出层',
                        params: [],
                        layer: {},
                        rules: [],
                        action: ''
                    },
                    methods: {
                        layerSubmit() {
                            const self = this;
                            //校验
                            for (let key in self.params) {
                                let item = self.params[key];
                                if (item.require) {
                                    if (!item.value || item.value == '' || item.length == 0) {
                                        self.$message.error(`"${item.label}" Can't be empty.`)
                                        return;
                                    }
                                }
                            }
                            //开始提交
                            let data = new FormData();
                            //方法名
                            data.append('_action', self.action);
                            let selecteds = [];
                            $("#result_list .selected input[name='_selected_action']").each((index, item) => selecteds.push(item.value));
                            data.append('_selected', selecteds.join(','));
                            data.append('select_across',document.querySelector("input[name='select_across']").value)
                            //获取选中的数据
                            data.append('csrfmiddlewaretoken', document.querySelector('[name="csrfmiddlewaretoken"]').value);
                            for (let key in self.params) {
                                let item = self.params[key];
                                if (item.type === "file") {
                                    data.append(item.key, self.$refs[item.key][0].files[0]);
                                } else if (item.value) {
                                    data.append(item.key, item.value);
                                }
                            }
                            axios.post('None'+window.location.search, data).then(res => {
                                if (res.data.status === 'redirect') {
                                    self.visible = false;
                                    window.location.href = res.data.url;
                                    return;
                                }
                                if (res.data.status == 'success') {
                                    self.visible = false;
                                    //1.5s 后刷新
                                    setTimeout(() => window.location.reload(), 1000);
                                }
                                self.$message({
                                    message: res.data.msg,
                                    type: res.data.status
                                });
                            }).catch(err => self.$message.error(err));
                        }
                    }
                })
                //弹出层处理
                function layer(data, action) {
                    layerApp.layer = data.layer;
                    layerApp.title = data.layer.title;
                    layerApp.params = data.layer.params;
                    layerApp.action = action;
                    layerApp.$nextTick(() => {
                        layerApp.visible = true;
                    });
                }
                function actionsCleaning(name) {
                    $("#changelist-form input[name='action']").val(name);
                    $("#changelist-form [name='_save']").removeAttr('name');
                    $("#changelist-form [name!='']").each(function () {
                        var obj = $(this);
                        if (obj.attr('name') && obj.attr('name').indexOf('form-') == 0) {
                            obj.removeAttr('name');
                        }
                    });
                }
                var _action = new Vue({
                    el: '.actions',
                    data: {
                        select_across: 0,
                        file_format: 1,
                        show: true,
                        options: [{
                            value: 0,
                            label: 'csv'
                        }, {
                            value: 1,
                            label: 'xls'
                        }, {
                            value: 2,
                            label: 'xlsx'
                        }, {
                            value: 3,
                            label: 'tsv'
                        }, {
                            value: 4,
                            label: 'ods'
                        }, {
                            value: 5,
                            label: 'json'
                        }, {
                            value: 6,
                            label: 'yaml'
                        }, {
                            value: 7,
                            label: 'html'
                        }],
                        customButton:{"delete_selected": {"allowed_permissions": ["delete"], "short_description": "\u5220\u9664\u6240\u9009\u7684 %(verbose_name_plural)s", "eid": 0}},
                        exts: []
                    },
                    created() {
                        if (localStorage && typeof (localStorage.searchStatus) != 'undefined') {
                            this.show = localStorage.searchStatus == 'true';
                        }
                    },
                    watch: {
                        'show': function (newValue) {
                            obj = document.querySelector('.xfull')
                            if (!newValue) {
                                //隐藏
                                document.getElementById('toolbar').style.display = 'none';
                                if (obj) {
                                    obj.style.display = 'none';
                                }
                            } else {
                                //显示
                                document.getElementById('toolbar').style.display = 'inherit';
                                if (obj) {
                                    obj.style.display = 'inherit';
                                }
                            }
                            if (localStorage) {
                                localStorage['searchStatus'] = newValue;
                            }
                        }
                    },
                    methods: {
                        searchDisplay: function () {
                            this.show = !this.show;
                        },
                        reload: function () {
                            window.location.reload()
                        },
                        openNewPage: function () {
                            window.open(window.location.href)
                        },
                        getIcon: getIcon,
                        extClick: function (item) {
                            window.location.href = item.url;
                        },
                        formSubmit: function () {
                            $("#changelist-form").submit();
                        },
                        delSelected: function (name) {
                            actionsCleaning(name);
                            var self = this;

                            // 增加非空判断！
                            if ($("#changelist-form").serializeArray().length <= 2) {
                                this.$message.error(getLanuage("Please select at least one option!"));
                                return;
                            }

                            //#67 #66 修复删除问题，改为弹出确认

                            this.$confirm(getLanuage('Are you sure you want to delete the selected?'))
                                .then(_ => {
                                    self.formSubmit();
                                }).catch(_ => {

                            });
                        }
                    }
                });
                function selectAll() {
                    _action.select_across = 1;
                }
                function unSelect() {
                    _action.select_across = 0;
                }
                $(function () {
                    action_btns = $(".actions button").not('.stop-submit');
                    action_btns.click(function () {
                        var url = $(this).attr("url");
                        var eid = $(this).attr('eid');
                        var confirm = $(this).attr('confirm');
                        var checkbox_checked = $(".action-checkbox input:checked").length;
                        var data_name = $(this).attr('data-name');
                        var _vue = new Vue();
                        //这边处理弹出层对话框
                        if (eid) {
                            for (var i in _action.customButton) {
                                var temp = _action.customButton[i];
                                if (temp.eid == eid && temp.layer) {
                                    layer(temp, i);
                                    return;
                                }
                            }
                        }
                        //TODO 需要做国际化
                        if (checkbox_checked == 0 && data_name != "add_item" && !_action.customButton[data_name].action_url) {
                            _vue.$alert(getLanuage("Please select at least one option!"), '', {
                                type: 'warning'
                            })
                        } else if (confirm) {
                            _vue.$confirm(confirm, '提示', {
                                confirmButtonText: '确定',
                                cancelButtonText: '取消',
                                type: 'warning'
                            }).then(() => done.call(this));
                        } else {
                            done.call(this)
                        }
                        function done() {
                            if (eid) {
                                for (var i in _action.customButton) {
                                    var temp = _action.customButton[i];
                                    if (temp.eid == eid) {
                                        if (typeof (temp.action_type) != 'undefined') {

                                            if (!temp.action_url) {
                                                this.$notify({
                                                    title: 'error',
                                                    message: 'action must contain attributes:action_url! ',
                                                    type: 'error',
                                                    dangerouslyUseHTMLString: true
                                                });
                                                return;
                                            }

                                            switch (temp.action_type) {
                                                case 0:
                                                    window.location.href = temp.action_url;
                                                    break;
                                                case 1:
                                                    parent.window.app.openTab({
                                                        url: temp.action_url,
                                                        icon: temp.icon || 'fa fa-file',
                                                        name: temp.short_description,
                                                        breadcrumbs: []
                                                    });
                                                    break;
                                                case 2:
                                                    window.open(temp.action_url);
                                                    break;
                                            }
                                            console.log('中断后续操作');
                                            return;
                                        }
                                        //终止执行
                                        break;
                                    }
                                }
                            }
                            if (url) {
                                window.location.href = url;
                                return;
                            }
                            if ($(this).attr('data-name')) {
                                var name = $(this).attr("data-name");
                                actionsCleaning(name);
                            }
                            $("#changelist-form").submit();
                        }
                    });
                });