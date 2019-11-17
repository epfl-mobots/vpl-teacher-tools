
/**
    @constructor
    @param {Object} options
*/
VPLTeacherTools.makeVPLURL = function (group) {
	var url0 = "/vpl/vpl.html?ui=ui/classic/ui.json&uilanguage=$LANGUAGE&server=ws://" + document.location.hostname + ":8001/";
	var tdmURL = VPLTeacherTools.getHashOption("w") || "ws://" + document.location.hostname + ":8597/";
	var url = url0 +
		"&session=" + group.session_id +
		(group.students ? "&user=" + encodeURIComponent(group.students.join(", ")) : "") +
		(group.robot[0] === "!" ? "&robot=sim"
			: group.robot ? "&robot=thymio-tdm#w=" + tdmURL + "&uuid=" + group.robot
			: "");
	return url;
};
