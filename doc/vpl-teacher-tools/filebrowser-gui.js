function updateGUI(fileBrowser) {
	function enable(id, enabled) {
		document.getElementById(id).disabled = !enabled;
		document.getElementById(id).style.display = enabled ? "inline" : "none";
	}

	enable("btn-new", fileBrowser.canCreateProgramFile());
	enable("btn-get-conf", fileBrowser.canGetConfigFile());
	enable("btn-edit-teacher", fileBrowser.canEditTeacherFile());
	enable("btn-rename-teacher", fileBrowser.canRenameTeacherFile());
	enable("btn-move-teacher", fileBrowser.canMoveTeacherFile());
	enable("btn-duplicate-teacher", fileBrowser.canDuplicateTeacherFile());
	enable("btn-import-teacher", fileBrowser.canImportTeacherFile());
	enable("btn-export-teacher", fileBrowser.canExportTeacherFile());
	enable("btn-remove-teacher", fileBrowser.canDeleteTeacherFiles());
	enable("btn-view-st", fileBrowser.canViewStudentFile());
	enable("btn-export-st", fileBrowser.canExportStudentFile());
	enable("btn-remove-st", fileBrowser.canDeleteStudentFiles());
}

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

function fillFileTable(fileArray, fileBrowser, forStudents) {
	var tableId = forStudents ? "files-students" : "files-teacher";
	var table = document.getElementById(tableId);
	var renamedFilename = null;	// input element for renamed file name
	var movedSet = null;	// input element for moved file set
	if (fileArray.length > 0) {
		clearTable(tableId,
			VPLTeacherTools.translateArray(forStudents
				? ["", "Filename", "Set", "Students", "Time", "Size", "Submitted"]
				: ["", "Filename", "Set", "Time", "Size", "Dashboard", "Default"]));

		fileArray.forEach(function (file) {
			if (!file.renamed && !file.moved) {
				function select(ev) {
					fileBrowser.selectFile(forStudents, file.id,
						ev.ctrlKey || ev.metaKey, ev.shiftKey);
					if (renamedFilename) {
						// rename + refresh
						fileBrowser.renameTeacherFile(renamedFilename.value);
					} else if (movedSet) {
						// move + refresh
						fileBrowser.moveTeacherFile(movedSet.value);
					} else {
						// just refresh
						fileBrowser.refreshFiles();
					}
					ev.preventDefault();
				}
				function doubleclick(ev) {
					if (!(ev.ctrlKey || ev.metaKey || ev.shiftKey)) {
						fileBrowser.selectFile(forStudents, file.id, false, false);
						ev.preventDefault();
						fillFileTable(fileArray, fileBrowser, forStudents);
						fileBrowser.openFile(forStudents);
					}
				}
			}

			var suffix = VPLTeacherTools.FileBrowser.getFileSuffix(file.filename).toLowerCase();

			var tr = document.createElement("tr");

			// icon
			var td = document.createElement("td");
			var fileIconURL = VPLTeacherTools.FileBrowser.getFileIconURL(file.filename);
			if (fileIconURL) {
				var img = document.createElement("img");
				img.src = fileIconURL;
				td.appendChild(img);
				td.addEventListener("click", select, false);
				td.addEventListener("dblclick", doubleclick, false);
			}
			tr.appendChild(td);

			// filename
			td = document.createElement("td");
			if (file.renamed) {
				renamedFilename = document.createElement("input");
				renamedFilename.value = file.filename;
				renamedFilename.addEventListener("keydown", function (ev) {
					if (ev.key === "Escape") {
						file.renamed = false;
						fillFileTable(fileArray, fileBrowser, forStudents);
					} else if (ev.key === "Enter") {
						// "change" listener not called if value hasn't changed
						ev.stopPropagation();
						ev.preventDefault();
						fileBrowser.renameTeacherFile(renamedFilename.value);
					}
				}, false);
				td.appendChild(renamedFilename);
			} else {
				td.textContent = file.filename;
			}
			td.addEventListener("click", select, false);
			td.addEventListener("dblclick", doubleclick, false);
			td.className = fileBrowser.isFileSelected(forStudents, file.id) ? "selected" : "";
			tr.appendChild(td);

			// set
			td = document.createElement("td");
			if (file.moved) {
				movedSet = document.createElement("input");
				movedSet.value = file.tag;
				movedSet.addEventListener("keydown", function (ev) {
					if (ev.key === "Escape") {
						file.moved = false;
						fillFileTable(fileArray, fileBrowser, forStudents);
					} else if (ev.key === "Enter") {
						// "change" listener not called if value hasn't changed
						ev.stopPropagation();
						ev.preventDefault();
						fileBrowser.moveTeacherFile(movedSet.value);
					}
				}, false);
				td.appendChild(movedSet);
			} else {
				td.textContent = file.tag;
			}
			td.addEventListener("click", select, false);
			td.addEventListener("dblclick", doubleclick, false);
			td.className = fileBrowser.isFileSelected(forStudents, file.id) ? "selected" : "";
			tr.appendChild(td);

			if (forStudents) {
				// list of students
				td = document.createElement("td");
				td.textContent = file.students.join(", ");
				td.addEventListener("click", select, false);
				td.addEventListener("dblclick", doubleclick, false);
				td.className = fileBrowser.isFileSelected(forStudents, file.id) ? "selected" : "";
				tr.appendChild(td);
			}

			// time
			td = document.createElement("td");
			td.textContent = file.time || "";
			td.addEventListener("click", select, false);
			td.addEventListener("dblclick", doubleclick, false);
			td.className = fileBrowser.isFileSelected(forStudents, file.id) ? "selected" : "";
			tr.appendChild(td);

			// size
			td = document.createElement("td");
			td.textContent = file.size != null ? file.size.toString(10) : "";
			td.addEventListener("click", select, false);
			td.addEventListener("dblclick", doubleclick, false);
			td.className = fileBrowser.isFileSelected(forStudents, file.id) ? "selected" : "";
			tr.appendChild(td);

			if (forStudents) {
				// submitted
				td = document.createElement("td");
				td.textContent = file.submitted ? "\u2713" : "";
				td.addEventListener("click", select, false);
				td.addEventListener("dblclick", doubleclick, false);
				tr.appendChild(td);
			} else {
				// available in dashboard
				td = document.createElement("td");
				if (["vpl3", "vpl3ui", "txt", "html", "jpg", "png", "svg"].indexOf(suffix) >= 0) {
					td.textContent = file.mark ? "\u2612" : "\u2610";
					td.addEventListener("click", function () {
						fileBrowser.toggleMark(file.id);
					}, false);
				}
				tr.appendChild(td);

				// default
				td = document.createElement("td");
				if (suffix === "vpl3") {
					td.textContent = file["default"] ? "\u2612" : "\u2610";
					td.addEventListener("click", function () {
						fileBrowser.setDefaultFile(file.id, suffix);
					}, false);
				}
				tr.appendChild(td);
			}

			table.appendChild(tr);
		});
	} else {
		clearTable(tableId);
		var tr = document.createElement("tr");
		var td = document.createElement("td");
		td.setAttribute("class", "empty");
		td.textContent = VPLTeacherTools.translate("(none)");
		tr.appendChild(td);
		table.appendChild(tr);
	}

	updateGUI(fileBrowser);
	if (renamedFilename) {
		var str = renamedFilename.value;
		var r = /^(.*)\.([^.]*)$/.exec(str);
		var basename = r ? r[1] : str;
		renamedFilename.focus();
		renamedFilename.setSelectionRange(0, basename.length);
	}
	if (movedSet) {
		movedSet.focus();
		movedSet.setSelectionRange(0, movedSet.value.length);
	}
}

window.addEventListener("load", function () {
	var fileBrowser = new VPLTeacherTools.FileBrowser({
		onTeacherFiles: function (fileArray, fileBrowser) {
    		fillFileTable(fileArray, fileBrowser, false);
			updateGUI(fileBrowser);
		},
		onStudentFiles: function (fileArray, fileBrowser) {
    		fillFileTable(fileArray, fileBrowser, true);
			updateGUI(fileBrowser);
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
			document.location = "vpl$LANGSUFFIX.html?ui=$VPLUIURI&robot=sim&uilanguage=$VPLLANGUAGE" +
				(teacherFile ? "&role=teacher" : "") +
				(file.students ? "&user=" + encodeURIComponent(file.students.join(", ")) : "");
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
		onStudents: function (students) {
			// fill student filter
			var selFilterStudent = document.getElementById("sel-filter-student");
			while (selFilterStudent.firstElementChild) {
				selFilterStudent.removeChild(selFilterStudent.firstElementChild);
			}
			students.forEach(function (st) {
				var option = document.createElement("option");
				option.textContent = st;
				selFilterStudent.appendChild(option);
			});
			var option = document.createElement("option");
			option.textContent = VPLTeacherTools.translate("All pupils");
			option.selected = true;
			selFilterStudent.appendChild(option);
		},
		onSets: function (sets) {
			// fill set filters
			["sel-filter-set-teacher", "sel-filter-set-student"].forEach(function (selId) {
				var selFilterSet = document.getElementById(selId);
				var currentSet = selFilterSet.selectedIndex === selFilterSet.options.length - 1
					? null
					: selFilterSet.options[selFilterSet.selectedIndex].value;

				while (selFilterSet.firstElementChild) {
					selFilterSet.removeChild(selFilterSet.firstElementChild);
				}
				sets.forEach(function (s) {
					var option = document.createElement("option");
					option.textContent = s;
					if (s === currentSet) {
						option.selected = true;
					}
					selFilterSet.appendChild(option);
				});
				var option = document.createElement("option");
				option.textContent = VPLTeacherTools.translate("All files");
				if (currentSet === null) {
					option.selected = true;
				}
				selFilterSet.appendChild(option);
			}, this);
		}
	});

	function importFile(file, noRename, props) {
		var isBase64 = VPLTeacherTools.FileBrowser.storeAsBase64(file.name);
		var reader = new window.FileReader();
		reader.addEventListener("load", function (event) {
			var content = event.target.result;
			if (isBase64) {
				// skip data: header
				content = content.slice(content.indexOf(',') + 1);
			}
			fileBrowser.addFile(file.name, content, noRename, props);
		});
		reader[isBase64 ? "readAsDataURL" : "readAsText"](file);
	}

	document.body.addEventListener("dragover", function (ev) {
		ev.preventDefault();
	}, false);
	document.body.addEventListener("drop", function (ev) {
		ev.stopPropagation();
		ev.preventDefault();
		// plain files
		var files = ev.dataTransfer.files;
		for (var i = 0; i < files.length; i++) {
			importFile(files[i], files.length !== 1, {tag: fileBrowser.filterTeacherSet || null});
		}
		// folders
		var items = ev.dataTransfer.items;
		for (var i = 0; i < items.length; i++) {
			var entry = items[i].getAsEntry ? items[i].getAsEntry()
				: items[i].webkitGetAsEntry ? items[i].webkitGetAsEntry()
				: null;
			if (entry && entry.isDirectory) {
				var dirReader = entry.createReader();
				dirReader.readEntries(function (entries) {
					// read files, not subdirectories, and import them
					fileBrowser.filterTeacherSet = entry.name;	// to see them
					for (var j = 0; j < entries.length; j++) {
						if (entries[j].isFile) {
							entries[j].file(function (file) {
								importFile(file, true, {tag: entry.name});
							});
						}
					}
				});
			}
		}
	}, false);

	var btn;

	btn = document.getElementById("btn-new");
	btn.addEventListener("click", function () {
		var file = fileBrowser.selectedOrDefaultUIFile();
		var filename = file.filename.replace(/vpl3ui$/, "vpl3");
		fileBrowser.duplicateFile(file, filename);
	}, false);

	btn = document.getElementById("btn-new-conf");
	btn.addEventListener("click", function () {
		fileBrowser.addFile("untitled.vpl3ui",
			'{"disabledUI":["vpl:download","vpl:load"]}');
	}, false);

	btn = document.getElementById("btn-get-conf");
	btn.addEventListener("click", function () {
		fileBrowser.extractConfigFromVPL3();
	}, false);

	btn = document.getElementById("btn-edit-teacher");
	btn.addEventListener("click", function () {
		fileBrowser.openFile(false);
	}, false);

	btn = document.getElementById("btn-rename-teacher");
	btn.addEventListener("click", function () {
		fileBrowser.renameTeacherFile(null);
	}, false);

	btn = document.getElementById("btn-move-teacher");
	btn.addEventListener("click", function () {
		fileBrowser.moveTeacherFile(null);
	}, false);

	btn = document.getElementById("btn-duplicate-teacher");
	btn.addEventListener("click", function () {
		fileBrowser.duplicateTeacherFile(null);
	}, false);

	btn = document.getElementById("btn-import-teacher");
	var loadModalDialog = new LoadModalDialog({
		ok: VPLTeacherTools.translate("OK"),
		cancel: VPLTeacherTools.translate("Cancel"),
		title: VPLTeacherTools.translate("Import Files")
	}, {
		accept: ".vpl3,.vpl3ui,.html,.txt,.jpg,.png,.svg",
		multiple: true
	});
	btn.addEventListener("click", function () {
		loadModalDialog.show(function (files) {
			files.forEach(function (file) {
				importFile(file, files.length !== 1);
			});
		});
	}, false);

	btn = document.getElementById("btn-export-teacher");
	btn.addEventListener("click", function () {
		fileBrowser.exportFile();
	}, false);

	btn = document.getElementById("btn-remove-teacher");
	btn.addEventListener("click", function () {
		fileBrowser.deleteFiles();
	}, false);

	var selFilterTeacherSet = document.getElementById("sel-filter-set-teacher");
	selFilterTeacherSet.addEventListener("change", function () {
		fileBrowser.filterTeacherSet = selFilterTeacherSet.selectedIndex === selFilterTeacherSet.options.length - 1
			? null
			: selFilterTeacherSet.options[selFilterTeacherSet.selectedIndex].value;
		fileBrowser.updateFiles();
	}, false);

	var selFilterStudentSet = document.getElementById("sel-filter-set-student");
	selFilterStudentSet.addEventListener("change", function () {
		fileBrowser.filterStudentSet = selFilterStudentSet.selectedIndex === selFilterStudentSet.options.length - 1
			? null
			: selFilterStudentSet.options[selFilterStudentSet.selectedIndex].value;
		fileBrowser.updateFiles();
	}, false);

	var btn = document.getElementById("btn-view-st");
	btn.addEventListener("click", function () {
		fileBrowser.openFile(true);
	}, false);

	btn = document.getElementById("btn-export-st");
	btn.addEventListener("click", function () {
		fileBrowser.exportFile();
	}, false);

	btn = document.getElementById("btn-remove-st");
	btn.addEventListener("click", function () {
		fileBrowser.deleteFiles();
	}, false);

	var selFilterClass = document.getElementById("sel-filter-class");
	selFilterClass.addEventListener("change", function () {
		var filterClass = selFilterClass.selectedIndex === selFilterClass.options.length - 1
			? null
			: selFilterClass.options[selFilterClass.selectedIndex].value;
		fileBrowser.setClass(filterClass);
		fileBrowser.updateFiles();
	}, false);

	var selFilterStudent = document.getElementById("sel-filter-student");
	selFilterStudent.addEventListener("input", function () {
		fileBrowser.filterStudent = selFilterStudent.selectedIndex === selFilterStudent.options.length - 1
			? null
			: selFilterStudent.options[selFilterStudent.selectedIndex].value;
		fileBrowser.updateFiles();
	}, false);

	var chkFilterStLast = document.getElementById("chk-filter-students-last");
	chkFilterStLast.addEventListener("change", function () {
		fileBrowser.filterStudentLast = chkFilterStLast.checked;
		fileBrowser.updateFiles();
	}, false);
}, false);
