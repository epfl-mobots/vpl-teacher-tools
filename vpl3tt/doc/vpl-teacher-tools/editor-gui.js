var client = null;

function resizeEditor() {
	var textarea = document.getElementById("ta");
	var textareaRect = textarea.getBoundingClientRect();
	var availableHeight = window.innerHeight;
	var containerHeight = textarea.parentElement.parentElement.parentElement.parentElement.getBoundingClientRect().height;
	var textareaHeight = availableHeight - (containerHeight - textareaRect.height) - 10;
	textarea.style.height = textareaHeight + "px";
}

window.addEventListener("DOMContentLoaded", function () {
	client = new VPLTeacherTools.HTTPClient();

	var options = JSON.parse(sessionStorage.getItem("options"));
	var filename = options["initialFileName"];
	var fileContent = sessionStorage.getItem("initialFileContent");

	var title = document.getElementById("title");
	title.textContent = filename;

	var textarea = document.getElementById("ta");
	textarea.value = fileContent;

	window.addEventListener("resize", resizeEditor, false);

	resizeEditor();
}, false);

function saveContent() {
	var options = JSON.parse(sessionStorage.getItem("options") || "{}");
	var readOnly = options ? options["readOnly"] === true : false;
	var fileId = options ? options["fileId"] : null;
	var fileContentOrig = sessionStorage.getItem("initialFileContent");
	var textarea = document.getElementById("ta");
	fileContent = textarea.value;
	if (!readOnly && fileId != null && fileContent !== fileContentOrig) {
		client.updateFile(fileId, fileContent, {asBeacon: true});
	}
}

window.addEventListener("beforeunload", saveContent, false);

// for modern browsers
window.addEventListener("visibilitychange ", function () {
	if (document.visibilityState !== "visible") {
		saveContent();
	}
});

// for Safari
window.addEventListener("pagehide", saveContent, false);
