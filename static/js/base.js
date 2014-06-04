$(document).ready(function() {
	// Style navigation links

	var currentPage = window.location.pathname;
	$("a.nav-link[href='" + currentPage + "']").addClass("current");

});