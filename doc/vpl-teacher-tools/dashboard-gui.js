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
	clearTable("groups");
	var table = document.getElementById("groups");

	sessionArray.forEach(function (session) {
		function select() {
			dashboard.selectGroup(session, null);
			fillGroupTable(sessionArray, dashboard);
		}

		var tr = document.createElement("tr");

		var td = document.createElement("td");
		td.textContent = session.students ? session.students.join(", ") : session.group;
		td.addEventListener("click", select);
		td.className = dashboard.isGroupSelected(session) ? "rect selected" : "rect";
		tr.appendChild(td);

		td = document.createElement("td");
		td.textContent = session.isConnected ? "\u260d" : "";
		tr.appendChild(td);

		if (session.lastVPLChangedLogEntry != null) {
			var time = session.lastVPLChangedLogEntry["time"].split(" ")[1];
			var hms = time.split(":").map(function (str) { return parseInt(str, 10); });
			var now = new Date();
			var elapsedSec = ((((now.getHours() * 60) + now.getMinutes()) * 60 + now.getSeconds() + 86400 -
				((hms[0] * 60) + hms[1]) * 60 + hms[2])) % 86400;
			var elapsedStr = elapsedSec < 60 ? elapsedSec.toString(10) + " sec"
 				: elapsedSec < 300 ? Math.floor(elapsedSec / 60).toString(10) + " min " +
					(elapsedSec % 60).toString(10) + " sec"
				: elapsedSec < 3600 ? Math.floor(elapsedSec / 60).toString(10) + " min"
				: elapsedSec < 18000 ? Math.floor(elapsedSec / 3600).toString(10) + " hr " +
					Math.floor(elapsedSec % 3600 / 60).toString(10) + " min"
				: Math.floor(elapsedSec / 3600).toString(10) + " hr";
			var lastVPLChangedData = JSON.parse(session.lastVPLChangedLogEntry["data"]);
			var details = [elapsedStr];
			if (lastVPLChangedData && lastVPLChangedData["nrules"] != undefined) {
				details = [
					elapsedStr,
					lastVPLChangedData["nrules"].toString(10) + "\u25ad",
					lastVPLChangedData["nblocks"].toString(10) + "\u25ab"
				];
			}
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
	clearTable("files-dashboard", VPLTeacherTools.translateArray(["Filename", "Default"]));
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

		var td = document.createElement("td");
		td.textContent = file.filename;
		tr.appendChild(td);

		td = document.createElement("td");
		if (/\.vpl3$/.test(file.filename)) {
			td.textContent = file["default"] ? "\u2612" : "\u2610";
			td.addEventListener("click", function () {
				dashboard.setDefaultFile(file.id);
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
	dashboard = new VPLTeacherTools.Dashboard("ws://" + document.location.hostname + ":8001/", {
		log: function (str) {
			document.getElementById("log").textContent += str + "\n";
		},
		onGroups: function (newSessions) {
			sessions = newSessions;
			fillGroupTable(sessions, dashboard);
		},
		onFiles: function (fileArray) {
			fillFileTable(fileArray, dashboard);
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
		"vpl:new",
		"vpl:run",
		"vpl:stop"
	].forEach(function (name) {
		document.getElementById(name).addEventListener("click", function () {
			dashboard.sendCommand(name);
		}, false);
	});

	document.getElementById("suspended").addEventListener("change", function () {
		dashboard.suspend(this.checked,
			"<p style='text-align: center;'>" +
				document.getElementById("suspended-text").value +
			"</p>");
	});

	document.getElementById("clear-log").addEventListener("click", function () {
		document.getElementById("log").textContent = "";
	}, false);
}, false);
