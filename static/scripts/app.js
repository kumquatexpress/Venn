window.fbAsyncInit = function() {
  FB.init({
    appId      : '820584261317849',
    xfbml      : true,
    version    : 'v2.2'
  });
};

function statusChangeCallback(response) {
  if (response.status === 'connected') {
    register_new_user(response);
  }
}

$('.fb-login-button').click(function(){
  FB.getLoginStatus(function(response) {
    statusChangeCallback(response);
  });
});

FB.getLoginStatus(function(response) {
  statusChangeCallback(response);
});

function register_new_user(response){
  FB.api('/me', function(data){
    console.log(JSON.stringify(data));
  })
}