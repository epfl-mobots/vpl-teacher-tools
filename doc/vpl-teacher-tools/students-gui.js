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
	var fldStudentName;

	function addRow(studentName, studentClass) {

		var tr = document.createElement("tr");
		var td = document.createElement("td");
		td.className = "rect";

		if (studentName === students.editedStudent) {
			var btnAcceptEdit;
			fldStudentName = document.createElement("input");
			fldStudentName.value = studentName;
			fldStudentName.addEventListener("input", function () {
				btnAcceptEdit.disabled = !students.canAddStudent(fldStudentName.value);
			}, false);
			fldStudentName.addEventListener("keyup", function (event) {
				if (event.key === "Enter") {
					event.preventDefault();
					students.acceptEditStudent(fldStudentName.value, fldStudentClass.value);
				} else if (event.key === "Escape") {
					event.preventDefault();
					students.cancelEditStudent();
				}
			}, false);
			td.appendChild(fldStudentName);
			tr.appendChild(td);

			td = document.createElement("td");
			var fldStudentClass = document.createElement("input");
			fldStudentClass.value = studentClass;
			fldStudentClass.addEventListener("keyup", function (event) {
				if (event.key === "Enter") {
					event.preventDefault();
					students.acceptEditStudent(fldStudentName.value, fldStudentClass.value);
				} else if (event.key === "Escape") {
					event.preventDefault();
					students.cancelEditStudent();
				}
			}, false);
			td.appendChild(fldStudentClass);
			tr.appendChild(td);

			td = document.createElement("td");
			var btnCancelEdit = document.createElement("button");
			btnCancelEdit.textContent = VPLTeacherTools.translate("cancel");
			btnCancelEdit.addEventListener("click", function () {
				students.cancelEditStudent();
			}, false);
			td.appendChild(btnCancelEdit);
			tr.appendChild(td);

			td = document.createElement("td");
			btnAcceptEdit = document.createElement("button");
			btnAcceptEdit.textContent = VPLTeacherTools.translate("OK");
			btnAcceptEdit.addEventListener("click", function () {
				students.acceptEditStudent(fldStudentName.value, fldStudentClass.value);
			}, false);
			td.appendChild(btnAcceptEdit);
			tr.appendChild(td);
		} else {
			td.textContent = studentName;
			tr.appendChild(td);

			td = document.createElement("td");
			td.textContent = studentClass;
			td.className = "rect";
			tr.appendChild(td);

			if (!students.editedStudent) {
				td = document.createElement("td");
				var btn = document.createElement("button");
				btn.textContent = VPLTeacherTools.translate("edit");
				btn.addEventListener("click", function () {
					students.editStudent(studentName);
				}, false);
				td.appendChild(btn);
				tr.appendChild(td);

				td = document.createElement("td");
				var btn = document.createElement("button");
				btn.textContent = VPLTeacherTools.translate("remove");
				btn.addEventListener("click", function () {
					students.removeStudent(studentName);
				}, false);
				td.appendChild(btn);
				tr.appendChild(td);
			}
		}

		table.appendChild(tr);
	}

	studentArray.forEach(function (student) {
		addRow(student.name, student["class"]);
	});

	// row for adding a new student
	if (!students.editedStudent) {
		var tr = document.createElement("tr");

		var td = document.createElement("td");
		td.className = "rect";
		fldStudentName = document.createElement("input");
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
	}

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
