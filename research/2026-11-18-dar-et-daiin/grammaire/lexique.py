"""Petit lexique annoncé avant d'ouvrir les résultats. La casse et les accents sont ceux du corpus."""
FORMS = {
 'latin':{
  'coordonnant':'et aut vel neque nec sed atque ac seu sive',
  'preposition':'ab ad apud absque de ex erga inter per praeter pro propter sine sub trans in',
  'article':'',
  'nom':'aqua aquam aquae aquis aquas aquarum oleum olei oleo olea vinum vini vino mel mellis melle melli salem salis sale sanguis sanguinis sanguine sanguinem sanguini pus puris pure sanies saniem sanie saniei cutis cutem cute cuti caput capitis capite oculus oculi oculo oculum oculos oculis osse ossis ossa ossibus dentes dentem dentis dente dentibus panis pane panem panibus radix radicis radicem radice radices radicibus folium folii folio foliis herba herbae herbam herbis herbas vulnus vulnere vulneris vulnera vulnerum vulneribus febris febrem febre febres febribus lac lacte lactis succus sucus succum sucum suco succo cucumeris aceti acetum aceto farina farinam farinae piper piperis pipere rosa rosae rosam rosis viola violae violam violis salivam saliua saliuam medulla medullam felle fel bilis bilem bile urina urinam urinae tussis tussim tussi tussis stomachus stomachum stomacho oculorum aurem auris aure auribus vesica vesicam vesicae alvus alvum alvo pulmonis pulmo pulmonem dolore dolorem dolor dolores doloribus ulcus ulcere ulcera ulcerae nervus nervi nervos nervis',
  'ambigu':'a e cum post super ultra ante circa contra extra os sal ore oris an ut qui quae quod nam si quam quamquam'},
 'français':{
  'coordonnant':'et mais car',
  'preposition':'de par pour por sans sanz avec avecques aveques parmi entre envers devers sus soubz devant parmi outre',
  'article':'',
  'contraction':'du aux es',
  'nom':'eau eaue eaux aigues aigue yaue vin vins vinaigre verjus vertjus pain pains mie farine farines huile huille oile olle sel sels miel lait laict lart lard saffran safran poivre gingembre gingibre canelle cannelle chair char chars chairs sang sanc gresse graisse graisses moelle racine racines fueille fueilles feuille feuilles herbe herbes fleur fleurs rose roses amandes amande amandres oeuf oeufs oeulx oignons oignon oingnon oingnons persil percil poisson poissons brochet brochets fresne truite truites poule poules poulet poulets poulaille poullet poisson pois porree beuf boeuf porc porcs venoison roux cervelle foye foie estomac maladie maladies sangler',
  'ambigu':'ne en le la les l li un une ung uns des ou a se si quant comme que ce leur son maisn quele quel'},
 'italien':{
  'coordonnant':'et e overo ovvero oppure ma',
  'preposition':'de di in con per senza fra tra presso',
  'article':'il',
  'contraction':'del della delle dello degli dal dalla dallo dalle dagli nella nelle nello negli nel sul sulla',
  'nom':'acqua aqua acque vino vini aceto agresto aglio agli zenzero zenzevero pepe pevere sale sali mele miele pan pane pani farina farine olio oleo ova ovo uovo uova latte lardo grasso carne carni pesce pesci pollo polli gallina galline cappone capponi petto petti fegato sangue osso ossa foglia foglie radice radici herba herbe erba erbe fiore fiori rose rosa zafferano zafrano zaffarano zucharo zuccaro zucchero caso cascio formaggio mandorle amandole mandola mandorla amido brodo brodi piselli ceci ceci cipolla cipolle prezzemolo petrosillo petroselli canella cannella',
  'ambigu':'da o a che la le lo gli li i l un una uno unde poi come sopra sotto ne se sia od salvia'},
 'allemand':{
  'coordonnant':'und vnd vnnd unnd oder voder aber sondern',
  'preposition':'mit mitt ohne on aus auß von vonn durch durchh bey bei beiß nach gegen zwischen zuo zwüschen vmbe',
  'article':'',
  'contraction':'zum zur im vom beim',
  'nom':'wasser wassers wazzer wazzeres wasserlein wein weins wyn weyn essig eßig essich öl oel ol oele salz saltz saltzes honig honigs honich honigk honick milch milich blut bluttes blutes bluot blatt blat bletter blätter blumen blume kraut krut krauts krautt wurzel wurtzel wurtz wurcz wurzen wurtzen saft saff saf safft saffs brot brott brotes brode mehl mel fleisch fleisches fleischs haut magen magens lunge lungen herz hertz hertzen rosen rose rosens holtz holz heimel',
  'ambigu':'der den dem des die das dy dis dieser ein eins eyn eyne einer einem einen eine eim ain ains zu an in als wie so doch noch wann dann denn nacher vor auf auff vff uber über under umb um'}
}

# Retirer quelques unités particulièrement homographes du vocabulaire nominal.
for language, words in {'français':('char','chars','roux'), 'italien':('sale','mele','agli','caso'),
                        'latin':('rosa','viola','aqua','aquae','pure','cute','sal','os'),
                        'allemand':('mal','mel')}.items():
    records=FORMS[language]
    records['nom']=' '.join(w for w in records['nom'].split() if w not in words)
    records['ambigu']+=' '+' '.join(words)


def labels():
    out={}
    for language,groups in FORMS.items():
        items={}
        for group,words in groups.items():
            for w in words.split():
                if w in items and items[w]!=group:
                    raise ValueError((language,w,items[w],group))
                items[w]=group
        out[language]=items
    return out
