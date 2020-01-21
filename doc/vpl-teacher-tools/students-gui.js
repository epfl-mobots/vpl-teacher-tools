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

function fillStudentTable(studentArray, students) {
	clearTable("students");
	var table = document.getElementById("students");

	function addRow(studentName, groupName) {

		function selectRow() {
			students.selectStudent(studentName);
			fillStudentTable(studentArray, students);
		}

		var tr = document.createElement("tr");

		// drag student name
		tr.draggable = true;
		tr.addEventListener("dragstart", function (ev) {
			ev.dataTransfer.setData("text/plain", studentName);
			ev.dataTransfer.setDragImage(tr.getElementsByTagName("td")[0], 0, 0);
			ev.dataTransfer.effectAllowed = "copy";
		});

		var td = document.createElement("td");
		td.textContent = studentName;
		// td.addEventListener("click", selectRow, false);
		td.className = students.isStudentSelected(studentName) ? "rect selected" : "rect";
		tr.appendChild(td);

		td = document.createElement("td");
		var btn = document.createElement("button");
		btn.textContent = VPLTeacherTools.translate("remove");
		btn.addEventListener("click", function () {
			students.removeStudent(studentName);
		}, false);
		td.appendChild(btn);
		tr.appendChild(td);

		table.appendChild(tr);
	}

	studentArray.forEach(function (student) {
		addRow(student.name, student.group);
	});

	// row for adding a new student
	var tr = document.createElement("tr");

	var td = document.createElement("td");
	td.className = "rect";
	var fldStudentName = document.createElement("input");
	var btnAddStudent = document.createElement("button");
	btnAddStudent.disabled = true;
	fldStudentName.addEventListener("input", function () {
		btnAddStudent.disabled = !students.canAddStudent(fldStudentName.value);
	}, false);
	fldStudentName.addEventListener("change", function () {
		students.addStudent(fldStudentName.value);
	}, false);
	td.appendChild(fldStudentName);
	tr.appendChild(td);

	td = document.createElement("td");
	btnAddStudent.textContent = VPLTeacherTools.translate("add");
	btnAddStudent.addEventListener("click", function () {
		students.addStudent(fldStudentName.value);
	}, false);
	td.appendChild(btnAddStudent);
	tr.appendChild(td);

	table.appendChild(tr);

	fldStudentName.select();
	fldStudentName.focus();
}

window.addEventListener("load", function () {
	var students = new VPLTeacherTools.StudentManagement({
		onStudents: function (studentArray, students) {
    		fillStudentTable(studentArray, students);
		},
	});

	var btn;

	btn = document.getElementById("btn-import");
	btn.addEventListener("click", function () {
		var loadBox = new VPLTeacherTools.Load(function (file) {
			var names = VPLTeacherTools.convertFromCSV(file)
				.map(function (row) {
					return row[0];
				});
			students.addStudents(names);
		}, VPLTeacherTools.translate("Import Pupil Names"), ".txt,.csv");
	}, false);

	btn = document.getElementById("btn-export");
	btn.addEventListener("click", function () {
		// make list of students, one name per line
		var csv = students.students.map(function (student) {
			return student.name + "\n";
		}).join("");
		VPLTeacherTools.downloadText(csv, "pupils.csv", "text/csv");
	}, false);

}, false);
