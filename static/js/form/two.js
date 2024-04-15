new Vue({
            created: function () {
                var self = this;
                messages.forEach(item => {
                    setTimeout(function () {
                        self.$notify({
                            title: getLanuage('Tips'),
                            message: item.msg,
                            type: item.tag,
                            dangerouslyUseHTMLString: true
                        });
                    }, 200);
                });
            }
        })