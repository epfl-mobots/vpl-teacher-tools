
/**
	@constructor
	@param {Object} options
*/
VPLTeacherTools.Login = function (options) {
	this.options = options || {};
	this.groups = [];

	this.client = new VPLTeacherTools.HTTPClient();
	this.updateGroups();
};

VPLTeacherTools.Login.prototype.updateGroups = function () {
	var self = this;
	this.client.listGroupsWithStudents(null, {
		onSuccess: function (groups) {
			self.client.listSessions({
				onSuccess: function (sessions) {
					// convert array of sessions to array of connected groups
					var connected_groups = []
					sessions.forEach(function (session) {
						if (session.is_connected) {
							connected_groups.push(session.group_id);
						}
					});

					self.groups = groups.filter(function (group) {
						group.is_connected = connected_groups.indexOf(group.group_id) >= 0;
						return group.session_id != null;
					});
					if (self.options.onGroups) {
						self.options.onGroups(self.groups, self);
					}
				}
			});
		}
	});
};

VPLTeacherTools.Login.prototype.launchVPL = function (group) {
	var url = VPLTeacherTools.makeVPLURL(group, "$BRIDGE");
	document.location = url;
};
