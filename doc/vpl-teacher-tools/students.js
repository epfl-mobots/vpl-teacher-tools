
/**
    @constructor
    @param {Object} options
*/
VPLTeacherTools.StudentManagement = function (options) {
    this.options = options || {};
    this.students = [];
    this.groups = [];
    this.selectedStudent = "";
    this.selectedGroup = "";

	this.client = new VPLTeacherTools.HTTPClient();

    if (options.onStudents) {
        this.students = [];
        options.onStudents([], this);
    }
    this.updateStudents();
    this.updateGroups();
};

VPLTeacherTools.StudentManagement.prototype.doesStudentExist = function (studentName) {
    return this.students.find(function (student) { return student.name === studentName; }) != null;
};

/** Find the group a student belongs to
    @param {string} studentName
    @return {?string} group name, or null if student isn't found or doesn't belong to a group
*/
VPLTeacherTools.StudentManagement.prototype.groupForStudent = function (studentName) {
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
VPLTeacherTools.StudentManagement.prototype.findGroup = function (groupName) {
    for (var i = 0; i < this.groups.length; i++) {
        if (this.groups[i].name === groupName) {
            return this.groups[i];
        }
    }
    return null;
};

VPLTeacherTools.StudentManagement.prototype.updateStudents = function () {
    var self = this;
	this.client.listStudents({
		onSuccess: function (students) {
            self.students = students;
            if (self.options.onStudents) {
                self.options.onStudents(students, self);
            }
        }
	});
};

VPLTeacherTools.StudentManagement.prototype.updateGroups = function () {
    var self = this;
	this.client.listGroupsWithStudents({
		onSuccess: function (groups) {
            self.groups = groups;
            if (self.options.onGroups) {
                self.options.onGroups(groups, self);
            }
        }
	});
};

VPLTeacherTools.StudentManagement.prototype.selectStudent = function (studentName) {
    this.selectedStudent = studentName;
};

VPLTeacherTools.StudentManagement.prototype.unselectStudent = function () {
    this.selectedStudent = "";
};

VPLTeacherTools.StudentManagement.prototype.isStudentSelected = function (studentName) {
    return this.selectedStudent === studentName;
};

VPLTeacherTools.StudentManagement.prototype.selectGroup = function (groupName) {
    this.selectedGroup = groupName;
};

VPLTeacherTools.StudentManagement.prototype.unselectGroup = function () {
    this.selectedGroup = "";
};

VPLTeacherTools.StudentManagement.prototype.isGroupSelected = function (groupName) {
    return this.selectedGroup === groupName;
};

VPLTeacherTools.StudentManagement.prototype.canAddStudent = function (name) {
    // check name is not empty and not already used
    name = name.trim();
    return name !== "" &&
        this.students.find(function (student) {
            return student.name === name;
        }) == undefined;
};

VPLTeacherTools.StudentManagement.prototype.addStudent = function (name) {
    name = name.trim();
    var self = this;
    this.client.addStudent(name, {
        onSuccess: function (r) {
            self.updateStudents();
        }
    });
};

VPLTeacherTools.StudentManagement.prototype.removeStudent = function (name) {
    name = name.trim();
    var self = this;
    this.client.removeStudent(name, {
        onSuccess: function (r) {
            self.updateStudents();
        }
    });
};
