
/** Connection from VPL (student tool) to server via WebSocket
*/
VPLTeacherTools.Connection = function (wsURL, sessionId) {
	this.wsURL = wsURL;
	/** @type {WebSocket} */
	this.ws = null;
	this.sessionId = sessionId;
	this.eventListeners = {};
};

/** Add an event listener
	@param {string} name "open" or "log"
	@return {void}
*/
VPLTeacherTools.Connection.prototype.addEventListener = function (name, cb) {
	if (this.eventListeners[name]) {
		this.eventListeners[name].push(cb);
	} else {
		this.eventListeners[name] = [cb];
	}
};

/** Execute the event listeners
	@param {string} name
	@return {void}
*/
VPLTeacherTools.Connection.prototype.callEventListeners = function (name, ev) {
	if (this.eventListeners[name]) {
		this.eventListeners[name].forEach(function (listener) {
			listener(ev);
		});
	}
};

/** Log a command
	@param {string} name
	@return {void}
*/
VPLTeacherTools.Connection.prototype.logCommand = function (name) {
	var msg = {
		"sender": {
			"type": "vpl",
			"sessionid": this.sessionId
		},
		"type": "log",
		"data": {
			"type": "cmd",
			"data": {
				"cmd": name
			}
		}
	};
	this.ws.send(JSON.stringify(msg));
}

/** Start websocket
	@return {void}
*/
VPLTeacherTools.Connection.prototype.connect = function () {
	var ws = new WebSocket(this.wsURL);
	var self = this;
	ws.addEventListener("open", function () {
		var helloMsg = {
			"sender": {
				"type": "vpl",
				"sessionid": self.sessionId
			},
			"type": "hello"
		};
		ws.send(JSON.stringify(helloMsg));
		self.callEventListeners("open", {"type": "open"})
	});
	ws.addEventListener("message", function (event) {
		try {
			var msg = JSON.parse(event.data);
console.info(msg);
			switch (msg["type"]) {
			case "log":
				self.callEventListeners("log", msg);
				break;
			}
		} catch (e) {
			console.info(e);
		}
	});
	this.ws = ws;
};
