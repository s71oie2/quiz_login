/**
 * Created by shin on 2019-05-25.
 */
function needLogin() {
    var con_test = confirm("로그인이 필요합니다.");
    if(con_test == true){
      location.href ="user/login"
    }
}
