// The boilerplate code below is copied from the Django 1.10 documentation.
// It establishes the necessary HTTP header fields and cookies to use
// Django CSRF protection with jQuery Ajax requests.

$( document ).ready(function() {  // Runs when the document is ready
  window.setInterval(getCommentsUpdates,5000);
  // using jQuery
  // https://docs.djangoproject.com/en/1.10/ref/csrf/

  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }

  var csrftoken = getCookie('csrftoken');

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      }
  });

  // TODO:  Use jQuery to send an Ajax GET request to /sio/get-courses and
  // update the list of courses on the web page.  (Use our provided
  // helper method, updateChanges, below.)
  $('.commentbutton').click(function(event){
        var commentbutton = event.target.id;
        var end            = commentbutton.lastIndexOf('_');
        var post_id        = commentbutton.slice(end+1);
        CommentBlock(post_id);
      })


  $(document).on('submit','.commentform',function(event) {
      event.preventDefault(); // Prevent form from being submitted
      var commentform_id = event.target.id;
      var end            = commentform_id.lastIndexOf('_');
      var post_id        = commentform_id.slice(end+1);
      $.post("../create_comment"+'/'+post_id+'/', $('#'+commentform_id).serialize())
        .done(function(data){
        getCommentsUpdates();
        $('#'+commentform_id).parent().remove();
        $('#comment_'+post_id).toggle();
    });
  });


  function getCommentsUpdates() {
    var stamp=$('#timestamp').val();
    $.get("../update_comment",{timestamp:stamp})
      .done(function(data) {
          debugger;
          updateComments(data);
      });
  }

  function CommentBlock(post_pk){
    var commentDiv = $("<div>",{
      "class" : "container",
      "id": "comment_block",
    }).appendTo('#carddiv_'+post_pk);
    
    var commentForm = $("<form>",{
      "id": "commentform_"+post_pk,
      "class":"commentform",
      "name":"UserCommentForm",
      "method": "POST",
    }).appendTo(commentDiv);
    var textArea = $("<textarea>",{
      "class" : "form-control",
      "rows": '3',
      "name":"comment",
      "id": "comment",
      "placeholder":"write your comment here."
    }).appendTo(commentForm);
    
    var buttonDiv = $("<div>",{
      "class" : "container",
    }).appendTo(commentForm);

    commentForm.append('<input type="hidden" name="csrfmiddlewaretoken" value=' + csrftoken + '>');
    buttonDiv.append('<input type="submit" value="comment" class="btn btn-sm btn-outline-info">');

    $('#comment_'+post_pk).toggle();
  }
  function updateComments(data){
    
    for(var i = 0; i < data.comments.length; i++) {
      var comment_uername = data.comments[i]['username'];
      var post_pk         = data.comments[i]['post_pk'];
      var comment_time    = data.comments[i]['time'];
      var comment_pk      = data.comments[i]['comment_pk'];
      
      var comment_div     = $("<div>",{
         "id"    : "commentarea_"+comment_pk,
         "class" : "card",
      }).appendTo("#commentarea_"+post_pk);
      
      var commentheader = $("<div>",{
        "class" : "card-header",
        "text"  : "Comment",
      }).appendTo(comment_div);
      
      var commentbody   = $("<div>",{
        "class" : "card-body",
      }).appendTo(comment_div);
      
      var commenttext   = $("<p>",{
        "text": data.comments[i]['comment'],
      }).appendTo(commentbody);
      
      if(data.comments[i]['image']) {
        var UserProfileImg = $("<img>",{
          "src" : "../photo/" + comment_uername,
          'width':"30px",
          "height": '30px',
        }).appendTo(commentbody);
      }
      var commentuser   = $("<a/>",{
        "href"  : "../profile/" + comment_uername,
        "class" : "username",
        "text"  : comment_uername,
      }).appendTo(commentbody);
      
      var commenttime   = $("<span>",{
        "text": data.comments[i]['time'],
      }).appendTo(commentbody); 
    } 

    // Update timestamp
    $('#timestamp').val(data.timestamp);

  }

}); // End of $(document).ready