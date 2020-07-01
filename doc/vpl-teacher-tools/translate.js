
VPLTeacherTools.translate = function(str, language) {
	/** @const */
	var en = {
		"Time (d)": "Time"
	};

	/** @const */
	var fr = {
		"add": "ajouter",
		"Blocks": "Blocs",
		"Class": "Classe",
		"Connection": "Connexion",
		"Dashboard": "Tableau de bord",
		"Default": "Défaut",
		"error:": "erreur:",
		"Filename": "Fichier",
		"Group": "Groupe",
		"hr": "h",
		"Import Pupil Names": "Importer les noms des élèves",
		"min": "min",
		"pupil local bridge": "passerelle locale",
		"(pupil local bridge)": "(passerelle locale)",
		"Marked": "Marque",
		"Message": "Message",
		"Name": "Nom",
		"no": "non",
		"Program": "Programme",
		"remove": "supprimer",
		"Rows": "Lignes",
		"sec": "s",
		"simulator": "simulateur",
		"(simulator)": "(simulateur)",
		"Size": "Taille",
		"Students": "Élèves",
		"Teacher": "Enseignant.e",
		"Time": "Heure",
		"Time (d)": "Temps",
		"warning:": "remarque:",
		"yes": "oui"
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
