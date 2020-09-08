function clearChildren(id) {
	var el = document.getElementById(id);
	while (el.firstElementChild) {
		el.removeChild(el.firstElementChild);
	}
}

function addLabels(id, labels) {
	var table = document.getElementById(id);
	var tr = document.createElement("tr");
	labels.forEach(function (label) {
		var th = document.createElement("th");
		th.textContent = label;
		tr.appendChild(th);
	});
	table.appendChild(tr);
}

/*
Drag-and-drop data:
"S/" + student name: item in the pupil table (to add to a group)
"G/" + student name: item in the group table (to move to another group or remove)
"R/" + robot name: item in the robot table (to add to a group to make an association)
*/

function fillRobotTable(robotArray, pairing) {
	if (!pairing.noRedraw) {
		clearChildren("robots");
		var table = document.getElementById("robots");

		robotArray.forEach(function (robot) {
			var tr = document.createElement("tr");

			var td = document.createElement("td");
			td.textContent = robot.niceName;
			td.addEventListener("click", function () {
				if (pairing.selectByRobotName(robot.name)) {
					pairing.updateGroups();
				}
			});
			td.className = "rect";

			// drag robot name
			td.draggable = true;
			td.addEventListener("dragstart", function (ev) {
				ev.dataTransfer.setData("text/plain", "R/" + robot.name);
				ev.dataTransfer.setDragImage(tr.getElementsByTagName("td")[0], 0, 0);
				ev.dataTransfer.effectAllowed = "copy";
			});

			tr.appendChild(td);

			td = document.createElement("td");
			td.textContent = !robot.multiple && pairing.findGroupByRobotName(robot.name) ? "\u2713" : "";	// checkmark
			tr.appendChild(td);

			td = document.createElement("td");
			if (robot.hasFlash()) {
				var btn = document.createElement("button");
				btn.textContent = "flash";
				btn.disabled = !robot.canFlash();
				btn.addEventListener("mousedown", function () {
					pairing.noRedraw = true;
					robot.flash(true);
					pairing.noRedraw = false;
				}, false);
				btn.addEventListener("mouseup", function () {
					pairing.noRedraw = true;
					robot.flash(false);
					pairing.noRedraw = false;
				}, false);
				td.appendChild(btn);
			}
			tr.appendChild(td);

			table.appendChild(tr);
		});
	}
}

function fillStudentTable(studentArray, pairing) {
	clearChildren("students");
	addLabels("students",
		VPLTeacherTools.translateArray(["Name", "Class"]));

	var table = document.getElementById("students");

	function addRow(studentName, studentClass, groupId) {

		var tr = document.createElement("tr");

		// drag student name
		tr.draggable = true;
		tr.addEventListener("dragstart", function (ev) {
			ev.dataTransfer.setData("text/plain", "S/" + studentName);
			ev.dataTransfer.setDragImage(tr.getElementsByTagName("td")[0], 0, 0);
			ev.dataTransfer.effectAllowed = "copy";
		});

		var td = document.createElement("td");
		td.textContent = studentName;
		td.className = "rect";
		td.addEventListener("click", function () {
			if (pairing.selectByStudentName(studentName)) {
				pairing.updateGroups();
			}
		}, false);
		tr.appendChild(td);

		td = document.createElement("td");
		td.textContent = studentClass;
		td.className = "rect";
		td.addEventListener("click", function () {
			if (pairing.selectByStudentName(studentName)) {
				pairing.updateGroups();
			}
		}, false);
		tr.appendChild(td);

		td = document.createElement("td");
		td.textContent = groupId ? "\u2713" : "";	// checkmark
		tr.appendChild(td);

		table.appendChild(tr);
	}

    if (studentArray.length > 0) {
        studentArray.forEach(function (student) {
            addRow(student.name, student["class"], student.group_id);
        });
        document.getElementById("student-help").style.display = "block";
        document.getElementById("nostudent-help").style.display = "none";
    } else {
        document.getElementById("student-help").style.display = "none";
        document.getElementById("nostudent-help").style.display = "block";
    }
}

function qrCodeSize() {
	var minViewportSize = window.visualViewport ?
		Math.min(window.visualViewport.width,
			window.visualViewport.height)
		: document.documentElement.clientWidth ?
		Math.min(document.documentElement.clientWidth,
			document.documentElement.clientHeight)
		: window.innerWidth ?
		Math.min(window.innerWidth, window.innerHeight)
		: 200;
	var size = Math.min(Math.floor(minViewportSize * 0.8), 200);
	return size;
}

function fillGroupTable(groupArray, pairing) {

	function checkDragType(ev) {
		if (ev.dataTransfer.types.includes("text/plain")) {
			ev.preventDefault();
			return false;
		}
		return true;
	}

	clearChildren("groups");
	var table = document.getElementById("groups");

	groupArray.forEach(function (group) {
		function select() {
			pairing.selectGroup(group.group_id);
			fillGroupTable(groupArray, pairing);
		}

		if (group.students && group.students.length > 0) {
			var tr = document.createElement("tr");

			var td = document.createElement("td");
			td.className = pairing.isGroupSelected(group.group_id) ? "rect selected" : "rect";
			group.students.forEach(function (studentName, i) {
				var span = document.createElement("span");
				span.className = "rect";
				span.textContent = studentName;

				// drag student name
				span.draggable = true;
				span.addEventListener("dragstart", function (ev) {
					ev.dataTransfer.setData("text/plain", "G/" + studentName);
					ev.dataTransfer.effectAllowed = "move";
				});

				td.appendChild(span);
			});
			td.addEventListener("click", select);

			// drop student or robot name
			tr.addEventListener("dragenter", checkDragType);
			tr.addEventListener("dragover", checkDragType);
			tr.addEventListener("drop", function (ev) {
				ev.stopPropagation();
				ev.preventDefault();
				var data = ev.dataTransfer.getData("text/plain");
				if (data && /^[SG]\//.test(data)) {
					ev.stopPropagation();
					var studentName = data.slice(2);
					pairing.addStudentToGroup(studentName, group.group_id, true);
				} else if (data && /^R\//.test(data)) {
					ev.stopPropagation();
					var robotName = data.slice(2);
					pairing.beginSession(robotName, group.group_id);
				}
			});

			tr.appendChild(td);

			// robot
			td = document.createElement("td");
			tr.appendChild(td);
			if (group.pair) {
				td.className = pairing.isGroupSelected(group.group_id) ? "rect selected" : "rect";
				td.textContent = (/^\{/.test(group.pair.robot) ? "Thymio II" : group.pair.robot.replace(/[()]/g, "")) + " ";
				var rmBtn = document.createElement("span");
				rmBtn.textContent = "\u2716";	// heavy multiplication mark
				rmBtn.style.cursor = "pointer";
				rmBtn.addEventListener("click", function (ev) {
					ev.stopPropagation();
					pairing.endSession(group.pair.session_id);
				}, false);
				td.appendChild(rmBtn);
				td.addEventListener("click", select);

				var robot = pairing.getRobot(group.pair.robot);
				if (robot && robot.hasFlash()) {
					td = document.createElement("td");
					var btn = document.createElement("button");
					btn.textContent = "flash";
					btn.disabled = !robot.canFlash();
					btn.addEventListener("mousedown", function () {
						pairing.noRedraw = true;
						robot.flash(true);
						pairing.noRedraw = false;
					}, false);
					btn.addEventListener("mouseup", function () {
						pairing.noRedraw = true;
						robot.flash(false);
						pairing.noRedraw = false;
					}, false);
					td.appendChild(btn);
					tr.appendChild(td);
				}
			}

			table.appendChild(tr);
		}
	});

	// row to create new group
	var tr = document.createElement("tr");
	var td = document.createElement("td");
	td.className = "rect";
	td.textContent = "\u00a0";

	// drop student name
	tr.addEventListener("dragenter", checkDragType);
	tr.addEventListener("dragover", checkDragType);
	tr.addEventListener("drop", function (ev) {
		ev.stopPropagation();
		ev.preventDefault();
		var data = ev.dataTransfer.getData("text/plain");
		if (data && /^[SG]\//.test(data)) {
			var studentName = data.slice(2);
			pairing.addGroup(studentName);
		}
	}, false);

	tr.appendChild(td);
	table.appendChild(tr);

	// drop student name outside a group -> delete
	var body = document.body;
	body.addEventListener("dragenter", checkDragType);
	body.addEventListener("dragover", checkDragType);
	body.addEventListener("drop", function (ev) {
		ev.stopPropagation();
		ev.preventDefault();
		var studentName = ev.dataTransfer.getData("text/plain");
		if (studentName.slice(0, 2) === "G/") {
			studentName = studentName.slice(2);
			var groupId = pairing.groupForStudent(studentName);
			if (groupId) {
				pairing.removeStudentFromGroup(studentName, groupId, true);
				pairing.selectGroup(groupId);
			}
		}
	}, false);

	clearChildren("info");
	var selectedGroup = pairing.getSelectedGroup();
	if (selectedGroup && selectedGroup.robot) {
		var div = document.createElement("div");
		var p = document.createElement("p");
		var groupDescr = selectedGroup.students.length > 0
			? selectedGroup.students.join(", ")
			: selectedGroup.group_id;
		p.textContent = VPLTeacherTools.translate("Group") + ": " + groupDescr;
		div.appendChild(p);
		p = document.createElement("p");
		p.style.overflowWrap = "break-word";
		var a = document.createElement("a");
		a.setAttribute("class", "url");
		a.setAttribute("target", "_blank");
		a.setAttribute("rel", "noopener");
		p.appendChild(a);
		div.appendChild(p);
		var toolURL = VPLTeacherTools.makeVPLURL(selectedGroup, "$BRIDGE");
		var url = document.location.origin + toolURL;

		if (window.QRCode) {
			var qrdiv = document.createElement("div");
			div.appendChild(qrdiv);
			var size = qrCodeSize();
			var qrcode = new window.QRCode(qrdiv,
				{
					text: url,
					width: size,
					height: size,
					correctLevel: QRCode.CorrectLevel.L
				});
            if ($SHORTENURL) {
    			pairing.shortenURL(url, function (shortenedURL) {
    				a.textContent = shortenedURL;
    				a.setAttribute("href", shortenedURL);
    				while (qrdiv.firstElementChild) {
    					qrdiv.removeChild(qrdiv.firstElementChild);
    				}
    				qrcode = new window.QRCode(qrdiv,
    					{
    						text: shortenedURL,
    						width: size,
    						height: size,
    						correctLevel: QRCode.CorrectLevel.L
    					});
    			});
            } else {
				a.textContent = url;
				a.setAttribute("href", url);
			}
		} else {
            if ($SHORTENURL) {
    			pairing.shortenURL(url, function (shortenedURL) {
    				a.textContent = shortenedURL;
    			});
            } else {
				a.textContent = url;
				a.setAttribute("href", url);
			}
		}
		document.getElementById("info").appendChild(div);
	}
}

window.addEventListener("load", function () {
	var useTDM = "$BRIDGE" === "tdm";
	var useJWS = "$BRIDGE" === "jws";
	var tdmURL = VPLTeacherTools.getHashOption("w") || "ws://" + document.location.hostname + ":8597/";
	var jwsURL = VPLTeacherTools.getHashOption("w") || "ws://" + document.location.hostname + ":8002/";
	var url0 = "/vpl/vpl.html?ui=ui/classic/ui.json&uilanguage=$LANGUAGE&server=ws://" + document.location.hostname + ":8001/";
	var pairing = new VPLTeacherTools.Pairing({
		tdmURL: useTDM ? tdmURL : null,
		jwsURL: useJWS ? jwsURL : null,
		onRobots: function (robotArray, pairing) {
    		fillRobotTable(robotArray, pairing);
		},
		robotLaunchURL: function (group) {
			return url0 +
				"&robot=" + (useJWS ? "thymio-jws" : "thymio-tdm") +
				"&session=" + group.pair.session_id +
				(group.students ? "&user=" + encodeURIComponent(group.students.join(", ")) : "") +
				"#w=" + (useJWS ? jwsURL : tdmURL) + "&uuid=" + group.pair.robot;
		},
		nonRobots: [
			{
				name: VPLTeacherTools.translate("(simulator)"),
				niceName: VPLTeacherTools.translate("simulator"),
				launchURL: function (group) {
					// set user to comma-separated users if they exist
					return url0 + "&robot=sim&session=" + group.pair.session_id +
						(group.students ? "&user=" + encodeURIComponent(group.students.join(", ")) : "");
				}
			},
			{
				name: VPLTeacherTools.translate("(pupil local bridge)"),
				niceName: VPLTeacherTools.translate("pupil local bridge"),
				launchURL: function (group) {
					// set user to comma-separated users if they exist
					return url0 + "&robot=thymio&session=" + group.pair.session_id +
						(group.students ? "&user=" + encodeURIComponent(group.students.join(", ")) : "");
				}
			}
		],
		nonRobotNameMapping: {
			"!sim": VPLTeacherTools.translate("(simulator)"),
			"!thymio": VPLTeacherTools.translate("(pupil local bridge)")
		},
		onStudents: function (studentArray) {
    		fillStudentTable(studentArray, pairing);
		},
		onClasses: function (classes, currentClass) {
			// fill class filter
			var selFilterClass = document.getElementById("sel-filter-class");

			while (selFilterClass.firstElementChild) {
				selFilterClass.removeChild(selFilterClass.firstElementChild);
			}
			classes.forEach(function (cl) {
				var option = document.createElement("option");
				option.textContent = cl;
				if (cl === currentClass) {
					option.selected = true;
				}
				selFilterClass.appendChild(option);
			});
			var option = document.createElement("option");
			option.textContent = VPLTeacherTools.translate("All classes");
			if (currentClass === null) {
				option.selected = true;
			}
			selFilterClass.appendChild(option);
		},
		onGroups: function (groupArray) {
			fillGroupTable(groupArray, pairing);
		},
		nonGroups: [
			"(teacher)"
		]
	});

	var urlLogin = document.location.href.replace(/^(.*\/\/[^\/]*)\/.*$/, "$1");
	var aLogin = document.getElementById("login");
	aLogin.textContent = urlLogin;
	aLogin.href = urlLogin;
	if (window.QRCode && $LOGINQRCODE) {
		var qrdiv = document.createElement("div");
		document.getElementById("loginqrcode").appendChild(qrdiv);
		var size = qrCodeSize();
		var qrcode = new window.QRCode(qrdiv,
			{
				text: urlLogin,
				width: size,
				height: size,
				correctLevel: QRCode.CorrectLevel.L
			});
	}

	// class filter
	var selFilterClass = document.getElementById("sel-filter-class");
	selFilterClass.addEventListener("change", function () {
		var filterClass = selFilterClass.selectedIndex === selFilterClass.options.length - 1
			? null
			: selFilterClass.options[selFilterClass.selectedIndex].value;
		pairing.setClass(filterClass);
		pairing.updateStudents();
	}, false);

	// show which connection method is used
	document.getElementById("tdm-msg").style.display = useTDM ? "block" : "none";
	document.getElementById("jws-msg").style.display = useJWS ? "block" : "none";

}, false);
