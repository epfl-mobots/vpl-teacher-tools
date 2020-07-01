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
	clearTable("students",
		VPLTeacherTools.translateArray(["Name", "Class"]));
	var table = document.getElementById("students");

	function addRow(studentName, studentClass) {

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
		td.textContent = studentClass;
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
		addRow(student.name, student["class"]);
	});

	// row for adding a new student
	var tr = document.createElement("tr");

	var td = document.createElement("td");
	td.className = "rect";
	var fldStudentName = document.createElement("input");
	var fldStudentClass = document.createElement("input");
	var btnAddStudent = document.createElement("button");
	btnAddStudent.disabled = true;
	fldStudentName.addEventListener("input", function () {
		btnAddStudent.disabled = !students.canAddStudent(fldStudentName.value);
	}, false);
	fldStudentName.addEventListener("keypress", function (event) {
		if (event.keyCode === 13) {
			event.preventDefault();
			students.addStudent(fldStudentName.value, fldStudentClass.value);
		}
	}, false);
	td.appendChild(fldStudentName);
	tr.appendChild(td);

	td = document.createElement("td");
	fldStudentClass.addEventListener("keypress", function () {
		if (event.keyCode === 13) {
			event.preventDefault();
			students.addStudent(fldStudentName.value, fldStudentClass.value);
		}
	}, false);
	td.appendChild(fldStudentClass);
	tr.appendChild(td);

	td = document.createElement("td");
	btnAddStudent.textContent = VPLTeacherTools.translate("add");
	btnAddStudent.addEventListener("click", function () {
		students.addStudent(fldStudentName.value, fldStudentClass.value);
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
			var table = VPLTeacherTools.convertFromCSV(file);
			// check if 1st col is completely empty
			var col = 1;
			for (var i = 0; i < table.length; i++) {
				if (table[i].length > 0 && table[i][0]) {
					col = 0;
					break;
				}
			}
			// pick non-empty names
			var names = [];
			var classes = [];
			for (var i = 0; i < table.length; i++) {
				if (table[i][col]) {
					names.push(table[i][col]);
					classes.push(table[i][col + 1]);
				}
			}
			students.addStudents(names, classes);
		}, VPLTeacherTools.translate("Import Pupil Names"), ".txt,.csv");
	}, false);

	btn = document.getElementById("btn-export");
	btn.addEventListener("click", function () {
		// make list of students, one name per line
		var csv = students.students.map(function (student) {
			return student.name + "\t" + student["class"] + "\n";
		}).join("");
		VPLTeacherTools.downloadText(csv, "pupils.csv", "text/csv");
	}, false);

	var vFilterClass = document.getElementById("v-filter-class");
	vFilterClass.addEventListener("change", function () {
		students.filterClass = vFilterClass.value;
		students.updateStudents();
	}, false);

}, false);
