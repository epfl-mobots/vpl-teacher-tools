window["vplConfig"] = {
	"ignoredCommands": [
		"vpl:flash"
	]
};

window["vplStorageGetFunction"] = function (filename, fun) {

	var progJSON = sessionStorage.getItem("initialFileContent");
	var options = JSON.parse(sessionStorage.getItem("options") || "{}");
	filename = options && options["initialFileName"] || filename;
	var readOnly = options ? options["readOnly"] === true : false;
	var customizationMode = options ? options["customizationMode"] === true : false;
	// change toolbars
	var prog = progJSON ? JSON.parse(progJSON) : {};
	// disable some buttons in addition to the ones specified in program
	prog["disabledUI"] = [
		"src:language",
		"vpl:new",
		"vpl:load",
		"vpl:text",
		"vpl:sim",
		"sim:vpl",
		"sim:text",
		"sim:teacher"
	]
		.concat($ADVANCEDSIMFEATURES ? [] : ["sim:noise", "sim:map-kind"])
		.reduce(function (acc, val) {
			return acc.indexOf(val) < 0 ? acc.concat(val) : acc;
		}, prog["disabledUI"] || []);
	progJSON = JSON.stringify(prog);

	fun(progJSON,
		{
			"filename": filename,
			"readOnly": readOnly,
			"customizationMode": customizationMode
		});
	sessionStorage.setItem("initialUISettings", window["vplGetUIAsJSON"]());
};

window.addEventListener("load", function () {
	var vplTab = document.getElementById("tab-vpl");
	var simTab = document.getElementById("tab-sim");
	vplTab.addEventListener("click", function () {
		vplTab.setAttribute("class", "current");
		simTab.setAttribute("class", "");
		window["vplApp"].setView(["vpl"]);
	}, false);
	simTab.addEventListener("click", function () {
		vplTab.setAttribute("class", "");
		simTab.setAttribute("class", "current");
		window["vplApp"].setView(["sim"]);
	}, false);
}, false);

window.addEventListener("beforeunload", function () {
	var options = JSON.parse(sessionStorage.getItem("options") || "{}");
	var readOnly = options ? options["readOnly"] === true : false;
	var customizationMode = options ? options["customizationMode"] === true : false;
	var fileId = options ? options["fileId"] : null;
	if (!readOnly && fileId != null &&
		(window["vplIsProgramChanged"]() ||
			window["vplGetUIAsJSON"]() !== sessionStorage.getItem("initialUISettings"))) {
		var json = window["vplGetProgramAsJSON"](customizationMode);
		console.info(json);
		var client = new VPLTeacherTools.HTTPClient();
		client.updateFile(fileId, json, {asBeacon: true});
	}
}, false);
