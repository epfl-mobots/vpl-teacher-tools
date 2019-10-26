
/**
    @constructor
    @param {Object} options
*/
VPLTeacherTools.FileBrowser = function (options) {
    this.teacherFiles = [];
    this.studentFiles = [];
    this.options = options || {};
    this.filterTeacherLast = true;
    this.filterStudent = null;
    this.filterStudentLast = true;
	this.client = new VPLTeacherTools.HTTPClient();
    this.updateFiles();
};

VPLTeacherTools.FileBrowser.prototype.updateFiles = function () {
    var self = this;

	// teacher files
	this.client.listFiles({
        last: this.filterTeacherLast
    },
    {
		onSuccess: function (files) {
            self.teacherFiles = files.map(function (file) {
                var file1 = Object.create(file);    // prototype-based "copy"
                file1.selected = false;
                return file1;
            });
            if (self.options.onTeacherFiles) {
                self.options.onTeacherFiles(files, self);
            }
        }
	});
	this.client.listFiles({
        filterStudent: this.filterStudent || "*",
        last: this.filterStudentLast
    },
    {
		onSuccess: function (files) {
            self.studentFiles = files.map(function (file) {
                var file1 = Object.create(file);    // prototype-based "copy"
                file1.selected = false;
                return file1;
            });
            if (self.options.onStudentFiles) {
                self.options.onStudentFiles(files, self);
            }
        }
	});
};

VPLTeacherTools.FileBrowser.prototype.refreshFiles = function () {
    if (this.options.onTeacherFiles) {
        this.options.onTeacherFiles(this.teacherFiles, this);
    }
    if (this.options.onStudentFiles) {
        this.options.onStudentFiles(this.studentFiles, this);
    }
};

VPLTeacherTools.FileBrowser.prototype.fileIdToIndex = function (isStudentFile, fileId) {
    return (isStudentFile ? this.studentFiles : this.teacherFiles)
		.findIndex(function (file) { return file.id === fileId; });
};

VPLTeacherTools.FileBrowser.prototype.selectFile = function (isStudentFile, fileId, toggleKey, extendKey) {
    var ix = this.fileIdToIndex(isStudentFile, fileId);
    if (ix < 0) {
        return;
    }
	this.unselectFile(!isStudentFile);
	var files = isStudentFile ? this.studentFiles : this.teacherFiles;
    if (toggleKey) {
        if (ix >= 0) {
            files[ix].selected = !files[ix].selected;
        }
    } else if (extendKey) {
        if (!files[ix].selected) {
            // not already selected
            var state = 1;
                // 1=before first selected, 2=after first selected, 3=after clicked item before 1st selected
            for (var i = 0; i < files.length; i++) {
                if (files[i].id === fileId) {
                    if (state === 1) {
                        if (files[i].selected) {
                            break;  // extend by clicking first selected file: no op
                        }
                        // start selecting until first already selected
                        state = 3;
                        files[i].selected = true;
                    } else if (state === 2) {
                        files[i].selected = true;
                        break;
                    }
                } else if (state === 2) {
                    files[i].selected = true;
                } else if (state === 3) {
                    if (files[i].selected) {
                        break;  // stop extending
                    }
                    files[i].selected = true;
                } else if (files[i].selected) {
                    state = 2;
                }
            }
        }
    } else {
        for (var i = 0; i < files.length; i++) {
            files[i].selected = i === ix;
        }
    }
};

VPLTeacherTools.FileBrowser.prototype.unselectFile = function (isStudentFile) {
	var files = isStudentFile ? this.studentFiles : this.teacherFiles;
    for (var i = 0; i < files.length; i++) {
        files[i].selected = false;
    }
};

VPLTeacherTools.FileBrowser.prototype.isFileSelected = function (isStudentFile, fileId) {
    var ix = this.fileIdToIndex(isStudentFile, fileId);
    return ix >= 0 && (isStudentFile ? this.studentFiles : this.teacherFiles)[ix].selected;
};

VPLTeacherTools.FileBrowser.prototype.countSelectedFiles = function (isStudentFile) {
    return (isStudentFile ? this.studentFiles : this.teacherFiles)
		.reduce(function (acc, val) { return val.selected ? acc + 1 : acc; }, 0);
};

VPLTeacherTools.FileBrowser.prototype.canAddFile = function (filename, content, owner, isGroupOwner) {
    return filename != "" && owner != "";
};

VPLTeacherTools.FileBrowser.prototype.addFile = function (filename, content, owner, isGroupOwner) {
    var props = {};
    if (owner) {
        if (isGroupOwner) {
            props.groupName = owner;
        } else {
            props.studentName = owner;
        }
    }
    var self = this;
    this.client.addFile(filename, content,
        props,
        {
            onSuccess: function () {
                self.updateFiles();
            }
        });
};

VPLTeacherTools.FileBrowser.prototype.canOpenFiles = function () {
    return this.countSelectedFiles(false) + this.countSelectedFiles(true) == 1;
};

VPLTeacherTools.FileBrowser.prototype.openFiles = function () {
    if (this.canOpenFiles()) {
        var file = this.teacherFiles.find(function (val) {
            return val.selected;
        }) || this.studentFiles.find(function (val) {
            return val.selected;
        });
        var self = this;
        this.client.getFile(file.id, {
            onSuccess: function (file) {
                self.options.onOpen && self.options.onOpen(file);
            }
        });
    }
};

VPLTeacherTools.FileBrowser.prototype.canExportFiles = function () {
    return this.countSelectedFiles(false) + this.countSelectedFiles(true) == 1;
};

/** Set anchor element so that it downloads text
	@param {Element} anchor "a" element
	@param {string} text
	@param {string=} filename filename of downloaded file (default: "untitled.xml")
	@param {string=} mimetype mime type of downloaded file (default: "application/xml")
	@return {void}
*/
VPLTeacherTools.FileBrowser.setAnchorDownload = function (anchor, text, filename, mimetype) {
	mimetype = mimetype || "application/xml";
	/** @type {string} */
	var url;
	if (typeof window.Blob === "function" && window.URL) {
		// blob URL
		var blob = new window.Blob([text], {"type": mimetype});
		url = window.URL.createObjectURL(blob);
	} else {
		// data URL
		url = "data:" + mimetype + ";base64," + window["btoa"](text);
	}
	anchor.href = url;
	anchor["download"] = filename || "untitled.xml";
};

/** Download file
	@param {string} text
	@param {string=} filename filename of downloaded file (default: "untitled.xml")
	@param {string=} mimetype mime type of downloaded file (default: "application/xml")
	@return {void}
*/
VPLTeacherTools.FileBrowser.downloadText = (function () {
	// add a hidden anchor to document, which will be reused
	/** @type {Element} */
	var anchor = null;

	return function (text, filename, mimetype) {
		if (anchor === null) {
			anchor = document.createElement("a");
			document.body.appendChild(anchor);
			anchor.style.display = "none";
		}

		mimetype = mimetype || "application/xml";

		/** @type {string} */
		var url;
		if (typeof window.Blob === "function" && window.URL) {
			// blob URL
			var blob = new window.Blob([text], {"type": mimetype});
			url = window.URL.createObjectURL(blob);
		} else {
			// data URL
			url = "data:" + mimetype + ";base64," + window["btoa"](text);
		}
		VPLTeacherTools.FileBrowser.setAnchorDownload(anchor, text, filename, mimetype);
		anchor.click();
		if (typeof url !== "string") {
			window.URL.revokeObjectURL(url);
		}
	};
})();

VPLTeacherTools.FileBrowser.prototype.exportFiles = function () {
    if (this.canExportFiles()) {
        var file = this.teacherFiles.find(function (val) {
            return val.selected;
        }) || this.studentFiles.find(function (val) {
            return val.selected;
        });
        var self = this;
        this.client.getFile(file.id, {
            onSuccess: function (file) {
                var suffix = VPLTeacherTools.FileBrowser.getFileSuffix(file.filename);
                var mimetype = VPLTeacherTools.FileBrowser.suffixToMimetype(suffix);
                VPLTeacherTools.FileBrowser.downloadText(file.content, file.filename, mimetype);
            }
        });
    }
};

VPLTeacherTools.FileBrowser.prototype.canDeleteFiles = function () {
    return this.countSelectedFiles(false) + this.countSelectedFiles(true) > 0;
};

VPLTeacherTools.FileBrowser.prototype.deleteFiles = function () {
    var selectedFileIds = this.teacherFiles.concat(this.studentFiles).reduce(function (acc, val) {
        return val.selected ? acc.concat(val.id) : acc;
    }, []);
    if (selectedFileIds.length > 0) {
        var self = this;
        this.client.removeFiles(selectedFileIds, {
            onSuccess: function () {
                self.updateFiles();
            }
        });

    }
};

VPLTeacherTools.FileBrowser.getFileSuffix = function (filename) {
    return /(\.[^.]*|)$/.exec(filename)[0].slice(1);
};

VPLTeacherTools.FileBrowser.suffixToMimetype = function (suffix) {
    return {
        "gif": "image/gif",
        "html": "text/html",
        "jpg": "image/jpeg",
        "json": "application/json",
        "pdf": "application/pdf",
        "png": "image/png",
        "txt": "text/plain"
    }[suffix] || "application/octet-stream";
};
