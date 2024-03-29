
/**
    @param {Object} group
	@param {string} method "tdm" or "jws" or "none"
*/
VPLTeacherTools.makeVPLURL = function (group, method) {
	var url0 = "/vpl/vpl.html?ui=$VPLUIURI&uilanguage=$VPLLANGUAGE&server=ws://" + document.location.hostname + ":$TTSERVERWSPORT/";
	var tdmURL = VPLTeacherTools.getHashOption("w") || "ws://" + document.location.hostname + ":8597/";
	var jwsURL = VPLTeacherTools.getHashOption("w") || "ws://" + document.location.hostname + ":8002/";
	var url = url0 +
		"&session=" + group.session_id +
		(group.students ? "&user=" + encodeURIComponent(group.students.join(", ")) : "") +
		(group.robot === "!sim" ? "&robot=sim"
			: group.robot === "!thymio" ? "&robot=thymio"
			: group.robot
				? method === "tdm" ? "&robot=thymio-tdm#w=" + tdmURL + "&uuid=" + group.robot
					: method === "jws" ? "&robot=thymio-jws#w=" + jwsURL + "&uuid=" + group.robot
					: ""
			: "");
	return url;
};
