function renderViewer () {
	var fileContent = sessionStorage.getItem("initialFileContent");
	var options = JSON.parse(sessionStorage.getItem("options"));

	var div = document.getElementById("viewer");

	switch (options.suffix) {
	case "txt":
		var pre = document.createElement("pre");
		pre.textContent = fileContent;
		div.appendChild(pre);
		break;
	case "html":
		div.innerHTML = fileContent;
		break;
	case "jpg":
	case "png":
	case "svg":
		var containerDiv = document.createElement("div");
		containerDiv.style.display = "table";
		containerDiv.style.height = "100%";
		containerDiv.style.width = "100%";
		containerDiv.style.overflow = "hidden";
		div.appendChild(containerDiv);

		var containerDiv2 = document.createElement("div");
		containerDiv2.style.display = "table-cell";
		containerDiv2.style.verticalAlign = "middle";
		containerDiv2.style.textAlign = "center";
		containerDiv2.style.overflow = "hidden";
		containerDiv.appendChild(containerDiv2);

		var img = document.createElement("img");
		img.src = "data:" + options.mimetype +  ";base64," + (options.isBase64 ? fileContent : btoa(fileContent));
		img.style.maxWidth = "100%";
		img.style.maxHeight = "100%";
		containerDiv2.appendChild(img);

		var divComputedStyle = window.getComputedStyle(div);
		div.style.height = (window.innerHeight - div.getBoundingClientRect().y
			- parseFloat(divComputedStyle["margin-top"])
			- parseFloat(divComputedStyle["margin-bottom"])) + "px";
		break;
	case "vpl3":
		var containerDiv = document.createElement("div");
		var html = window["vplConvertToHTML"](fileContent, false);
		containerDiv.innerHTML = html;
		break;
	case "vpl3ui":
		var containerDiv = document.createElement("div");
		var html = window["vplConvertToHTML"](fileContent, true);
		containerDiv.innerHTML = html;
		break;
	case "zip":
		var zipContent = options.isBase64 ? atob(fileContent) : fileContent;
		var zipbundle = new VPLTeacherTools.ZipBundle();
		zipbundle.load(zipContent, () => {
			var containerDiv = document.createElement("div");
			containerDiv.style.display = "table";
			containerDiv.style.height = "100%";
			containerDiv.style.width = "100%";
			containerDiv.style.overflow = "hidden";
			div.appendChild(containerDiv);

			var dl = document.createElement("dl");
			containerDiv.appendChild(dl);

			for (var i = 0; i < zipbundle.toc.length; i++) {
				var path = zipbundle.toc[i];
				var dt = document.createElement("dt");
				dl.appendChild(dt);
				var codeEl = document.createElement("code");
				codeEl.textContent = path;
				dt.appendChild(codeEl);

				// content
				var suffix = VPLTeacherTools.JSZip.getSuffix(path);

				var contentContainer = null;
				switch (suffix) {
				case "txt":
					contentContainer = document.createElement("div");
					var pre = document.createElement("pre");
					((pre) => {
						zipbundle.zip.file(zipbundle.pathPrefix + path).async("string").then((data) => {
							pre.textContent = data;
						});
					})(pre);
					contentContainer.appendChild(pre);
					break;
				case "jpg":
				case "png":
				case "svg":
					contentContainer = document.createElement("div");
					var img = document.createElement("img");
					((img, suffix) => {
						zipbundle.zip.file(zipbundle.pathPrefix + path).async("uint8array").then((data) => {
							var dataAsString = String.fromCharCode(...data);	// crazy, but required to give a string to btoa
							img.src = "data:image/" + {"jpg":"jpeg","png":"png","svg":"svg+xml"}[suffix] +  ";base64," + btoa(dataAsString);
						});
					})(img, suffix);
					img.style.maxWidth = "100%";
					img.style.maxHeight = "100%";
					contentContainer.appendChild(img);
					break;
				case "vpl3":
					contentContainer = document.createElement("div");
					((div) => {
						zipbundle.zip.file(zipbundle.pathPrefix + path).async("string").then((data) => {
							var html = "";
							try {
								var obj = JSON.parse(data);
								if (obj.program.length > 0) {
									// not empty
									html = window["vplConvertToHTML"](data, false);
								}
							} catch (e) {}
							if (html === "") {
								html = "<p>&mdash;</p>"
							}
							div.innerHTML = html;
						});
					})(contentContainer);
					break;
				case "vpl3ui":
					contentContainer = document.createElement("div");
					((div) => {
						zipbundle.zip.file(zipbundle.pathPrefix + path).async("string").then((data) => {
							var html = window["vplConvertToHTML"](data, true);
							div.innerHTML = html;
						});
					})(contentContainer);
					break;
				}

				if (contentContainer != null) {
					contentContainer.style.margin = "1ex";
					contentContainer.style.padding = "1ex";
					contentContainer.style.border = "1px solid silver";
					var dd = document.createElement("dd");
					dd.appendChild(contentContainer);
					dl.appendChild(dd);
				}
			}
		});
		break;
	}
}

window.addEventListener("DOMContentLoaded", function () {
	setTimeout(renderViewer, 500);
}, false);
