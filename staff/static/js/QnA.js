// summernote 에디터 설정
$(document).ready(function() {
     $('#summernote').summernote({
         height: 300,
         minHeight: null,
         maxHeight: null
         // airMode: true  // 테두리가 사라짐

     });
    // 5.28 소이
    $(this).summernote("insertImage", url);
});

// 5.28 소이
//노트 쓰기 금지
$(document).ready(function(){
    // 안 써지게 막음
    $('.note-editable').attr('contenteditable', false)
});

// 질문
$(function(){
    $("tr[id^='flip_']").on("click", function(){
      var $parent = $(this).closest("tr");
      $parent.siblings().next("tr.panel").slideUp("fast");
      $(this).next("tr.panel").slideToggle("fast");
     });
});
//답변
$(function(){
    $("tr[id^='flip_']").on("click", function(){
      var $parent = $(this).closest("tr");
      $parent.siblings().next("tr.panel").next("tr.apanel").slideUp("fast");
      $(this).next("tr.panel").next("tr.apanel").slideToggle("fast");
     });
});
// 로그인 알림창
function needLogin() {
    var con_test = confirm("로그인이 필요합니다.");
    if(con_test){
      location.href ='/user/login/'
    }
}