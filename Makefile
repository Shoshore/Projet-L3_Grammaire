# Variables pour les fichiers d'entrée et les scripts Python
INPUTS = test_cour_1.general test_cour_2.general test_complexe.general test_prof_1.general test_prof_2.general test_prof_3.general
INPUTS_NO_DOT = test_cour_1 test_cour_2 test_complexe test_prof_1 test_prof_2 test_prof_3
GRAMMAIRE_SCRIPT = grammaire.py
GENERER_SCRIPT = generer.py

# Taille par défaut (peut être personnalisée via une variableo d'environnement ou la ligne de commande)
SIZES = 10 5 15 7 8 15

# Cible par défaut (exécutée lorsque "make" est tapé)
all: run_examples

# Règle pour exécuter les programmes sur les fichiers d'exemple
run_examples:
	@echo "Exécution des transformations avec $(GRAMMAIRE_SCRIPT)..."
	@for file in $(INPUTS); do \
		echo "Traitement de $$file"; \
		python3 $(GRAMMAIRE_SCRIPT) $$file; \
	done
	@echo "Génération de mots avec $(GENERER_SCRIPT)..."
	@set -- $(SIZES); \
	for file in $(INPUTS_NO_DOT); do \
		size=$$1; shift; \
		echo "Génération pour $$file.chomsky avec taille $$size"; \
		python3 $(GENERER_SCRIPT) $$size $$file.chomsky; \
		echo "Génération pour $$file.greibach avec taille $$size"; \
		python3 $(GENERER_SCRIPT) $$size $$file.greibach; \
	done

# Nettoyage (si nécessaire, par exemple suppression des fichiers générés)
clean:
	@echo "Nettoyage des fichiers générés..."
	@rm -f *.chomsky *.greibach
