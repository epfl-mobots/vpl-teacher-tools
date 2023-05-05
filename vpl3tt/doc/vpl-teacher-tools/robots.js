
/*

Manage robots.

Usage:

var options = {
	method: "tdm", // or "jws" or "none"
	url: "ws://...",
	name: function (str) { return ...; },  // convert name
	onChange: function (robotCon) { ... }
};

var robotCon = VPLTeacherTools.RobotConnection(options);

*/

/**
	@constructor
	@param {VPLTeacherTools.RobotConnection} robotCon
	@param {string} name
	@param {string=} niceName
	@param {boolean=} multiple
*/
VPLTeacherTools.Robot = function (robotCon, name, niceName, multiple) {
	this.robotCon = robotCon;
	this.name = name;
	this.niceName = niceName || name;
	this.multiple = multiple || false;
};

VPLTeacherTools.Robot.prototype.isAvailable = function () {
	return true;
};

VPLTeacherTools.Robot.prototype.hasFlash = function () {
	return false;
};

VPLTeacherTools.Robot.prototype.canFlash = function () {
	return false;
};

VPLTeacherTools.Robot.prototype.flash = function (on) {
	// empty
};

/**
	@constructor
	@extends {VPLTeacherTools.Robot}
	@param {VPLTeacherTools.RobotConnection} robotCon
	@param {string} name
	@param {*} node
*/
VPLTeacherTools.RobotTDM = function (robotCon, name, node) {
	VPLTeacherTools.Robot.call(this, robotCon, name, node.name || "Thymio II");
	this.node = node;
};

VPLTeacherTools.RobotTDM.prototype.isAvailable = function () {
	return node.status === window["TDM"].status.ready ||
		node.status === window["TDM"].status.available ||
		node.status === window["TDM"].status.busy;
};

VPLTeacherTools.RobotTDM.prototype.hasFlash = function () {
	return true;
};

VPLTeacherTools.RobotTDM.prototype.canFlash = function () {
	return this.node.status === window["TDM"].status.ready ||
		this.node.status === window["TDM"].status.available;
};

VPLTeacherTools.RobotTDM.prototype.flash = function (on) {
	window["TDM"].runOnNode(this.node,
        on
		   ? "call leds.circle(32,32,32,32,32,32,32,32)\n"
           : "call leds.circle(0,0,0,0,0,0,0,0)\n"
	);
};

/**
	@constructor
	@extends {VPLTeacherTools.Robot}
	@param {VPLTeacherTools.RobotConnection} robotCon
	@param {string} name
	@param {string} nodeId
*/
VPLTeacherTools.RobotJWS = function (robotCon, name, nodeId) {
	VPLTeacherTools.Robot.call(this, robotCon, name, "Thymio II");
	this.nodeId = nodeId;
};

VPLTeacherTools.RobotJWS.prototype.isAvailable = function () {
	return true;
};

VPLTeacherTools.RobotJWS.prototype.hasFlash = function () {
	return true;
};

VPLTeacherTools.RobotJWS.prototype.canFlash = function () {
	return this.isAvailable();
};

VPLTeacherTools.RobotJWS.prototype.flash = function (on) {
	var pushConst = on ? 0x1020 : 0x1000;	// push.s 32 or 0
	var yellowLedsBC = [
		3,          // total size of vector table
		0xffff, 3,  // event 0xffff (init) at address 3
		pushConst,  // push.s 32 or 0
		0x426b,     // store 619
		0x126b,     // push.s 619
		pushConst,  // push.s 32 or 0
		0x426a,     // store 618
		0x126a,     // push.s 618
		pushConst,  // push.s 32 or 0
		0x4269,     // store 617
		0x1269,     // push.s 617
		pushConst,  // push.s 32 or 0
		0x4268,     // store 616
		0x1268,     // push.s 616
		pushConst,  // push.s 32 or 0
		0x4267,     // store 615
		0x1267,     // push.s 615
		pushConst,  // push.s 32 or 0
		0x4266,     // store 614
		0x1266,     // push.s 614
		pushConst,  // push.s 32 or 0
		0x4265,     // store 613
		0x1265,     // push.s 613
		pushConst,  // push.s 32 or 0
		0x4264,     // store 612
		0x1264,     // push.s 612
		// 0xc01e,     // callnat 30 (older firmware)
		0xc027,     // callnat 39 (firmware 13)
		0x0000      // stop
	];

	this.robotCon.jws.run(this.nodeId, yellowLedsBC);
};

/**
    @constructor
    @param {Object} options
*/
VPLTeacherTools.RobotConnection = function (options) {
    this.options = options || {method: "tdm"};
    var self = this;

	this.otherRobotObjects = options.otherRobots.map(function (descr) {
		var robot = new VPLTeacherTools.Robot(self, descr.name, descr.niceName, true);
		return robot;
	}) || [];

    this.robots = this.otherRobotObjects.slice();

    var self = this;
	switch (this.options.method) {
	case "tdm":
	    this.tdm = new window["TDM"](this.options.url || null,
			{
				"uuid": null,
				"anyNodeChange": function () {
	                var nodes = self.tdm.nodes.filter(function (node) {
				        return node.robotCon == undefined ||
			 				node.status === window["TDM"].status.ready ||
				            node.status === window["TDM"].status.available ||
				            node.status === window["TDM"].status.busy;
				    });
	                var a = nodes
	                    .map(function (node) {
							var robot = new VPLTeacherTools.RobotTDM(self,
								node.id
									? node.id.toString()
									: node.name,
								node);
							return robot;
	                    });
					self.otherRobotObjects.forEach(function (robot) {
						if (a.indexOf(robot) < 0) {
							a.push(robot);
						}
					});
	                self.robots = a;
	                if (self.options.onChange) {
					    self.options.onChange(self);
	                }
				}
			});
		break;
	case "jws":
		this.jws = new ThymioJSONWebSocketBridge(this.options.url || null);
		this.jws.onConnectNode = function (id) {
			var name = "{" + id + "}";
			var robot = self.getRobot(name);
			if (robot == undefined) {
				robot = new VPLTeacherTools.RobotJWS(self, name, id);
				self.robots.unshift(robot);	// leave otherRobots at the end
			}
	        if (self.options.onChange) {
			    self.options.onChange(self);
	        }
		};
		this.jws.onDisconnectNode = function (id) {
            if (self.options.onChange) {
			    self.options.onChange(self);
            }
		};
		this.jws.connect();
		break;
	}
};

VPLTeacherTools.RobotConnection.prototype.update = function () {
    if (self.options.onChange) {
	    self.options.onChange(self);
    }
};

VPLTeacherTools.RobotConnection.prototype.getRobot = function (robotName) {
    return this.robots.find(function (r) { return r.name === robotName}, this);
};
