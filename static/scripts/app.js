$(document).ready(function(){
  window.fbAsyncInit = function() {
    FB.init({
      appId      : '820584261317849',
      xfbml      : true,
      version    : 'v2.2'
    });
  };

  $('#fb-login').click(function(){
    FB.login(function(response){
      if (response.status === 'connected') {
        register_new_user(response);
      }
    });
  });

  function register_new_user(response){
    FB.api('/me', function(data){
      console.log(JSON.stringify(data));
      $.ajax({
        url: "/facebook_auth",
        type: "POST",
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: function(){
          window.location.replace("/");
        },
        error: function(){
          $("#alert").show();
        }
      })
    })
  }
});