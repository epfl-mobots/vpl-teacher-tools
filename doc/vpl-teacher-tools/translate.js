
VPLTeacherTools.translate = function(str, language) {
	/** @const */
	var fr = {
		"add": "ajouter",
		"Dashboard": "Tableau de bord",
		"Default": "Défaut",
		"Filename": "Nom de fichier",
		"Group": "Groupe",
		"pupil local bridge": "passerelle locale",
		"(pupil local bridge)": "(passerelle locale)",
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
