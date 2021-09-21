function clearChildren(id) {
	var el = document.getElementById(id);
	while (el.firstElementChild) {
		el.removeChild(el.firstElementChild);
	}
}

function fillGroupTable(groupArray, login) {

	clearChildren("groups");
	var table = document.getElementById("groups");

	groupArray.forEach(function (group) {
		if (group.students && group.students.length > 0) {
			var tr = document.createElement("tr");

			var td = document.createElement("td");
			td.className = "rect";
			group.students.forEach(function (studentName, i) {
				var span = document.createElement("span");
				span.className = "rect";
				span.textContent = studentName;
				td.appendChild(span);
			});

			tr.appendChild(td);

			if (group.is_connected) {
				td.className = "rect disabled"
			} else {
				tr.addEventListener("click", function () {
					login.launchVPL(group);
				});
			}

			table.appendChild(tr);
		}
	});
}

window.addEventListener("load", function () {
	var login = new VPLTeacherTools.Login({
		onGroups: function (groupArray) {
			fillGroupTable(groupArray, login);
		}
	});
}, false);
