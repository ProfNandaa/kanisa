$(function() {
    $("#schedule-weeks-events").mouseover(function() {
        $(".noautoschedule").fadeTo('fast', 0.3);
      }).mouseout(function(){
        $(".noautoschedule").fadeTo('fast', 1.0);
    });
});
