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


})(jQuery);

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