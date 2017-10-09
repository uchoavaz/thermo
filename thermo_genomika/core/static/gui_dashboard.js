$(document).ready(function(){
	var snd = new Audio("/static/alert.wav");
	function update_dashboard() {
		var pk = $("#local_pk").val()
		var color = $("#bk_color").val()
		var time_now_str = $("#time_now").val()
		var horn = $("#horn").val()
		var play_horn = $("#play_horn").val()
		if (horn === "true") {
			snd.play()
			play_horn = 'true'
		}

		$.ajax({
			type: "GET",
			url: "/gui_dashboard/" + 1,
			data: {bk_color: color, time_now: time_now_str, horn:horn, play_horn:play_horn}
		}).done(function(tr_lookup){
			$("#body_dashboard").empty();
			$("#body_dashboard").append(tr_lookup);
			setTimeout(update_dashboard, 1000);
		});
	}

	update_dashboard();
});
