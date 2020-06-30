var dashboard = null;

function clearTable(id, labels) {
	var table = document.getElementById(id);
	while (table.firstElementChild) {
		table.removeChild(table.firstElementChild);
	}
	if (labels) {
		var tr = document.createElement("tr");
		labels.forEach(function (label) {
			var th = document.createElement("th");
			th.textContent = label;
			tr.appendChild(th);
		});
		table.appendChild(tr);
	}
}

function fillGroupTable(sessionArray, dashboard) {
	clearTable("groups", VPLTeacherTools.translateArray(["", "T", "R", "Time (d)", "Filename", "#R", "#B", "Message"]));
	var table = document.getElementById("groups");

	sessionArray.forEach(function (session) {
		function select() {
			dashboard.selectGroup(session, null);
			fillGroupTable(sessionArray, dashboard);
		}

		var tr = document.createElement("tr");

		// group
		var td = document.createElement("td");
		td.textContent = session.students ? session.students.join(", ") : session.group;
		td.addEventListener("click", select);
		td.className = dashboard.isGroupSelected(session) ? "rect selected" : "rect";
		tr.appendChild(td);

		// connection to teacher (VPL server)
		td = document.createElement("td");
		td.textContent = session.isConnected ? "\u260d" : "";
		tr.appendChild(td);

		if (session.lastVPLChangedLogEntry != null) {
			var lastVPLChangedData = JSON.parse(session.lastVPLChangedLogEntry["data"]);

			// connection to robot
			td = document.createElement("td");
			td.textContent = lastVPLChangedData["robot"] ? "r" : "";
			tr.appendChild(td);

			// elapsed time
			td = document.createElement("td");
			var datetime = session.lastVPLChangedLogEntry["time"].split(" ");
			var ymd = datetime[0].split("-").map(function (str) { return parseInt(str, 10); });;
			var hms = datetime[1].split(":").map(function (str) { return parseInt(str, 10); });
			var dateLogEntry = new Date(ymd[0], ymd[1] - 1, ymd[2], hms[0], hms[1], hms[2]);
			var now = new Date();
			var elapsedSec = (now - dateLogEntry) / 1000;
			var elapsedStr = elapsedSec < 120 ? elapsedSec.toString(10) + " sec"
				: elapsedSec < 7200 ? Math.floor(elapsedSec / 60).toString(10) + " min"
				: elapsedSec < 172800 ? Math.floor(elapsedSec / 3600).toString(10) + " hr"
				: Math.floor(elapsedSec / 86400).toString(10) + " d";
			td.textContent = elapsedStr;
			tr.appendChild(td);

			// program
			if (lastVPLChangedData && lastVPLChangedData["nrules"] != undefined) {
				// filename
				td = document.createElement("td");
				if (lastVPLChangedData["filename"]) {
					var btn = document.createElement("button");
					btn.textContent = lastVPLChangedData["filename"];
					btn.addEventListener("click", function () {
						dashboard.openLastFile(session.group_id,
                            session.students ? session.students.join(", ") : session.group);
					}, false);
				    td.appendChild(btn);
				}
				tr.appendChild(td);

				details = [
					lastVPLChangedData["filename"] || "",
					lastVPLChangedData["nrules"].toString(10),
					lastVPLChangedData["nblocks"].toString(10)
				];
			}

			var details = [];
			if (lastVPLChangedData["error"]) {
				details.push("error: " + lastVPLChangedData["error"]);
			} else if (lastVPLChangedData["warning"]) {
				details.push("warning: " + lastVPLChangedData["warning"]);
			}
			details.forEach(function (str) {
				td = document.createElement("td");
				td.textContent = str;
				tr.appendChild(td);
			});
		}

		table.appendChild(tr);
	});
}

function fillFileTable(fileArray, dashboard) {
	clearTable("files-dashboard", VPLTeacherTools.translateArray(["", "Filename", "Default"]));
	var table = document.getElementById("files-dashboard");

	if (fileArray.length === 0) {
		var tr = document.createElement("tr");
		var td = document.createElement("td");
		td.textContent = "(none)";
		tr.appendChild(td);
		table.appendChild(tr);
		return;
	}

	fileArray.forEach(function (file) {
		var tr = document.createElement("tr");

		var suffix = VPLTeacherTools.FileBrowser.getFileSuffix(file.filename);
		var td = document.createElement("td");
		var fileIconURL = {"vpl3": "icon-file-vpl3.svg", "vpl3ui": "icon-file-vpl3ui.svg"}[suffix];
		if (fileIconURL) {
			var img = document.createElement("img");
			img.src = fileIconURL;
			td.appendChild(img);
		}
		tr.appendChild(td);

		var td = document.createElement("td");
		td.textContent = file.filename;
		tr.appendChild(td);

		td = document.createElement("td");
		if (/\.vpl3$/.test(file.filename)) {
			td.textContent = file["default"] ? "\u2612" : "\u2610";
			td.addEventListener("click", function () {
				dashboard.setDefaultProgram(file.id);
			}, false);
		}
		tr.appendChild(td);

		td = document.createElement("td");
		var btn = document.createElement("button");
		btn.textContent = "\u2197";
		btn.addEventListener("click", function () {
			dashboard.sendFileById(file.id);
		}, false);
		td.appendChild(btn);

		tr.appendChild(td);

		table.appendChild(tr);
	});
}

window.addEventListener("load", function () {
	var sessions = null;
	if (!$LOGDISPLAY) {
		document.getElementById("divlog").style.display = "none";
	}
	dashboard = new VPLTeacherTools.Dashboard("ws://" + document.location.hostname + ":8001/", {
		log: $LOGDISPLAY
			? function (str) {
				document.getElementById("log").textContent += str + "\n";
			}
			: function (str) {},
		onGroups: function (newSessions) {
			sessions = newSessions;
			fillGroupTable(sessions, dashboard);
		},
		onFiles: function (fileArray) {
			fillFileTable(fileArray, dashboard);
		},
		onOpen: function (file, readOnly) {
			var teacherFile = !file.owner || file.owner.length == 0;
			var options = {
				"initialFileName": file.filename,
				"fileId": teacherFile ? file.id : null,
				"readOnly": readOnly,
				"customizationMode": /\.vpl3ui/.test(file.filename)
			};
            sessionStorage.setItem("options", JSON.stringify(options));
            sessionStorage.setItem("initialFileContent", file.content);
			document.location = "vpl$LANGSUFFIX.html?robot=sim&uilanguage=$LANGUAGE" +
				(teacherFile ? "&role=teacher" : "") +
				(file.students ? "&user=" + encodeURIComponent(file.students.join(", ")) : "");
		}
	});
	setInterval(function () {
		if (sessions) {
			fillGroupTable(sessions, dashboard);
		}
	}, 5000);
	dashboard.onConnectionStateChanged = function (state) {
		document.getElementById("disconnected-msg").style.display = state ? "none" : "block";
	};
	dashboard.connect();

	[
		"vpl:stop"
	].forEach(function (name) {
		document.getElementById(name).addEventListener("click", function () {
			dashboard.sendCommand(name);
		}, false);
	});

	document.getElementById("suspended").addEventListener("change", function () {
		dashboard.suspend(this.checked,
			"<div style='display: table; height: 100%; width: 100%; overflow: hidden;'>" +
				"<div style='display: table-cell; vertical-align: middle;'>" +
					"<p style='text-align: center;'>" +
						document.getElementById("suspended-text").value +
					"</p>" +
				"</div>" +
			"</div>");
	});

	document.getElementById("clear-log").addEventListener("click", function () {
		document.getElementById("log").textContent = "";
	}, false);
}, false);
