$(document).ready(function(){
	function update_dashboard() {
		var pk = $("#local_pk").val()
		$.ajax({
			type: "GET",
			url: "/gui_dashboard/" + 1,
			data: {bk_color: $("#bk_color").val()}
		}).done(function(tr_lookup){
			$("#body_dashboard").empty();
			$("#body_dashboard").append(tr_lookup);
			setTimeout(update_dashboard, 1000);
		});
	}

	update_dashboard();
});
