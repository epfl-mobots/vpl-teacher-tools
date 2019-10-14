/*
	Author: Yves Piguet, EPFL
	Please don't redistribute without author's permission.
*/

/** Access to HTTP server as a client
	@constructor
*/
VPLTeacherTools.HTTPClient = function () {
};

/** Send an http request, GET if !data or POST if data
	@param {string} url
	@param {Object=} opt
	@param {string=} data
*/
VPLTeacherTools.HTTPClient.prototype.rest = function (url, opt, data) {
	var xhr = new XMLHttpRequest();
	if (opt && opt.onSuccess) {
		xhr.addEventListener("load", function () {
			try {
				var msg = JSON.parse(this.responseText);
				if (msg["status"] === "ok") {
					opt.onSuccess(msg["result"]);
				} else if (opt.onError) {
					opt.onError(msg["msg"]);
				}
			} catch (e) {
				if (opt.onError) {
					opt.onError(e.toString());
				} else {
					throw e;
				}
			}
		});
	}
	if (opt && opt.onError) {
		xhr.addEventListener("error", function () {
			opt.onError("Connection");
		});
	}
	xhr.open(data ? "POST" : "GET", url);
	if (opt && opt.logURL) {
		opt.logURL(url);
	}
	xhr.send(data || null);
};

VPLTeacherTools.HTTPClient.prototype.deleteAllStudents = function (opt) {
	this.rest("/api/deleteAllStudents", opt);
};

VPLTeacherTools.HTTPClient.prototype.addStudent = function (name, opt) {
	this.rest("/api/addStudent?name=" + encodeURIComponent(name), opt);
};

VPLTeacherTools.HTTPClient.prototype.removeStudent = function (name, opt) {
	this.rest("/api/removeStudent?name=" + encodeURIComponent(name), opt);
};

VPLTeacherTools.HTTPClient.prototype.listStudents = function (opt) {
	this.rest("/api/listStudents", opt);
};

VPLTeacherTools.HTTPClient.prototype.addGroup = function (groupName, opt) {
	this.rest("/api/addGroup?group=" + encodeURIComponent(groupName), opt);
};

VPLTeacherTools.HTTPClient.prototype.removeGroup = function (groupName, opt) {
	this.rest("/api/removeGroup?group=" + encodeURIComponent(groupName), opt);
};

VPLTeacherTools.HTTPClient.prototype.listGroups = function (opt) {
	this.rest("/api/listGroups", opt);
};

VPLTeacherTools.HTTPClient.prototype.addStudentToGroup = function (name, groupName, opt) {
	this.rest("/api/addStudentToGroup?name=" +
		encodeURIComponent(name) + "&group=" + encodeURIComponent(groupName),
		opt);
};

VPLTeacherTools.HTTPClient.prototype.removeStudentFromGroup = function (name, groupName, opt) {
	this.rest("/api/removeStudentFromGroup?name=" +
		encodeURIComponent(name) + "&group=" + encodeURIComponent(groupName),
		opt);
};

VPLTeacherTools.HTTPClient.prototype.listGroupStudents = function (groupName, opt) {
	this.rest("/api/listGroupStudents?group=" + encodeURIComponent(groupName), opt);
};

VPLTeacherTools.HTTPClient.prototype.listGroupsWithStudents = function (opt) {
	var self = this;
	this.listGroups({
		onSuccess: function (groups) {
			var remaining = groups.length;
			var errMsg = null;
			if (groups.length > 0) {
				groups.forEach(function (group) {
					self.listGroupStudents(group.name, {
	                    onSuccess: function (students) {
	                        group.students = students;
							remaining--;
							if (remaining == 0 && opt) {
								if (errMsg != null) {
									opt.onError && opt.onError(errMsg);
								} else {
									opt.onSuccess && opt.onSuccess(groups);
								}
							}
	                    },
						onError: function (msg) {
							remaining--;
							errMsg = msg;
							if (remaining == 0 && opt && opt.onError) {
								opt.onError(msg);
							}
						}
	                });
				});
			} else {
				// must still call onSuccess
				opt && opt.onSuccess && opt.onSuccess(groups);
			}
		},
		onError: opt && opt.onError
	});
};

VPLTeacherTools.HTTPClient.prototype.beginSession = function (groupName, robot, force, opt) {
	var url = "/api/beginSession?group=" + encodeURIComponent(groupName);
	if (robot) {
		url += "&robot=" + encodeURIComponent(robot);
	}
	if (force) {
		url += "&force=true";
	}
	this.rest(url, opt);
};

VPLTeacherTools.HTTPClient.prototype.endSession = function (sessionId, opt) {
	this.rest("/api/endSession?session=" + encodeURIComponent(sessionId), opt);
};

VPLTeacherTools.HTTPClient.prototype.endAllSessions = function (opt) {
	this.rest("/api/endAllSessions", opt);
};

VPLTeacherTools.HTTPClient.prototype.listSessions = function (opt) {
	this.rest("/api/listSessions", opt);
};

VPLTeacherTools.HTTPClient.prototype.addFile = function (filename, content, props, opt) {
	this.rest("/api/addFile?filename=" + encodeURIComponent(filename) +
		(props && props.studentName ? "&student=" + encodeURIComponent(props.studentName) : "") +
		(props && props.groupName ? "&group=" + encodeURIComponent(props.groupName) : "") +
		(props && props.metadata ? "&metadata=" + encodeURIComponent(props.metadata) : ""),
		opt, content);
};

VPLTeacherTools.HTTPClient.prototype.getFile = function (id, opt) {
	this.rest("/api/getFile?id=" + id.toString(10), opt);
};

VPLTeacherTools.HTTPClient.prototype.updateFile = function (id, content, opt) {
	this.rest("/api/updateFile?id=" + id.toString(10), opt, content);
};

VPLTeacherTools.HTTPClient.prototype.removeFiles = function (idArray, opt) {
	this.rest("/api/removeFiles?id=" + idArray.map(function (id) { return id.toString(10); }).join("+"), opt);
};

VPLTeacherTools.HTTPClient.prototype.listFiles = function (queryProps, opt) {
	var params = [];
	if (queryProps) {
		if (queryProps.filterStudent != null) {
			params.push("student=" + encodeURIComponent(queryProps.filterStudent));
		}
		if (queryProps.filterGroup != null) {
			params.push("group=" + encodeURIComponent(queryProps.filterGroup));
		}
		if (queryProps.last) {
			params.push("last=true");
		}
	}
	this.rest("/api/listFiles" + (params.length > 0 ? "?" + params.join("&") : ""), opt);
};

VPLTeacherTools.HTTPClient.prototype.getLog = function (sessionId, last, opt) {
	var params = [
		"id=" + encodeURIComponent(sessionId)
	];
	if (last) {
		params.push("last=" + last);
	}
	this.rest("/api/getLog" + "?" + params.join("&"), opt);
};

VPLTeacherTools.HTTPClient.prototype.shortenURL = function (url, cb) {
	var xhr = new XMLHttpRequest();
	xhr.addEventListener("load", function () {
		var shortenedURL = this.responseText.trim();
		cb(shortenedURL);
	});
	xhr.open("GET", "/api/shortenURL?u=" + encodeURIComponent(url));
	xhr.send(null);
};
