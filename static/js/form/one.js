var fontConfig = new Vue({
        data: {
            fontSize: null
        },
        watch: {
            fontSize: function (newValue) {
                if (newValue != 0) {
                    var fontStyle = document.getElementById('fontStyle');
                    if (!fontStyle) {
                        fontStyle = document.createElement('style');
                        fontStyle.id = 'fontStyle';
                        fontStyle.type = 'text/css';
                        document.head.append(fontStyle);
                    }
                    fontStyle.innerHTML = '*{font-size:' + newValue + 'px!important;}'

                } else {
                    var fontStyle = document.getElementById('fontStyle');
                    if (fontStyle) {
                        fontStyle.remove();
                    }
                }
            }
        },
        created: function () {
            var val = getCookie('fontSize');
            if (val) {
                this.fontSize = parseInt(val);
            } else {
                this.fontSize = 0;
            }
        },
        methods: {}
    });


    new Vue({
        el: '#theme',
        data: {
            theme: '',
        },
        created: function () {
            this.theme = getCookie('theme');

            var self = this;
            //向父组件注册事件
            if (parent.addEvent) {
                parent.addEvent('theme', function (theme) {
                    self.theme = theme;
                });

                parent.addEvent('font', function (font) {
                    fontConfig.fontSize = font;
                });
                // {% if not cl %}
                // parent.addEvent('title', '{{title}}');
                // {% endif %}
            }

        }
    })
    window.addEventListener('beforeunload', () => {
        if (window.beforeLoad) {
            window.beforeLoad();
        }
    });
