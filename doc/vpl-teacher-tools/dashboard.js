
/**
	@constructor
	@param {string} wsURL
	@param {{
		log: (function(string):void | undefined),
		onGroups: (function(Array.<Objects>):void | undefined),
		onFiles: (function(Array.<Object>):void | undefined)
	}} options
*/
VPLTeacherTools.Dashboard = function (wsURL, options) {
	this.wsURL = wsURL;
	/** @type {WebSocket} */
	this.ws = null;

	this.options = options;

	this.sessions = [];
	this.wsConnections = [];

	this.client = new VPLTeacherTools.HTTPClient();
	this.loadSessions();
	this.updateFiles();

	var self = this;
	window.addEventListener("unload", function () {
		if (self.ws) {
			self.ws.addEventListener("open", function () {
				this.send(JSON.stringify({
					"sender": {
						"type": "dashboard"
					},
					"type": "bye"
				}));
			});
		}
	});
};

/** Refresh sessions by calling onGroups
	@param {Array=} sessions session array (default: this.sessions)
	@return {void}
*/
VPLTeacherTools.Dashboard.prototype.refreshSessions = function (sessions) {
    if (this.options.onGroups) {
        this.options.onGroups((sessions || this.sessions)
			.filter(function (session) {
				return !session.special && session.students.length > 0;
			})
			.map(function (session) {
				session.isConnected = this.wsConnections.indexOf(session.session_id) >= 0;
				return session;
			}, this));
    }
};

/** Load the list of sessions
	@return {void}
*/
VPLTeacherTools.Dashboard.prototype.loadSessions = function () {
    var self = this;
	this.client.listSessions({
		onSuccess: function (sessions) {
            self.sessions = sessions.map(function (session) {
				session.students = [];
				session.lastLogEntry = null;
				session.selected = false;

				self.client.listGroupStudents(session.group, {
                    onSuccess: function (students) {
                        session.students = students;
			            self.refreshSessions(sessions);
                    }
                });

				self.client.getLog(session.session_id, "vpl-changed", {
					onSuccess: function (logEntries) {
						if (logEntries.length > 0) {
							session.lastLogEntry = logEntries[0];
			            	self.refreshSessions(sessions);
						}
					}
				});

				return session;
			});
            self.refreshSessions();
        }
	});
};

/** Update the list of session using the last log message received
	@param {number} sessionIndex
	@param {Object} msg
	@return {void}
*/
VPLTeacherTools.Dashboard.prototype.updateSessions = function (sessionIndex, msg) {
	function datetimeStr(d) {
		function s(num, len) {
			var str = num.toString(10);
			return "0000".slice(0, len - str.length) + str;
		}
		return s(d.getFullYear(), 4) + "-" + s(d.getMonth(), 2) + "-" + s(d.getDate(), 2) +
			" " + s(d.getHours(), 2) + ":" + s(d.getMinutes(), 2) + ":" + s(d.getSeconds(), 2);
	}

	this.sessions[sessionIndex].lastLogEntry = {
		"type": "log",
		"time": datetimeStr(new Date()),
		"data": JSON.stringify(msg["data"])
	};
	this.refreshSessions();
};

VPLTeacherTools.Dashboard.prototype.updateFiles = function () {
	var self = this;
	this.client.listFiles({
        filterStudent: this.filterStudent,
        filterGroup: this.filterGroup,
        last: this.filterLast
    },
    {
		onSuccess: function (files) {
            self.files = files.map(function (file) {
                var file1 = Object.create(file);    // prototype-based "copy"
                file1.selected = false;
                return file1;
            });
            if (self.options.onFiles) {
                self.options.onFiles(files);
            }
        }
	});
};

/** Get the index of a session specified by its id
	@param {string} sessionId
	@return {number}
*/
VPLTeacherTools.Dashboard.prototype.sessionIndex = function (sessionId) {
	return this.sessions.findIndex(function (session) { return session.session_id === sessionId; });
};

/** Select, unselect or toggle group
	@param {?boolean} state
	@return {void}
*/
VPLTeacherTools.Dashboard.prototype.selectGroup = function (session, state) {
    session.selected = state === null ? !session.selected : state;
};

VPLTeacherTools.Dashboard.prototype.isGroupSelected = function (session) {
    return session.selected;
};

VPLTeacherTools.Dashboard.prototype.getIdOfSelectedSessions = function () {
	return this.sessions
		.filter(function (session) { return session.selected; })
		.map(function (session) { return session.session_id; });
};

/** Send a command to selected sessions, if any, or to all
	@param {string} name
	@param {{
		toAll: (boolean | undefined),
		selected: (boolean | undefined),
		state: (string | undefined)
	}=} opt
	@return {void}
*/
VPLTeacherTools.Dashboard.prototype.sendCommand = function (name, opt) {
	var sessions = opt && opt.toAll ? [] : this.getIdOfSelectedSessions();
	var msg = {
		"sender": {
			"type": "dashboard"
		},
		"rcpt": sessions.length > 0 ? sessions : null,
		"type": "cmd",
		"data": {
			"cmd": name
		}
	};
	if (opt && opt.selected) {
		msg["data"]["selected"] = opt.selected;
	} else if (opt && opt.state) {
		msg["data"]["state"] = opt.state;
	}
	this.ws.send(JSON.stringify(msg));
};

/** Send a file
	@param {number} fileId
	@return {void}
*/
VPLTeacherTools.Dashboard.prototype.sendFile = function (filename, kind, content) {
	var msg = {
		"sender": {
			"type": "dashboard"
		},
		"rcpt": null,
		"type": "file",
		"data": {
			"name": filename,
			"kind": kind,
			"metadata": {},
			"content": content
		}
	};
	this.ws.send(JSON.stringify(msg));
};

/** Send a file
	@param {number} fileId
	@return {void}
*/
VPLTeacherTools.Dashboard.prototype.sendFileById = function (fileId) {
	var self = this;
    this.client.getFile(fileId, {
        onSuccess: function (file) {
			self.sendFile(file.filename, "vpl", file.content);
        }
    });
};

/** Suspend (selected) or unsuspend (all) VPL web apps
	@param {boolean} state
	@param {string=} html
	@return {void}
*/
VPLTeacherTools.Dashboard.prototype.suspend = function (state, html) {
	if (html && state) {
		this.sendFile("suspend.html", "suspend", html);
	}
	this.sendCommand("vpl:suspend", {selected: state, toAll: !state});
};

/** Start websocket
	@return {void}
*/
VPLTeacherTools.Dashboard.prototype.connect = function () {
	this.ws = new WebSocket(this.wsURL);
	var self = this;
	this.ws.addEventListener("message", function (event) {
		try {
			var msg = JSON.parse(event.data);
			switch (msg["type"]) {
			case "hello":
			case "change":
				self.wsConnections = msg["data"];
				self.refreshSessions();
				break;
			case "log":
				if (self.options.log) {
					var sessionId = msg["sender"]["sessionid"] || "-";
					var i = self.sessionIndex(sessionId);
					var session = i >= 0 ? self.sessions[i] : null;
					if (!session || session.special !== "!teacher") {
						self.options.log(sessionId +
							(session && session.students && session.students.length > 0 ? " (" + session.students.join(", ") + ")"
	 							: "") +
							"  " +
							JSON.stringify(msg["data"]));
					}
					if (session) {
						self.updateSessions(i, msg);
					}
				}
				break;
			}
		} catch (e) {
			console.info(e);
		}
	});
	this.ws.addEventListener("open", function () {
		this.send(JSON.stringify({
			"sender": {
				"type": "dashboard"
			},
			"type": "hello"
		}));
	});
};
