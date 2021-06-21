/** Set anchor element so that it downloads text
	@param {Element} anchor "a" element
	@param {string} text
	@param {string=} filename filename of downloaded file (default: "untitled.xml")
	@param {string=} mimetype mime type of downloaded file (default: "application/xml")
	@return {void}
*/
VPLTeacherTools.setAnchorDownload = function (anchor, text, filename, mimetype) {
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

/** Download text file
	@param {string} text
	@param {string=} filename filename of downloaded file (default: "untitled.xml")
	@param {string=} mimetype mime type of downloaded file (default: "application/xml")
	@return {void}
*/
VPLTeacherTools.downloadText = (function () {
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
		VPLTeacherTools.setAnchorDownload(anchor, text, filename, mimetype);
		anchor.click();
		if (typeof url !== "string") {
			window.URL.revokeObjectURL(url);
		}
	};
})();

/** Load modal box
	@param {function(*,string):void} loadFile
	@param {string} accept comma-separated list of dotted suffices
	@constructor
*/
VPLTeacherTools.Load = function (loadFile, title, accept) {
	var self = this;

	this.backgroundDiv = document.createElement("div");
	this.backgroundDiv.style.width = "100%";
	this.backgroundDiv.style.height = "100%";
	this.backgroundDiv.style.position = "fixed";
	this.backgroundDiv.style.top = "0";
	this.backgroundDiv.style.left = "0";
	this.backgroundDiv.style.zIndex = "1000";
	this.backgroundDiv.style.backgroundColor = "rgba(1,1,1,0.5)";
	this.backgroundDiv.style.display = "block";

	this.div = document.createElement("div");
	this.div.style.width = "40em";
	this.div.style.position = "fixed";
	this.div.style.top = "50%";
	this.div.style.left = "50%";
	this.div.style.backgroundColor = "white";
	this.div.style.padding = "2em";
	this.backgroundDiv.appendChild(this.div);
	document.body.appendChild(this.backgroundDiv);

	var el = document.createElement("p");
	el.textContent = title || "Open";
	this.div.appendChild(el);
	el = document.createElement("table");
	el.style.width = "100%";
	this.div.appendChild(el);
	var tr = document.createElement("tr");
	el.appendChild(tr);
	var td = document.createElement("td");
	tr.appendChild(td);
	this.input = document.createElement("input");
	this.input.setAttribute("type", "file");
	if (accept) {
		this.input.setAttribute("accept", accept);
	}
	this.input.style.width = "35em";
	td.appendChild(this.input);

	td = document.createElement("td");
	td.align = "right";
	tr.appendChild(td);
	var button = document.createElement("input");
	button.setAttribute("type", "button");
	button.setAttribute("value", "OK");
	button.addEventListener("click", function () {
		var file = self.input.files[0];
		if (file) {
			var reader = new window.FileReader();
			reader.onload = function (event) {
				var data = event.target.result;
				loadFile(data, file.name);
			};
			reader["readAsText"](file);
		}
		self.close();
	}, false);
	td.appendChild(button);

	td.appendChild(document.createTextNode("\u00a0\u00a0"));	// nbsp

	button = document.createElement("input");
	button.setAttribute("type", "button");
	button.setAttribute("value", "Cancel");
	button.addEventListener("click", function () {
		self.close();
	}, false);
	td.appendChild(button);

	// close box
	var closebox = document.createElement("div");
	closebox.style.position = "absolute";
	closebox.style.width = "32px";
	closebox.style.height = "32px";
	closebox.style.top = "0";
	closebox.style.left = "0";
	closebox.textContent = "\u00d7";	// times
	closebox.style.font = "bold 30px sans-serif";
	closebox.style.textAlign = "left";
	closebox.style.padding = "5px";
	closebox.style.paddingLeft = "10px";
	closebox.addEventListener("click", function () {
		self.close();
	}, false);
	el.appendChild(closebox);

	var boundingBox = this.div.getBoundingClientRect();
	this.div.style.marginLeft = (-boundingBox.width / 2) + "px";
	this.div.style.marginTop = (-boundingBox.height / 2) + "px";
};

/** Hide Load modal box
	@return {void}
*/
VPLTeacherTools.Load.prototype.close = function () {
    this.backgroundDiv.parentNode.removeChild(this.backgroundDiv);
};

/** Convert CSV (',' or ';' separator) or TSV data to array of array of strings,
	removing double-quotes
	@param {string} csv
	@return {Array.<{Array.<string>>}}
*/
VPLTeacherTools.convertFromCSV = function (csv) {
	var a = csv
		.replace(/\r\n/g, "\n")
		.replace(/\r/g, "\n")
		.split("\n")
		.map(function (line) {
			var a1 = [];
			for (var i = 0; i < line.length; ) {
				if (line[i] == "," || line[i] == ";" || line[i] == "\t") {
					a1.push("");
					i++;
				} else if (line[i] == "\"") {
					i++;
					var len;
					for (len = 0; i + len < line.length && line[i + len] != "\""; len++) {}
					a1.push(line.slice(i, i + len));
					i += len + 1;
				} else {
					var len;
					for (len = 0; i + len < line.length && line[i + len] != "," && line[i + len] != ";" && line[i + len] != "\t"; len++) {}
					a1.push(line.slice(i, i + len));
					i += len + 1;
				}
			}
			return a1;
		});
	if (a.length > 0 && a[a.length - 1].length === 0) {
		a.splice(a.length - 1, 1);
	}
	return a;
};
