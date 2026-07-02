# -*- coding: utf-8 -*-
# Follow-up cadence engine — D+3 / D+10 / D+17, FR/PT/ES/NL. Warm, truthful, low-pressure.
import urllib.parse
FROM="meridante.pt@gmail.com"; CAL="https://cal.com/meridante-studios-brxjh0/15min"

FU={
'FR':[
 ("Re: {su}",
  "Bonjour,\n\nJe me permets de revenir vers vous au sujet de la maquette offerte pour {c}.\n\nAu fond, l'idée n'est pas seulement d'avoir un plus beau site, mais d'en faire un outil qui travaille pour vous : rapide et soigné sur mobile, trouvé sur Google, et prêt à capter les demandes à toute heure.\n\nSi vous préférez en parler de vive voix, voici mon agenda pour 15 minutes, quand cela vous arrange : "+CAL+"\n\nBien à vous,\nJoão · Meridante\n"+FROM),
 ("Re: {su}",
  "Bonjour,\n\nJe voulais simplement m'assurer que mon message vous était bien parvenu, je sais combien les journées sont remplies.\n\nLa proposition tient toujours : une maquette de votre nouveau site pour {c}, offerte et sans engagement. Un mot de votre part et je m'en occupe.\n\nBien cordialement,\nJoão · Meridante\n"+FROM),
 ("Je reste à votre disposition, {c}",
  "Bonjour,\n\nJe ne voudrais pas vous importuner, alors je n'insisterai pas davantage.\n\nSi l'envie vous vient un jour, même dans plusieurs mois, répondez simplement « maquette » et je serai ravi de vous préparer cela, gratuitement.\n\nJe vous souhaite une très belle continuation,\nJoão · Meridante\n"+FROM)],
'PT':[
 ("Re: {su}",
  "Olá,\n\nPermito-me voltar ao contacto sobre a maquete oferecida para a {c}.\n\nNo fundo, a ideia não é só ter um site mais bonito, mas torná-lo numa ferramenta que trabalha por vós: rápido e cuidado no telemóvel, encontrado no Google, e pronto a captar pedidos a qualquer hora.\n\nSe preferirem falar, aqui fica a minha agenda para 15 minutos, quando vos der jeito: "+CAL+"\n\nCom os melhores cumprimentos,\nJoão · Meridante\n"+FROM),
 ("Re: {su}",
  "Olá,\n\nQueria apenas certificar-me de que a minha mensagem chegou, sei bem como os dias são cheios.\n\nA proposta mantém-se: uma maquete do vosso novo site para a {c}, oferecida e sem compromisso. Uma palavra vossa e trato disso.\n\nCom estima,\nJoão · Meridante\n"+FROM),
 ("Fico ao vosso dispor, {c}",
  "Olá,\n\nNão quero ser inconveniente, por isso não insistirei mais.\n\nSe um dia vos apetecer, mesmo daqui a uns meses, respondam apenas « maquete » e terei todo o gosto em preparar isso, gratuitamente.\n\nDesejo-vos uma excelente continuação,\nJoão · Meridante\n"+FROM)],
'ES':[
 ("Re: {su}",
  "Hola,\n\nMe permito volver a escribirle sobre la maqueta gratuita para {c}.\n\nEn el fondo, la idea no es solo tener una web más bonita, sino convertirla en una herramienta que trabaje para usted: rápida y cuidada en el móvil, encontrada en Google y lista para captar solicitudes a cualquier hora.\n\nSi prefiere hablarlo, aquí tiene mi agenda para 15 minutos, cuando le venga bien: "+CAL+"\n\nUn cordial saludo,\nJoão · Meridante\n"+FROM),
 ("Re: {su}",
  "Hola,\n\nSolo quería asegurarme de que mi mensaje le llegó, sé lo llenos que están los días.\n\nLa propuesta sigue en pie: una maqueta de su nueva web para {c}, gratuita y sin compromiso. Una palabra suya y me encargo.\n\nUn saludo cordial,\nJoão · Meridante\n"+FROM),
 ("Quedo a su disposición, {c}",
  "Hola,\n\nNo quiero molestar, así que no insistiré más.\n\nSi algún día le apetece, incluso dentro de unos meses, responda simplemente « maqueta » y estaré encantado de prepararla, gratis.\n\nLe deseo lo mejor,\nJoão · Meridante\n"+FROM)],
'NL':[
 ("Re: {su}",
  "Goedendag,\n\nIk kom nog even terug op het gratis ontwerp voor {c}.\n\nDe kern is niet alleen een mooiere website, maar een die voor u werkt: snel en verzorgd op mobiel, vindbaar op Google en klaar om aanvragen op elk moment op te vangen.\n\nLiever even bellen? Hier is mijn agenda voor 15 minuten, wanneer het u uitkomt: "+CAL+"\n\nMet vriendelijke groet,\nJoão · Meridante\n"+FROM),
 ("Re: {su}",
  "Goedendag,\n\nIk wilde even checken of mijn bericht is aangekomen, ik weet hoe vol de dagen zijn.\n\nHet voorstel staat nog: een ontwerp van uw nieuwe website voor {c}, gratis en vrijblijvend. Eén woord van u en ik regel het.\n\nMet vriendelijke groet,\nJoão · Meridante\n"+FROM),
 ("Ik blijf tot uw beschikking, {c}",
  "Goedendag,\n\nIk wil niet opdringerig zijn, dus ik laat het hierbij.\n\nMocht u er ooit zin in krijgen, ook over een paar maanden, antwoord dan gewoon « ontwerp » en ik maak het graag voor u, gratis.\n\nIk wens u het allerbeste,\nJoão · Meridante\n"+FROM)],
}
def gm(to,su,bo): return "https://mail.google.com/mail/?"+urllib.parse.urlencode({'view':'cm','fs':'1','to':to,'su':su,'body':bo,'authuser':FROM})
def followups(company, orig_subject, lang, email):
    L=(lang or 'FR').upper(); L=L if L in FU else 'FR'
    out=[]
    for su_t,bo_t in FU[L]:
        su=su_t.format(su=orig_subject,c=company); bo=bo_t.format(c=company)
        out.append({'subject':su,'body':bo,'gmail':gm(email,su,bo)})
    return out  # [D+3, D+10, D+17]
