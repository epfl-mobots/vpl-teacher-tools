
/**
    @constructor
    @param {Object} options
*/
VPLTeacherTools.StudentManagement = function (options) {
    this.options = options || {};
    this.students = [];
    this.editedStudent = null;
    this.focusOnClass = false;
    this.filterClass = "";

	this.client = new VPLTeacherTools.HTTPClient();
	this.client.onInvalidToken = function () {
		document.getElementById("token-error-msg").style.display = "block";
	};

    if (options.onStudents) {
        this.students = [];
        options.onStudents([], this);
    }
    this.updateStudents();
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

VPLTeacherTools.StudentManagement.prototype.updateStudents = function () {
    var self = this;
	this.client.listStudents(this.filterClass, {
		onSuccess: function (students) {
            self.students = students;
            if (self.options.onStudents) {
                self.options.onStudents(students, self);
            }
        }
	});
};

VPLTeacherTools.StudentManagement.prototype.canAddStudent = function (name) {
    // check name is not empty and not already used
    name = name.trim();
    return name !== "" &&
        this.students.find(function (student) {
            return student.name === name;
        }) == undefined;
};

VPLTeacherTools.StudentManagement.prototype.addStudent = function (name, className) {
    name = name.trim();
    className = className && className.trim();
    var self = this;
    this.client.addStudent(name, className, {
        onSuccess: function (r) {
            self.updateStudents();
        }
    });
};

VPLTeacherTools.StudentManagement.prototype.addStudents = function (names, classNames) {
    var self = this;
    this.client.addStudents(names, classNames, {
        onSuccess: function (r) {
            self.updateStudents();
        }
    });
};

VPLTeacherTools.StudentManagement.prototype.editStudent = function (name, focusOnClass) {
    name = name.trim();
    if (this.editedStudent) {
        // already editing: cancel
        return;
    }

    for (var i = 0; i < this.students.length; i++) {
        if (name === this.students[i].name) {
            // found
            this.editedStudent = name;
            this.focusOnClass = focusOnClass === true;
            this.updateStudents();
            return;
        }
    }
};

VPLTeacherTools.StudentManagement.prototype.cancelEditStudent = function () {
    this.editedStudent = null;
    this.updateStudents();
};

VPLTeacherTools.StudentManagement.prototype.acceptEditStudent = function (newName, newClassName) {
    newName = newName.trim();
    newClassName = newClassName && newClassName.trim();
    var self = this;
    this.client.updateStudent(self.editedStudent, newName, newClassName, {
        onSuccess: function (r) {
            self.editedStudent = null;
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
