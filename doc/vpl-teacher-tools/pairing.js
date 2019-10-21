
/**
    @constructor
    @param {Object} options
*/
VPLTeacherTools.Pairing = function (options) {
    this.options = options || {};
    this.robots = [];
    this.groups = [];
    this.pairs = [];
    this.selectedRobot = "";
    this.selectedGroup = "";
    this.groupOfSelectedPair = "";

    var self = this;
    this.nonRobots = options && options.nonRobots
        ? options.nonRobots.map(function (nr) {
            return {
                name: nr.name(null),
				url: nr.url,
                flash: null
            };
        })
        : [];
    this.nonRobotNameMapping = options && options.nonRobotNameMapping || {};
    if (options.onRobots) {
        options.onRobots(this.nonRobots, this);
    }
    this.tdm = new window["TDM"](options && options.tdmURL || null,
		{
			"uuid": null,
			"change": function () {
                var nodes = options.robot ? self.getRobotNodes() : [];
                var a = nodes
                    .map(function (node) {
                        return {
                            name: options.robot.name(node.id.toString()),
							url: options.robot.url,
                            flash: function (on) {
                				window["TDM"].runOnNode(node,
                                    on
                					   ? "call leds.circle(32,32,32,32,32,32,32,32)\n"
                                       : "call leds.circle(0,0,0,0,0,0,0,0)\n"
                				);
                			}
                        };
                    })
                    .concat(self.nonRobots);
                self.robots = a;
                if (options && options.onRobots) {
				    options.onRobots(a, self);
                }
			}
		});

    var nonGroups = options && options.nonGroups.map(function (name) { return {"name": name}}) || [];
    if (options.onRobots) {
        this.robots = this.nonRobots.slice();
        options.onRobots(this.nonRobots, this);
    }
	this.client = new VPLTeacherTools.HTTPClient();
	this.client.listStudents({
		onSuccess: function (students) {
            self.students = students;
            if (self.options.onStudents) {
                self.options.onStudents(students);
            }
        }
	});
    this.updateGroups();
};

/** Find the group a student belongs to
    @param {string} studentName
    @return {?string} group name, or null if student isn't found or doesn't belong to a group
*/
VPLTeacherTools.Pairing.prototype.groupForStudent = function (studentName) {
    for (var i = 0; i < this.students.length; i++) {
        if (this.students[i].name === studentName) {
            return this.students[i].group;
        }
    }
    return null;
};

/** Find group
    @param {string} groupName
    @return {?Object}
*/
VPLTeacherTools.Pairing.prototype.findGroup = function (groupName) {
    for (var i = 0; i < this.groups.length; i++) {
        if (this.groups[i].name === groupName) {
            return this.groups[i];
        }
    }
    return null;
};

VPLTeacherTools.Pairing.prototype.updateGroups = function () {
    var self = this;
	this.client.listGroupsWithStudents({
		onSuccess: function (groups) {
            self.groups = groups;
            if (self.options.onGroups) {
                self.options.onGroups(groups, self);
            }
        	self.client.listSessions({
        		onSuccess: function (pairs) {
                    pairs = pairs.map(function (pair) {
                        if (!self.isRobot(pair.robot)) {
                            pair.robot = self.nonRobotNameMapping[pair.robot] || pair.robot;
                        }
                        return pair;
                    });
                    // add pair to group
                    pairs.forEach(function (pair) {
                        var i = self.groups.findIndex(function (group) {
                            return pair.group === group.name;
                        });
                        if (i >= 0) {
                            self.groups[i].pair = pair;
                        }
                    });
                    self.pairs = pairs;
                    if (self.options.onGroups) {
                        self.options.onGroups(self.groups, self);
                    }
                }
        	});
        }
	});
};

/** Add a new group with optional initial student
    @param {string} groupName group name
    @param {string=} studentName student name
    @param {boolean=} true to autoremove group left by student if empty
    @return {void}
*/
VPLTeacherTools.Pairing.prototype.addGroup = function (groupName, studentName, autoremove) {
    groupName = groupName.trim();
    var self = this;
    this.client.addGroup(groupName, {
        onSuccess: function (r) {
            self.updateGroups();
            if (studentName) {
                self.addStudentToGroup(studentName, groupName, autoremove);
            }
        }
    });
};

VPLTeacherTools.Pairing.prototype.removeGroup = function (groupName) {
    groupName = groupName.trim();
    var self = this;
    this.client.removeGroup(groupName, {
        onSuccess: function (r) {
            self.updateGroups();
        }
    });
};

/** Add or move a student to a group
    @param {string} groupName group name
    @param {string=} studentName student name
    @param {boolean=} true to autoremove group left by student if empty
    @return {void}
*/
VPLTeacherTools.Pairing.prototype.addStudentToGroup = function (studentName, groupName, autoremove) {
    studentName = studentName.trim();
    groupName = groupName.trim();
    var previousGroupName = this.groupForStudent(studentName);
	if (groupName !== previousGroupName) {
	    var self = this;
	    this.client.addStudentToGroup(studentName, groupName, {
	        onSuccess: function (r) {
	            if (autoremove && previousGroupName) {
	                var group = self.findGroup(previousGroupName);
	                if (group && group.students && group.students.length <= 1) {   // not yet updated
	                    self.removeGroup(previousGroupName);
	                    return;
	                }
	            }
	            self.updateGroups();
	        }
	    });
	}
};

/** Remove a student from a group
    @param {string} studentName
    @param {string} groupName
    @param {boolean=} autoremove true to remove group if it becomes empty
    @return {void}
*/
VPLTeacherTools.Pairing.prototype.removeStudentFromGroup = function (studentName, groupName, autoremove) {
    studentName = studentName.trim();
    groupName = groupName.trim();
    var self = this;
    this.client.removeStudentFromGroup(studentName, groupName, {
        onSuccess: function (r) {
            if (autoremove) {
                var group = self.findGroup(groupName);
                if (group && group.students.length <= 1) {   // not yet updated
                    self.removeGroup(groupName);
                    return;
                }
            }
            self.updateGroups();
        }
    });
};

VPLTeacherTools.Pairing.prototype.getRobotNodes = function () {
    return this.tdm.nodes;
};

VPLTeacherTools.Pairing.prototype.selectRobot = function (robotName) {
    this.selectedRobot = robotName;
};

VPLTeacherTools.Pairing.prototype.unselectRobot = function () {
    this.selectedRobot = "";
};

VPLTeacherTools.Pairing.prototype.isRobotSelected = function (robotName) {
    return this.selectedRobot === robotName;
};

VPLTeacherTools.Pairing.prototype.isRobot = function (robotName) {
    robotName = this.nonRobotNameMapping[robotName] || robotName;
    return this.nonRobots.find(function (r) { return r.name === robotName; }) == null;
};

VPLTeacherTools.Pairing.prototype.selectGroup = function (groupName) {
    this.selectedGroup = groupName;
};

VPLTeacherTools.Pairing.prototype.unselectGroup = function () {
    this.selectedGroup = "";
};

VPLTeacherTools.Pairing.prototype.isGroupSelected = function (groupName) {
    return this.selectedGroup === groupName;
};

VPLTeacherTools.Pairing.prototype.getSelectedGroup = function () {
    return this.groups.find(function (group) {
        return group.name === this.selectedGroup;
    }, this);
};

VPLTeacherTools.Pairing.prototype.canBeginSession = function (robotName, groupName) {
    robotName = robotName || this.selectedRobot;
    groupName = groupName || this.selectedGroup;
    return this.robots.find(function (r) { return r.name === robotName}, this) != undefined &&
        this.groups.find(function (g) { return g.name === groupName}, this) != undefined;
};

VPLTeacherTools.Pairing.prototype.deletePairByGroup = function (group) {
    var ix = this.pairs.findIndex(function (pair) {
        return pair.group === group;
    });
    if (ix >= 0) {
        this.pairs.splice(ix, 1);
    }
};

VPLTeacherTools.Pairing.prototype.deletePairBySessionId = function (sessionId) {
    var ix = this.pairs.findIndex(function (pair) {
        return pair.session_id === sessionId;
    });
    if (ix >= 0) {
        var groupIx = this.groups.findIndex(function (group) {
            return group.pair === this.pairs[ix];
        }, this);
        if (groupIx >= 0) {
            this.groups[groupIx].pair = null;
        }
        this.pairs.splice(ix, 1);
    }
};

/** Begin a session by associating a robot with a group
    @param {?string=} robotName robot name (default: selected robot)
    @param {?string=} groupName group name (default: selected group)
    @return {void}
*/
VPLTeacherTools.Pairing.prototype.beginSession = function (robotName, groupName) {
    if (this.canBeginSession(robotName, groupName)) {
        var self = this;
        var group = (groupName || this.selectedGroup)
            .replace(/^\(teacher\)$/, "!teacher");
        this.client.beginSession(group,
            this.isRobot(robotName || this.selectedRobot) ? robotName || this.selectedRobot : "!sim",
            true,
            {
                onSuccess: function (r) {
                    self.selectGroup(group);
                    self.updateGroups();
                }
            });
    }
};

VPLTeacherTools.Pairing.prototype.getGroup = function (groupName) {
    var group = this.groups.find(function (group) {
        return group.name === groupName;
    });
    return group;
};

VPLTeacherTools.Pairing.prototype.getToolURL = function (pair) {
    var robotAltName = this.nonRobotNameMapping[pair.robot];
	var r = this.robots.find(function (robot) {
        return robot.name === pair.robot || robot.name === robotAltName;
    });
	return r ? r.url(pair) : null;
};

VPLTeacherTools.Pairing.prototype.endSession = function (sessionId) {
    var self = this;
    this.client.endSession(sessionId, {
        onSuccess: function (r) {
            self.deletePairBySessionId(sessionId);
            if (self.options.onGroups) {
                self.options.onGroups(self.groups, self);
            }
        }
    });
};

VPLTeacherTools.Pairing.prototype.canEndAllSessions = function () {
    return this.pairs.length > 0;
};

VPLTeacherTools.Pairing.prototype.endAllSessions = function () {
    var self = this;
    this.client.endAllSessions(
        {
            onSuccess: function (r) {
                self.pairs = [];
                self.groups.forEach(function (group) {
                    group.pair = null;
                });
                if (self.options.onGroups) {
                    self.options.onGroups(self.groups, self);
                }
            }
        });
};

VPLTeacherTools.Pairing.prototype.shortenURL = function (url, cb) {
	this.client.shortenURL(url, cb);
};
