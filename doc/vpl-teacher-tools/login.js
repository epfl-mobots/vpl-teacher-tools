
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
	this.client.listGroupsWithStudents({
		onSuccess: function (groups) {
            self.groups = groups.filter(function (group) {
                return group.session_id != null;
            });
            if (self.options.onGroups) {
                self.options.onGroups(self.groups, self);
            }
        }
	});
};

VPLTeacherTools.Login.prototype.launchVPL = function (group) {
	var url = VPLTeacherTools.makeVPLURL(group);
	document.location = url;
};
