# Gmail Draft Maker — v3 (image embeds right after the mockup-offer paragraph)

Creates a Gmail **draft** in **meridante.pt@gmail.com** with: recipient, subject, the email body,
the website mockup **embedded inline right after the paragraph that offers the mockup**, the same image
**attached** with a **per-company filename** (e.g. `Carpintaria Paulino - Meridante.jpg`), and the draft
auto-filed under the **"To Send - Team"** label.

## Update (re-paste + New version — same URL)
1. Open the **Meridante Draft Maker** Apps Script project (logged in as meridante.pt@gmail.com).
2. Select all → delete → paste the **Code.gs** below → **💾 Save**.
3. **Deploy → Manage deployments → ✏️ Edit → Version: New version → Deploy.** (URL unchanged.)
4. Reply "redeployed".

## Code.gs

```javascript
function sanitizeName_(s){
  s=(s||'').normalize('NFKD').replace(/[̀-ͯ]/g,'');
  s=s.replace(/[^\w &().,'-]+/g,' ').replace(/\s+/g,' ').trim();
  return s||'Meridante';
}
function escHtml_(t){return (t||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}

function doPost(e){
  try{
    var p=JSON.parse(e.postData.contents);
    var L=(p.lang||'').toUpperCase(), fr=L==='FR', es=L==='ES';
    var file=p.file || (sanitizeName_(p.company)+' - Meridante.jpg');
    var blob=UrlFetchApp.fetch(p.image).getBlob().setName(file);

    var head=fr?'Aperçu de votre nouveau site':es?'Vista previa de su nuevo sitio web':'Pré-visualização do seu novo site';
    var note=fr?('Voici la maquette ('+file+'), également jointe à cet e-mail :')
            :es?('Esta es la maqueta ('+file+'), también adjunta a este correo:')
            :('Aqui está a maquete ('+file+'), também em anexo a este e-mail:');

    var preview='<table role="presentation" width="100%" style="margin:22px 0"><tr><td style="border-top:1px solid #e4e4e4;border-bottom:1px solid #e4e4e4;padding:20px 0">'+
      '<div style="font:600 16px Georgia,serif;color:#0c1322;margin-bottom:4px">'+head+'</div>'+
      '<div style="font-size:13px;color:#666;margin-bottom:14px">'+note+'</div>'+
      '<img src="cid:mockup" style="display:block;width:100%;max-width:600px;border:1px solid #ddd;border-radius:8px"/>'+
      '<div style="font-size:12px;color:#999;margin-top:7px">📎 '+escHtml_(file)+'</div></td></tr></table>';

    var html=p.htmlBody;
    if(!html){
      var paras=(p.body||'').split(/\n\s*\n/);
      // insert the preview right AFTER the paragraph that offers the mockup
      var ins=-1;
      for(var i=0;i<paras.length;i++){ if(/maquette|maquete|maqueta|mockup/i.test(paras[i])){ ins=i; break; } }
      if(ins<0) ins=Math.min(1,paras.length-1);
      var out='<div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;color:#222;line-height:1.65">';
      for(var i=0;i<paras.length;i++){ out+='<div style="margin:0 0 14px">'+escHtml_(paras[i]).replace(/\n/g,'<br>')+'</div>'; if(i===ins) out+=preview; }
      out+='</div>'; html=out;
    }
    var plain=(p.body||'')+'\n\n'+head+'\n'+note;

    var draft=GmailApp.createDraft(p.to,p.subject,plain,{htmlBody:html,inlineImages:{mockup:blob},attachments:[blob],name:'Meridante'});

    var labeled=false, labelName=p.label||'To Send - Team';
    try{var lbl=GmailApp.getUserLabelByName(labelName)||GmailApp.createLabel(labelName); draft.getMessage().getThread().addLabel(lbl); labeled=true;}catch(le){}

    return ContentService.createTextOutput(JSON.stringify({ok:true,file:file,labeled:labeled})).setMimeType(ContentService.MimeType.JSON);
  }catch(err){ return ContentService.createTextOutput(JSON.stringify({ok:false,error:String(err)})).setMimeType(ContentService.MimeType.JSON); }
}
function doGet(){return ContentService.createTextOutput('Meridante Draft Maker is running.');}
```
