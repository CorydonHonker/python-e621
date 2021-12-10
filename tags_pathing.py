from my_IO import name_filter

gender_filter = {'female', 'male', 'maleherm', 'herm', 'gynomorph', 'andromorph', 'ambiguous_gender'}
quantity_filters = {
    frozenset({'trio_focus'}): 'trio focus',
    frozenset({'duo_focus'}): 'duo focus',
    frozenset({'solo_focus'}): 'solo focus',
    frozenset({'absolutely_everyone'}): 'Everyone',
    frozenset({'mass_orgy', 'orgy'}): 'orgy',
    frozenset({'crowd', 'audience'}): 'Public',
    frozenset({'group', 'large_group'}): 'group',
    frozenset({'trio', 'threesome', 'semi_incest'}): 'trio',
    frozenset({'duo'}): 'duo',
    frozenset({'solo'}): 'solo',
    frozenset({'unseen_character'}): 'unseen',
    frozenset({'offscreen_character'}): 'off_screen',
    frozenset({'zero_pictured'}): 'zero'
}
kink_filters = {
    frozenset(
        {"expression_sheet", "pinup", "portrait", "proper_art", "mousepad_design", "inspired_by_proper_art"}): "Art",
    frozenset({"model_sheet", "chart"}): "Chart",
    frozenset({"feces", "dirty_anal", "imminent_disposal", "scat", "soiling", "disposal"}): "Scat",
    frozenset({"body_horror", "what_has_science_done", "where_is_your_god_now", "nightmare_fuel", "what"}): "Nope",
    frozenset({"vomit", "nausea", "ill", "fart", "filth"}): "Gross",
    frozenset(
        {"dying", "death_by_snu_snu", "death_by_penis", "death", "corpse", "imminent_death", "necrophilia", "killing",
         "snuff"}): "Dead",
    frozenset({"gore", "blood", "disembowelment"}): "Gore",
    frozenset({"angry_sex", "abuse", "violence", "weapon", "threat", "intimidation", "knife_play"}): "Violence",
    frozenset({"digestion", "cooking_vore", "fatal_vore", "hard_vore"}): "Hard Vore",
    frozenset({"diaper", "cub", "incontinence", "infantilism"}): "Cub Play",
    frozenset({"stuffing", "weight_gain", "obese", "overweight", "moobs", "morbidly_obese"}): "Fat",
    frozenset({"incest", "bad_parenting", "semi_incest", "sibling", "brother", "sister", "parent"}): "Family",
    frozenset({"hyper", "extreme_penetration", "ridiculous_fit"}): "Extreme",
    frozenset({"huge_muscles", "genital_piercing", "scrotum_piercing", "sheath_piercing", "pussy_piercing", "penis_piercing", "anal_piercing", "chastity_piercing", "nipple_piercing", "nipple_chain", "nipple_bell", "nipple_clamp", "nipple_leash", "nipple_weights"}): "General Bl",
    frozenset({"nullo", "nullification", "genital_mutilation", "eunuch", "imminent_genital_mutilation", "penectomy",
               "mastectomy", "orchiectomy_scar", "monorchid", "null"}): "Nullification",
    frozenset({"torture", "cuntbusting", "cock_and_ball_torture", "ballbusting", "imminent_pain", "sadism", "masochism",
               "pain"}): "Pain Play",
    frozenset({"rape", "rape_play", "after_rape", "gang_rape", "imminent_rape", "molestation"}): "Rape",
    frozenset(
        {"castration", "brainwashing", "hypnosis", "identity_death", "mind_control", "reprogramming"}): "Mind Control",
    frozenset({"imminent_transfomation", "mid_transformation", "post_transformation", "species_transformation",
               "suit_transformation", "transformation", "after_transformation", "forced_transformation",
               "gender_transformation", "implied_transformation", "inanimate_transformation"}): "Transformation",
    frozenset({"living_plushie", "animate_inanimate", "fabric_creature", "living_inflatable", "living_piñata", "food_creature", "flora_fauna", "plushophilia"}): "Inanimate",
    frozenset({"infidelity", "cuckquean", "cuckold", "voyeur", "webcam", "livestream", "being_watched", "enhibitionism",
               "exhibitionism", "flashing", "mooning", "public_exposure", "public_masturbation", "public_sex",
               "stealth_masturbation", "stealth_sex", "walk-in", "streaming", "recording",
               "unprofessional_behavior"}): "Exhibitionism",
    frozenset({"giga", "imminent_stomp", "macro", "micro", "nano"}): "Macro-Micro",
    frozenset({"null_bulge", "permanent", "frustration", "edging", "chastity_device", "orgasm_control", "orgasm_delay",
               "orgasm_denial"}): "Denial",
    frozenset(
        {"assimilation", "unbirthing", "absorption_vore", "healing_vore", "full_tour", "anal_vore", "cloacal_vore",
         "soul_vore", "cock_vore", "unusual_vore", "plushie_vore"}): "Strange Vore",
    frozenset(
        {"endosoma", "body_in_mouth", "mawplay", "mouth_shot", "after_vore", "imminent_vore", "soft_vore", "tail_vore",
         "unaware_vore", "vore"}): "Soft Vore",
    frozenset({"gameplay_mechanics", "video_games"}): "Game",
    frozenset({"paw_worship", "autofootjob", "foot_fetish", "foot_focus", "foot_in_mouth", "foot_lick", "foot_play",
               "foot_sniffing", "footjob", "footjob_pov"}): "Paws",
    frozenset({"drowning", "choking", "breath_play", "asphyxiation", "autoerotic_asphyxiation"}): "Breath Play",
    frozenset(
        {"marking_territory", "omorashi", "peeing", "peeing_on_another", "wetting", "watersports", "drinking_urine",
         "urine", "urine_pool", "golden_shower", "toilet_slave"}): "Piss Play",
    frozenset({"birthing_tentacles", "infestation", "living_insertion", "parasite", "urethral_worm",
               "tentacles"}): "Parasite",
    frozenset({"oviposition", "ovipositor"}): "Ovi",
    frozenset({"plushification", "plushsuit"}): "Plush",
    frozenset({"drugged", "aphrodisiac", "pheromones", "in_heat", "in_rut", "substance_intoxication",
               "psychedelic", }): "Chemestry",
    frozenset(
        {"age_difference", "age_regression", "ageplay", "younger_dom_older_sub", "older_dom_younger_sub"}): "Age Play",
    frozenset({"imminent_pegging", "pegging", "strapon", "dominant_andromorph", "dominant_female", }): "FemDom",
    frozenset({"worship", "ball_worship", "butt_worship", "cock_worship", "facesitting"}): "Worship",
    frozenset(
        {"egg_insertion", "egg_play", "artificial_insemination", "pregnancy_test", "pregnant", "self_impregnation",
         "unwanted_impregnation", "accidental_impregnation", "impregnation", "male_impregnation",
         "mutual_impregnation"}): "Pregnancy",
    frozenset({"humiliation", "fucked_silly", "degradation", "embarrassed", "corruption", " mind_break",
               "bimbofication", "public_humiliation"}): "Degradation",
    frozenset(
        {"pinned", "genital_danger_play", "finger_in_mouth", "dirty_talk", "begging", "spitting_in_mouth", "rough_sex",
         "overstimulation", "insult", "homophobic_slur"}): "Rough",
    frozenset({"larger_on_top", "bodyjob", "big_dom_small_sub", "size_difference", "size_play", "small_dom_big_sub",
               "smaller_on_top"}): "Size Play",
    frozenset(
        {"petplay", "pet_praise", "ponyplay", "role_reversal", "roleplay", "good_girl", "good_boy", "holding_leash",
         "leash"}): "Role Play",
    frozenset({"girly", "feminization", "crossdressing", "sissification", "penis_shrinking"}): "Girly",
    frozenset({"kidnapping", "forced_nudity", "forced_orgasm", "forced", "explicitly_stated_nonconsent", "blackmail",
               "begging_for_mercy", "questionable_consent", "until_they_like_it", "unwanted_cumshot",
               "unwanted_ejaculation"}): "Forced",
    frozenset({"punishment", "discipline", "submissive", "power_bottom", "ownership", "dominant", "two_doms_one_sub",
               "sex_slave"}): "DomSub",
    frozenset({"breast_milking", "lactating", "breastfeeding", "milking_machine"}): "Milk",
    frozenset(
        {"kissing", "imminent_kiss", "happy_sex", "hand_holding", "romantic_ambiance", "romantic_couple", "romantic",
         "love", "making_out"}): "Romantic",
    frozenset({"crotch_sniffing", "armpit_sniffing", "ball_sniffing", "butt_sniffing", "shoe_sniffing", "sock_sniffing", "underwear_sniffing", "musk"}): "Musk",
    frozenset({"stuck", "quadruple_amputee", "public_use", "petrification", "penis_milking", "hogtied", "gimp_mask",
               "gimp_suit", "fully_restrained", "encasement", "bitchsuit", "immobilization", "restrained", "restraints",
               "bondage_gloves", "saint_andrew's_cross", "sex_swing", "suitcase_bondage", "fuck_bench", "chained_up"}): "Heavy Bondage",
    frozenset(
        {"straitjacket", "sensory_deprivation", "harness", "handcuff", "gag", "frogtied", "belly_riding", "blindfold",
         "muzzle_(object)", "muzzled", "bound", "bound_top", "fully_bound", "light_bondage", "ribbon_bondage",
         "rope_bondage", "bondage", "bondage_gear", "bodysuit", "rubber_suit", "skinsuit",
         "gas_mask"}): "Light Bondage",
    frozenset({"bestiality", "imminent_bestiality", "anthro_on_feral", "dominant_feral", "feral", "feral_pov",
               "submissive_feral"}): "Feral",
    frozenset({"first_person_view", "leashed_pov", "leashing_pov", "penetrating_pov", "receiving_pov", "submissive_pov",
               "double_pov", "dominant_pov", "fellatio_pov", "micro_pov"}): "POV",
    frozenset({"stealth_sex", "sleep_sex"}): "Alt Sex",
    frozenset({"gooey", "liquefactiophilia", "goo_creature"}): "Goo",
    frozenset({"crossgender", "feralized", "alternate_form", "anthrofied", "body_swap", "square_crossover"}): "Alt Char",
    frozenset({"prostate", "pseudo-penis", "anatomically_correct", "cloaca", "prehensile_penis", "unusual_anatomy", "unusual_genitalia", "unusual_genitalia_placement"}): "Anatomy",
    frozenset({"spooning", "hug", "aftercare", "afterglow", "cuddling", "embrace", "entwined_tails"}): "Embrace",
    frozenset({"presenting", "bedroom_eyes", "beckoning", "ahegao", "inviting", "seductive", "torogao", "teasing",
               "orgasm_face", "looking_pleasured", "lust", "lust"}): "lusty",
    frozenset({"sex_toy", "feeldoe", "vibrator", "sybian", "broken_condom", "condom", "thinking_with_portals",
               "portal_panties", "voodoo_sex", "voodoo", "plushophilia", "voodoo_masturbation", "vr_headset",
               "improvised_sex_toy", "toying_partner", "toying_self"}): "Toys",
    frozenset({"humor", "meme", "reaction_image", "joke", "silly"}): "Humor",
    frozenset({"inflation", "taur", "harem", "harem_outfit", "glory_hole"}): "Misc",
}
meta_filters = {
    frozenset({"3d_(artwork)"}): "3D",
    frozenset({"comic", "sequence"}): "Comic",
    frozenset({"dialogue", "voice_acted", "speech_bubble", "thought_bubble", "sound"}): "Dialogue",
    frozenset({"greyscale", "monochrome", "sepia", "black_and_white"}): "Monochrome",
}
ultra_tag_set = {
    "0600hours", "0r0ch1", "2d10", "absorption_vore", "acidapluvia", "adelaherz", "aennor", "aeroo", "after_rape", "after_transformation", "aftercare", "afterglow", "aggrobadger", "airu", "akelun", "alduinred", "alex_marx", "alhazred", "alibi-cami", "allagar", "altowovurr", "amaichix", "amara_telgemeier", "amyth", "anatomically_correct_anus", "anchee", "animancer", "animated_comic", "anixis", "antanariva", "antar_dragon", "anthro_to_feral", "antiander", "antiroo", "aoru", "aphrodisiac", "apogee", "apoptosis", "appleseed_(artist)", "araivis-edelveys", "arh", "arios", "ark_gullwing", "arsauron", "artificial_insemination", "artonis", "ash_(ashkelling)", "ashtalon", "askar", "askatrash", "asphyxiation", "asriel_dreemurr", "asriel_dreemurr_(god_form)", "assimilation", "autumndeer", "avalondragon", "avery_(roanoak)", "ayrrenth", "azathura", "backlash91", "backsash", "ball_tugging", "ball_worship", "ballbusting", "bambii_dog", "bassenji", "bechamel_(fuzzamorous)", "begging", "begging_for_more", "bella_(gasaraki2007)", "ben_(roanoak)", "bestiality", "bgn", "binxxy_(artist)", "bitemylip", "black-kitten", "blindcoyote", "blitzdrachin", "blizzard_(blizzyfox)", "bloo", "blotch", "blown-ego", "blusky", "body_takeover", "bondi_(braeburned)", "borky-draws", "bound_top", "braeburned", "brainwashing", "breath_play", "breeding_mount", "breeding_slave", "brushfire", "bubbeh", "bunsen", "butt_worship", "byzil", "caboni32", "camychan", "canary_(fiaskers)", "cannibalistic_tendencies", "captain_otter", "captainskee", "captainzepto", "caribou_(artist)", "carrot_(artist)", "casparr", "castitas", "castration", "celeste_(artist)", "ceylon", "chapaevv", "chastity_cage", "chastity_device", "chazcatrix", "chewycuticle", "chibi-marrow", "choking", "choko_(chokodonkey)", "chokodonkey", "chromamancer", "citrinelle", "clade", "clyde_wolf", "cock_and_ball_torture", "cock_worship", "codyblue-731", "coffeesoda", "collaborative_cunnilingus", "collaborative_fellatio", "collaborative_footjob", "conrie", "contraption_concept", "cookiedraggy", "cosmiclife", "crimetxt", "crisstail", "crossdressing", "crusch_lulu", "ctrl_alt_yiff", "cubi", "cubi_(rabbit)", "cuckold", "curiodraco", "cygnovum", "cyrakhis", "cyrus_(klutztron)", "d3mo", "dacad", "daintydragon", "dallas_(gingersnaps)", "dallas_prairiewind", "danji-isthmus", "danomil", "danza", "dark_nek0gami", "dark_violet", "darkarlett", "darkenstardragon", "darkgem", "darkmirage", "darkwingo", "darylith", "davad_(odissy)", "deanosaior", "deep_rimming", "deessel", "degradation", "deke_(ittybittykittytittys)", "demicoeur", "deormynd", "desertkaiju", "deusexmoose", "difetra", "digitoxici", "dimwitdog", "dinkysaurus", "dirty.paws", "dirtyfox911911", "discipline", "dizfoley", "dlw", "dominant_female", "dominant_feral", "doublepopsicle", "draco_(artist)", "dradmon", "draegonis", "dragonsponies", "dragoviir", "drake239", "drakorax", "drayk_dagger", "dredjir", "dreiker", "dripponi", "drmax", "drugged", "dumderg", "dusk_(tabuley)", "ebonychimera", "ecmajor", "edging", "edi", "edjit", "efilon", "egg_bulge", "egg_insertion", "electrixocket", "electro_current_(oc)", "elijah-draws", "endium", "ennismore", "epileptic_goat", "eris_(marefurryfan)", "ernesto_(rebeldragon101)", "ether-0", "eto_ya", "eunuch", "evalion", "evalion_(character)", "eve_azure_(pikmin117)", "evillabrat", "exterio", "extreme_french_kiss", "f-r95", "face_mounting", "falvie", "fatal_dx", "fatz_geronimo", "faunoiphilia", "fearingfun", "feeldoe", "feet_on_balls", "fefairy", "fellatio_pov", "female_domination", "female_rape", "feminization", "feral_domination", "feral_on_taur", "feral_to_anthro", "ferilla", "ferro_the_dragon", "fey_(zavan)", "fgs", "fhyra", "fiaskers", "firondraak", "fisis", "fivel", "flamespitter", "flexible_survival", "flinters", "flir_(panther)", "flir_(rabbit)", "fluffydisk42", "foot_fetish", "foot_focus", "foot_lick", "foot_on_face", "foot_play", "foot_shot", "foot_sniffing", "forced", "forced_orgasm", "forced_partners", "forced_transformation", "foxeh", "frisky-lime", "frost_(cinderfrost)", "frusha", "frustration", "ftg_transformation", "fti_transformation", "ftm_transformation", "fucked_silly", "fuel_(artist)", "furfragged", "furikake", "furx_(character)", "fuze", "fuzzamorous", "gameplay_mechanics", "garnetto", "garrett_the_turtle_(character)", "gay_to_straight", "gender_transformation", "genital_scar", "genital_torture", "ghost738589", "glopossum", "goo_creature", "goo_dragon", "goo_transformation", "good_boy", "good_girl", "gooey", "gothwolf", "greame", "greasyhyena", "greedygulo", "grimart", "gryf_(flir)", "gryphon489", "gtf_transformation", "gustav", "h0rs3", "haiku_(character)", "halbean", "hamilton_loree", "harlem", "hassana", "haswell", "haychel", "head_in_crotch", "herpydragon", "hexdragon", "hida", "higsby", "hioshiru", "hladilnik", "holly_marie_ogburn", "hoot", "hornedfreak", "howlart", "hueroc", "hufnaar", "humiliation", "huru", "huska", "hypnosis", "i-psilone", "identity_death", "ifus", "iggi", "iggy_(graffitidragon)", "ikshun", "ill_dingo", "imaginarydragon", "imgonnaloveyou", "immelmann", "imminent_knotting", "imminent_pegging", "imminent_rape", "imminent_vore", "implied_transformation", "impregnation", "in_heat", "in_rut", "inanimate_transformation", "incontinence", "incorgnito", "infestation", "inoby", "interrupted_orgasm", "ishiru", "ismar", "itf_transformation", "iti_transformation", "itm_transformation", "ittybittykittytittys", "izrez", "jack_savage", "jack-jackal_(character)", "jackrow", "jagon", "jailbird", "jaiy", "jajuka", "jana_(jana's_lab)", "jayne_doe", "jb_greymane", "jedayskayvoker", "jellybats", "jem", "jenni_(jennibutt)", "jenny_(slither)", "jetshark", "jodira", "jonas-puppeh", "jotun22", "juantriforce", "julien_(artist)", "jush", "kaeaskavi", "kaeldu", "kailys", "kalemendrax", "kamelotnoah", "kamuri", "kannos", "kaputotter", "karhyena", "karukuji", "katahane3", "kawfee", "kebi", "keishinkae", "kenket", "kidnapping", "kindle", "kinsheph", "kirion_pegu", "kirsten_odessa", "kittydee", "kiva~", "klaus", "klongi", "km-15", "knives4cats", "knot_hanging", "knotting", "koba", "koba_(koba)", "kodardragon", "kohtek", "kola_(artist)", "koldia", "kona", "korichi", "kotyami", "kouryuu", "kra-ra", "kuribon", "kuroodod", "kyotoleopard", "kyra_(greyshores)", "larovin", "latex_transformation", "lazybutts", "lenexwants", "leniovias", "letodoesart", "leuphe", "lilith_(sefeiren)", "lillianwinters", "lily_(sefeiren)", "liquefactiophilia", "liquid_latex", "livestream", "living_clothing", "living_costume", "living_inflatable", "living_latex", "living_plushie", "living_rubber", "lizanne", "lizardlars", "lizeron", "lizet", "loimu", "loimu_(character)", "lonelycharart", "loonertick", "lostdragon01", "lothar", "lotus_(whitefeathersrain)", "louart", "luck_(animancer)", "luna_(tehaxis)", "lunalei", "luskfoxx", "lustylamb", "macharius", "madrigal", "magenta7", "magpi", "maim", "malfaren", "malik", "mana", "manahallowhound", "mandarax", "mango_(mangobird)", "mangobird", "maquenda", "marc_(theblueberrycarrots)", "marjani", "marking_territory", "marsminer", "martinballamore", "mawmain", "mawplay", "maxtheshadowdragon", "mcfan", "meandraco", "meesh", "meheheehehe", "mej", "melthecannibal", "meraence", "mercy_(mercy)", "mestiso_(character)", "metalfox", "mikey6193", "miles_df", "milkyway", "milligram_smile", "milo_(juantriforce)", "milodesty", "mind_break", "mind_control", "miramore", "miraoff", "moetempura", "monorchid", "morca", "morca_(character)", "morhlis", "morticus", "moses_(samur_shalem)", "moth_sprout", "mr._mephit", "mricantdraw", "mtf_transformation", "mti_transformation", "muffin_(themuffinly)", "muriat", "mustard_(welcometothevoid)", "mutt_(character)", "mutual_chastity", "muzz", "muzzle_(object)", "muzzled", "narse", "nate_(dragoneill)", "navarchus_zepto", "navos", "navos_(wordcaster)", "necrodrone", "neverneverland", "nib-roc", "nicnak044", "nicole_(nicnak044)", "nik159", "nipple_lick", "nitani", "nitrods", "nommz", "non-euclidean_sex", "nopetrol", "nowandlater", "noxy_(equinox)", "null_bulge", "nullification", "nullo", "nummynumz", "nx-3000", "ochropus", "oksara_(character)", "olivia_(kadath)", "olli_(braeburned)", "omari", "omnipresentcrayon", "omorashi", "oouna", "orchiectomy_scar", "orgasm_control", "orgasm_denial", "orientation_play", "orlandofox", "oselotti", "otterlike", "ouros_(character)", "oviposition", "ovipositor", "ovorange", "ownership", "padjetxharrington", "paganee", "pandora's_fox", "parasite", "passel_(ralek)", "patto", "pawpadpup", "peable", "peeing", "peeing_on_another", "penectomy", "penetrable_sex_toy", "penis_shrinking", "permanent", "personalami", "peskybatfish", "pet_praise", "phenyanyanya", "pheromones", "phosaggro", "photonoko", "pickles-hyena", "pig_(artist)", "pikajota", "pillow_humping", "piranha_fish", "pirate_eagle", "plushification", "plushsuit", "plussun", "pocketpaws", "pointedfox", "pone_keith", "power_bottom", "predatory_look", "pridark", "princess_(paigeforsyth)", "prostate", "prostate_stimulation", "prsmrti", "pseudo-penis", "psy101", "psychedelic", "psychosocial", "punishment", "pur3", "puzzle_(kadath)", "quas_naart", "questionable_consent", "quetzalli_(character)", "quillu", "quizzical_(artist)", "qwaxi~lixard", "qwertydragon", "raaz", "rainstorm_(marefurryfan)", "rajii", "rakisha", "ralek", "ralsei", "ramaelfox", "ramzymo", "rannik", "rape", "rarakie", "rattatatus78", "ravensflock", "reallynxgirl", "red_(redponei)", "red-izak", "redfeatherstorm", "redponei", "redraptor16", "redrosid", "redrusker", "reggie_(whygena)", "rektalius", "revous", "reysi", "rezukii", "richard_foley", "richarddeus", "rick_griffin", "rika", "rimming", "rionquosue", "rip_(character)", "riska_(artist)", "rithnok_tatsukao_(rithnok)", "rml", "roanoak", "roksim", "role_reversal", "roleplay", "romantic_couple", "rosy_firefly", "rough_sex", "rov", "roxythefoxy", "ruaidri", "rue_(the-minuscule-task)", "rufus_b._cobber", "rufus_black", "rukis", "ruska", "sabretoothed_ermine", "sabuky", "sadcat16hrz", "sahara_(nicnak044)", "sairaks", "salkitten", "sam_(the_sunfish)", "samur_shalem", "sandra_(roanoak)", "saphira", "scafen_(artist)", "scale_(artist)", "scalesindark", "scarlet_sound_(oc)", "scarlet-frost", "scritt", "scruffythedeer", "seamen", "securipun", "seductive", "sefeiren", "selenophile", "sendar", "sensory_deprivation", "serialdad", "seth-iova", "seyumei", "sheppermint", "sherri_mayim", "shido-tara", "shinigamisquirrel", "shiuk", "shorttail", "shou_(securipun)", "sicklyhypnos", "sidnithefox", "sika", "silicas", "silveredge", "siroc", "sissification", "siyah", "skadjer", "skeletonguys-and-ragdolls", "sketh", "skia", "skulldog", "skully", "skylar_zero", "sleep_sex", "sleepy_(sleepylp)", "slug_(artist)", "smileeeeeee", "smirgel", "smitty_g", "smooshkin", "sneakerfox", "snowfoxatheart", "snowskau", "somnamg", "sonsasu", "sovy", "spaal", "species_transformation", "spectrumshift", "spinal22", "spiral_eyes", "spiral_pupils", "spitey", "spitting_in_mouth", "stack_(character)", "staffkira2891", "stargazer", "stephie_(fraydia1)", "sterr", "stith", "stomak", "storm_(stormwx_wolf)", "story", "straight_to_gay", "strapon", "strapon_over_chastity", "stygimoloch_(artist)", "styxandstoned", "sucked_silly", "sugarlesspaints", "suit_transformation", "sunderlovely", "sunny_way", "sybian", "sylvia_ritter", "synx_the_lynx", "syrazor", "syrinoth", "sytheras", "syynx", "tabra", "tacet_the_terror", "tacokurt", "tail_coil", "tailgrip", "tailtufts", "taking_turns", "tashi_gibson", "tenecayr_(artist)", "tennis_ball_gag", "terryburrs", "teryx_commodore", "tess_(frisky_ferals)", "thathornycat", "the_lils", "the-minuscule-task", "theblueberrycarrots", "thejoyfuldragon", "thelordp_chan", "themuffinly", "theothefox", "theowlette", "thesecretcave", "thevale", "thevixenmagazine", "thistle", "throat_hug", "tiercel", "tirrel", "tochka", "tohupo", "tojo_the_thief", "tomness", "tonitrux", "toradoshi", "torakuta", "toshabi", "totesfleisch8", "toumal_(character)", "toxoglossa", "translucent_body", "tres-apples", "tres-art", "trevart", "trigaroo", "trixythespiderfox", "trout_(artist)", "truegrave9", "tuke", "turquoise_(ralek)", "tuwka", "twinkle-sez", "twiren", "two_doms_one_sub", "tyba", "tylon", "tyroo", "ulvbecker", "umbreveon", "uni", "unimpressive_(artist)", "unprofessional_behavior", "untied_verbeger", "unwanted_cumshot", "unwanted_ejaculation", "unwanted_impregnation", "urine", "urine_on_face", "vader-san", "valderic_blackstag", "vallhund", "velannal", "vera_(sefeiren)", "vibrator", "virtual_reality", "virtyalfobo", "vis_(bob0424)", "visibly_trans", "visionaryserpent", "viwrastupr", "vore_sex", "vorell", "voyeur", "vr_headset", "vulgarstarling", "vurrus", "warden006", "wardy", "water_jacking", "watersports", "watsup", "webcam", "wemd", "wesley_(suave_senpai)", "whitefeathersrain", "whiteperson", "will_(hladilnik)", "winddragon", "windy_dripper", "wingedwolf", "wings_of_fire", "wintersnowolf", "wiredhooves", "wolfluffyfly", "wolfy-nail", "worship", "x-kid", "xane", "xanthor", "xenoforge", "xenoguardian", "xero_(captainscales)", "xnirox", "yeenr", "yiffy1234", "yinglet", "youwannaslap", "yurusa", "zackary911", "zaire_(nightdancer)", "zambuka", "zaush", "zawmg", "zazush-una", "zebra_domination", "zeeb", "zelenyy", "zephyr_(dragon)", "zephyr_the_drake", "zero-sum", "zhanbow", "ziggie13", "zonkpunch", "zoophobia"}


def list_sum(my_list):
    counter = 0
    for my_int in my_list:
        counter += int(my_int)
    return counter


def filter_tags(tag_list):
    tag_list = set(tag_list)
    intersect = tag_list.intersection(ultra_tag_set)
    if len(intersect) != 0:
        return intersect
    else:
        return set()


def set_meta(tag_set):
    for meta_filter in meta_filters:
        intersect = tag_set.intersection(meta_filter)
        if len(intersect) != 0:
            return meta_filters[meta_filter]
    return 'No Meta'


def set_gender(tag_set):
    gen = tag_set.intersection(gender_filter)
    if len(gen) == 0:
        return 'No gen'
    # sort gen as list  # fixes order (sets are unordered)
    gen = list(gen)
    gen.sort()
    return " ".join(gen).replace('maleherm', 'herm'). \
        replace('gynomorph', 'dickgirl'). \
        replace('andromorph', 'cuntboy'). \
        replace('ambiguous_gender', 'ambiguous')


def set_kink(tag_set):
    for kink_filter in kink_filters:
        intersect = tag_set.intersection(kink_filter)
        if len(intersect) != 0:
            return kink_filters[kink_filter]
    return 'No kink'


def set_qty(tag_set):
    for qty_filter in quantity_filters:
        intersect = tag_set.intersection(qty_filter)
        if len(intersect) != 0:
            return quantity_filters[qty_filter]
    return 'No qty'


def set_download_path(rating, copy, char, tags, ext=None, name=None, p_type='post'):
    quantity = set_qty(tags)
    gender = set_gender(tags)
    kink = set_kink(tags)
    meta = set_meta(tags)
    animate = 'Not Animated'
    if ext is not None:
        tmp = ext.replace('png', animate).replace('jpg', animate)
        if tmp != animate:  # checks if animated
            animate = 'Animated'
    if copy:
        copy = 'Copy'
    else:
        copy = 'No Copy'
    if char:
        char = 'Char'
    else:
        char = 'No Char'
    # path formatting
    if p_type == 'post':
        return f"downloads/Posts/{meta}-{animate}/Rating {rating}-{kink}/{copy}-{char}/" \
               f"{quantity}-{gender}/"
    if p_type == 'pool':
        if name is None:
            print('Name is None~!!!')
            return 'Name is None~!!!'
        return f"downloads/Pools/Rating {rating}-{kink}/{copy}-{char}/" \
               f"{gender}-{quantity}/{name_filter(name)}/"
    if p_type == 'family':
        return f"downloads/Posts/{meta}-{animate}/Rating {rating}-{kink}/{copy}-{char}/" \
               f"{quantity}-{gender}/F-{name_filter(str(name))}/"  # parent_id
