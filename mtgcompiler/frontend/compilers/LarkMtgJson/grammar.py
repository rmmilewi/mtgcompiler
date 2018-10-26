def getGrammar():
        return r"""
        typeline: typelinesupert typelinet ("—" typelinesubt)?
        typelinesupert: SUPERTYPE*
        typelinet: TYPE*
        typelinesubt: (SUBTYPESPELL | SUBTYPELAND | SUBTYPEARTIFACT | SUBTYPEENCHANTMENT | SUBTYPEPLANESWALKER | SUBTYPECREATUREA | SUBTYPECREATUREB | SUBTYPEPLANAR)*

        //[NOTE: Added support for starting reminder text, but what does it attach to?]
        cardtext : remindertext? ability? ("\n" ability)* //[TODO: Do we need to explicitly recognize newlines? We might in order to separate distinct abilities.]
        remindertext : /\(.*?\)/

        ability : abilityword? statementblock remindertext? -> regularability
        | keywordlist remindertext?
        abilityword: WORD "—"

        keywordlist: keywordsequence
        keywordsequence: keywordability | keywordsequence ("," | ";") keywordability

        statementblock : (statement ["."])+

        //STATEMENTS

        statement: compoundstatement
        | expressionstatement
        | conditionalstatement 
        | activationstatement
        | beingstatement
        | dostatement
        | thenstatement
        | insteadstatement
        | maystatement
        | wouldstatement
        | additionalcoststatement
        | modalstatement

        thenstatement: "then" statement
        insteadstatement: statement "instead"
        maystatement:  playerdeclref? ("may" | "may" "have") statement
        wouldstatement: playerdeclref? "would" statement
        additionalcoststatement: "as" "an" "additional" "cost" "to" statement "," statement
        modalstatement: "choose" valuecardinal DASH (modalchoiceexpression)+
        modalchoiceexpression: MODALCHOICE statementblock

        dostatement: declarationorreference? ("do" | "does") statement? -> dostatement
        | declarationorreference? ("do" "not" | "does" "not") statement? -> dontstatement

        beingstatement: isstatement
        | hasstatement
        | isntstatement
        | canstatement
        | becomesstatement
        | costchangestatement
        | wherestatement

        !isstatement: declarationorreference ("is" | "was" | "are" "each"?) ("still"|"not")? (declarationorreference | characteristicexpression | statement)
        !hasstatement: declarationorreference? ("has"|"have"|"had") (abilitysequencestatement | characteristicexpression | beexpression | statement)
        | declarationorreference?  ("has"|"have"|"had") ("a"|valueexpression) countertype "counter"["s"] "on" declarationorreference -> hascounterstatement
        isntstatement: declarationorreference? "is" "not" statement
        canstatement: declarationorreference? "can" statement
        | declarationorreference? "can" "not" statement -> cantstatement
        becomesstatement: declarationorreference? "become"["s"] genericdeclarationexpression
        costchangestatement: declarationorreference "cost"["s"] manasymbolexpression "more" "to" "cast" -> costincreasestatement
        | declarationorreference "cost"["s"] manasymbolexpression "less" "to" "cast" -> costreductionstatement
        wherestatement: statement "," "where" statement //[Note: Used in elaborating variables.]

        expressionstatement: (effectexpression | beexpression | valueexpression) timeexpression? //[TODO: Do time expressions need to go here?]
        beexpression: ("be"|"been") modifier valueexpression? ("by" declarationorreference)? timeexpression?//[TODO: Not sure how to categorize this one yet.]
        activationstatement: cost ":" statementblock

        compoundstatement: statement  ("," statement)* ","? "then" statement -> compoundthenstatement
        | statement ("," statement)* ","? "and" statement -> compoundandstatement
        | statement ("," statement)* ","? "or" statement -> compoundorstatement

        conditionalstatement: ifstatement
        | wheneverstatement
        | whenstatement
        | atstatement
        | aslongasstatement
        | forstatement
        | untilstatement
        | afterstatement
        | otherwisestatement
        | unlessstatement
        | asstatement
        | whilestatement
        | duringstatement
        | exceptstatement
        | ratherstatement
        | nexttimestatement
        | beforestatement

        ifstatement: "if" statement "," statement
        | statement "only"? "if" statement -> ifstatementinv

        wheneverstatement:  "whenever" statement timeexpression? "," statement 
        | statement "whenever" statement timeexpression? -> wheneverstatementinv

        whenstatement:  "when" statement "," statement 
        | statement "when" statement -> whenstatementinv

        atstatement:  "at" timeexpression "," statement 
        | statement "at" timeexpression -> atstatementinv

        aslongasstatement:  "for"? "as" "long" "as" statement "," statement
        | statement "for"? "as" "long" "as" statement -> aslongasstatementinv

        forstatement:  "for" "each" (genericdeclarationexpression | "time" statement) ("beyond" "the" "first")? "," statement 
        | statement "for" "each" (genericdeclarationexpression | "time" statement) ("beyond" "the" "first")? -> forstatementinv

        untilstatement:  "until" timeexpression "," statement 
        | statement "until" timeexpression -> untilstatementinv

        afterstatement:  "after" timeexpression "," statement 
        | statement "after" timeexpression -> afterstatementinv

        otherwisestatement: "otherwise" "," statement

        unlessstatement:  statement "unless" statement

        asstatement: "as" statement "," statement -> asstatement

        whilestatement:  "while" statement "," statement

        duringstatement:  statement "during" timeexpression
        | statement "only" "during" timeexpression -> exclusiveduringstatement

        exceptstatement:  statement "except" (("by"|"for") genericdeclarationexpression | statement)

        ratherstatement:  statement "rather" "than" statement

        nexttimestatement: "the" "next" "time" statement timeexpression? "," statement

        beforestatement: statement "before" (timeexpression | statement)

        //KEYWORD ABILITIES

        abilitysequencestatement: (keywordability | quotedabilitystatement) (("," (keywordability | quotedabilitystatement) ",")* ("and" (keywordability | quotedabilitystatement)))?
        quotedabilitystatement: "\"" statementblock "\""

        keywordability: kwdeathtouch
        | kwdefender | kwdoublestrike | kwenchant | kwequip | kwfirststrike
        | kwflash | kwflying | kwhaste | kwhexproof | kwindestructible
        | kwintimidate | kwlandwalk | kwlifelink | kwprotection | kwreach 
        | kwshroud | kwtrample | kwvigilance | kwbanding 
        | kwrampage | kwcumulativeupkeep | kwflanking | kwphasing
        | kwbuyback | kwshadow | kwcycling | kwecho | kwhorsemanship
        | kwfading | kwkicker | kwflashback | kwmadness | kwfear
        | kwmorph | kwamplify | kwprovoke | kwstorm | kwaffinity
        | kwentwine | kwmodular | kwsunburst | kwbushido | kwsoulshift
        | kwsplice | kwoffering |kwninjutsu | kwepic | kwconvoke
        | kwdredge | kwtransmute | kwbloodthirst | kwhaunt | kwreplicate
        | kwforecast | kwgraft | kwrecover | kwripple | kwsplitsecond
        | kwsuspend | kwvanishing | kwabsorb | kwauraswap | kwdelve
        | kwfortify | kwfrenzy | kwgravestorm | kwpoisonous | kwtransfigure
        | kwchampion | kwchangeling | kwevoke | kwhideaway | kwprowl
        | kwreinforce | kwconspire | kwpersist | kwwither | kwretrace
        | kwdevour | kwexalted | kwunearth | kwcascade | kwannihilator
        | kwlevelup | kwrebound | kwtotemarmor | kwinfect | kwbattlecry
        | kwlivingweapon | kwundying | kwmiracle | kwsoulbond | kwoverload
        | kwscavenge | kwunleash |kwcipher | kwevolve | kwextort
        | kwfuse | kwbestow | kwtribute | kwdethrone | kwhiddenagenda
        | kwoutlast | kwprowess | kwdash | kwexploit | kwmenace
        | kwrenown | kwawaken | kwdevoid | kwingest | kwmyriad
        | kwsurge | kwskulk | kwemerge | kwescalate | kwmelee
        | kwcrew | kwfabricate | kwpartner | kwundaunted | kwimprovise
        | kwaftermath | kwembalm | kweternalize | kwafflict | kwascend
        | kwassist

        kwdeathtouch: "deathtouch"
        kwdefender: "defender"
        kwdoublestrike: "double" "strike"
        kwenchant: "enchant" genericdescriptionexpression
        kwequip: "equip" cost | "equip" genericdescriptionexpression cost
        kwfirststrike: "first strike"
        kwflash: "flash"
        kwflying: "flying"
        kwhaste: "haste"
        kwhexproof: "hexproof" | "hexproof" "from" genericdescriptionexpression
        kwindestructible: "indestructible"
        kwintimidate: "intimidate"
        kwlandwalk: typeexpression "walk"
        kwlifelink: "lifelink"
        kwprotection: "protection" "from" genericdescriptionexpression ("and" "from" genericdescriptionexpression)*
        kwreach: "reach"
        kwshroud: "shroud"
        kwtrample: "trample"
        kwvigilance: "vigilance"
        kwbanding: "banding" | "bands" "with" "other" genericdescriptionexpression
        kwrampage: "rampage" valuenumber
        kwcumulativeupkeep: "cumulative" "upkeep" cost
        kwflanking: "flanking"
        kwphasing: "phasing"
        kwbuyback: "buyback" cost
        kwshadow: "shadow"
        kwcycling: [typeexpression] "cycling" cost
        kwecho: "echo" cost
        kwhorsemanship: "horsemanship"
        kwfading: "fading" valuenumber
        kwkicker: "kicker" cost -> kicker
        | "multikicker" cost -> multikicker
        kwflashback: "flashback" cost
        kwmadness: "madness" cost
        kwfear: "fear"
        kwmorph: "morph" cost -> kwmorph
        | "megamorph" cost -> kwmegamorph
        kwamplify: "amplify" valuenumber
        kwprovoke: "provoke"
        kwstorm: "storm"
        kwaffinity: "affinity" "for" typeexpression
        kwentwine: "entwine" cost
        kwmodular: "modular" valuenumber
        kwsunburst: "sunburst"
        kwbushido: "bushido" valuenumber
        kwsoulshift: "soulshift" valuenumber
        kwsplice: "splice" "onto" typeexpression cost
        kwoffering: typeexpression "offering"
        kwninjutsu: "ninjutsu" cost
        kwepic: "epic"
        kwconvoke: "convoke"
        kwdredge: "dredge" valuenumber
        kwtransmute: "transmute" cost
        kwbloodthirst: "bloodthirst" valuenumber
        kwhaunt: "haunt"
        kwreplicate: "replicate" cost
        kwforecast: "forecast" activationstatement
        kwgraft: "graft"
        kwrecover: "recover" cost
        kwripple: "ripple" valuenumber
        kwsplitsecond: "split" "second"
        kwsuspend: "suspend" valuenumber cost 
        kwvanishing: "vanishing" [valuenumber]
        kwabsorb: "absorb" valuenumber
        kwauraswap: "aura" "swap" cost
        kwdelve: "delve"
        kwfortify: "fortify" cost
        kwfrenzy: "frenzy"
        kwgravestorm: "gravestorm"
        kwpoisonous: "poisonous" valuenumber
        kwtransfigure: "transfigure" cost
        kwchampion: "champion" "a"["n"] typeexpression
        kwchangeling: "changeling"
        kwevoke: "evoke" cost
        kwhideaway: "hideaway"
        kwprowl: "prowl" cost
        kwreinforce: "reinforce" cost
        kwconspire: "conspire"
        kwpersist: "persist"
        kwwither: "wither"
        kwretrace: "retrace" cost
        kwdevour: "devour" valuenumber
        kwexalted: "exalted"
        kwunearth: "unearth" cost
        kwcascade: "cascade"
        kwannihilator: "annihilator" valuenumber
        kwlevelup: "level up" cost
        kwrebound: "rebound"
        kwtotemarmor: "totem" "armor"
        kwinfect: "infect"
        kwbattlecry: "battle" "cry"
        kwlivingweapon: "living" "weapon"
        kwundying: "undying"
        kwmiracle: "miracle" cost
        kwsoulbond: "soulbond"
        kwoverload: "overload" cost
        kwscavenge: "scavenge" cost
        kwunleash: "unleash"
        kwcipher: "cipher"
        kwevolve: "evolve"
        kwextort: "extort"
        kwfuse: "fuse"
        kwbestow: "bestow" cost
        kwtribute: "tribute" valuenumber
        kwdethrone: "dethrone"
        kwhiddenagenda: "hidden" "agenda" -> kwhiddenagenda
        | "double" "agenda" -> kwdoubleagenda
        kwoutlast: "outlast" cost
        kwprowess: "prowess"
        kwdash: "dash" cost
        kwexploit: "exploit"
        kwmenace: "menace"
        kwrenown: "renown" valuenumber
        kwawaken: "awaken" cost
        kwdevoid: "devoid"
        kwingest: "ingest"
        kwmyriad: "myriad"
        kwsurge: "surge" cost
        kwskulk: "skulk"
        kwemerge: "emerge" cost
        kwescalate: "escalate" cost
        kwmelee: "melee"
        kwcrew: "crew" valuenumber
        kwfabricate: "fabricate" valuenumber
        kwpartner: "partner" ["with" objectname]
        kwundaunted: "undaunted"
        kwimprovise: "improvise"
        kwaftermath: "aftermath"
        kwembalm: "embalm" cost
        kweternalize: "eternalize" cost
        kwafflict: "afflict" valuenumber
        kwascend: "ascend"
        kwassist: "assist"

        //ABILITY COSTS

        cost: costsequence | dashcostexpression
        costsequence: (loyaltycost | tapuntapsymbol | manasymbolexpression | effectexpression) ("," (loyaltycost | tapuntapsymbol | manasymbolexpression | effectexpression))*
        dashcostexpression: DASH ( manasymbolexpression | effectexpression )

        ///VALUE EXPRESSIONS

        //[TODO: Need to account for custom values, variables, 'equals to' expressions, etc.]
        valueexpression: valueterm | equaltoexpression | numberofexpression | uptoexpression | thatmanyexpression 
        | ltexpression | lteqexpression | gtexpression | gteqexpression | timesexpression
        ltexpression: effectexpression? "less" "than" (valueexpression | declarationorreference)
        lteqexpression: effectexpression? (valueexpression "or" ("less" | "fewer") | "less" "than" "or" "equal" "to" valueexpression)
        gtexpression: effectexpression? "greater" "than" (valueexpression | declarationorreference)
        | "more" "than" valueexpression
        gteqexpression: effectexpression? (valueexpression "or" ("greater" | "more")  | "greater" "than" "or" "equal" "to" valueexpression)
        | CARDINAL "or" "more" "times"-> gteqfrequencyexpression
        equaltoexpression: effectexpression? "equal" "to" (valueexpression | declarationorreference)
        uptoexpression: "up" "to" valueterm
        !thatmanyexpression: valuefrequency? "that" ("much"|"many")
        !numberofexpression: ("a"|"the"|"any") "number" "of" declarationorreference
        timesexpression: "times" statement? //[example: the number of times ~ was kicked]
        valueterm: valuenumber | valuecardinal | valueordinal | valuefrequency | valuecustom
        valuenumber: NUMBER
        valuecardinal: CARDINAL
        valueordinal: ORDINAL
        valuefrequency: FREQUENCY | CARDINAL "times"
        FREQUENCY: "once" | "twice"
        CARDINAL: "one" | "two" | "three" | "four" | "five" | "six" | "seven" | "eight" | "nine" | "ten" 
        | "eleven" | "twelve" | "thirteen" | "fourteen" | "fifteen" | "sixteen" | "seventeen" | "eighteen" | "nineteen" | "twenty" //[TODO]
        ORDINAL: "first" | "second" | "third" | "fourth" | "fifth" //[TODO]
        valuecustom: "x" | "*"
        quantityrulemodification: "rounded" "up" -> roundedupmod
        | "rounded" "down" -> roundeddownmod
        | "divided" "evenly" -> dividedevenlymod
        | "divided" "as" "you" "choose" -> dividedfreelymod
        | "plus" valueterm -> plusmod
        | "minus" valueterm -> minusmod


        //DECLARATIONS AND REFERENCES

        declarationorreference: genericdeclarationexpression | reference | playerreference | objectreference | anytargetexpression
        genericdeclarationexpression: (playerdeclaration | objectdeclaration)
        | declarationorreference ("," declarationorreference ",")* "or" declarationorreference -> orgenericdeclarationexpression
        | declarationorreference ("," declarationorreference ",")* "and" declarationorreference -> andgenericdeclarationexpression
        | declarationorreference ("," declarationorreference ",")* "and/or" declarationorreference -> andorgenericdeclarationexpression

        genericdescriptionexpression: objectdescriptionexpression | playerdescriptionexpression

        playerdeclref: playerdeclaration | playerreference
        playerdeclaration: declarationdecorator* playerdefinition
        playerreference: referencedecorator+ playerdefinition
        playerdefinition: playerdescriptionexpression
        playerdescriptionexpression : playerdescriptionterm (","? playerdescriptionterm)*
        playerdescriptionterm: valueordinal | modifier | playerterm | withexpression | withoutexpression | whoexpression
        playerterm: PLAYERTERM
        whoexpression: "who" statement

        objectdeclref: objectdeclaration | objectreference
        objectdeclaration: declarationdecorator* objectdefinition
        objectreference: referencedecorator+ objectdefinition
        objectdefinition: objectdescriptionexpression
        | objectdescriptionexpression ("," objectdescriptionexpression ",")* "or" objectdescriptionexpression -> orobjectdescriptionexpression
        | objectdescriptionexpression ("," objectdescriptionexpression ",")* "and" objectdescriptionexpression -> andobjectdescriptionexpression
        | objectdescriptionexpression ("," objectdescriptionexpression ",")* "and/or" objectdescriptionexpression -> andorobjectdescriptionexpression

        ///[TODO: Rewriting objectdescriptionexpression to respect a canonical order because it makes parsing so much faster.]
        //objectdescriptionexpression: objectdescriptionterm (","? objectdescriptionterm)*
        objectdescriptionexpression: objectpreterm* objectpostterm*
        objectpreterm:  colorexpression | namedexpression | manasymbolexpression | typeexpression | ptexpression | valueexpression
        | qualifier | modifier | locationexpression | valuecardinal | additionalexpression | characteristicexpression
        objectpostterm: withexpression | withoutexpression | choiceexpression | ofexpression | characteristicexpression | atrandomexpression
        | "that"? dealtdamageexpression | "that" doesnthaveexpression | controlpostfix | ownpostfix | putinzonepostfix | castpostfix | "that" ispostfix | targetspostfix
        | "that" sharepostfix

        //[TODO: Mana type declarations. Mana is now a first-class citizen!]
        manadeclref: manadeclaration | manareference
        manadeclaration: declarationdecorator* manadefinition
        manareference: referencedecorator+ manadefinition
        manadefinition: manadescriptionexpression
        | manadescriptionexpression ("," manadescriptionexpression ",")* "or" manadescriptionexpression -> ormanadescriptionexpression
        | manadescriptionexpression ("," manadescriptionexpression ",")* "and" manadescriptionexpression -> andmanadescriptionexpression
        | manadescriptionexpression ("," manadescriptionexpression ",")* "and/or" manadescriptionexpression -> andormanadescriptionexpression
        manadescriptionexpression: puremanaexpression | textmanaexpression
        puremanaexpression: manasymbolexpression
        textmanaexpression: 
        productionexpression: "produced" "by" declarationorreference -> producedbyexpression
        | "that" declarationorreference "could" "produce" -> couldproduceexpression
        anycolorexpression: "of" "any" "color"
        | "of" "any" "one" "color" -> anyonecolorexpression



        declarationdecorator: "each" -> eachdecorator
        | "all" -> alldecorator
        | ["an"]"other" -> otherdecorator
        | "a"["n"] -> indefinitearticledecorator
        | "the" -> definitearticledecorator
        | valueexpression? "target" -> targetdecorator
        | "any" -> anydecorator
        anytargetexpression: "any" "target" //Special nullary variant

        reference: neutralreference | selfreference | namereference
        neutralreference: "it" | "them"
        selfreference: "itself" | "himself" | "herself" -> selfreference
        namereference: NAMEREFSYMBOL

        referencedecorator: ("that" | "those") -> thatreference
        | ("this"|"these") -> thisreference
        | possessiveterm -> possessivereference
        !possessiveterm: "its" | "your" | "their" | namereference ("'s"|"'") | objectdeclref ("'s"|"'") | playerdeclref ("'s"|"'") | typeexpression ("'s"|"'") | genericdeclarationexpression ("'s"|"'")

        ptexpression: valueexpression "/" valueexpression
        namedexpression: "named" (namereference | objectname)
        !locationexpression: ("into" | "onto" | "in" | "on" | "from" | "on top of" | "on bottom of")? zonedeclarationexpression
        withexpression: "with" (reference | abilitysequencestatement | characteristicexpression | (valueexpression | "a"["n"])? countertype "counter"["s"] "on" reference)
        withoutexpression: "without" (reference | abilitysequencestatement | characteristicexpression | (valueexpression | "a"["n"])? countertype "counter"["s"] "on" reference)
        doesnthaveexpression: "does" "not" "have" declarationorreference //[Basically equivalent to 'without']
        dealtdamageexpression: "dealt" DAMAGETYPE ("this" "way")? ("by" declarationorreference)? timeexpression?
        choiceexpression: "of" possessiveterm "choice"
        ofexpression: "of" declarationorreference
        additionalexpression: "additional"
        controlpostfix: playerdeclref "control"["s"]
        | playerdeclref ("do" "not" | "does" "not") "control"["s"] -> negativecontrolpostfix
        ownpostfix: playerdeclref "own"["s"]
        | playerdeclref ("do" "not" | "does" "not") "own"["s"] -> negativeownpostfix
        castpostfix: playerdeclref "cast"
        putinzonepostfix: "put" locationexpression zoneplacementmodifier? ("this" "way")?
        targetspostfix: "that" "target"["s"] declarationorreference
        atrandomexpression: "at" "random" //[TODO: Need to find out where to put this.]
        ispostfix: isstatement
        sharepostfix: "share"["s"] declarationorreference

        //EFFECT EXPRESSIONS


        effectexpression: keywordactionexpression
        | dealsdamageexpression
        | preventdamageexpression
        | returnexpression
        | putinzoneexpression
        | putcounterexpression
        | removecounterexpression
        | spendmanaexpression
        | paylifeexpression
        | addmanaexpression
        | paymanaexpression
        | payexpression
        | gainlifeexpression
        | loselifeexpression
        | getsptexpression
        | diesexpression
        | gainabilityexpression
        | loseabilityexpression
        | lookexpression
        | takeextraturnexpression
        | flipcoinsexpression
        | winloseeventexpression
        | remainsexpression
        | assigndamageexpression
        | ableexpression
        | changezoneexpression
        | skiptimeexpression
        | switchexpression
        | targetsexpression
        | shareexpression

        dealsdamageexpression:  declarationorreference? ("deal"["s"]|"dealt") valueexpression? DAMAGETYPE ("to" declarationorreference)? (","? quantityrulemodification)* -> dealsdamagevarianta
        | valueexpression DAMAGETYPE ("to" declarationorreference)?  (","? quantityrulemodification)* -> dealsdamagevariantaimplied //variant a, implied antecedent
        | declarationorreference ("deal"["s"]|"dealt") DAMAGETYPE valueexpression ("to" declarationorreference)?  (","? quantityrulemodification)* -> dealsdamagevariantb
        | declarationorreference ("deal"["s"]|"dealt") DAMAGETYPE ("to" declarationorreference)?  valueexpression  (","? quantityrulemodification)* -> dealsdamagevariantc
        preventdamageexpression: "prevent" "the" "next" valueexpression DAMAGETYPE "that" "would" "be" "dealt" "to" declarationorreference timeexpression? -> preventdamagevarianta
        | "prevent" "the" "next" valueexpression DAMAGETYPE "that" declarationorreference "would" "deal" "to" declarationorreference timeexpression? -> preventdamagevariantb
        | "prevent" "all" DAMAGETYPE "that" "would" "be" "dealt" ("to" declarationorreference)? timeexpression? -> preventdamagevariantc
        | "prevent" valueexpression "of" "that" DAMAGETYPE -> preventdamagevariantd 
        | "prevent" "that" DAMAGETYPE -> preventdamagevariante
        | DAMAGETYPE "is" "prevented" "this" "way" -> preventdamagevariantf //[TODO: There may be a more general is-statement for stuff like 'damage'.]

        returnexpression: playerdeclref? "return"["s"] declarationorreference atrandomexpression? ("from" zonedeclarationexpression)? "to" zonedeclarationexpression genericdeclarationexpression? zoneplacementmodifier?//[TODO]

        putinzoneexpression: playerdeclref? "put"["s"] (declarationorreference | cardexpression) (locationexpression | "back" | zoneplacementmodifier) (objectdefinition | playerdefinition | zoneplacementmodifier)?
        putcounterexpression: playerdeclref? "put"["s"] ("a"|valueexpression) countertype "counter"["s"] "on" declarationorreference
        removecounterexpression: playerdeclref? "remove"["s"] ("a"|valueexpression) countertype "counter"["s"] "from" declarationorreference
        spendmanaexpression: "spend" "mana" //[TODO: this is just a stub]
        paylifeexpression: playerdeclref? "pay"["s"] valueexpression? "life"
        addmanaexpression: playerdeclref? "add"["s"] manadeclref
        paymanaexpression: playerdeclref? "pay"["s"] manadeclref
        payexpression: playerdeclref? "pay"["s"] declarationorreference //[TODO: This might change. Added for 'rather than pay this spell's mana cost'.]
        gainlifeexpression: playerdeclref? "gain"["s"] (valueexpression? "life" | "life" valueexpression)
        | playerdeclref "gained" (valueexpression? "life" | "life" valueexpression) timeexpression?
        loselifeexpression: playerdeclref? "lose"["s"] (valueexpression? "life" | "life" valueexpression) 
        | playerdeclref "lost" (valueexpression? "life" | "life" valueexpression) timeexpression?
        getsptexpression: declarationorreference? "get"["s"] ptchangeexpression
        diesexpression: declarationorreference? "die"["s"] timeexpression?
        gainabilityexpression: declarationorreference? "gain"["s"]  abilitysequencestatement
        loseabilityexpression: declarationorreference? "lose"["s"] abilitysequencestatement
        lookexpression: playerdeclref? ("look"["s"]|"looked") "at" (declarationorreference | cardexpression)
        takeextraturnexpression: playerdeclref? "take"["s"] timeexpression
        flipcoinsexpression: playerdeclref? "flip"["s"] ("a" | valuecardinal) "coin"["s"]
        !winloseeventexpression: playerdeclref? ("lose"|"win")["s"] ("the" "flip" | "the" "game")?
        remainsexpression: declarationorreference? "remain"["s"] (modifier | locationexpression)
        assigndamageexpression: declarationorreference? "assign"["s"] DAMAGETYPE "to" declarationorreference -> damageredirectionexpression
        | declarationorreference? "assign"["s"] "no" DAMAGETYPE timeexpression -> nodamageassignedexpression
        | declarationorreference? "assign"["s"] DAMAGETYPE valueexpression -> alternatedamageassignmentexpression
        ableexpression: declarationorreference? "able" ("to" statement "do" "so")?
        changezoneexpression: declarationorreference "enter"["s"] locationexpression genericdeclarationexpression? zoneplacementmodifier? timeexpression? -> enterzoneexpression
        | declarationorreference "leaves" locationexpression -> leavezoneexpression
        skiptimeexpression: playerdeclref? "skip"["s"] timeexpression
        switchexpression: playerdeclref? "switch"["es"] declarationorreference
        targetsexpression: objectdeclref? "target"["s"] declarationorreference?
        shareexpression: declarationorreference "share"["s"] declarationorreference


        keywordactionexpression: basickeywordaction | specialkeywordaction
        basickeywordaction: activateexpression
        | attacksexpression
        | blocksexpression
        | attachexpression
        | castexpression
        | chooseexpression
        | controlsexpression
        | gaincontrolexpression
        | uncastexpression
        | createexpression
        | destroyexpression
        | drawexpression
        | discardexpression
        | doubleexpression
        | exchangeexpression
        | exileexpression
        | fightexpression
        | playexpression
        | revealexpression
        | sacrificeexpression
        | searchexpression
        | shuffleexpression
        | tapuntapexpression

        activateexpression: "activate" declarationorreference
        !attacksexpression: declarationorreference? "only"? "attack"["s"] "only"? (timeexpression? declarationorreference?| declarationorreference? timeexpression?) "alone"?
        | declarationorreference? "attacked" (timeexpression? declarationorreference?| declarationorreference? timeexpression?) "alone"? -> attackedexpression
        //| "be" "attacked" "by" declarationorreference? timeexpression? -> beattackedexpression
        !blocksexpression: declarationorreference? "only"? "block"["s"] "only"? (timeexpression? declarationorreference? | declarationorreference? timeexpression?) "alone"?
        | declarationorreference? "blocked" (timeexpression? declarationorreference? | declarationorreference? timeexpression?) "alone"? -> blockedexpression
        //| "be" "blocked" "by" declarationorreference? timeexpression? -> beattackedexpression

        attachexpression: "attach" declarationorreference "to" declarationorreference
        | "unattach" declarationorreference ("from" declarationorreference)? -> unattachexpression
        | playerdeclref "attaches" declarationorreference "to" declarationorreference -> playerattachesexpression

        castexpression: playerdeclref? "cast"["s"] declarationorreference (castmodifier ("and" castmodifier)?)* timeexpression?
        castmodifier: "without" "paying" "its" "mana" "cost" -> castwithoutpaying //[TODO: We may be able to fold this into the pay-expression]
        | "as" "though" beingstatement -> castasthough
        chooseexpression: playerdeclref? ("choose"["s"]|"chose") declarationorreference ("from" "it")? atrandomexpression? //[TODO]
        controlsexpression: playerdeclref? ("control"["s"] | "controlled") genericdeclarationexpression
        gaincontrolexpression: playerdeclref? ("gain"["s"] | "gained") "control" "of" declarationorreference

        uncastexpression: "counter" declarationorreference
        createexpression: playerdeclref? "create"["s"] declarationorreference
        destroyexpression: "destroy" declarationorreference
        drawexpression: playerdeclref? ("draw"["s"]|"drew") cardexpression //[("a" "card" | valueexpression "card"["s"] | "cards"["s"] valueexpression)]
        discardexpression: playerdeclref? ("discard"["s"] | "discarded") (declarationorreference | "a" "card" | valueexpression "card"["s"] | "card"["s"] valueexpression) "at random"?
        doubleexpression: "double" //[TODO]
        exchangeexpression: "exchange" //[TODO]
        exileexpression: "exile" declarationorreference
        fightexpression: declarationorreference? "fight"["s"] declarationorreference?
        playexpression: playerdeclref? ("play"["s"] | "played") declarationorreference timeexpression?
        revealexpression: playerdeclref? ("reveal"["s"] | "revealed") (cardexpression | declarationorreference)
        sacrificeexpression: playerdeclref? ("sacrifice"["s"] | "sacrificed") declarationorreference
        searchexpression: playerdeclref? ("search"["es"] | "searched") zonedeclarationexpression? "for" declarationorreference
        shuffleexpression: playerdeclref? ("shuffle"["s"] | "shuffled") zonedeclarationexpression
        tapuntapexpression: "tap" declarationorreference? -> tapexpression
        | "untap" declarationorreference? -> untapexpression

        specialkeywordaction: regenerateexpression
        | scryexpression
        | fatesealexpression
        | clashexpression
        | detainexpression
        | planeswalkexpression
        | setinmotionexpression
        | abandonexpression
        | proliferateexpression
        | transformexpression
        | populateexpression
        | voteexpression
        | bolsterexpression
        | manifestexpression
        | supportexpression
        | investigateexpression
        | meldexpression
        | goadexpression
        | exertexpression
        | exploreexpression
        | turnfaceexpression
        | cycleexpression
        | levelupexpression~2

        regenerateexpression: "regenerate" declarationorreference
        scryexpression: "scry" valueexpression
        fatesealexpression: "fateseal" valueexpression
        clashexpression: playerdeclref? "clash" "with" playerdeclref
        detainexpression: "detain" objectdeclref
        planeswalkexpression: playerdeclref "planeswalk"["s"] "to" SUBTYPEPLANAR
        setinmotionexpression: playerdeclref "set"["s"] declarationorreference "in" "motion"
        abandonexpression: playerterm? "abandon"["s"] declarationorreference //[Note: Has never been used]
        proliferateexpression: "proliferate"
        transformexpression: "transform" declarationorreference
        populateexpression: "populate"
        voteexpression: playerdeclref "vote"["s"] "for" (objectname "or" objectname | declarationorreference) //[TODO]
        bolsterexpression: "bolster" valueexpression
        manifestexpression: playerdeclref? "manifest"["s"] cardexpression
        supportexpression: "support" valueexpression
        investigateexpression: "investigate"
        meldexpression: "meld" "them" "into" objectname
        goadexpression: "goad" declarationorreference
        exertexpression: playerdeclref? "exert"["s"] declarationorreference
        exploreexpression: declarationorreference? "explores"
        //[This one below is a bit weird because it's not 'becomes turned face up', it's 'is turned face up'.]
        //[It's a passive construction, but it's not a modifier like face-up.]
        !turnfaceexpression: playerdeclref? "turn"["s"] declarationorreference "face" ("down" | "up")
        | "turned" "face" ("down" | "up") -> turnedfaceexpression
        cycleexpression: playerdeclref? ("cycle"["s"] | "cycled") declarationorreference? 

        levelupexpression: ("level" levelrangeexpression ptexpression ability*)
        levelrangeexpression: NUMBER "-" NUMBER | NUMBER "+"


        //TYPE/MANA/COLOR EXPRESSIONS, MODIFIERS, AND MISCELLANEOUS

        timeexpression: startendspecifier? timeterm ("of" timeexpression)?
        startendspecifier: "the"? "beginning" "of" -> timebeginmodifier
        | "the"? "end" "of" -> timeendmodifier
        timeterm: (referencedecorator* | declarationdecorator*) possessiveterm* timemodifier* (PHASE | STEP | TURN | GAME |  "one")
        timemodifier: "next" valuecardinal? -> nexttimemodifier
        | "additional" -> additionaltimemodifier
        | valuecardinal? "extra" -> extratimemodifier
        PHASE: "beginning phase" | ("precombat" | "postcombat")? "main phase" | ("combat" | "combat phase") | "ending phase"
        STEP: "untap step" | ("upkeep step" | "upkeep") | "draw step" | "beginning of combat" | "declare attackers step"
        | "declare blockers step" | "combat damage step" | "end of combat" | "end step" | "cleanup step" | "step"
        TURN: "turn"
        GAME: "game" 

        //[TODO: What about comma-delimited type expressions?]
        typeexpression: (typeterm)+ | typeterm ("," typeterm)+
        | typeterm ("," typeterm ",")* "or" typeterm -> ortypeexpression

        typeterm: (TYPE ["s"] | SUBTYPESPELL ["s"] | SUBTYPELAND ["s"] | SUBTYPEARTIFACT ["s"] | SUBTYPEENCHANTMENT ["s"] | SUBTYPEPLANESWALKER | SUBTYPECREATUREA ["s"] | SUBTYPECREATUREB ["s"] | SUBTYPEPLANAR | SUPERTYPE)
        | "non"["-"] typeterm -> nontypeterm

        TYPE: "planeswalker" | "conspiracy" | "creature" | "enchantment" | "instant"
        | "land" | "phenomenon" | "plane" | "artifact" | "scheme" | "sorcery"
        | "tribal" | "vanguard"

        SUBTYPESPELL : "arcane" | "trap"

        SUBTYPELAND: "desert" | "forest" | "gate" | "island" | "lair" | "locus"
        | "mine" | "mountain" | "plains" | "power-plant" | "swamp" | "tower" | "urza's"

        SUBTYPEARTIFACT: "clue" | "contraption" | "equipment" | "fortification" | "treasure" | "vehicle"

        SUBTYPEENCHANTMENT: "aura" | "cartouche" | "curse" | "saga" | "shrine"

        SUBTYPEPLANESWALKER: "ajani" | "aminatou" | "angrath" | "arlinn" | "ashiok" | "bolas" | "chandra"
        | "dack" | "daretti" | "domri" | "dovin" | "elspeth" | "estrid" | "freyalise" | "garruk" | "gideon"
        | "huatli" | "jace" | "jaya" | "karn" | "kaya" | "kiora" | "koth" | "liliana" | "nahiri" | "narset"
        | "nissa" | "nixilis" | "ral" | "rowan" | "saheeli" | "samut" | "sarkhan" | "sorin" | "tamiyo" | "teferi"
        | "tezzeret" | "tibalt" | "ugin" | "venser" | "vivien" | "vraska" | "will" | "windgrace" | "xenagos"
        | "yanggu" | "yanling"


        //[TODO: SUBTYPECREATUREA and SUBTYPECREATUREB are split up because having such a long list of alternatives apparently]
        //[causes Lark to suffer a recursion depth error. We should see if this is fixable.]

        SUBTYPECREATUREA: "advisor" | "aetherborn" | ("ally"|"allies") | "angel" | "antelope" | "ape" | "archer" | "archon" 
        | "artificer" | "assassin" | "assembly-worker" | "atog" | "aurochs" | "avatar" | "azra" | "badger"
        | "barbarian" | "basilisk" | "bat" | "bear" | "beast" | "beeble" | "berserker" | "bird" | "blinkmoth"
        | "boar" | "bringer" | "brushwagg" | "camarid" | "camel" | "caribou" | "carrier" | "cat" | "centaur"
        | "cephalid" | "chimera" | "citizen" | "cleric" | "cockatrice" | "construct" | "coward" | "crab"
        | "crocodile" | "cyclops" | "dauthi" | "demon" | "deserter" | "devil" | "dinosaur" | "djinn" | "dragon"
        | "drake" | "dreadnought" | "drone" | "druid" | "dryad" | ("dwarf"|"dwarves") | "efreet" | "egg" | "elder" | "eldrazi"
        | "elemental" | "elephant" | ("elf"|"elves") | "elk" | "eye" | "faerie" | "ferret" | "fish" | "flagbearer" | "fox"

        SUBTYPECREATUREB: "frog" | "fungus" | "gargoyle" | "germ" | "giant" | "gnome" | "goat" | "goblin" | "god" | "golem" | "gorgon"
        | "graveborn" | "gremlin" | "griffin" | "hag" | "harpy" | "hellion" | "hippo" | "hippogriff" | "homarid" | "homunculus"
        | "horror" | "horse" | "hound" | "human" | "hydra" | "hyena" | "illusion" | "imp" | "incarnation" | "insect"
        | "jackal" | "jellyfish" | "juggernaut" | "kavu" | "kirin" | "kithkin" | "knight" | "kobold" | "kor" | "kraken"
        | "lamia" | "lammasu" | "leech" | "leviathan" | "lhurgoyf" | "licid" | "lizard" | "manticore" | "masticore"
        | ("mercenary"|"mercenaries") | "merfolk" | "metathran" | "minion" | "minotaur" | "mole" | "monger" | "mongoose" | "monk" 
        | "monkey" | "moonfolk" | "mutant" | "myr" | "mystic" | "naga" | "nautilus" | "nephilim" | "nightmare" 
        | "nightstalker" | "ninja" | "noggle" | "nomad" | "nymph" | ("octopus"|"octopuses") | "ogre" | "ooze" | "orb" | "orc" 
        | "orgg" | "ouphe" | "ox" | "oyster" | "pangolin" | "pegasus" | "pentavite" | "pest" | "phelddagrif" | "phoenix"
        | "pilot" | "pincher" | "pirate" | "plant" | "praetor" | "prism" | "processor" | "rabbit" | "rat" | "rebel"
        | "reflection" | "rhino" | "rigger" | "rogue" | "sable" | "salamander" | "samurai" | "sand" | "saproling" | "satyr"
        | "scarecrow" | "scion" | "scorpion" | "scout" | "serf" | "serpent" | "servo" | "shade" | "shaman" | "shapeshifter"
        | "sheep" | "siren" | "skeleton" | "slith" | "sliver" | "slug" | "snake" | "soldier" | "soltari" | "spawn" | "specter"
        | "spellshaper" | "sphinx" | "spider" | "spike" | "spirit" | "splinter" | "sponge" | "squid" | "squirrel" | "starfish"
        | "surrakar" | "survivor" | "tetravite" | "thalakos" | "thopter" | "thrull" | "treefolk" | "trilobite" | "triskelavite"
        | "troll" | "turtle" | "unicorn" | "vampire" | "vedalken" | "viashino" | "volver" | "wall" | "warrior" | "weird"
        | ("werewolf"|"werewolves") | "whale" | "wizard" | ("wolf"|"wolves") | "wolverine" | "wombat" | "worm" | "wraith" | "wurm" | "yeti" 
        | "zombie" | "zubera"

        SUBTYPEPLANAR: "alara" | "arkhos" | "azgol" | "belenon" | "bolas’s meditation realm"
        | "dominaria" | "equilor" | "ergamon" | "fabacin" | "innistrad" | "iquatana" | "ir" 
        | "kaldheim" | "kamigawa" | "karsus" | "kephalai" | "kinshala" | "kolbahan" | "kyneth"
        | "lorwyn" | "luvion" | "mercadia" | "mirrodin" | "moag" | "mongseng" | "muraganda"
        | "new phyrexia" | "phyrexia" | "pyrulea" | "rabiah" | "rath" | "ravnica" | "regatha"
        | "segovia" | "serra’s realm" | "shadowmoor" | "shandalar" | "ulgrotha" | "valla"
        | "vryn" | "wildfire" | "xerex" | "zendikar"

        subtype: SUBTYPESPELL | SUBTYPELAND | SUBTYPEARTIFACT | SUBTYPEENCHANTMENT | SUBTYPEPLANESWALKER | SUBTYPECREATUREA | SUBTYPECREATUREB | SUBTYPEPLANAR

        SUPERTYPE: "basic" | "legendary" | "ongoing" | "snow" | "world"

        DAMAGETYPE: "damage" | "combat damage" | "noncombat damage"

        modifier: ABILITYMODIFIER | COMBATSTATUSMODIFIER | KEYWORDSTATUSMODIFIER | TAPPEDSTATUSMODIFIER | EFFECTSTATUSMODIFIER
        | controlmodifier | attachmentmodifier

        ABILITYMODIFIER: "triggered" | "activated" | "mana" | "loyalty"
        COMBATSTATUSMODIFIER: "attacking" | "defending" | "attacked" | "blocking" | "blocked" | "active"
        KEYWORDSTATUSMODIFIER: "paired" | "kicked" | "face-up" | "face-down" | "transformed" | "enchanted" | "equipped"
        | "fortified" | "monstrous" | "regenerated" | "suspended" | "flipped"
        TAPPEDSTATUSMODIFIER: "tapped" | "untapped"
        EFFECTSTATUSMODIFIER: "named" | "chosen" | "chosen at random" | "revealed" | "returned" | "destroyed" | "exiled" | "died" | "countered" | "sacrificed"
        | "the target of a spell or ability" | "prevented" | "created"
        controlmodifier: "under" referencedecorator+ "control"
        attachmentmodifier: "attached" ("only"? "to" declarationorreference)? -> attachedmodifier
        | "unattached" ("from" declarationorreference)? -> unattachedmodifier

        qualifier: QUALIFIER["s"]
        QUALIFIER: ("ability"|"abilities") | "card" | "permanent" | "source" | "spell" | "token" | "effect"

        characteristicexpression: characteristicterms 
        | (characteristicterms (valueexpression|ptexpression) | (valueexpression|ptexpression) characteristicterms) -> characteristicvaluecompexpr

        characteristicterms: characteristicterm
        | possessiveterm+ characteristicterm -> characteristicpossessiveexpr
        | "the" characteristicterm -> characteristicthereference
        | characteristicterm  ("," characteristicterm ",")* "or" characteristicterm -> characteristicorexpr
        | characteristicterm  ("," characteristicterm ",")* "and" characteristicterm -> characteristicandexpr
        | characteristicterm  ("," characteristicterm ",")* "and/or" characteristicterm -> characteristicandorexpr
        | "no" characteristicterm -> nocharacteristicexpr //[example: no maximum hand size]

        characteristicterm: modifier* characteristic
        characteristic: OBJECTCHARACTERISTIC | PLAYERCHARACTERISTIC
        PLAYERCHARACTERISTIC: "maximum hand size" | "life total" | "life" | "cards in hand"
        OBJECTCHARACTERISTIC: "card"? "name" | "mana cost" | "converted mana cost" | "color"["s"] | "color indicator" | "type"["s"] | "card type"["s"] | "subtype"["s"] | "supertype"["s"]
        | "rules text" | "abilities" | "power" | "toughness" | "base power" | "base toughness" | "loyalty" | "hand modifier" | "life modifier"

        //[TODO: Not quite done, there are expressions like 'a number of cards equal to [...]'. There's some overlapping responsibilities with descriptions involving cards, maybe.]
        !cardexpression: ("the" "top" | "the" "bottom")? (valueterm | thatmanyexpression | "a")? "card"["s"] ("from" "the" "top" | "from" "the" "bottom")? ("of" zonedeclarationexpression)?  

        zonedeclarationexpression: (declarationdecorator* | referencedecorator*) zone
        zoneplacementmodifier: "in" "any" "order" -> anyorderplacement
        | "in" "a" "random" "order" -> randomorderplacement
        | ORDINAL "from" "the" "top" -> fromtopplacement
        | ORDINAL "from" "the" "bottom" -> frombottomplacement
        zone: ZONE
        ZONE: "the battlefield" | "graveyard"["s"] | ("library"|"libraries") | "hand"["s"] | "stack" | "exile" | "command zone" | "outside the game" | "anywhere"

        colorexpression: colorterm -> colorsingleexpr
        | colorterm  ("," colorterm ",")* "or" colorterm -> colororexpr
        | colorterm ("," colorterm ",")* "and" colorterm -> colorandexpr
        | colorterm ("," colorterm ",")* "and/or" colorterm -> colorandorexpr

        colorterm: COLORTERM
        | "non" COLORTERM -> noncolorterm

        COLORTERM: "white" | "blue" | "black" | "red" | "green" | "monocolored" | "multicolored" | "colorless"

        objectname: OBJECTNAME //[TODO: No demarcations around names is difficult also. Need preprocessor help here.]
        OBJECTNAME: NAMEWORD ((WS | ",") NAMEWORD)* //[TODO: commas in names? This is problematic. Need preprocessor help here.]
        NAMEWORD: UCASE_LETTER (LCASE_LETTER)*

        countertype: ptchangeexpression | WORD

        loyaltycost: (PLUS | PWMINUS)? valueterm
        //[NOTE: Both Scryfall and Mtgjson use a long dash, not a short dash, to indicate a minus on a planeswalker ability]
        PWMINUS: "−"
        ptchangeexpression: (PLUS | MINUS) valueterm "/" (PLUS | MINUS) valueterm
        PLUS: "+"
        MINUS: "-"

        manaspecificationexpression: valueterm "mana" manaspecifier+
        manaspecifier: anycolorexpression //[TODO: Need to add the rest of these]

        manasymbolexpression: manasymbol+
        | manasymbolexpression "or" manasymbolexpression -> ormanaexpression
        manasymbol: "{" manamarkerseq "}"
        manamarkerseq: manamarker_color -> regularmanasymbol
        | manamarker_halfmana manamarker_color -> halfmanasymbol
        | manamarker_color "/" manamarker_phyrexian -> phyrexianmanasymbol
        | manamarker_color "/" manamarker_color -> hybridmanasymbol
        | "2" "/" manamarker_color -> alternate2manasymbol
        | manamarker_snow -> snowmanasymbol
        | manamarker_colorless -> colorlessmanasymbol
        | manamarker_x -> xmanasymbol
        | NUMBER -> genericmanasymbol

        manamarker_halfmana: "H"i -> halfmarker
        manamarker_color: "W"i -> whitemarker
        | "U"i -> bluemarker
        | "B"i -> blackmarker
        | "R"i -> redmarker
        | "G"i -> greenmarker
        manamarker_snow: "S"i -> snowmarker
        manamarker_phyrexian: "P"i -> phyrexianmarker
        manamarker_colorless: "C"i -> colorlessmarker
        manamarker_x: "X"i -> xmarker

        DASH: "—"
        MODALCHOICE: "•"

        NAMEREFSYMBOL: "~" | "~f"
        PLAYERTERM: "player"["s"] | "opponent"["s"] | "you" |  "teammate"["s"] | "team"["s"] | "they" | "controller"["s"] | "owner"["s"]

        tapuntapsymbol: TAPSYMBOL | UNTAPSYMBOL
        TAPSYMBOL: "{T}"i
        UNTAPSYMBOL: "{Q}"i

        %import common.UCASE_LETTER -> UCASE_LETTER
        %import common.LCASE_LETTER -> LCASE_LETTER
        %import common.WORD -> WORD
        %import common.SIGNED_NUMBER -> NUMBER
        %import common.WS -> WS
        %ignore WS
        """