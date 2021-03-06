$(document).ready(function(){
        $("#up-img-touch").click(function(){
        		  $("#doc-modal-1").modal({width:'600px'});
        });
});


function GetRequest(localUrl) {
	console.log(localUrl);
	//url例子：XXX.aspx?ID=" + ID + "&Name=" + Name；
    var url = localUrl; //获取url中"?"符以及其后的字串

    var addressParameter = {};
    if(url.indexOf("?") != -1)//url中存在问号，也就说有参数。
    {
    	var str;
    	if(url.indexOf("=")!=-1){
    		str = url.substr(1,url.indexOf("=")-1);
    	}else{
    		str =  url.substr(1);
    	}
    	console.log(str);
        //地址栏参数解密
		var addressUrl=decodeURIComponent(atob(str));
		var addressData = addressUrl.split('&');
		for(var i = 0; i < addressData.length; i ++){
	         	addressParameter[addressData[i].split("=")[0]]=unescape(addressData[i].split("=")[1]);
	        }

    }
    return addressParameter;
}


$(function() {
    'use strict';
    // 初始化
    var $image = $('#image');
    $image.cropper({
        aspectRatio: '1',
        autoCropArea:0.8,
        preview: '.up-pre-after',
        
    });

    //获取地址栏里（URL）传递的参数
    var Request = GetRequest(location.search);
    var email = Request['email']; //ID
    //alert(email);


    $.ajax( {
        url:"../cgi-bin/get_user_name.py",
        // dataType:'json',
        dataType:"json",
        type: "post",
        contentType: "application/x-www-form-urlencoded; charset=utf-8",
        data: {"email":email.toString()},
        success: function(data, textStatus){
            //alert(data['email']);
            //alert(getCookie('token'));
            if (email === data['email'] && data['name'] !== "") {
                document.getElementById("name").innerText=data['name'];
            } else {
                alert('请刷新登录界面后重新登录！')
                window.location.href = "../register";
            }
        },
        error: function(){
            //alert(document.cookie);
            alert('暂未登录！');
            window.location.href = "../register";
        }
    });

    $.ajax( {
        url:"../cgi-bin/get_user_pic.py",
        dataType:'html',
        type: "post",
        data: {"email":email.toString()},
        success: function(data, textStatus){
            if (data !== "") {
                //alert(data);
                imag.src = data;
            } else {
                alert('身份校验失败，请重新登录！');
                window.location.href = "../register";
            }

        },
    });



    // 事件代理绑定事件
    $('.docs-buttons').on('click', '[data-method]', function() {
   
        var $this = $(this);
        var data = $this.data();
        var result = $image.cropper(data.method, data.option, data.secondOption);
        switch (data.method) {
            case 'getCroppedCanvas':
            if (result) {
                // 显示 Modal
                $('#cropped-modal').modal().find('.am-modal-bd').html(result);
                $('#download').attr('href', result.toDataURL('image/jpeg'));
            }
            break;
        }
    });
    
    

    // 上传图片
    var $inputImage = $('#inputImage');
    var URL = window.URL || window.webkitURL;
    var blobURL;

    if (URL) {
        $inputImage.change(function () {
            var files = this.files;
            var file;

            if (files && files.length) {
               file = files[0];

               if (/^image\/\w+$/.test(file.type)) {
                    blobURL = URL.createObjectURL(file);
                    $image.one('built.cropper', function () {
                        // Revoke when load complete
                       URL.revokeObjectURL(blobURL);
                    }).cropper('reset').cropper('replace', blobURL);
                    $inputImage.val('');
                } else {
                    window.alert('Please choose an image file.');
                }
            }

            // Amazi UI 上传文件显示代码
            var fileNames = '';
            $.each(this.files, function() {
                fileNames += '<span class="am-badge">' + this.name + '</span> ';
            });
            $('#file-list').html(fileNames);
        });
    } else {
        $inputImage.prop('disabled', true).parent().addClass('disabled');
    }
    
    //绑定上传事件
    $('#up-btn-ok').on('click',function(){
    	var $modal = $('#my-modal-loading');
    	var $modal_alert = $('#my-alert');
    	var img_src=$image.attr("src");
    	if(img_src===""){
    		set_alert_info("没有选择上传的图片");
    		$modal_alert.modal();
    		return false;
    	}
    	
    	$modal.modal();
    	
    	var url=$(this).attr("url");
    	var canvas=$("#image").cropper('getCroppedCanvas');
    	var data=canvas.toDataURL(); //转成base64

        $.ajax( {  
                url:url,  
                // dataType:'json',
                dataType:'html',
                type: "POST",
                data: {
                    "image":data.toString(),
                    "email":email,
                    //提交表单时要求加入token，用于后端校验，防止CSRF攻击
                    "token":getCookie("token")
                },
                success: function(data, textStatus){
                    //alert(data);
                    // 身份验证错误或者cookie失效
                    //alert(document.cookie);
                    if (data === "" || getCookie("token") === "") {
                        if (getCookie("token") === "") {
                            alert("身份过期，请重新登录!");
                        } else {
                            alert("身份校验失败，无法更改头像，请重新登录!");
                        }
                         window.location.href = "../register";
                    } else {
                         // imag.src = canvas.toDataURL();
                        imag.src = data;

                        $modal.modal('close');
                        set_alert_info(data.result);
                        $modal_alert.modal();

                        if(data.result=="ok"){
                            // $("#up-img-touch img").attr("src", data.file);

                            var img_name=data.file.split('/')[2];
                            console.log(img_name);
                            $("#pic").text(img_name);
                        }
                    }


                },
                error: function(){
                    //alert("失败啦");
                	$modal.modal('close');
                	set_alert_info("上传文件失败了！");
                	$modal_alert.modal();
                	//console.log('Upload error');  
                }  
         });  
    	
    });


    $('#logout').on('click',function(){
    	var url=$(this).attr("url");

        $.ajax( {
                url:url,
                dataType:'html',
                type: "POST",
                data: {},
                success: function(data, textStatus){
                    alert("退出成功!点击确定返回登录界面");
                    window.location.href = "../register";

                },
                error: function(){
                	$modal.modal('close');
                	set_alert_info("上传文件失败了！");
                	$modal_alert.modal();
                	//console.log('Upload error');
                }
         });

    });
    
});

function rotateimgright() {
$("#image").cropper('rotate', 90);
}


function rotateimgleft() {
$("#image").cropper('rotate', -90);
}

function set_alert_info(content){
	$("#alert_content").html(content);
}

// 获取指定名称的cookie
function getCookie(name){
    var strcookie = document.cookie;//获取cookie字符串
    var arrcookie = strcookie.split(";");//分割
    //遍历匹配
    for ( var i = 0; i < arrcookie.length; i++) {
        var arr = arrcookie[i].split("=");
        if (arr[0] == name){
            return arr[1];
        }
    }
    return "";
}