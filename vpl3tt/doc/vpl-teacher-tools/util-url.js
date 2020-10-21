
/** Get value corresponding to key in the URI query
	@param {string} key
	@return {string}
*/
VPLTeacherTools.getQueryOption = function (key) {
	var r = /^[^?]*\?([^#]*)/.exec(document.location.href);
	var query = r && r[1];
	if (query) {
		var pairs = query
			.split("&").map(function (p) {
				return p.split("=")
					.map(function (s) {
						return decodeURIComponent(s);
					});
				});
		for (var i = 0; i < pairs.length; i++) {
			if (pairs[i][0] === key) {
				return pairs[i][1];
			}
		}
	}
	return "";
}

/** Get value corresponding to key in the location hash
	@param {string} key
	@return {string}
*/
VPLTeacherTools.getHashOption = function (key) {
	var dict = (document.location.hash || "#")
		.slice(1)
		.split("&").map(function (p) {
			return p.split("=");
		})
		.reduce(function (acc, p) {
			acc[p[0]] = p[1];
			return acc;
		}, {});
	return dict[key] || null;
}
