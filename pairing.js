
VPLTeacherTools.Pairing = function (change) {
    var self = this;
    this.tdm = new window["TDM"](vplGetHashOption("w"),
		{
			"uuid": null,
			"change": change && function () {
				change(self);
			}
		});
};

VPLTeacherTools.Pairing.prototype.getRobots = function () {
    return this.tdm.nodes;
};

var pairing = new VPLTeacherTools.Pairing(function (pairing) {
    fillTable(pairing);
});
