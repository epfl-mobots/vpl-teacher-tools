
VPLTeacherTools.translate = function(str, language) {
	/** @const */
	var en = {
		"Time (d)": "Time"
	};

	/** @const */
	var fr = {
		"add": "ajouter",
		"Dashboard": "Tableau de bord",
		"Default": "Défaut",
		"Filename": "Fichier",
		"Group": "Groupe",
		"pupil local bridge": "passerelle locale",
		"(pupil local bridge)": "(passerelle locale)",
		"Marked": "Marque",
		"Message": "Message",
		"remove": "supprimer",
		"simulator": "simulateur",
		"(simulator)": "(simulateur)",
		"Size": "Taille",
		"Students": "Élèves",
		"Time": "Heure",
		"Time (d)": "Temps",
		"# blocks": "# blocs",
		"# rules": "# règles"
	};

	var dict = {
		"en": en,
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
