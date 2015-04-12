$("#submit").on('click', function(e) {
	e.preventDefault();
	e.stopPropagation();
	$("#message").text("");

	var ajaxData = {
		domain: $("#domain").val(),
		section_selector: $("#section_selector").val(),
		comment_selector: $("#comment_selector").val(),
		template: $("#template").val(),
		category: $("#category").val(),
	};

	$.ajax({
		method: "POST",
		url: "/drtc/profile",
		data: ajaxData,
	})
	.done(function(data) {
		$("#message").text(data);
	});
})