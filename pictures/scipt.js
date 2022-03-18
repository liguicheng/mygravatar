function getQueryVariable(variable)
{
       var query = window.location.search.substring(1);
       var vars = query.split("&");
       for (var i=0;i<vars.length;i++) {
               var pair = vars[i].split("=");
               if(pair[0] == variable){return pair[1];}
       }
       return(false);
}

$(function() {
    //获取地址栏里（URL）传递的参数
    var email = getQueryVariable("email");
    //alert(email);

    $.ajax( {
        url:"../cgi-bin/picInterface.py",
        dataType:'html',
        type: "post",
        data: {"email":email.toString()},
        success: function(url, textStatus){
            //alert(url);
            window.location.href = "../" + url;
        },
    });

});

