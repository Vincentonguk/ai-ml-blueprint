# src/semantic/concepts.py
# Camada Semântica Interna (Core Concepts)
# - O sistema "pensa" em conceitos estáveis (IDs)
# - Idiomas são apenas renderização (skin), não lógica

CONCEPTS = {
    "APP_TITLE": {
        "pt": "🧠 ALIENGBUK",
        "en": "🧠 ALIENGBUK",
        "fr": "🧠 ALIENGBUK",
        "de": "🧠 ALIENGBUK",
    },

    "APP_TAGLINE": {
        "pt": "Base estável • Infraestrutura validada • Evolução consciente",
        "en": "Stable base • Validated infrastructure • Conscious evolution",
        "fr": "Base stable • Infrastructure validée • Évolution consciente",
        "de": "Stabile Basis • Validierte Infrastruktur • Bewusste Entwicklung",
    },

    "INTRO": {
        "pt": "Este aplicativo é construído como um **sistema vivo**, onde cada decisão, código ou ideia passa por **validação estrutural, temporal e contextual** antes de ser executada.",
        "en": "This app is built as a **living system**, where every decision, code, or idea goes through **structural, temporal, and contextual validation** before execution.",
        "fr": "Cette application est conçue comme un **système vivant**, où chaque décision, code ou idée passe par une **validation structurelle, temporelle et contextuelle** avant exécution.",
        "de": "Diese App wird als **lebendes System** aufgebaut, in dem jede Entscheidung, jeder Code oder jede Idee vor der Ausführung eine **strukturelle, zeitliche und kontextuelle Validierung** durchläuft.",
    },

    "SECTION_ARCH_TITLE": {
        "pt": "🧩 Construção do App & Observações Arquiteturais",
        "en": "🧩 App Construction & Architectural Notes",
        "fr": "🧩 Construction de l’App & Notes d’Architecture",
        "de": "🧩 App-Aufbau & Architekturnotizen",
    },

    "SPIRAL_MODEL": {
        "pt": "### 🌀 Modelo de Evolução em Espiral (Spiral-Up)\n\nEste sistema **não evolui por tentativa e erro cega**, nem por ciclos fechados.\n\nEle evolui em **espiral ascendente**, onde:\n\n- Nada é forçado a entrar onde não pertence\n- Nada é apagado apenas por não servir *agora*\n- O aprendizado é acumulado, não descartado\n\nO sistema **não gira em círculos** tentando encaixar algo à força.\nEle sobe em espiral, preservando coerência e contexto.",
        "en": "### 🌀 Spiral-Up Evolution Model\n\nThis system **does not evolve by blind trial-and-error**, nor by closed loops.\n\nIt evolves in an **ascending spiral**, where:\n\n- Nothing is forced where it doesn't belong\n- Nothing is deleted just because it doesn't fit *yet*\n- Learning is accumulated, not discarded\n\nThe system does **not spin in circles** trying to force-fit.\nIt rises in a spiral, preserving coherence and context.",
        "fr": "### 🌀 Modèle d’Évolution en Spirale (Spiral-Up)\n\nCe système **n’évolue pas par essais-erreurs aveugles**, ni par cycles fermés.\n\nIl évolue en **spirale ascendante**, où :\n\n- Rien n’est forcé là où il n’a pas sa place\n- Rien n’est supprimé seulement parce que ça ne convient pas *encore*\n- L’apprentissage est accumulé, non rejeté\n\nLe système ne tourne pas en rond.\nIl s’élève en spirale en préservant cohérence et contexte.",
        "de": "### 🌀 Spiral-Up-Entwicklungsmodell\n\nDieses System **entwickelt sich nicht durch blindes Trial-and-Error**, noch durch geschlossene Zyklen.\n\nEs entwickelt sich in einer **aufsteigenden Spirale**, in der:\n\n- Nichts wird erzwungen, wo es nicht hingehört\n- Nichts wird gelöscht, nur weil es *noch* nicht passt\n- Lernen wird aufgebaut, nicht verworfen\n\nDas System dreht sich nicht im Kreis.\nEs steigt spiralförmig auf und bewahrt Kohärenz und Kontext.",
    },

    "FIT_CRITERIA": {
        "pt": "### 🔍 Critérios de Encaixe\n\nAntes de qualquer alteração, o sistema avalia:\n\n- Objetivo atual\n- Estrutura existente\n- Dependências técnicas\n- Impacto e segurança\n- Maturidade do estágio\n\n👉 **Sem encaixe semântico, estrutural e temporal, nada é executado.**",
        "en": "### 🔍 Fit Criteria\n\nBefore any change, the system evaluates:\n\n- Current objective\n- Existing structure\n- Technical dependencies\n- Impact and safety\n- Stage maturity\n\n👉 **Without semantic, structural, and temporal fit, nothing is executed.**",
        "fr": "### 🔍 Critères d’Adéquation\n\nAvant toute modification, le système évalue :\n\n- Objectif actuel\n- Structure existante\n- Dépendances techniques\n- Impact et sécurité\n- Maturité de l’étape\n\n👉 **Sans adéquation sémantique, structurelle et temporelle, rien n’est exécuté.**",
        "de": "### 🔍 Passkriterien\n\nVor jeder Änderung bewertet das System:\n\n- Aktuelles Ziel\n- Bestehende Struktur\n- Technische Abhängigkeiten\n- Auswirkung und Sicherheit\n- Reifegrad der Phase\n\n👉 **Ohne semantische, strukturelle und zeitliche Passung wird nichts ausgeführt.**",
    },

    "NOT_RIGHT_MOMENT": {
        "pt": "### ⛔ Quando não é o momento certo\n\nSe um código, ideia ou comando **não encaixa**:\n\n- ❌ Não é executado\n- 🛡️ A estrutura atual é preservada\n- 🧩 As variáveis relevantes são armazenadas como candidatas\n\nNada é descartado — apenas aguardado conscientemente, até que o contexto correto apareça.",
        "en": "### ⛔ When it's not the right moment\n\nIf a code, idea, or command **does not fit**:\n\n- ❌ It is not executed\n- 🛡️ The current structure is preserved\n- 🧩 Relevant variables are stored as candidates\n\nNothing is discarded — only consciously deferred until the right context appears.",
        "fr": "### ⛔ Quand ce n’est pas le bon moment\n\nSi un code, une idée ou une commande **ne convient pas** :\n\n- ❌ Elle n’est pas exécutée\n- 🛡️ La structure actuelle est préservée\n- 🧩 Les variables pertinentes sont conservées comme candidates\n\nRien n’est jeté — seulement reporté consciemment jusqu’au bon contexte.",
        "de": "### ⛔ Wenn es nicht der richtige Zeitpunkt ist\n\nWenn ein Code, eine Idee oder ein Befehl **nicht passt**:\n\n- ❌ Wird nicht ausgeführt\n- 🛡️ Die aktuelle Struktur bleibt erhalten\n- 🧩 Relevante Variablen werden als Kandidaten gespeichert\n\nNichts wird verworfen — nur bewusst verschoben, bis der richtige Kontext entsteht.",
    },

    "PARAM_DRIFT": {
        "pt": "### 🛡️ Auto-detecção de Modificações (Parâmetros)\n\nO sistema detecta desvios de parâmetros em três níveis:\n\n- **Mínimos** → variações aceitáveis (ajustes finos)\n- **Médios** → mudanças relevantes (exigem reavaliação)\n- **Grandes** → mudanças estruturais (risco sistêmico)\n\n> Nada que deixe de ser aquilo que foi definido como essência pode prosseguir sem validação.\n\nQuando ultrapassa parâmetros esperados, o sistema reanalisa o cenário e identifica onde está sendo desviado ou reescrito.",
        "en": "### 🛡️ Modification Auto-Detection (Parameters)\n\nThe system detects parameter drift at three levels:\n\n- **Minor** → acceptable variations (fine-tuning)\n- **Medium** → relevant changes (require reassessment)\n- **Major** → structural changes (systemic risk)\n\n> Anything that stops being what was defined as essence cannot proceed without validation.\n\nWhen expected parameters are exceeded, the system re-checks the scenario and identifies where it is being diverted or rewritten.",
        "fr": "### 🛡️ Auto-détection des Modifications (Paramètres)\n\nLe système détecte les dérives de paramètres à trois niveaux :\n\n- **Minimes** → variations acceptables (ajustements fins)\n- **Moyennes** → changements pertinents (réévaluation nécessaire)\n- **Grandes** → changements structurels (risque systémique)\n\n> Rien qui cesse d’être l’essence définie ne peut avancer sans validation.\n\nLorsque les paramètres attendus sont dépassés, le système réanalyse le scénario et détecte où il est détourné ou réécrit.",
        "de": "### 🛡️ Automatische Änderungs-Erkennung (Parameter)\n\nDas System erkennt Parameterabweichungen auf drei Ebenen:\n\n- **Klein** → akzeptable Variationen (Feintuning)\n- **Mittel** → relevante Änderungen (Neubewertung erforderlich)\n- **Groß** → strukturelle Änderungen (systemisches Risiko)\n\n> Was nicht mehr der definierten Essenz entspricht, darf ohne Validierung nicht fortfahren.\n\nBei Überschreitung erwarteter Parameter analysiert das System das Szenario neu und erkennt, wo es abgelenkt oder umgeschrieben wird.",
    },
}

def t(concept_id: str, lang: str = "pt") -> str:
    \"\"\"Translate by concept id. Falls back to PT then EN then id.\"\"\"
    entry = CONCEPTS.get(concept_id, {})
    return entry.get(lang) or entry.get("pt") or entry.get("en") or concept_id
