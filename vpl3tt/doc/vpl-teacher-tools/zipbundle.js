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
	this.manifest = new VPLTeacherTools.ZipBundle.Manifest();
};

VPLTeacherTools.ZipBundle.prototype.load = function (zipContent, cb) {
	this.zip = new VPLTeacherTools.JSZip();
	this.toc = [];
	this.pathPrefix = "";
	var self = this;
	this.zip.loadAsync(zipContent)
		.then(() => {

			// check if there is a single root directory
			this.pathPrefix = "";
			var rootEntries = this.zip.getEntries();
			if (rootEntries.length === 1 && rootEntries[0].dir) {
				this.pathPrefix = rootEntries[0].name;
			}

			this.toc = this.zip.getCompleteFileList()
				.map((path) => path.slice(this.pathPrefix.length));

			var manifestFile = self.zip.file(this.pathPrefix + "manifest.txt");
			if (manifestFile) {
				manifestFile.async("string").then((manifestSrc) => {
					self.manifest.parse(manifestSrc, self.toc);
					if (cb) {
						cb(this);
					}
				});
			} else if (cb) {
				cb(this);
			}
		});
};

/**
	@param {string} filename
	@return VPLTeacherTools.ZipBundle.Manifest.File.Type
*/
VPLTeacherTools.ZipBundle.prototype.getType = function (filename) {
	var manifestFile = this.manifest.getEntry(filename);
	return manifestFile
		? manifestFile.type
		: VPLTeacherTools.ZipBundle.Manifest.File.Type.unknown;
};

/**
	@constructor
*/
VPLTeacherTools.ZipBundle.Manifest = function () {
	this.src = "";
	/** @type {Array.<VPLTeacherTools.ZipBundle.Manifest.File>} */
	this.files = [];
};

/**
	@param {string} src
	@param {Array.<string>} filenames
	@return {void}
*/
VPLTeacherTools.ZipBundle.Manifest.prototype.parse = function (src, filenames) {
	this.files = [];
	var lines = src.split("\n").map((line) => line.trim());
	for (var i = 0; i < lines.length; i++) {
		if (lines[i].slice(-1) === ":") {
			var type = VPLTeacherTools.ZipBundle.Manifest.File.Type.unknown;
			switch (lines[i].slice(0, -1).trim().toLowerCase()) {
			case "vpl3":
				type = VPLTeacherTools.ZipBundle.Manifest.File.Type.vpl3;
				break;
			case "ui":
				type = VPLTeacherTools.ZipBundle.Manifest.File.Type.ui;
				break;
			case "attention":
				type = VPLTeacherTools.ZipBundle.Manifest.File.Type.attention;
				break;
			case "doc":
				type = VPLTeacherTools.ZipBundle.Manifest.File.Type.doc;
				break;
			case "statement":
				type = VPLTeacherTools.ZipBundle.Manifest.File.Type.statement;
				break;
			}
			if (type !== VPLTeacherTools.ZipBundle.Manifest.File.Type.unknown) {
				var re = /([-_\/.a-z0-9]+)(\s+\([^)]*\))?$/i;
				for (; i + 1 < lines.length; i++) {
					var line = lines[i + 1];
					if (line != "") {
						var r = re.exec(line);
						if (r == null) {
							break;
						}
						var filename = r[1];
						if (filenames.indexOf(filename) >= 0) {
							this.files.push(new VPLTeacherTools.ZipBundle.Manifest.File(filename, type));
						}
					}
				}
			}
		}
	}
};

/**
	@param {string} filename
	@return VPLTeacherTools.ZipBundle.Manifest.File
*/
VPLTeacherTools.ZipBundle.Manifest.prototype.getEntry = function (filename) {
	for (var i = 0; i < this.files.length; i++) {
		if (this.files[i].filename === filename) {
			return this.files[i];
		}
	}
	return null;
};

/**
	@constructor
	@param {string} filename
	@param {VPLTeacherTools.ZipBundle.Manifest.File.Type} type
*/
VPLTeacherTools.ZipBundle.Manifest.File = function (filename, type) {
	this.filename = filename;
	this.type = type;
};

/** @enum {number} */
VPLTeacherTools.ZipBundle.Manifest.File.Type = {
	unknown: 0,
	vpl3: 1,
	ui: 2,
	attention: 3,
	doc: 4,
	statement: 5
};