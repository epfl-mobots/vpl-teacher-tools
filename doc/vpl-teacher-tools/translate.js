
VPLTeacherTools.translate = function(str, language) {
	/** @const */
	var fr = {
		"add": "ajouter",
		"Default": "Défaut",
		"Filename": "Nom de fichier",
		"Group": "Groupe",
		"local bridge": "passerelle locale",
		"(local bridge)": "(passerelle locale)",
		"Marked": "Marque",
		"remove": "supprimer",
		"simulator": "simulateur",
		"(simulator)": "(simulateur)",
		"Size": "Taille",
		"Students": "Élèves",
		"Time": "Heure"
	};

	var dict = {
		"fr": fr
	};

	var tr = (dict[language || uiLanguage] || {})[str];
	return tr || str;
};

VPLTeacherTools.translateArray = function (a, language) {
	return a.map(function (str) {
		return VPLTeacherTools.translate(str, language);
	});
};
