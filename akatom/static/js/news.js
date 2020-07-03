
$(function (){
    function getCookie(name) {
    if (document.cookie && document.cookie.length) {
        var cookies = document.cookie
            .split(';')
            .filter(function (cookie) {
                return cookie.indexOf(name + "=") !== -1;
            })[0];
        try {
            return decodeURIComponent(cookies.trim().substring(name.length + 1));
        } catch (e) {
            if (e instanceof TypeError) {
                console.info("No cookie with key \"" + name + "\". Wrong name?");
                return null;
            }
            throw e;
        }
    }
    return null;
    };
    function csrfSafeMethod(method) {
    // These HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    };
    //从cookie获取 csrftoken
    let csrftoken = getCookie('csrftoken');
    // 这个设置会让所有Ajax POST/DELETE请求在其请求头中都携带 X-CSRFToken 信息
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $('#newsFormModal').on('shown.bs.modal', function () {
        $('#newsInput').trigger('focus')
    });

    $("#postNews").click(function (){
        if($("#newsInput").val() === ''){
            alert("请输入新闻动态的内容");
            return;
        }
        if(currentUser ===""){
            alert("请登录后在发布新闻！");
        }
        else{
            // Ajax call after pushing button, to register a News object.
            $.ajax({
                url: '/news/post-news/',
                data: $("#postNewsForm").serialize(),
                type: 'POST',
                cache: false,
                success: function (data) {
                    $("ul.stream").prepend(data);
                    $("#newsInput").val("");
                    $("#newsFormModal").modal("hide");
                    // hide_stream_update();
                },
                error: function (data) {
                    alert(data.responseText);
                },
            });
        }
    });

    $("ul.stream").on("click", ".like", function(){
        let li = $(this).closest('li');
        let newsId = $(li).attr("news-id");
        let payload ={
            'newsId':newsId,
            'csrf_token':csrftoken,
        };
         $.ajax({
            url: '/news/like/',
            data: payload,
            type: 'POST',
            cache: false,
            success: function (data) {
                $(".like .like-count", li).text(data.likers_count);
                if ($(".like .heart", li).hasClass("fa fa-heart")) {
                    $(".like .heart", li).removeClass("fa fa-heart");
                    $(".like .heart", li).addClass("fa fa-heart-o");
                }
                else {
                    $(".like .heart", li).removeClass("fa fa-heart-o");
                    $(".like .heart", li).addClass("fa fa-heart");
                }
            }
        });
    });

    $('#replyFormModal').on('show.bs.modal', function (event) {
        let button = $(event.relatedTarget); // Button that triggered the modal
        let recipient = button.data('who');
        let newsid = button.data('newsid');// Extract info from data-* attributes
        // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
        // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
        let modal = $(this);
        modal.find('.modal-title').text('新的回复给： ' + recipient);
        modal.find('.modal-body input.recipient').val(recipient);
        modal.find('.modal-body input.newsid').val(newsid);
    });

    //发表评论
    $("#postReply").click(function (){
        if($("#reply-content").val() === ''){
            alert("请输入评论内容");
            return;
        }
        if(currentUser ===""){
            alert("请登录后再评论！");
        }
        else{
            // Ajax call after pushing button, to register a News object.
            $.ajax({
                url: '/news/post-reply/',
                data: $("#postReplyForm").serialize(),
                type: 'POST',
                cache: false,
                success: function (data) {
                    let li = $('[news-id='+data.newsid+']');
                    $(".reply .reply-count", li).text(data.replies_count);
                    //$("#reply-content").val(value: "");
                    $("#reply-content").val("");
                    $("#replyFormModal").modal("hide");
                },
                error: function (data) {
                    alert(data.responseText);
                },
            });
        }
    });

    //获取评论列表
    $("ul.stream").on("click", ".reply", function () {
        let li = $(this).closest('li');
        let newsId = $(li).attr("news-id");
        $.ajax({
            url: '/news/get-replies/',
            data: {'newsId': newsId},
            cache: false,
            success: function (data) {
                $("#replyListModal .modal-body").html(data.replies_html);
            }
        });
    });

});
