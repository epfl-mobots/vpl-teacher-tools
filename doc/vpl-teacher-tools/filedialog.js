/*
	Copyright 2019-2020 ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE,
	Miniature Mobile Robots group, Switzerland
	Author: Yves Piguet

	Licensed under the 3-Clause BSD License;
	you may not use this file except in compliance with the License.
	You may obtain a copy of the License at
	https://opensource.org/licenses/BSD-3-Clause
*/

/** @fileoverview

Modal box for selecting a file.

*/

/** Load modal box
	@constructor
	@param {{
		ok: string,
		cancel: string,
		title: string
	}} msg
	@param {{
		accept: (string | undefined),
		multiple: (boolean | undefined)
	}=} options options (accept: dotted comma-separated suffices)
*/
LoadModalDialog = function (msg, options) {
	var self = this;

	this.backgroundDiv = document.createElement("div");
	this.backgroundDiv.style.width = "100%";
	this.backgroundDiv.style.height = "100%";
	this.backgroundDiv.style.position = "fixed";
	this.backgroundDiv.style.top = "0";
	this.backgroundDiv.style.left = "0";
	this.backgroundDiv.style.zIndex = "1000";
	this.backgroundDiv.style.backgroundColor = "rgba(1,1,1,0.5)";
	this.backgroundDiv.style.display = "none";

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
	el.textContent = msg["title"];
	this.div.appendChild(el);
	el = document.createElement("table");
	el.style.width = "100%";
	this.div.appendChild(el);
	var tr = document.createElement("tr");
	el.appendChild(tr);
	var td = document.createElement("td");
	tr.appendChild(td);
	var fileInput = document.createElement("input");
	fileInput.setAttribute("type", "file");
	if (options && options.accept) {
		fileInput.setAttribute("accept", options.accept);
	}
	fileInput.setAttribute("multiple", options && options.multiple ? true : false);
	fileInput.style.width = "35em";
	td.appendChild(fileInput);

	td = document.createElement("td");
	td.align = "right";
	tr.appendChild(td);
	var button = document.createElement("input");
	button.setAttribute("type", "button");
	button.setAttribute("value", msg["ok"]);
	button.addEventListener("click", function () {
		var files = [];
		for (var i = 0; i < fileInput.files.length; i++) {
			files.push(fileInput.files[i]);
		}
		self.loadFun(files);
		self.hide();
	}, false);
	td.appendChild(button);

	td.appendChild(document.createTextNode("\u00a0\u00a0"));	// nbsp

	button = document.createElement("input");
	button.setAttribute("type", "button");
	button.setAttribute("value", msg["cancel"]);
	button.addEventListener("click", function () {
		self.hide();
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
		self.hide();
	}, false);
	el.appendChild(closebox);

	this.loadFun = null;
};

/** Show Load modal box
	@param {string} accept file input attribute "accept"
	(comma-separated dotted file extensions
	@param {function(File):void} loadFun
	@return {void}
*/
LoadModalDialog.prototype.show = function (loadFun) {
	this.loadFun = loadFun;
	this.backgroundDiv.style.display = "block";
	var boundingBox = this.div.getBoundingClientRect();
	this.div.style.marginLeft = (-boundingBox.width / 2) + "px";
	this.div.style.marginTop = (-boundingBox.height / 2) + "px";
};

/** Hide Load modal box
	@return {void}
*/
LoadModalDialog.prototype.hide = function () {
	this.backgroundDiv.style.display = "none";
};
