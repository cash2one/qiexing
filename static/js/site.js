/*
    为字符串拓展format方法
    用例：
    String.format('{0}, {1}!', 'Hello', 'world');
*/
if (!String.format) {
    String.format = function(src){
        if (arguments.length == 0){
            return null;
        }

        var args = Array.prototype.slice.call(arguments, 1);
        return src.replace(/\{(\d+)\}/g, function(m, i){
            return args[i];
        });
    };
}


(function($){

	$.QXUtils = {
        version: '1.0.0',
        author: 'stranger',
        description: '工具包'
    };

    /*
        去掉所有的html标签
        target: 要操作的字符串

        用例:
        $.QXUtils.clearHtmlTags('<div>1</div>');
    */
    $.QXUtils.clearHtmlTags = function(target){
        if(!target){
            return '';
        }
        return target.replace(/<[^>].*?>/g,"");
    };

    /*
        去掉所有的转义字符
        target: 要操作的字符串

        用例:
        $.QXUtils.clearEscapeCharacters('<div>1</div>');
    */
    $.QXUtils.clearEscapeCharacters = function(target){
        if(!target){
            return '';
        }
        return target.replace(/&[^;].*?;/g, '');
    };

    /*
        屏幕宽度小于 768 归于手机
    */
    $.QXUtils.isPhone = function(){
        return ($(window).width() < 768) ? true : false;
    };

    /*
        屏幕宽度 大于768 而 小于1024 归于平板
    */
    $.QXUtils.isPad = function(){
        return (768 <= $(window).width() && $(window).width() <= 1024) ? true : false;
    };

    /*
        屏幕宽度大于 1024 归于桌面
    */
    $.QXUtils.isDesktop = function(){
        return (1024 < $(window).width()) ? true : false;
    };

    /*
        字典映射

        用例：
        $.QXUtils.dictMap({'a': '1', 'b': '2'}, {'a': 'a1', 'b': 'b1'})
        返回 {'a1': '1', 'b1': '2'}
    */
    $.QXUtils.dictMap = function(originDict, maps){
        var newDict = {};
        
        if(!originDict){
            return null;
        }
        
        for(var m in maps){
            newDict[m] = originDict[maps[m]]
        }

        return newDict;
    };

    /*
        批量字典映射解析

        $.QXUtils.dictMapParse([{'a': '1', 'b': '2'}], {'a': 'a1', 'b': 'b1'});
    */
    $.QXUtils.dictMapParse = function(data, maps){
        var temp = [];

            _.each(data, function(d){
                temp.push($.QXUtils.dictMap(d, maps));
            });

        return temp;
    };


    // 分享插件
    $.QXShare = {
        version: '1.0.0',
        author: 'stranger',
        description: '分享插件'
    };
    /*
        分享到微博
        url: 要分享的url
        title: 要分享的描述
        pic: 图片地址
        notOpenWin: 是否要弹出窗口
        
        用例：
        $.QXShare.sinaWeibo('www.a.com', 'test', '1.jpg', true);
    */
    $.QXShare.sinaWeibo = function(url, title, pic, notOpenWin){
        var clearTitle = $.QXUtils.clearEscapeCharacters($.QXUtils.clearHtmlTags(title)),
            sinaUrl = String.format(
                "http://service.weibo.com/share/share.php?url={0}&title={1}&pic={2}&appkey={3}&ralateUid={4}&searchPic=false",
                url,
                (clearTitle.length >= 110) ? (clearTitle.substring(0, 110) + '...') : clearTitle,
                pic ? pic : '',
                '266639437',
                '5083374708'
            );

        notOpenWin = notOpenWin ? notOpenWin : false;
        if(!notOpenWin){
            window.open(sinaUrl, '_blank');
        }

        return sinaUrl;
    };

    /*
        分享到qq
        url: 要分享的url
        title: 要分享的描述
        desc: 要分享的描述
        notOpenWin: 是否要弹出窗口

        用例：
        $.QXShare.qq('www.a.com', 'test', 'test', true);
    */
    $.QXShare.qq = function(url, title, desc, notOpenWin){
        var clearTitle = $.QXUtils.clearEscapeCharacters($.QXUtils.clearHtmlTags(title)),
            clearDesc = $.QXUtils.clearEscapeCharacters($.QXUtils.clearHtmlTags(desc)),
            qqUrl = String.format(
                "http://connect.qq.com/widget/shareqq/index.html?url={0}&title={1}&desc={2}&source={3}",
                url,
                (clearTitle.length >= 110) ? (clearTitle.substring(0, 110) + '...') : clearTitle,
                clearDesc ? clearDesc : '在且行上看到点好东西, 推荐你看看',
                'shareqq'
            );

        notOpenWin = notOpenWin ? notOpenWin : false;

        if(!notOpenWin){
            window.open(qqUrl, '_blank');
        } 

        return qqUrl;
    };


})(jQuery);


/*
    创建 KindEditor 编辑器
    selector: textarea的选择器
*/
function createEditor(selector){
    // 如果是手机端则直接使用html的textarea
    if($.QXUtils.isPhone()){
        return $(selector);
    } else {
        return KindEditor.create(selector, {
            resizeType : 1,
            width: '100%',
            //autoHeightMode : true,
            allowPreviewEmoticons : true,
            allowImageUpload : true,
            allowImageRemote: true,
            // basePath: '/',
            uploadJson: '/save_img',
            pasteType : 1,
            cssData: 'body{font-family: "Helvetica Neue",Helvetica,"Lucida Grande","Luxi Sans",Arial,"Hiragino Sans GB",STHeiti,"Microsoft YaHei","Wenquanyi Micro Hei","WenQuanYi Micro Hei Mono","WenQuanYi Zen Hei","WenQuanYi Zen Hei Mono",LiGothicMed; font-size: 14px; color: #222;}',
            themesPath: MEDIA_URL + "css/kindeditor/themes/",
            pluginsPath: MEDIA_URL + "js/kindeditor/plugins/",
            langPath: MEDIA_URL + "js/kindeditor/",
            items : [
                'bold', 'italic', 'underline', 'removeformat', '|', 
                'justifyleft', 'justifycenter', 'justifyright', 'insertorderedlist', 'insertunorderedlist', '|', 
                'image', 'link', '|', //'emoticons_zx',
                'fullscreen'
            ],
            afterCreate : function() { 
                //this.loadPlugin('autoheight');
            }, 
            afterBlur:function(){ 
                this.sync(); 
            },
            afterUpload : function(url) {
            }
        });
    }
};


$(document).ready(function(){

	var dropdownTimeout = null,
        showDropdown = function(target){
            $(target).addClass('open');
        },
        hideDropdown = function(target){
            $(target).removeClass('open');
        };

	// 电脑访问添加鼠标事件
    if($.QXUtils.isDesktop()){
        $('.user-menu .dropdown-toggle')
        .bind('mouseenter', function(){showDropdown('.user-menu')})
        .bind('mouseleave', function(){hideDropdown('.user-menu')})
        .bind('click', function(e){
            window.location.href = $(this).attr('href');
        });

        $('.user-menu .dropdown-menu')
        .bind('mouseenter', function(){showDropdown('.user-menu')})
        .bind('mouseleave', function(){hideDropdown('.user-menu')});
    }

});