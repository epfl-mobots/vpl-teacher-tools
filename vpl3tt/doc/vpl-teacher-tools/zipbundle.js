// requires jszip

// fixes for some jszip 3.6.0 issues

/**
    @constructor
	@extends {JSZip}
*/
VPLTeacherTools.JSZip = function () {
	JSZip.call(this);
};
VPLTeacherTools.JSZip.prototype = Object.create(JSZip.prototype);
VPLTeacherTools.JSZip.prototype.constructor = VPLTeacherTools.JSZip;

/**
	@inheritDoc
	@see https://github.com/Stuk/jszip/blob/master/lib/object.js
*/
VPLTeacherTools.JSZip.prototype.forEach = function (cb) {
	for (var path in this.files) {
		if (this.files.hasOwnProperty(path)
			&& path.slice(0, this.root.length) === this.root) {
			var filename = path.slice(this.root.length);
			if (/^[^\/]+\/?$/.test(filename)) {
				cb(filename, this.files[path]);
			}
		}
	}
};

/**
	@return {Array.<Object>}
*/
VPLTeacherTools.JSZip.prototype.getEntries = function () {
	var entries = [];
	this.forEach((relativePath, file) => {
		entries.push(file);
	});
	return entries;
};

/**
	@return {Array.<string>}
	@see https://github.com/Stuk/jszip/blob/master/lib/object.js
*/
VPLTeacherTools.JSZip.prototype.getCompleteFileList = function () {
	var paths = [];
	for (var path in this.files) {
		if (this.files.hasOwnProperty(path) && !this.files[path].dir) {
			paths.push(path);
		}
	}
	return paths;
};

/**
	@param {string} path
	@return {string}
*/
VPLTeacherTools.JSZip.getSuffix = function (path) {
	return /(\.[^.]*|)$/.exec(path)[0].slice(1);
}

/**
    @constructor
    @param {Object} options
*/
VPLTeacherTools.ZipBundle = function () {
	this.zip = null;
	this.toc = [];
	this.pathPrefix = "";
};

VPLTeacherTools.ZipBundle.prototype.load = function (zipContent, cb) {
	this.zip = new VPLTeacherTools.JSZip();
	this.toc = [];
	this.pathPrefix = "";
	this.zip.loadAsync(zipContent)
		.then(() => {

			// check if there is a single root directory
			this.pathPrefix = "";
			var rootEntries = this.zip.getEntries();
			if (rootEntries.length === 1 && rootEntries[0].dir) {
				this.pathPrefix = rootEntries[0].name;
			}

			this.toc = this.zip.getCompleteFileList();

			if (cb) {
				cb(this);
			}
		});
};
