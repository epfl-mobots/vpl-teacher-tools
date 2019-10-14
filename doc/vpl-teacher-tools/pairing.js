
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
                if (options && options.onPairs) {
                    // in case onPairs needs the robots
                    options.onPairs(self.pairs);
                }
			}
		});

    var nonGroups = options && options.nonGroups.map(function (name) { return {"name": name}}) || [];
    if (options.onRobots) {
        this.robots = this.nonRobots.slice();
        options.onRobots(this.nonRobots, this);
    }
	this.client = new VPLTeacherTools.HTTPClient();
	this.client.listGroups({
		onSuccess: function (groups) {
            function update() {
                self.groups = groups.concat(nonGroups);
                if (options.onGroups) {
                    options.onGroups(self.groups, self);
                }
            }
			groups.forEach(function (group) {
				self.client.listGroupStudents(group.name, {
                    onSuccess: function (students) {
                        group.students = students;
                        self.groups = groups.concat(nonGroups);
                        if (options.onGroups) {
                            options.onGroups(self.groups, self);
                        }
                    }
                });
			});
        }
	});
    this.updateSessions();
};

VPLTeacherTools.Pairing.prototype.updateSessions = function () {
    var self = this;
	this.client.listSessions({
		onSuccess: function (pairs) {
            pairs = pairs.map(function (pair) {
                if (!self.isRobot(pair.robot)) {
                    pair.robot = self.nonRobotNameMapping[pair.robot] || pair.robot;
                }
                return pair;
            });
            self.pairs = pairs;
            if (self.options.onPairs) {
                self.options.onPairs(pairs);
            }
            // get students
            pairs.forEach(function (pair) {
				self.client.listGroupStudents(pair.group, {
                    onSuccess: function (students) {
                        pair.students = students;
                        if (self.options.onPairs) {
                            self.options.onPairs(pairs);
                        }
                    }
                });
            });
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
                    self.selectPair(group);
                    self.updateSessions();
                }
            });
    }
};

VPLTeacherTools.Pairing.prototype.selectPair = function (groupName) {
    this.groupOfSelectedPair = groupName;
};

VPLTeacherTools.Pairing.prototype.unselectPair = function () {
    this.groupOfSelectedPair = "";
};

VPLTeacherTools.Pairing.prototype.isPairSelected = function (groupName) {
    return this.groupOfSelectedPair === groupName;
};

VPLTeacherTools.Pairing.prototype.selectedPair = function () {
	if (this.groupOfSelectedPair) {
	    var ix = this.pairs.findIndex(function (pair) {
	        return pair.group === this.groupOfSelectedPair;
	    }, this);
		return this.pairs[ix];
	} else {
		return null;
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
            if (self.options.onPairs) {
                self.options.onPairs(self.pairs);
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
                if (self.options.onPairs) {
                    self.options.onPairs([]);
                }
            }
        });
};

VPLTeacherTools.Pairing.prototype.shortenURL = function (url, cb) {
	this.client.shortenURL(url, cb);
};
