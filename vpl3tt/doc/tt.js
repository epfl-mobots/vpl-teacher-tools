window.addEventListener("load", function () {
	sessionStorage.setItem("token", document.location.search.replace(/^.*?/, "").replace(/^.*=/, ""));
	var url = "vpl-teacher-tools/students.html";
	document.getElementsByTagName("a")[0].href = url;	// useless
	location = url;	// redirect
});
