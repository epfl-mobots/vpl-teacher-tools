window.addEventListener("load", function () {
	var client = new VPLTeacherTools.HTTPClient();
	var opt = {
		logURL: function (url) {
			document.getElementById("console").textContent += "URL: " + url + "\n";
		},
		onSuccess: function (r) {
			document.getElementById("console").textContent += "Success: " + JSON.stringify(r, null, "\t") + "\n";
		},
		onError: function (msg) {
			document.getElementById("console").textContent += "Error: " + msg + "\n";
		}
	};

	var btn = document.getElementById("clc");
	btn.addEventListener("click", function () {
		document.getElementById("console").textContent = "";
	});

	btn = document.getElementById("reset-students");
	btn.addEventListener("click", function () {
		client.deleteAllStudents(opt);
	});

	btn = document.getElementById("init");
	btn.addEventListener("click", function () {
		client.addStudent("Alice", "Cl.1", opt);
		client.addStudent("Bob", "Cl.1", opt);
		client.addStudent("Carol", "Cl.2", opt);
		client.addStudent("David", "Cl.2", opt);
		client.addGroup("Alice", {
			logURL: opt.logURL,
			onSuccess: function (r) {
				opt.onSuccess(r);
				client.addStudentToGroup("Bob", r, opt);
				client.addGroup("Carol", opt);
			},
			onError: opt.onError
		});
	});

	btn = document.getElementById("list-students");
	btn.addEventListener("click", function () {
		client.listStudents(null, opt);
	});

	btn = document.getElementById("list-groups");
	btn.addEventListener("click", function () {
		client.listGroups(opt);
	});

	btn = document.getElementById("list-members-a");
	btn.addEventListener("click", function () {
		client.listGroups({
			logURL: opt.logURL,
			onSuccess: function (r) {
				opt.onSuccess(r);
				r.forEach(function (group) {
					client.listGroupStudents(group.group_id, opt);
				});
			},
			onError: opt.onError
		});
	});

	btn = document.getElementById("list-members-b");
	btn.addEventListener("click", function () {
		client.listGroupsWithStudents(opt);
	});

	btn = document.getElementById("reset-sessions");
	btn.addEventListener("click", function () {
		client.endAllSessions(opt);
	});

	btn = document.getElementById("list-sessions");
	btn.addEventListener("click", function () {
		client.listSessions(opt);
	});

	btn = document.getElementById("log");
	btn.addEventListener("click", function () {
		var sessionId = document.getElementById("log-file-sessionid").value;
		client.getLog(sessionId, null, opt);
	});

	btn = document.getElementById("last-log");
	btn.addEventListener("click", function () {
		var sessionId = document.getElementById("log-file-sessionid").value;
		client.getLog(sessionId, "vpl-changed", opt);
	});

	btn = document.getElementById("clear-log");
	btn.addEventListener("click", function () {
		client.clearLog(opt);
	});

	btn = document.getElementById("init-files-teacher");
	btn.addEventListener("click", function () {
		client.addFile("test-teacher.txt",
			"Hello, teacher!\n",
			{},
			opt);
	});

	btn = document.getElementById("init-files-students");
	btn.addEventListener("click", function () {
		// add one file for each group
		client.listGroups({
			logURL: opt.logURL,
			onSuccess: function (r) {
				opt.onSuccess(r);
				r.forEach(function (group) {
					client.addFile("test-gr" + group.group_id + ".txt",
						"Hello, group " + group.group_id + "!\n",
						{groupId: group.group_id},
						opt);
				});
			},
			onError: opt.onError
		});
	});

	btn = document.getElementById("remove-files");
	btn.addEventListener("click", function () {
		document.getElementById("console").textContent += "Not implemented\n";
	});

	btn = document.getElementById("list-files-teacher");
	btn.addEventListener("click", function () {
		client.listFiles(null, opt);
	});

	btn = document.getElementById("list-files-students");
	btn.addEventListener("click", function () {
		client.listFiles({filterStudent: "*"}, opt);
	});

	btn = document.getElementById("clear-files");
	btn.addEventListener("click", function () {
		client.clearFiles(opt);
	});

}, false);
