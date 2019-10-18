
/**
    @constructor
    @param {Object} options
*/
VPLTeacherTools.FileBrowser = function (options) {
    this.files = [];
    this.options = options || {};
    this.filterStudent = null;
    this.filterLast = false;
	this.client = new VPLTeacherTools.HTTPClient();
    this.updateFiles();
};

VPLTeacherTools.FileBrowser.prototype.updateFiles = function () {
    var self = this;
	this.client.listFiles({
        filterStudent: this.filterStudent,
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
                self.options.onFiles(files, self);
            }
        }
	});
};

VPLTeacherTools.FileBrowser.prototype.fileIdToIndex = function (fileId) {
    return this.files.findIndex(function (file) { return file.id === fileId; });
};

VPLTeacherTools.FileBrowser.prototype.selectFile = function (fileId, toggleKey, extendKey) {
    var ix = this.fileIdToIndex(fileId);
    if (ix < 0) {
        return;
    }
    if (toggleKey) {
        if (ix >= 0) {
            this.files[ix].selected = !this.files[ix].selected;
        }
    } else if (extendKey) {
        if (!this.files[ix].selected) {
            // not already selected
            var state = 1;
                // 1=before first selected, 2=after first selected, 3=after clicked item before 1st selected
            for (var i = 0; i < this.files.length; i++) {
                if (this.files[i].id === fileId) {
                    if (state === 1) {
                        if (this.files[i].selected) {
                            break;  // extend by clicking first selected file: no op
                        }
                        // start selecting until first already selected
                        state = 3;
                        this.files[i].selected = true;
                    } else if (state === 2) {
                        this.files[i].selected = true;
                        break;
                    }
                } else if (state === 2) {
                    this.files[i].selected = true;
                } else if (state === 3) {
                    if (this.files[i].selected) {
                        break;  // stop extending
                    }
                    this.files[i].selected = true;
                } else if (this.files[i].selected) {
                    state = 2;
                }
            }
        }
    } else {
        for (var i = 0; i < this.files.length; i++) {
            this.files[i].selected = i === ix;
        }
    }
};

VPLTeacherTools.FileBrowser.prototype.unselectFile = function () {
    for (var i = 0; i < this.files.length; i++) {
        this.files[i].selected = false;
    }
};

VPLTeacherTools.FileBrowser.prototype.isFileSelected = function (fileId) {
    var ix = this.fileIdToIndex(fileId);
    return ix >= 0 && this.files[ix].selected;
};

VPLTeacherTools.FileBrowser.prototype.countSelectedFiles = function () {
    return this.files.reduce(function (acc, val) { return val.selected ? acc + 1 : acc; }, 0);
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
    return this.countSelectedFiles() == 1;
};

VPLTeacherTools.FileBrowser.prototype.openFiles = function () {
    if (this.canOpenFiles()) {
        var file = this.files.find(function (val) {
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
    return this.countSelectedFiles() == 1;
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
        var file = this.files.find(function (val) {
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
    return this.countSelectedFiles() > 0;
};

VPLTeacherTools.FileBrowser.prototype.deleteFiles = function () {
    var selectedFileIds = this.files.reduce(function (acc, val) {
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
