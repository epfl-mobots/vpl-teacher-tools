window.addEventListener("load", function () {
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
	case "zip":
		console.info(fileContent);
		zip = new JSZip();
		zip.loadAsync(options.isBase64 ? atob(fileContent) : fileContent)
			.then(() => {
				var containerDiv = document.createElement("div");
				containerDiv.style.display = "table";
				containerDiv.style.height = "100%";
				containerDiv.style.width = "100%";
				containerDiv.style.overflow = "hidden";
				div.appendChild(containerDiv);

				var table = document.createElement("table");
				containerDiv.appendChild(table);

				zip.forEach((relativePath, file) => {
					if (!file.dir) {
						var tr = document.createElement("tr");
						table.appendChild(tr);
						var td = document.createElement("td");
						td.textContent = relativePath;
						tr.appendChild(td);
						console.info(file);
					}
				});
			});
		break;
	}
}, false);
